import math
import random

from Pos import Pos
from constants import DRAWING_SIZE
from helperFns import interpolate_colour
from numpyHelperFns import vect, mx_rotd, mx_refl_x, mx_sq, mx_dh


# -------------------------------------
# General methods


# Turn Numpy vector into Pos
def get_canvas_pos(v1, mx, v2, wobble_px=0, scale=1):
    wobble_x = wobble_px * (random.random() - 0.5)
    wobble_y = wobble_px * (random.random() - 0.5)
    v3 = v1 + (mx @ v2) * scale + vect(wobble_x, wobble_y)
    pos1 = Pos(v3[0], DRAWING_SIZE - v3[1])
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
def idgen_rand(list_of_ids):
    def callback():
        return random.choice(list_of_ids)
    return callback


# -------------------------------------
# Methods to calculate a random vector

# Calculate a random continuous vector in the rectangle [x1, x2] x [y1, y2]
def vectgen_rand(x1, y1, x2, y2):
    def callback():
        return vect(x1 + (x2 - x1) * random.random(), y1 + (y2 - y1) * random.random())
    return callback


# -------------------------------------
# Methods to calculate a random matrix

# Any rotation or reflection in the circle
def mxgen_rand_circ(scale=1, reflect=True):
    def callback():
        mx = mx_rotd(360 * random.random())
        if reflect and (random.random() < 0.5):
            mx = mx @ mx_refl_x()
        return mx * scale
    return callback

# Any rotation or reflection in a square with a flat edge down
def mxgen_rand_sq(scale=1, reflect=True):
    max_num = 4
    if reflect:
        max_num = 8
    def callback():
        return mx_sq(random.randint(1, max_num)) * scale
    return callback

# Any rotation or reflection in a triangle with a flat edge down
def mxgen_rand_tri(scale=1, reflect=True):
    max_num = 3
    if reflect:
        max_num = 6
    def callback():
        return mx_dh(3, random.randint(1, max_num)) * scale
    return callback

# Any rotation or reflection in a <sides>-sided polygon with a flat edge down
def mxgen_rand_dihedral(sides, scale=1, reflect=True):
    max_num = sides
    if reflect:
        max_num = sides * 2
    def callback():
        return mx_dh(sides, random.randint(1, max_num)) * scale
    return callback
