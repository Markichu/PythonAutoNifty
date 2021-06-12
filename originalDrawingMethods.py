from PIL import Image
import random
import math

from Pos import Pos

from constants import DRAWING_SIZE, GOLDEN_RATIO, BLACK, WHITE
from helperFns import deg_to_rad, rotate, hsva_to_rgba


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
            if len(colour) == 4:
                if colour[3] > 0.25:
                    drawing.add_point(Pos((x + 0.5) * x_diff, (y + 0.5) * y_diff), colour, x_diff * pow(2, 0.5) / 2)
            else:
                colour.append(1)
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
        radians = i * (2 - (2 / GOLDEN_RATIO)) * math.pi
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
        radians = i * (2 - (2 / GOLDEN_RATIO)) * math.pi
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
    drawing.write(Pos(160, 170), ["Huyen", "Nguyen rocks!"], 50)

    drawing.write(Pos(160, 300), ["BEST...",
                                  "WIFE....",
                                  "EVA!!!"], 25, 1.35)

    return drawing
