import math
import random

from Pos import Pos
from constants import DRAWING_SIZE, BLACK
from helperFns import interpolate_colour
from numpyHelperFns import np_dim, vect, mx_rotd, mx_refl_X, mx_sq, mx_dh


# -------------------------------------
# General methods

# Turn Numpy vector into Pos
def get_canvas_pos(v1, mx, v2, wobble_px=0, scale=1):
    def get_wobble():
        return random.uniform(-0.5 * wobble_px, 0.5 * wobble_px)
    vw = None
    if np_dim(v1) == 2:
        vw = vect(get_wobble(), get_wobble())
    elif np_dim(v1) == 3:
        vw = vect(get_wobble(), get_wobble(), get_wobble())
    else:
        raise TypeError('Vector must be 2 or 3 dimensional')
    v3 = v1 + (mx @ v2) * scale + vw
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
# Plotting functions

# Plot a single dot for a fractal piece
def plot_dot(dot_expand_factor=1, wobble_px=0):
    def result_fn(drawing, piece, colour=BLACK):
        piece_vect = piece.get_vect()
        piece_mx = piece.get_mx()
        piece_radius = piece.get_radius()
        offset_vect = piece_vect * 0
        pos = get_canvas_pos(piece_vect, piece_mx, offset_vect, wobble_px, 1)
        circle_radius = dot_expand_factor * piece_radius
        drawing.add_point(pos, colour, circle_radius)
    return result_fn

# Plot a series of line segments for a fractal piece
def plot_lines(path_vects, path_close=False, path_width=1, path_expand_factor=1, wobble_px=0):
    def result_fn(drawing, piece, colour=BLACK):
        path_len = len(path_vects)
        piece_vect = piece.get_vect()
        piece_mx = piece.get_mx()
        pos_list = []
        for i in range(0, path_len):
            pos_list.append(get_canvas_pos(piece_vect, piece_mx, path_vects[i], wobble_px, path_expand_factor))
        if path_close:
            pos_list.append(pos_list[0])
        drawing.add_line(pos_list, colour, path_width)
    return result_fn

# -------------------------------------
# Colouring functions

# Colour by progress through list from FractalSystem
def colour_by_progress(colour_list):
    def inner_fn(piece, progress):
        return get_colour(colour_list, progress)
    return inner_fn

# Colour by a function of the piece's affine transformation (vector, matrix)
# tsfm_to_num_fn(vect, matrix) should output a number
def colour_by_tsfm(min_val, max_val, tsfm_to_num_fn, colour_list):
    def inner_fn(piece, progress):
        if not callable(tsfm_to_num_fn):
            return BLACK
        this_val = min(max_val, max(min_val, tsfm_to_num_fn(piece.get_vect(), piece.get_mx())))
        this_tsfm_progress = (this_val - min_val) / (max_val - min_val)
        return get_colour(colour_list, this_tsfm_progress)
    return inner_fn


# -------------------------------------
# FractalSystem sorters

# Sort pieces randomly
def sort_randomly(piece):
    return random.random()
    
# Sort by z-coordinate (reversed)
def sort_by_z(piece):
    return -piece.get_vect()[2]
    

# -------------------------------------
# Methods to calculate a random id

# Select an id at random from a list, equal weights
def idgen_rand(list_of_ids):
    def callback():
        return random.choice(list_of_ids)
    return callback


# -------------------------------------
# 2D or 3D methods to calculate a random vector

# Calculate a random continuous 2D or 3D vector in (x1, x2) x (y1, y2) [x (z1, z2)]
# Example: vectgen_rand([1, 2], [3, 4], [5, 6])
def vectgen_rand(x_range, y_range, z_range=None):
    def callback():
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        if z_range is None:
            return vect(x, y)
        z = random.uniform(z_range[0], z_range[1])
        return vect(x, y, z)
    return callback


# -------------------------------------
# 2D methods to calculate a random matrix

# Any rotation or reflection in the circle
def mxgen_rand_circ(scale=1, reflect=True):
    def callback():
        mx = mx_rotd(random.uniform(0, 360))
        if reflect and (random.random() < 0.5):
            mx = mx @ mx_refl_X()
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
