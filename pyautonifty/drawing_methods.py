from PIL import Image
import random
import math
import numpy as np

from .pos import Pos
from .constants import DRAWING_SIZE, GOLDEN_RATIO, BLACK, WHITE
from .helper_fns import rotate, hsva_to_rgba


# Draw an image from file using dots as pixels
# Many image formats are supported, including .jpg and .png
def point_image(drawing, image_name, do_a_shuffle=False,
                width=DRAWING_SIZE, height=DRAWING_SIZE,
                position=Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2), keep_aspect_ratio=False, rotation=None):
    # load image from file
    image = Image.open(image_name)

    # convert the image to RGBA values
    rgba_image = image.convert('RGBA')

    # init width and height
    pixel_width, pixel_height = image.size

    if keep_aspect_ratio:  # keep the images original shape
        x_diff = width / max(pixel_width, pixel_height)
        y_diff = height / max(pixel_width, pixel_height)
        max_diff = max(x_diff, y_diff)

        # Centre the image if it isn't a square
        x_offset = abs(max(pixel_width, pixel_height) - pixel_width) / 2
        y_offset = abs(max(pixel_width, pixel_height) - pixel_height) / 2
    else:  # stretch the image to be a square
        x_diff = width / pixel_width
        y_diff = height / pixel_height
        max_diff = max(x_diff, y_diff)

        x_offset = 0
        y_offset = 0

    for x in range(pixel_width):
        for y in range(pixel_height):
            colour = list(rgba_image.getpixel((x, y)))
            colour[3] /= 255

            # Do the initial position calculation
            px = (x + 0.5 + x_offset) * x_diff
            py = (y + 0.5 + y_offset) * y_diff

            # Adjust the position of the image
            px += position.x - (width / 2)
            py += position.y - (height / 2)

            pos = Pos(px, py)

            # Rotate the position
            if rotation:
                pos = rotate(pos, rotation, origin=position)

            pr = max_diff * pow(2, 0.5) / 2
            drawing.add_point(pos=pos, colour=colour, brush_radius=pr)

    if do_a_shuffle:
        drawing.shuffle_lines()

    return drawing


# Draw an image from file using square pixels
def square_image(drawing, image_name, brush_radius=1, do_a_shuffle=False,
                 width=DRAWING_SIZE, height=DRAWING_SIZE,
                 position=Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2), keep_aspect_ratio=False, rotation=None):
    # load image from file
    image = Image.open(image_name)

    # convert the image to RGBA values
    rgba_image = image.convert('RGBA')

    # init width and height
    pixel_width, pixel_height = image.size

    if keep_aspect_ratio:  # keep the images original shape
        square_pixel_width = width / max(pixel_width, pixel_height)
        square_pixel_height = height / max(pixel_width, pixel_height)

        # Centre the image if it isn't a square
        x_offset = abs(max(pixel_width, pixel_height) - pixel_width) / 2
        y_offset = abs(max(pixel_width, pixel_height) - pixel_height) / 2
    else:  # stretch the image to be a square
        square_pixel_width = width / pixel_width
        square_pixel_height = height / pixel_height

        x_offset = 0
        y_offset = 0

    for x in range(pixel_width):
        for y in range(pixel_height):
            colour = list(rgba_image.getpixel((x, y)))
            colour[3] /= 255

            # Do the initial position calculation
            px = (x + 0.5 + x_offset) * square_pixel_width
            py = (y + 0.5 + y_offset) * square_pixel_height

            # Adjust the position of the image
            px += position.x - (width / 2)
            py += position.y - (height / 2)

            pos = Pos(px, py)

            # Rotate the position
            if rotation:
                pos = rotate(pos, rotation, origin=position)

            drawing.add_rounded_rectangle(centre_pos=pos, width=square_pixel_width, height=square_pixel_height, colour=colour, brush_radius=brush_radius)

    if do_a_shuffle:
        drawing.shuffle_lines()

    return drawing


# Draw four black squares nearly filling the canvas, with different rounding on each corner
def square_example(drawing):
    drawing.add_rounded_square(centre_pos=Pos(250, 250), width=400, colour=BLACK, brush_radius=0.1)
    drawing.add_rounded_square(centre_pos=Pos(750, 250), width=400, colour=BLACK, brush_radius=2)
    drawing.add_rounded_square(centre_pos=Pos(250, 750), width=400, colour=BLACK, brush_radius=40)
    drawing.add_rounded_square(centre_pos=Pos(750, 750), width=400, colour=BLACK, brush_radius=1000)
    return drawing


# Draw four black rectangles nearly filling the canvas, with different rounding on each corner
def rectangle_example(drawing):
    drawing.add_rounded_rectangle(centre_pos=Pos(250, 250), width=400, height=200, colour=BLACK, brush_radius=0.1)
    drawing.add_rounded_rectangle(centre_pos=Pos(750, 250), width=200, height=400, colour=BLACK, brush_radius=2)
    drawing.add_rounded_rectangle(centre_pos=Pos(250, 750), width=400, height=200, colour=BLACK, brush_radius=40)
    drawing.add_rounded_rectangle(centre_pos=Pos(750, 750), width=200, height=400, colour=BLACK, brush_radius=1000)
    return drawing


# Draw a square that appears to rotate on the Nifty Ink canvas
def rotating_square(drawing):
    drawing.add_background((255, 255, 255, 1))
    p1 = Pos(200, 200)
    p2 = Pos(200, 800)
    p3 = Pos(800, 800)
    p4 = Pos(800, 200)
    for _ in range(500):
        drawing.add_line([p1, p2, p3, p4], (0, 0, 0, 1), 10)
        drawing.add_pause(10)
        drawing.add_background((255, 255, 255, 1))
        p1 = rotate(p1, 0.1)
        p2 = rotate(p2, 0.1)
        p3 = rotate(p3, 0.1)
        p4 = rotate(p4, 0.1)
    drawing.add_line([p1, p2, p3, p4], (0, 0, 0, 1), 10)
    return drawing


# Draw a pattern involving a lot of diagonal lines
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


# Draw a pattern of spiralling dots
def fibonacci_dots(drawing, n=1000):
    for i in range(n):
        # calc radians of rotation and radius from centre
        radians = i * (2 - (2 / GOLDEN_RATIO)) * math.pi
        radius = math.sqrt(i + 1) * DRAWING_SIZE / math.sqrt(n)

        # calc position of dot
        pos = Pos.from_rotational(radians, radius)

        # draw dot
        drawing.add_point(pos, BLACK, 5)

    return drawing


# Draw an image using spiralling dots
def fibonacci_image(drawing, image_filename, n=3000):
    # load image from file
    image = Image.open(image_filename)

    # init result
    width, height = image.size

    for i in range(n):
        # calc radians of rotation and radius from centre
        radians = i * (2 - (2 / GOLDEN_RATIO)) * math.pi
        radius = math.sqrt(i + 1) * DRAWING_SIZE / math.sqrt(n)

        # calc position of dot
        pos = Pos.from_rotational(radians, radius)

        # calc size of dot from image brightness
        image_pos = round((pos.copy() / DRAWING_SIZE) * width) - Pos(1, 1)
        colour = list(image.getpixel((image_pos.x, image_pos.y)))
        brightness = 1 - ((0.2126 * colour[0] + 0.7152 * colour[1] + 0.0722 * colour[2]) / 265)

        # draw dot
        drawing.add_point(pos, colour, brightness * DRAWING_SIZE / math.sqrt(n) / 2)

    return drawing


# Squared Circle example
def squared_circle(drawing, n=8):
    # init step and drawing
    step = 90 / n
    current_h = 0.8

    for i in range(n):
        # get degrees around circle and position
        degrees = i * step + (step / 2)

        # get pos for corners
        pos1 = Pos.from_rotational(np.radians(degrees), DRAWING_SIZE).rotate(np.radians(45))
        pos2 = Pos(pos1.x, DRAWING_SIZE - pos1.y).rotate(np.radians(45))
        pos3 = Pos(DRAWING_SIZE - pos1.x, DRAWING_SIZE - pos1.y).rotate(np.radians(45))
        pos4 = Pos(DRAWING_SIZE - pos1.x, pos1.y).rotate(np.radians(45))

        # do colour
        colour = hsva_to_rgba(current_h, 0.8, 0.85)
        current_h -= 0.7 / n

        # add square
        drawing.add_line([pos1, pos2, pos3, pos4], colour, DRAWING_SIZE / (25 * n))

    return drawing


# Draw straight lines that combine to create impression of curved lines
def curved_lines(drawing, n=20):
    # init drawing
    step = DRAWING_SIZE / n

    # do curved lines
    for i in range(n + 1):
        offset = i * step
        # do bottom left line
        drawing.add_straight_line(Pos(offset, DRAWING_SIZE), Pos(0, offset), BLACK, DRAWING_SIZE / (25 * n))
        # do top right
        drawing.add_straight_line(Pos(DRAWING_SIZE, offset), Pos(offset, 0), BLACK, DRAWING_SIZE / (25 * n))

    # do diagonal lines
    for i in range(n - 1):
        offset = (i + 1) * step
        # do top left line
        drawing.add_straight_line(Pos(offset, 0), Pos(0, offset), BLACK, DRAWING_SIZE / (25 * n))
        # do bottom right
        drawing.add_straight_line(Pos(DRAWING_SIZE, DRAWING_SIZE - offset), Pos(DRAWING_SIZE - offset, DRAWING_SIZE), BLACK, DRAWING_SIZE / (25 * n))

    # do middle diagonal
    drawing.add_straight_line(Pos(DRAWING_SIZE, 0), Pos(0, DRAWING_SIZE), BLACK, DRAWING_SIZE / (25 * n))

    return drawing


# Draw concentric rings of circles getting smaller
def shrinking_circle_ring(drawing, n=20, m=36):
    radians_step = 2 * math.pi / m
    current_h = 0
    big_radius = DRAWING_SIZE / 2
    for _ in range(n):
        # calc current radius
        big_radius = (m * big_radius) / (m + 2 * math.pi)
        small_radius = (math.pi * big_radius) / m

        # do colour
        colour = hsva_to_rgba(current_h, 0.8, 0.9)
        current_h -= 1 / n

        # draw circles around radius
        for i in range(m):
            pos = Pos.from_rotational(radians_step * i, big_radius)
            drawing.add_point(pos, colour, small_radius)
            drawing.add_point(pos, WHITE, small_radius / 3)

    drawing *= 2

    return drawing


# Draw a square fractal which splits a square into 4 more squares (2x2), and iterates on 3 out of 4 smaller squares.
# Note - this is Markichu's original fractal drawing method for square fractals
# It was derived from davidryan59/niftymaestro drawings on Nifty Ink
# Subsequently, davidryan59 implemented more generalised fractal drawing methods, see fractalRunner, FractalSystem etc.
def square_fractal(drawing, master_key, iterations=5):
    # add gradient background
    drawing.add_gradient(Pos(0, 0), Pos(DRAWING_SIZE, DRAWING_SIZE), hsva_to_rgba(0, 0, 0.9), hsva_to_rgba(0, 0, 0.7), 200)
    drawing *= 1 / 0.95

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


def text_drawing_example(drawing, font_file_name=None, draw_bounding_box=False):
    drawing.add_gradient(Pos(0, 0), Pos(DRAWING_SIZE, DRAWING_SIZE), hsva_to_rgba(0, 0, 0.9), hsva_to_rgba(0, 0, 0.7), 200)
    drawing.add_gradient(Pos(150, 150), Pos(DRAWING_SIZE - 150, DRAWING_SIZE - 150), hsva_to_rgba(0, 0, 1), hsva_to_rgba(0, 0, 1), 200)

    # Examples of writing:
    # title text
    drawing.write(pos=Pos(160, 170), lines=["Add a title", "here!"], font_size=50, font_file_name=font_file_name, draw_bounding_box=draw_bounding_box)
    # body text
    drawing.write(pos=Pos(160, 300), lines=["Add some interesting",
                                            "content and words",
                                            "here!"], font_size=25, line_spacing=1.35, colour=(64, 64, 200, 1), font_file_name=font_file_name, draw_bounding_box=draw_bounding_box)

    return drawing


def alpha_example(drawing):
    for i in range(random.randint(0, 100)):
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.random())
        position = Pos(random.randint(0, DRAWING_SIZE), random.randint(0, DRAWING_SIZE))
        brush_radius = random.randint(1, 500)
        drawing.add_point(position, colour, brush_radius)
        line_points = []
        for j in range(random.randint(2, 20)):
            line_points.append(Pos(random.randint(0, DRAWING_SIZE), random.randint(0, DRAWING_SIZE)))
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.random())
        brush_radius = random.randint(1, 10)
        drawing.add_quadratic_bezier_curve(line_points, colour, brush_radius)
    return drawing


def star_example(drawing, lines=10, line_segments=100, draw_points=False, transparency=False, curved_lines=False, enclosed_path=False):
    all_points = []
    drawing.add_point(Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2), BLACK, 500)
    num = random.randint(2, 10)
    rot = random.random() * 1 + random.randint(0, 1)
    for j in range(random.randint(2, lines)):
        line_points = []
        for i in range(random.randint(2, line_segments)):
            # calc position of dot
            pos = Pos.from_rotational(rot * math.pi * i * j, num * j * i)
            # draw dot
            line_points.append(pos)

        colour = [random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 1]
        if transparency:
            colour[-1] = random.random()
        brush_radius = 1
        if curved_lines:
            drawing.add_quadratic_bezier_curve(line_points, colour, brush_radius, enclosed_path=True)
        else:
            drawing.add_line(line_points, colour, brush_radius, enclosed_path=enclosed_path)

        all_points.extend(line_points)

    if draw_points:
        for pnt in all_points:
            colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 1]
            if transparency:
                colour[-1] = random.random()
            brush_radius = random.randint(10, 20)
            position = pnt + Pos(0.5, 0.5)
            drawing.add_point(position, colour, brush_radius)
        for pnt in all_points:
            colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 1]
            if transparency:
                colour[-1] = random.random()
            brush_radius = random.randint(3, 9)
            position = pnt + Pos(0.5, 0.5)
            drawing.add_point(position, colour, brush_radius)
    return drawing
