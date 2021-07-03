import math
import random

from Pos import Pos
from FractalPiece import FractalPiece
from constants import DRAWING_SIZE, BLACK
from helperFns import interpolate_colour
from numpyHelperFns import array_rms_metric, vect, mx_id, mx_rotd, mx_refl_X, mx_sq, mx_dh


# -------------------------------------
# General methods

# Turn Numpy vector into Pos
# Pos has origin in top left, vectors in bottom left, so invert in y-axis
def get_canvas_pos_from_vect(vect):
    return Pos(vect[0], DRAWING_SIZE - vect[1])

# Get an interpolated colour using:
# - a list of colours,
# - a progress factor between 0 and 1 representing how far we are through the list
def get_colour(colour_list, progress, alpha=1):
    max_prog = len(colour_list) - 1
    prog2 = max(0, min(max_prog, progress * max_prog))
    prog_rem = prog2 - math.floor(prog2)
    colour_start = colour_list[math.floor(prog2)]
    colour_end = colour_list[math.ceil(prog2)]
    colour_this = interpolate_colour(colour_start, colour_end, prog_rem, alpha)
    return colour_this


# -------------------------------------
# Random vector functions for drawing-by-hand "hand wobble" effect

# Return 2D square or 3D cube uniform distribution
def wobble_square(pixels=2, dim=2):
    def get_rand_unif():
        return random.uniform(-0.5 * pixels, 0.5 * pixels)
    def result_fn():
        x, y, z = get_rand_unif(), get_rand_unif(), get_rand_unif()
        return vect(x, y, z) if dim == 3 else vect(x, y)
    return result_fn

# TODO: 2D circle uniform, 3D sphere uniform, 2D concentrated at centre, etc


# -------------------------------------
# Plotting functions

# Plot a dot (small circle) for each fractal piece
# Optional parameter expand_factor is to fine-tune control of dot size
def plot_dot(expand_factor=1, wobble_fn=None, offset_vect=None):
    def result_fn(drawing, piece, colour=BLACK):
        piece_vect = piece.get_vect()
        wobble_vect = wobble_fn() if callable(wobble_fn) else piece_vect * 0
        if not offset_vect is None:
            mx = piece.get_mx()
            piece_vect = piece_vect + mx @ offset_vect
        pos = get_canvas_pos_from_vect(piece_vect + wobble_vect)
        dot_radius = expand_factor * piece.get_radius()
        drawing.add_point(pos, colour, dot_radius)
    return result_fn

# Plot a path (series of line segments) for each fractal piece
def plot_path(vector_list, closed=False, width=1, expand_factor=1, wobble_fn=None):
    def result_fn(drawing, piece, colour=BLACK):
        piece_vect = piece.get_vect()
        piece_mx = piece.get_mx()
        pos_list = []
        for i in range(0, len(vector_list)):
            wobble_vect = wobble_fn() if callable(wobble_fn) else piece_vect * 0
            draw_vect = piece_vect + wobble_vect + (piece_mx @ vector_list[i]) * expand_factor
            pos_list.append(get_canvas_pos_from_vect(draw_vect))
        if closed:
            pos_list.append(pos_list[0])
        drawing.add_line(pos_list, colour, width)
    return result_fn


# -------------------------------------
# Colouring functions

# Colour by progress through list from FractalSystem
def colour_by_progress(colour_list):
    def result_fn(piece, progress):
        return get_colour(colour_list, progress)
    return result_fn

# Colour by a function of the piece's affine transformation (vector, matrix)
# tsfm_to_num_fn(vect, matrix) should output a number
def colour_by_tsfm(min_val, max_val, tsfm_to_num_fn, colour_list):
    def result_fn(piece, progress):
        if not callable(tsfm_to_num_fn):
            return BLACK
        # this_val = min(max_val, max(min_val, tsfm_to_num_fn(piece.get_vect(), piece.get_mx())))
        this_val = tsfm_to_num_fn(piece.get_vect(), piece.get_mx())
        this_tsfm_progress = (this_val - min_val) / (max_val - min_val)
        return get_colour(colour_list, this_tsfm_progress)
    return result_fn

# Colour by a function of the piece's affine transformation (vector, matrix)
# tsfm_to_num_fn(vect, matrix) should output a number
def colour_by_log2_size(min_val, max_val, colour_list):
    fn = lambda vect, mx: math.log(array_rms_metric(mx), 2)
    return colour_by_tsfm(min_val, max_val, fn, colour_list)


# -------------------------------------
# Sorting functions for lists of fractal pieces
# Usage:
# fractal_system.piece_sorter = sort_function(arguments_if_needed)

# Sort pieces randomly
def sort_randomly():
    def result_fn(piece):
        return random.random()
    return result_fn
    
# Sort by function of the piece's affine transformation (vector, matrix)
def sort_by_tsfm(tsfm_to_num_fn):
    def result_fn(piece):
        return tsfm_to_num_fn(piece.get_vect(), piece.get_mx())
    return result_fn
    
# Sort by z-coordinate (reversed), e.g. for 3D fractals
def sort_by_z():
    return sort_by_tsfm(lambda vect, mx: -vect[2])
    
# Sort by size
def sort_by_size():
    return sort_by_tsfm(lambda vect, mx: -array_rms_metric(mx))
    

# -------------------------------------
# Methods to calculate callback for children on fractal definitions

# For a square [-1, 1] x [-1, 1]
# split it into n^2 tiles (nxn)
# and then keep m out of n^2 at random
def defngen_rand_small_squares(id, m, n):
    sc = 1 / n
    def callback():
        children = []
        for x in range(n):
            for y in range(n):
                x0 = 2*x - (n-1)
                y0 = 2*y - (n-1)
                children.append(FractalPiece(id, vect(x0, y0) * sc, mx_id() * sc))
        return random.sample(children, m)
    return callback


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
