import math
import random

from Pos import Pos
from constants import DRAWING_SIZE, BLACK
from helperFns import interpolate_colour
from numpyHelperFns import metric_matrix_min_eig_val, vect


# -------------------------------------
# General methods

# Turn Numpy vector into Pos
# Pos has origin in top left, vectors in bottom left, so invert in y-axis
def get_canvas_pos_from_vect(vect):
    return Pos(vect[0], DRAWING_SIZE - vect[1])

# Get an interpolated colour using:
# - a list of colours,
# - a progress factor between 0 and 1 representing how far we are through the list
def get_colour(colours, progress, alpha=1):
    max_prog = len(colours) - 1
    prog2 = max(0, min(max_prog, progress * max_prog))
    prog_rem = prog2 - math.floor(prog2)
    colour_start = colours[math.floor(prog2)]
    colour_end = colours[math.ceil(prog2)]
    colour_this = interpolate_colour(colour_start, colour_end, prog_rem, alpha)
    return colour_this


# -------------------------------------
# Metrics for Fractal Pieces
# Currently using only the matrix, but could depend on many things,
# such as minimum diameter of convex hull after shear/stretching

# Use the minimum eigenvalue of the matrix
def metric_piece_min_eig():
    def callback(piece):
        return metric_matrix_min_eig_val(piece.get_mx())
    return callback


# -------------------------------------
# Random vector functions for drawing-by-hand "hand wobble" effect

# Return 2D square or 3D cube uniform distribution
def wobble_square(pixels=2, dim=2):
    def get_rand_unif():
        return random.uniform(-0.5 * pixels, 0.5 * pixels)
    def callback():
        x, y, z = get_rand_unif(), get_rand_unif(), get_rand_unif()
        return vect(x, y, z) if dim == 3 else vect(x, y)
    return callback

# TODO: 2D circle uniform, 3D sphere uniform, 2D concentrated at centre, etc

# Return vector in a rectangular grid. Example (considering x-coord only):
# x_steps = 4
# x_min = -1
# x_max = 1
# Then supply x_pos = 0, 1, 2, 3
# Output is x_this = -0.75, -0.25, 0.25, 0.75
def grid_generator(x_steps, y_steps, x_min, y_min, x_max, y_max):
    def grid(x_pos, y_pos):
        x_progress = (x_pos + 0.5) / x_steps
        y_progress = (y_pos + 0.5) / y_steps
        x_this = x_min + x_progress * (x_max - x_min)
        y_this = y_min + y_progress * (y_max - y_min)
        return vect(x_this, y_this)
    return grid


# -------------------------------------
# Plotting functions

# Plot a dot (small circle) for each fractal piece
# Optional parameter expand_factor is to fine-tune control of dot size
def plot_dot(expand_factor=1, wobble_fn=None, offset_vect=None):
    def callback(drawing, piece, colour=BLACK):
        piece_vect = piece.get_vect()
        wobble_vect = wobble_fn() if callable(wobble_fn) else piece_vect * 0
        if not offset_vect is None:
            mx = piece.get_mx()
            piece_vect = piece_vect + mx @ offset_vect
        pos = get_canvas_pos_from_vect(piece_vect + wobble_vect)
        dot_radius = expand_factor * piece.get_metric()
        drawing.add_point(pos, colour, dot_radius)
    return callback

# Plot a path (series of line segments) for each fractal piece
def plot_path(vector_list, closed=False, width=1, expand_factor=1, wobble_fn=None):
    def callback(drawing, piece, colour=BLACK):
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
    return callback


# -------------------------------------
# Colouring functions

# Colour by progress through list from FractalSystem
def colour_by_progress(colours):
    def callback(piece, progress):
        return get_colour(colours, progress)
    return callback

# Colour by a function of the piece's affine transformation (vector, matrix)
# tsfm(vect, matrix) should output a number
def colour_by_tsfm(min_val, max_val, colours, tsfm):
    def callback(piece, progress):
        if not callable(tsfm):
            return BLACK
        this_val = tsfm(piece.get_vect(), piece.get_mx())
        tsfm_progress = (this_val - min_val) / (max_val - min_val)
        return get_colour(colours, tsfm_progress)
    return callback

# Colour by a function of the piece's affine transformation (vector, matrix)
# metric(matrix) should output a number
def colour_by_log2_size(min_val, max_val, colours, metric=metric_matrix_min_eig_val):
    fn = lambda vect, mx: math.log(metric(mx), 2)
    return colour_by_tsfm(min_val, max_val, colours, fn)


# -------------------------------------
# Sorting functions for lists of fractal pieces
# Usage:
# fractal_system.piece_sorter = sort_function(arguments_if_needed)

# Sort pieces randomly
def sort_randomly():
    def callback(piece):
        return random.random()
    return callback
    
# Sort by function of the piece's affine transformation (vector, matrix)
def sort_by_tsfm(tsfm_to_num_fn):
    def callback(piece):
        return tsfm_to_num_fn(piece.get_vect(), piece.get_mx())
    return callback
    
# Sort by z-coordinate (reversed), e.g. for 3D fractals
def sort_by_z():
    return sort_by_tsfm(lambda vect, mx: -vect[2])
    
# Sort by size
def sort_by_size():
    return sort_by_tsfm(lambda vect, mx: -metric_matrix_min_eig_val(mx))
    
