import math
import random

from Pos import Pos
from Vector2D import Vector2D
from Matrix2D import Matrix2D
from constants import DRAWING_SIZE
from helperFns import interpolate_colour


# -------------------------------------
# General methods

# Turn vector into Pos
def vect_to_pos(v1, mx, v2, wobble_px=0, scale=1):
    wobble_x = wobble_px * (random.random() - 0.5)
    wobble_y = wobble_px * (random.random() - 0.5)
    v3 = v1 + (mx * v2) * scale + Vector2D(wobble_x, wobble_y)
    pos1 = Pos(v3.x, DRAWING_SIZE - v3.y)
    return pos1

# Get an interpolated colour using a list of colours, and the progress through the list
def get_colour(cols, progress, alpha=1):
    len_col = len(cols) - 1
    prog2 = progress * len_col
    prog_rem = prog2 - math.floor(prog2)
    colour_start = cols[math.floor(prog2)]
    colour_end = cols[math.ceil(prog2)]
    colour_this = interpolate_colour(colour_start, colour_end, prog_rem, alpha)
    return colour_this


# -------------------------------------
# Methods to calculate a random id

# Select an id at random from a list, equal weights
def rand_id(list_of_ids):
    def callback():
        return random.choice(list_of_ids)
    return callback


# -------------------------------------
# Methods to calculate a random vector

# Calculate a random continuous vector in the rectangle [x1, x2] x [y1, y2]
def rand_vect_cts(x1, y1, x2, y2):
    def callback():
        return Vector2D(x1 + (x2 - x1) * random.random(), y1 + (y2 - y1) * random.random())
    return callback


# -------------------------------------
# Methods to calculate a random matrix

# Any rotation in the circle
def rand_mx_rotation(scale=1):
    def callback():
        return Matrix2D.rotd(360 * random.random()) * scale
    return callback

# Any rotation or reflection in the circle
def rand_mx_circle(scale=1):
    def callback():
        mx = Matrix2D.rotd(360 * random.random())
        if (random.random() < 0.5):
            mx = mx * Matrix2D(-1, 0, 0, 1)
        return mx * scale
    return callback

# Any rotation or reflection in a square with a flat edge down
def rand_mx_square(scale=1):
    def callback():
        return Matrix2D.sq(random.randint(1, 8)) * scale
    return callback

# Any rotation or reflection in a triangle with a flat edge down
def rand_mx_triangle(scale=1):
    def callback():
        return Matrix2D.dh(3, random.randint(1, 6)) * scale
    return callback

# Any rotation or reflection in a <sides>-sided polygon with a flat edge down
def rand_mx_dihedral(sides, scale=1):
    def callback():
        return Matrix2D.dh(sides, random.randint(1, sides * 2)) * scale
    return callback
