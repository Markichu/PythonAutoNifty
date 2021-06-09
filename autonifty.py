from PIL import Image
import json
import random
import math

DRAWING_SIZE = 1000
GOLDEN = (1 + math.sqrt(5)) / 2
BLACK = (0, 0, 0, 1)
WHITE = (255, 255, 255, 1)


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_rotational(radians, radius, origin=None):
        if origin is None:
            origin = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)

        return Pos(math.cos(radians) * radius / 2, math.sin(radians) * radius / 2) + origin

    def point(self):
        return {"x": self.x, "y": self.y}

    def copy(self):
        return Pos(self.x, self.y)

    def rotate(self, rotation, origin=None):
        # get default center
        if origin is None:
            origin = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)

        self -= origin
        x = self.x * math.cos(rotation) - self.y * math.sin(rotation)
        self.y = self.x * math.sin(rotation) + self.y * math.cos(rotation)
        self.x = x
        return self + origin

    def __add__(self, other):
        result = self.copy()
        result.x += other.x
        result.y += other.y
        return result

    def __sub__(self, other):
        result = self.copy()
        result.x -= other.x
        result.y -= other.y
        return result

    def __mul__(self, mult):
        result = self.copy()
        result.x *= mult
        result.y *= mult
        return result

    def __truediv__(self, div):
        result = self.copy()
        result.x /= div
        result.y /= div
        return result

    def __round__(self):
        result = self.copy()
        result.x = round(self.x)
        result.y = round(self.y)
        return result

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Drawing:
    def __init__(self):
        self.object = {"lines": [],
                       "width": DRAWING_SIZE,
                       "height": DRAWING_SIZE}

    def add_point(self, pos, colour, brush_radius):
        # create a point at the desired point location
        point = pos.point()

        # create line with two points
        line = {"points": [point, point],
                "brushColor": "rgba({},{},{},{})".format(*colour),
                "brushRadius": brush_radius}

        # add line to object
        self.object["lines"].append(line)

    def add_background(self, colour):
        # create a point at the desired point location
        self.add_point(Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2), colour, DRAWING_SIZE * pow(2, 0.5) / 2)

    def add_gradient(self, pos1, pos2, colour1, colour2, divisions=30):
        r_step = (colour2[0] - colour1[0]) / divisions
        g_step = (colour2[1] - colour1[1]) / divisions
        b_step = (colour2[2] - colour1[2]) / divisions
        a_step = (colour2[3] - colour1[3]) / divisions
        size_step = (pos2.y - pos1.y) / divisions
        brush_radius = ((pos2.y - pos1.y) / (divisions - 1))

        for i in range(divisions + 1):
            colour = (colour1[0] + (r_step * i),
                      colour1[1] + (g_step * i),
                      colour1[2] + (b_step * i),
                      colour1[3] + (a_step * i))
            line_pos1 = Pos(pos1.x, pos1.y + (size_step * i))
            line_pos2 = Pos(pos2.x, pos1.y + (size_step * i))
            self.add_straight_line(line_pos1, line_pos2, colour, brush_radius)

    def add_straight_line(self, pos1, pos2, colour, brush_radius):
        # create points for line
        point1 = pos1.point()
        point2 = pos2.point()

        # create line with two points
        line = {"points": [point1, point2],
                "brushColor": "rgba({},{},{},{})".format(*colour),
                "brushRadius": brush_radius}

        # add line to object
        self.object["lines"].append(line)

    def add_line(self, pos_list, colour, brush_radius):
        # convert pos list to points list
        points_list = []
        for pos in pos_list:
            points_list.append(pos.point())

        # create line with two points
        line = {"points": points_list,
                "brushColor": "rgba({},{},{},{})".format(*colour),
                "brushRadius": brush_radius}

        # add line to object
        self.object["lines"].append(line)

    def add_strict_line(self, pos_list, colour, brush_radius, circular_path=False):
        # create points for square
        points_list = [pos_list[0].point()]
        for pos in pos_list[1:-1]:
            points_list.append(pos.point())
            points_list.append(pos.point())
        points_list.append(pos_list[-1].point())
        if circular_path:
            points_list.append(pos_list[-1].point())
            points_list.append(pos_list[0].point())

        # create line with all the points
        line = {"points": points_list,
                "brushColor": "rgba({},{},{},{})".format(*colour),
                "brushRadius": brush_radius}

        # add line to object
        self.object["lines"].append(line)

    def add_pause(self, length):
        # create points for square
        point = {"x": -10, "y": -10}

        # create line with all the points
        line = {"points": [point for _ in range(length)],
                "brushColor": "rgba({},{},{},{})".format(*(0, 0, 0, 0)),
                "brushRadius": 0}

        # add line to object
        self.object["lines"].append(line)

    def write(self, pos, lines, font_size, line_spacing=1.15):
        line_pos = pos.copy()
        y_offset = Pos(0, font_size * line_spacing)
        font = {"a": ([[Pos(0.1, 1), Pos(0.5, 0)],
                      [Pos(0.5, 0), Pos(0.9, 1)],
                      [Pos(0.2, 0.8), Pos(0.8, 0.8)]], 1),
                "b": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.1, 0.5)],
                      [Pos(0.1, 0.5), Pos(0.9, 0.5), Pos(0.9, 1), Pos(0.1, 1)]], 1),
                "c": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.7)]], 1),
                "d": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 1), Pos(0.1, 1)]], 1),
                "e": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0), Pos(0.9, 0)],
                      [Pos(0.1, 0.5), Pos(0.6, 0.5)],
                      [Pos(0.1, 1), Pos(0.9, 1)]], 1),
                "f": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0), Pos(0.9, 0)],
                      [Pos(0.1, 0.5), Pos(0.6, 0.5)]], 1),
                "g": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.7), Pos(0.9, 0.5)],
                      [Pos(0.5, 0.5), Pos(0.9, 0.5)]], 1),
                "h": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0.5), Pos(0.9, 0.5)],
                      [Pos(0.9, 0), Pos(0.9, 1)]], 1),
                "i": ([[Pos(0.1, 0), Pos(0.1, 1)]], 0.2),
                "j": ([[Pos(0.6, 0), Pos(0.6, 0.7), Pos(0.6, 0.7), Pos(0.6, 1), Pos(0.1, 1)]], 0.7),
                "k": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0.6), Pos(0.9, 0)],
                      [Pos(0.25, 0.5), Pos(0.9, 1)]], 1),
                "l": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 1), Pos(0.7, 1)]], 0.8),
                "m": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0), Pos(0.6, 1)],
                      [Pos(0.6, 1), Pos(1.1, 0)],
                      [Pos(1.1, 0), Pos(1.1, 1)]], 1.2),
                "n": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0), Pos(0.9, 1)],
                      [Pos(0.9, 0), Pos(0.9, 1)]], 1),
                "o": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.7), Pos(0.9, 0.3)]], 1),
                "p": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.1, 0.5)]], 1),
                "q": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.7), Pos(0.9, 0.3)],
                       [Pos(0.7, 0.8), Pos(0.9, 1)]], 1),
                "r": ([[Pos(0.1, 0), Pos(0.1, 1)],
                      [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.1, 0.5)],
                       [Pos(0.6, 0.5), Pos(0.9, 1)]], 1),
                "s": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.5), Pos(0.9, 0.5), Pos(0.9, 1), Pos(0.1, 1), Pos(0.1, 0.7)]], 1),
                "t": ([[Pos(0.5, 0), Pos(0.5, 1)],
                      [Pos(0.1, 0), Pos(0.9, 0)]], 1),
                "u": ([[Pos(0.1, 0), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.7), Pos(0.9, 0)]], 1),
                "v": ([[Pos(0.1, 0), Pos(0.5, 1)],
                       [Pos(0.5, 1), Pos(0.9, 0)]], 1),
                "w": ([[Pos(0.1, 0), Pos(0.4, 1)],
                      [Pos(0.4, 1), Pos(0.7, 0)],
                      [Pos(0.7, 0), Pos(1, 1)],
                      [Pos(1, 1), Pos(1.3, 0)]], 1.4),
                "x": ([[Pos(0.1, 0), Pos(0.9, 1)],
                       [Pos(0.1, 1), Pos(0.9, 0)]], 1),
                "y": ([[Pos(0.1, 0), Pos(0.5, 0.6)],
                       [Pos(0.5, 0.6), Pos(0.9, 0)],
                       [Pos(0.5, 0.6), Pos(0.5, 1)]], 1),
                "z": ([[Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.9, 0), Pos(0.1, 1)],
                       [Pos(0.1, 1), Pos(0.9, 1)]], 1),
                " ": ([], 0.75),
                "#": ([[Pos(0.1, 0.3), Pos(0.9, 0.3)],
                       [Pos(0.1, 0.7), Pos(0.9, 0.7)],
                       [Pos(0.2, 1), Pos(0.4, 0)],
                       [Pos(0.6, 1), Pos(0.8, 0)]], 1),
                "=": ([[Pos(0.1, 0.3), Pos(0.9, 0.3)],
                       [Pos(0.1, 0.7), Pos(0.9, 0.7)]], 1),
                "'": ([[Pos(0.1, 0), Pos(0.1, 0.4)]], 0.2),
                "\"": ([[Pos(0.1, 0), Pos(0.1, 0.4)],
                       [Pos(0.2, 0), Pos(0.2, 0.4)]], 0.3),
                ".": ([[Pos(0.1, 1), Pos(0.1, 1)]], 0.2),
                "!": ([[Pos(0.1, 0), Pos(0.1, 0.8)],
                       [Pos(0.1, 1), Pos(0.1, 1)]], 0.2),
                "1": ([[Pos(0.1, 1), Pos(0.9, 1)],
                       [Pos(0.5, 0), Pos(0.5, 1)],
                       [Pos(0.5, 0), Pos(0.1, 0.4)]], 1),
                "2": ([[Pos(0.1, 0.3), Pos(0.1, 0), Pos(0.8, 0), Pos(0.8, 0.4), Pos(0.1, 1)],
                       [Pos(0.1, 1), Pos(0.9, 1)]], 1),
                "3": ([[Pos(0.1, 0.2), Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.4, 0.5)],
                       [Pos(0.1, 0.8), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.5), Pos(0.4, 0.5)]], 1),
                "4": ([[Pos(0.1, 0.8), Pos(0.9, 0.8)],
                       [Pos(0.7, 0), Pos(0.7, 1)],
                       [Pos(0.1, 0.8), Pos(0.7, 0)]], 1),
                "5": ([[Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.1, 0.4), Pos(0.1, 0)],
                       [Pos(0.1, 0.4), Pos(0.9, 0.4), Pos(0.9, 1), Pos(0.1, 1), Pos(0.1, 0.8)]], 1),
                "6": ([[Pos(0.9, 0.2), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.4),
                        Pos(0.1, 0.6), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.5), Pos(0.1, 0.5), Pos(0.1, 0.6)]], 1),
                "7": ([[Pos(0.1, 0.2), Pos(0.1, 0)],
                       [Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.9, 0), Pos(0.4, 1)]], 1),
                "8": ([[Pos(0.5, 0.5), Pos(0.1, 0.5), Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.5, 0.5)],
                       [Pos(0.5, 0.5), Pos(0.1, 0.5), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.5), Pos(0.5, 0.5)]], 1),
                "9": ([[Pos(0.1, 0.8), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.6),
                        Pos(0.9, 0.4), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.5), Pos(0.9, 0.5), Pos(0.9, 0.4)]], 1),
                "0": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.7), Pos(0.9, 0.3)],
                       [Pos(0.1, 0.3), Pos(0.9, 0.7)]], 1)}

        def write_char(pos, char):
            # resize char to font size
            this_char = []
            x_offset = Pos(font_size * font[char][1], 0)
            for line in font[char][0]:
                this_line = []
                for point in line:
                    this_line.append((point.copy() * font_size) + pos)
                this_char.append(this_line)


            # draw character
            for line in this_char:
                self.add_line(line, BLACK, font_size / 30)

            return pos + x_offset

        for line in lines:
            for char in line:
                if char.lower() in font:
                    pos = write_char(pos.copy(), char.lower())
            line_pos = line_pos + y_offset
            pos = line_pos.copy()

    def __mul__(self, shrink_size):
        # origin for shrinking
        origin = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)

        # shrink each point
        for line_index in range(len(self.object["lines"])):
            line = self.object["lines"][line_index]
            for point_index in range(len(line["points"])):
                point = line["points"][point_index]
                point_pos = Pos(point["x"], point["y"])
                point_pos -= origin
                point_pos *= shrink_size
                point_pos += origin
                line["points"][point_index] = point_pos.point()
        return self

    def to_nifty_import(self):
        return "drawingCanvas.current.loadSaveData(\"" + json.dumps(self.object).replace('"', '\\"') + "\", false)"

    def shuffle_lines(self):
        random.shuffle(self.object["lines"])


def deg_to_rad(deg):
    return (deg * math.pi) / 180


def rotate(coord, rotation, origin=None):
    # get default center
    if origin is None:
        origin = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)

    coord -= origin
    x = coord.x * math.cos(rotation) - coord.y * math.sin(rotation)
    y = coord.x * math.sin(rotation) + coord.y * math.cos(rotation)
    return Pos(x, y) + origin


def hsva_to_rgba(h, s, v, a=1.0):
    i = math.floor(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if i % 6 == 0:
        r, g, b = v, t, p
    elif i % 6 == 1:
        r, g, b = q, v, p
    elif i % 6 == 2:
        r, g, b = p, v, t
    elif i % 6 == 3:
        r, g, b = p, q, v
    elif i % 6 == 4:
        r, g, b = t, p, v
    elif i % 6 == 5:
        r, g, b = v, p, q
    else:
        r, g, b = v, t, p

    return [r * 255, g * 255, b * 255, a]


def point_image(drawing, image_name):
    # load image from file
    image = Image.open(image_name)

    # init width and height
    width, height = image.size

    x_diff = 1000 / width
    y_diff = 1000 / height

    for x in range(width):
        for y in range(height):
            colour = list(image.getpixel((x, y)))
            if colour[3] > 0.25:
                drawing.add_point(Pos((x + 0.5) * x_diff, (y + 0.5) * y_diff), colour, x_diff * pow(2, 0.5) / 2)

    return drawing


def rotating_square(drawing):
    drawing.add_background((255, 255, 255, 1))
    p1 = Pos(200, 200)
    p2 = Pos(200, 800)
    p3 = Pos(800, 800)
    p4 = Pos(800, 200)
    for _ in range(500):
        drawing.add_strict_line([p1, p2, p3, p4], (0, 0, 0, 1), 10)
        drawing.add_pause(10)
        drawing.add_background((255, 255, 255, 1))
        p1 = rotate(p1, 0.1)
        p2 = rotate(p2, 0.1)
        p3 = rotate(p3, 0.1)
        p4 = rotate(p4, 0.1)
    drawing.add_strict_line([p1, p2, p3, p4], (0, 0, 0, 1), 10)

    return drawing


def tiled_diagonals(drawing, n=50):
    cell_size = DRAWING_SIZE / n
    for x in range(n):
        for y in range(n):
            if random.getrandbits(1):
                pos1 = Pos(x * cell_size, y * cell_size)
                pos2 = Pos((x + 1) * cell_size, (y + 1) * cell_size)
            else:
                pos1 = Pos((x + 1) * cell_size, y * cell_size)
                pos2 = Pos(x * cell_size, (y + 1) * cell_size)

            colour = hsva_to_rgba(random.random(), 0.5, 1)

            drawing.add_straight_line(pos1, pos2, colour, DRAWING_SIZE / n / 10)

    drawing.shuffle_lines()

    return drawing


def fibonacci_dots(drawing, n=1000):
    for i in range(n):
        # calc radians of rotation and raduis from center
        radians = i * (2 - (2 / GOLDEN)) * math.pi
        radius = math.sqrt(i + 1) * DRAWING_SIZE / math.sqrt(n)

        # calc position of dot
        pos = Pos.from_rotational(radians, radius)

        # draw dot
        drawing.add_point(pos, BLACK, 5)

    return drawing


def fibonacci_image(drawing, image_filename, n=3000):
    # load image from file
    image = Image.open(image_filename)

    # init result
    width, height = image.size

    for i in range(n):
        # calc radians of rotation and radius from center
        radians = i * (2 - (2 / GOLDEN)) * math.pi
        radius = math.sqrt(i + 1) * DRAWING_SIZE / math.sqrt(n)

        # calc position of dot
        pos = Pos.from_rotational(radians, radius)

        # calc size of dot from image brightness
        image_pos = round((pos.copy() / DRAWING_SIZE) * width) - Pos(1, 1)
        colour = list(image.getpixel((image_pos.x, image_pos.y)))
        brightness = 1 - ((0.2126 * colour[0] + 0.7152 * colour[1] + 0.0722 * colour[2]) / 265)

        # draw dot
        print(brightness * 4, (brightness * (DRAWING_SIZE / math.sqrt(n))) / 2)
        drawing.add_point(pos, colour, brightness * DRAWING_SIZE / math.sqrt(n) / 2)

    return drawing


def squared_circle(drawing, n=8):
    # init step and drawing
    step = 90 / n
    current_h = 0.8

    for i in range(n):
        # get degrees around circle and position
        degrees = i * step + (step / 2)

        # get pos for corners
        pos1 = Pos.from_rotational(deg_to_rad(degrees), DRAWING_SIZE).rotate(deg_to_rad(45))
        pos2 = Pos(pos1.x, 1000 - pos1.y).rotate(deg_to_rad(45))
        pos3 = Pos(1000 - pos1.x, 1000 - pos1.y).rotate(deg_to_rad(45))
        pos4 = Pos(1000 - pos1.x, pos1.y).rotate(deg_to_rad(45))

        # do color
        color = hsva_to_rgba(current_h, 0.8, 0.85)
        current_h -= 0.7 / n

        # add square
        drawing.add_strict_line([pos1, pos2, pos3, pos4], color, DRAWING_SIZE / (25 * n))

    return drawing


def curved_lines(drawing, n=20):
    # init drawing
    step = DRAWING_SIZE / n

    # do curved lines
    for i in range(n + 1):
        offset = i * step
        # do bottom left line
        drawing.add_straight_line(Pos(offset, 1000), Pos(0, offset), BLACK, DRAWING_SIZE / (25 * n))
        # do top right
        drawing.add_straight_line(Pos(1000, offset), Pos(offset, 0), BLACK, DRAWING_SIZE / (25 * n))

    # do diagonal lines
    for i in range(n - 1):
        offset = (i + 1) * step
        # do top left line
        drawing.add_straight_line(Pos(offset, 0), Pos(0, offset), BLACK, DRAWING_SIZE / (25 * n))
        # do bottom right
        drawing.add_straight_line(Pos(1000, 1000 - offset), Pos(1000 - offset, 1000), BLACK, DRAWING_SIZE / (25 * n))

    # do middle diagonal
    drawing.add_straight_line(Pos(1000, 0), Pos(0, 1000), BLACK, DRAWING_SIZE / (25 * n))

    return drawing


def shrinking_circle_ring(drawing, n=20, m=36):
    radians_step = 2 * math.pi / m
    current_h = 0
    big_radius = DRAWING_SIZE / 2
    for _ in range(n):
        # calc current radius
        print(big_radius, (m * big_radius) / (m + 2 * math.pi))
        big_radius = (m * big_radius) / (m + 2 * math.pi)
        small_radius = (math.pi * big_radius) / m

        # do color
        color = hsva_to_rgba(current_h, 0.8, 0.9)
        current_h -= 1 / n

        # draw circles around radius
        for i in range(m):
            pos = Pos.from_rotational(radians_step * i, big_radius)
            drawing.add_point(pos, color, small_radius)
            drawing.add_point(pos, WHITE, small_radius / 3)

    drawing *= 2

    return drawing


def square_fractal(drawing, master_key, iterations=5):
    # add gradient background
    drawing.add_gradient(Pos(0, 0), Pos(DRAWING_SIZE, DRAWING_SIZE), hsva_to_rgba(0, 0, 0.9), hsva_to_rgba(0, 0, 0.7), 200)
    drawing *= 1/0.95

    # Add text
    drawing.write(Pos(600, 125), ["Square", "Fractal", f'#{"".join([str(key) for key in master_key[:3]])}', f"n={iterations}"], 50)

    def rotate_left(ext_key):
        rotate_left_dict = {0: 0,
                       1: 2,
                       2: 3,
                       3: 4,
                       4: 1,
                       5: 6,
                       6: 7,
                       7: 8,
                       8: 5}
        modified_key = [rotate_left_dict[i] for i in ext_key]
        return [modified_key[1], modified_key[3], modified_key[0], modified_key[2]]

    def mirror(ext_key):
        mirror_dict = {0: 0,
                  1: 7,
                  2: 6,
                  3: 5,
                  4: 8,
                  5: 3,
                  6: 2,
                  7: 1,
                  8: 4}
        modified_key = [mirror_dict[i] for i in ext_key]
        return [modified_key[2], modified_key[3], modified_key[0], modified_key[1]]

    def next_ext_key(ext_key, this_key):
        if this_key == 1:
            return ext_key
        elif this_key == 2:
            return rotate_left(ext_key)
        elif this_key == 3:
            return rotate_left(rotate_left(ext_key))
        elif this_key == 4:
            return rotate_left(rotate_left(rotate_left(ext_key)))
        elif this_key == 5:
            return mirror(rotate_left(rotate_left(ext_key)))
        elif this_key == 6:
            return mirror(rotate_left(ext_key))
        elif this_key == 7:
            return mirror(ext_key)
        elif this_key == 8:
            return mirror(rotate_left(rotate_left(rotate_left(ext_key))))

    def square_fractal_recursive(drawing, ext_key, square_pos_corners, iterations):
        pos = (square_pos_corners[0] + square_pos_corners[1]) / 2
        size = (square_pos_corners[1].x - square_pos_corners[0].x) / 2
        if iterations > 0:
            # call recursively for all inner cells
            avg_pos = (square_pos_corners[0] + square_pos_corners[1]) / 2
            subdivisions = [[Pos(square_pos_corners[0].x, avg_pos.y), Pos(avg_pos.x, square_pos_corners[1].y)],
                            [square_pos_corners[0].copy(), avg_pos.copy()],
                            [avg_pos.copy(), square_pos_corners[1].copy()],
                            [Pos(avg_pos.x, square_pos_corners[0].y), Pos(square_pos_corners[1].x, avg_pos.y)]]
            for this_key, subdiv in zip(ext_key, subdivisions):
                if this_key != 0:
                    # draw transparent circle
                    # colour = hsva_to_rgba(0, 0, 0.4 - 0.4 * (pos.y / DRAWING_SIZE), 0.05)
                    # drawing.add_point(pos, colour, size)

                    square_fractal_recursive(drawing, next_ext_key(master_key, this_key), subdiv, iterations - 1)
        else:
            # draw dot in this cell
            colour = hsva_to_rgba(0, 0, 0.4 - 0.4 * (pos.y / DRAWING_SIZE))
            drawing.add_point(pos, colour, size)
        return drawing

    return square_fractal_recursive(drawing, master_key, [Pos(0, 0), Pos(DRAWING_SIZE, DRAWING_SIZE)], iterations)


def big_text_boi(drawing):
    drawing.add_gradient(Pos(0, 0), Pos(DRAWING_SIZE, DRAWING_SIZE), hsva_to_rgba(0, 0, 0.9), hsva_to_rgba(0, 0, 0.7), 200)
    drawing.add_gradient(Pos(150, 150), Pos(DRAWING_SIZE-150, DRAWING_SIZE-150), hsva_to_rgba(0, 0, 1), hsva_to_rgba(0, 0, 1), 200)

    # title text
    drawing.write(Pos(160, 170), ["You're the", "real legend!"], 50)

    drawing.write(Pos(160, 300), ["As for code it's not",
                                  "really in any state",
                                  "where it would be useful to",
                                  "anyone so you won't be",
                                  "finding it on github for now.",
                                  "The code is really bad and",
                                  "barely works just to",
                                  "prototype everything on nifty.",
                                  "I also don't know how the dev",
                                  "feels about me betraying the",
                                  "\"spirit\" of nifty, so I",
                                  "wouldn't want to release any",
                                  "code without permission.",
                                  "but If you ask in the chat",
                                  "i will likely dm you to",
                                  "share the code anyway."], 25, 1.35)

    return drawing


def main():

    # drawing = square_fractal(Drawing(), [8, 1, 5, 0], 8)
    drawing = big_text_boi(Drawing())

    # scale down so it not touch edgy
    # drawing *= 0.95

    print(f"Lines: {len(drawing.object['lines'])}, Size: {len(drawing.to_nifty_import())}")
    with open("output.txt", "w") as file:
        file.write(drawing.to_nifty_import())


if __name__ == '__main__':
    main()

# lines, chars, seconds
# 2187, 351713, 134
# 760, 114419, 23
#
#
#
#
#
#
#
#