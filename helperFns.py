import math

from Pos import Pos
from constants import DRAWING_SIZE
from math import comb


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

def get_bezier_curve(control_points, step_size=10, t=True):
    m, q, bezier_points, s = list(zip(*control_points)), len(control_points), [], (step_size - 1 if t else step_size) / 1.
    for i in range(step_size):
        b = [comb(q - 1, v) * (i / s) ** v * (1 - (i / s)) ** (q - 1 - v) for v in range(q)]
        bezier_points += [(tuple(sum(j * k for j, k in zip(d, b)) for d in m))]
    return bezier_points

def get_bounded_int(lowest_integer, highest_integer, num):
    return max(lowest_integer, min(highest_integer, round(num)))

def interpolate_colour(start_col, end_col, amount, alpha_factor=1):
    r = get_bounded_int(0, 255, start_col[0] * (1 - amount) + end_col[0] * amount)
    g = get_bounded_int(0, 255, start_col[1] * (1 - amount) + end_col[1] * amount)
    b = get_bounded_int(0, 255, start_col[2] * (1 - amount) + end_col[2] * amount)
    a = max(0, min(1, alpha_factor * (start_col[3] * (1 - amount) + end_col[3] * amount)))
    return (r, g, b, a)