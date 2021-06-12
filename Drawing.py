import json
import random
import pygame
import os

from Pos import Pos
from constants import DRAWING_SIZE, GOLDEN_RATIO, BLACK, WHITE, TITLE_BAR_HEIGHT, BORDER_WIDTH


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

    def add_strict_line(self, pos_list, colour, brush_radius, enclosed_path=False):
        # create points for square
        points_list = [pos_list[0].point()]
        for pos in pos_list[1:-1]:
            points_list.append(pos.point())
            points_list.append(pos.point())
        points_list.append(pos_list[-1].point())
        if enclosed_path:
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
                "c": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7)]], 1),
                "d": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 1), Pos(0.1, 1)]], 1),
                "e": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.1, 0.5), Pos(0.6, 0.5)],
                       [Pos(0.1, 1), Pos(0.9, 1)]], 1),
                "f": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.1, 0.5), Pos(0.6, 0.5)]], 1),
                "g": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7), Pos(0.9, 0.5)],
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
                "o": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7), Pos(0.9, 0.3)]], 1),
                "p": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.1, 0.5)]], 1),
                "q": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7), Pos(0.9, 0.3)],
                       [Pos(0.7, 0.8), Pos(0.9, 1)]], 1),
                "r": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.1, 0.5)],
                       [Pos(0.6, 0.5), Pos(0.9, 1)]], 1),
                "s": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.5), Pos(0.9, 0.5), Pos(0.9, 1), Pos(0.1, 1),
                        Pos(0.1, 0.7)]], 1),
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
                "0": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7), Pos(0.9, 0.3)],
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

    def render(self, pygame_scale=None, headless=False, filename="output.png"):
        # Set a fake video driver to hide output
        if headless:
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
            # No screen to get the dimensions, just render at normal size
            if pygame_scale is None:
                pygame_scale = 1

        pygame.init()

        # Position the window perfectly if it's not headless
        if not headless:
            info_object = pygame.display.Info()
            smallest_dimension = min(info_object.current_w, info_object.current_h)

            x = round((info_object.current_w-(smallest_dimension-TITLE_BAR_HEIGHT-(BORDER_WIDTH*2)))/2)
            y = TITLE_BAR_HEIGHT+BORDER_WIDTH
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

            # Scale the window and drawing to the maximum square size
            if pygame_scale is None:
                pygame_scale = (smallest_dimension-TITLE_BAR_HEIGHT-(BORDER_WIDTH*2)) / DRAWING_SIZE

        # Initialise the window with dimensions
        screen = pygame.display.set_mode((round(DRAWING_SIZE * pygame_scale), round(DRAWING_SIZE * pygame_scale)))

        pygame.display.set_caption("Drawing Render")
        screen.fill(WHITE[:3])

        for line in self.object["lines"]:
            brush_radius = line["brushRadius"] * pygame_scale
            color = [float(cell) for cell in list(line["brushColor"][5:-1].split(","))]

            points = []
            for point in line["points"]:
                this_point = (point["x"] * pygame_scale, point["y"] * pygame_scale)
                points.append(this_point)
                pygame.draw.circle(screen, color, this_point, int(brush_radius))

            pygame.draw.lines(screen, color, False, points, int(brush_radius*2))

        # update screen to render drawing
        pygame.display.update()
        print(f"\nSaving {filename}")
        pygame.image.save(screen, filename)
        print("Saved.")

        # enter a loop to prevent pygame from ending
        running = True
        while running and not headless:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    running = False
                    break

    def to_nifty_import(self):
        return "drawingCanvas.current.loadSaveData(\"" + json.dumps(self.object).replace('"', '\\"') + "\", false)"

    def shuffle_lines(self):
        random.shuffle(self.object["lines"])
