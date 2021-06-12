import math

from Pos import Pos
from constants import DRAWING_SIZE


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

def get_bounded_int(lowest_integer, highest_integer, num):
    return max(lowest_integer, min(highest_integer, round(num)))

def interpolate_colour(start_col, end_col, amount):
    r = get_bounded_int(0, 255, start_col[0] * (1 - amount) + end_col[0] * amount)
    g = get_bounded_int(0, 255, start_col[1] * (1 - amount) + end_col[1] * amount)
    b = get_bounded_int(0, 255, start_col[2] * (1 - amount) + end_col[2] * amount)
    a = get_bounded_int(0, 255, start_col[3] * (1 - amount) + end_col[3] * amount)
    return (r, g, b, a)