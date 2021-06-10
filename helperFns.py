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
