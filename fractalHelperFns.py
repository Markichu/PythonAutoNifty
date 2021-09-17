import math
import random

from Pos import Pos
from constants import DRAWING_SIZE, BLACK, BLUE
from fractalConstants import DEFAULT_MIN_DIAMETER, DEFAULT_MAX_ITERATIONS
from helperFns import interpolate_colour
from numpyHelperFns import vect, vect_len, metric_matrix_min_eig_val, metric_matrix_rms, metric_matrix_x_coord


# -------------------------------------
# General methods

# Turn Numpy vector into Pos
# Pos has origin in top left, vectors in bottom left, so invert in y-axis
def get_canvas_pos_from_vect(vect):
    return Pos(vect[0], DRAWING_SIZE - vect[1])

# Get an interpolated colour using:
# - a list of colours,
# - a progress factor between 0 and 1 representing how far we are through the list
# - an alpha factor saying how much to fade the opacity, between 0 and 1
# - whether to snap to the nearest colour in the list, or interpolate (default)
def get_colour(colours, progress, alpha=1, snap=False):
    max_prog = len(colours) - 1
    prog2 = max(0, min(max_prog, progress * max_prog))
    prog_rem = prog2 - math.floor(prog2)
    colour_start = colours[math.floor(prog2)]
    colour_end = colours[math.ceil(prog2)]
    if snap:
        # Override start and end colours to snap to nearest colour
        colour_start = colours[round(prog2)]
        colour_end = colours[round(prog2)]
    colour_this = interpolate_colour(colour_start, colour_end, prog_rem, alpha)
    return colour_this


# -------------------------------------
# Iteration functions. On a piece, return True to iterate, False to not iterate

# Standard function. Iterate if piece is not too small or too iterated
def get_iteration_fn_standard(min_diameter, max_iterations):
    def iteration_fn(piece):
        return min_diameter < piece.get_minimum_diameter() and piece.iteration < max_iterations
    return iteration_fn

# Turn iteration off
# Use as an override on a definition that should stop iterating
def get_iteration_fn_stop():
    def iteration_fn(piece):
        return False
    return iteration_fn

DEFAULT_ITERATION_FN = get_iteration_fn_standard(DEFAULT_MIN_DIAMETER, DEFAULT_MAX_ITERATIONS)


# -------------------------------------
# Metrics for Fractal Pieces
# Default metric is set on the FractalSystem
# Can override for any particular FractalDefn
# Currently using only the piece's matrix, but could depend on many things,
# such as minimum diameter of convex hull after shear/stretching

# Use the minimum eigenvalue of the matrix
def get_metric_fn_piece_min_eig():
    def metric_fn(piece):
        return metric_matrix_min_eig_val(piece.get_mx())
    return metric_fn

# Use the RMS of the matrix entries
def get_metric_fn_piece_rms():
    def metric_fn(piece):
        return metric_matrix_rms(piece.get_mx())
    return metric_fn

# Use the length of x-coord (1, 0) under mx transformation, e.g. for line fractals
def get_metric_fn_piece_x_coord():
    def metric_fn(piece):
        return metric_matrix_x_coord(piece.get_mx())
    return metric_fn

DEFAULT_METRIC_FN = get_metric_fn_piece_min_eig()


# -------------------------------------
# Random vector functions for drawing-by-hand "hand wobble" effect

# Return 2D square or 3D cube uniform distribution
def wobble_square(pixels=2, dim=2):
    def get_rand_unif():
        return random.uniform(-0.5 * pixels, 0.5 * pixels)
    def wobble_fn():
        x, y, z = get_rand_unif(), get_rand_unif(), get_rand_unif()
        return vect(x, y, z) if dim == 3 else vect(x, y)
    return wobble_fn

# TODO: 2D circle uniform, 3D sphere uniform, 2D concentrated at centre, etc

# Return vector in a rectangular grid. Example (considering x-coord only):
# x_steps = 4
# x_min = -1
# x_max = 1
# Then supply x_pos = 0, 1, 2, 3
# Output is x_this = -0.75, -0.25, 0.25, 0.75
def grid_generator(x_steps, y_steps, x_min=-1, y_min=-1, x_max=1, y_max=1):
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
    def plot_fn(drawing, piece, colour=BLACK):
        piece_vect = piece.get_vect()
        wobble_vect = wobble_fn() if callable(wobble_fn) else piece_vect * 0
        if not offset_vect is None:
            mx = piece.get_mx()
            piece_vect = piece_vect + mx @ offset_vect
        pos = get_canvas_pos_from_vect(piece_vect + wobble_vect)
        dot_radius = 0.5 * expand_factor * piece.get_minimum_diameter()
        drawing.add_point(pos, colour, dot_radius)
    return plot_fn

# Plot a path (series of line segments) for each fractal piece
def plot_path(vector_list, closed=False, width=1, expand_factor=1, wobble_fn=None, curved=False):
    def plot_fn(drawing, piece, colour=BLACK):
        piece_vect = piece.get_vect()
        piece_mx = piece.get_mx()
        pos_list = []
        for i in range(0, len(vector_list)):
            wobble_vect = wobble_fn() if callable(wobble_fn) else piece_vect * 0
            draw_vect = piece_vect + wobble_vect + (piece_mx @ vector_list[i]) * expand_factor
            pos_list.append(get_canvas_pos_from_vect(draw_vect))
        if closed:
            pos_list.append(pos_list[0])
        if curved:
            drawing.add_quadratic_bezier_curve(pos_list, colour, width)
        else:
            drawing.add_line(pos_list, colour, width)
    return plot_fn

# Plot a path (series of line segments) for each fractal piece
def plot_hull_outline(width=1, expand_factor=1, wobble_fn=None, curved=False):
    def plot_fn(drawing, piece, colour=BLACK):
        hull = piece.get_defn().hull
        if hull is not None:
            piece_vect = piece.get_vect()
            piece_mx = piece.get_mx()
            pos_list = []
            for i in range(0, len(hull)):
                wobble_vect = wobble_fn() if callable(wobble_fn) else piece_vect * 0
                draw_vect = piece_vect + wobble_vect + (piece_mx @ hull[i]) * expand_factor
                pos_list.append(get_canvas_pos_from_vect(draw_vect))
            pos_list.append(pos_list[0])  # Close the hull outline
            if curved:
                drawing.add_quadratic_bezier_curve(pos_list, colour, width)
            else:
                drawing.add_line(pos_list, colour, width)
    return plot_fn

# Fill a fractal piece using a spiralling path from the centre to the convex hull
def plot_hull_filled(width=2, expand_factor=1, wobble_fn=None, curved=False):
    def plot_fn(drawing, piece, colour=BLACK):
        hull = piece.get_defn().hull
        if hull is not None:
            n = len(hull)  # hull length
            piece_vect = piece.get_vect()
            piece_mx = piece.get_mx()
            piece_hull_list = []  # hull points
            plot_vect_list = []  # inspiralling points to plot
            pos_list = []  # convert to Pos format
            avg_vect = piece_vect * 0  # Going to spiral in towards this point
            for i in range(n):
                wobble_vect = wobble_fn() if callable(wobble_fn) else piece_vect * 0
                draw_vect = piece_vect + wobble_vect + (piece_mx @ hull[i]) * expand_factor
                piece_hull_list.append(draw_vect)
                avg_vect += draw_vect
            avg_vect /= n  # turn sum to (mean) average
            max_distance_from_avg = 0
            for i in range(n):
                max_distance_from_avg = max(max_distance_from_avg, vect_len(piece_hull_list[i] - avg_vect))
            # Calculate m, number of spirals in to the centre
            # width is brush radius, so x2
            # Add 2 to ensure overlapping, round to integer number of spirals
            m = round(2 + max_distance_from_avg / (2 * width))
            # Construct list of vectors to plot
            mid_boundary_point = (piece_hull_list[-2] + piece_hull_list[-1] ) * 0.5
            plot_vect_list = [mid_boundary_point, piece_hull_list[-1]] + piece_hull_list  # standard array concatenation
            for i in range(m):
                for j in range(n):
                    plot_vect_list.append(( (m - (i+1)) * piece_hull_list[j] + (i + 1) * avg_vect) * (1 / m))
            plot_vect_list.append(avg_vect)
            # Get canvas points in Pos format, also reverse order so it spirals out from the centre
            l = len(plot_vect_list)
            for j in range(l):
                pos_list.append(get_canvas_pos_from_vect(plot_vect_list[l-j-1]))
            if curved:
                drawing.add_quadratic_bezier_curve(pos_list, colour, width)
            else:
                drawing.add_line(pos_list, colour, width)
    return plot_fn

DEFAULT_PLOTTING_FN = plot_dot()

# -------------------------------------
# Colouring functions

# Simple colouring function, with 1 fixed colour throughout
# Option exists to vary the alpha, so still going via get_colour instead of
# just returning the fixed colour
def colour_fixed(colour, alpha=1):
    def colour_fn(piece):
        return get_colour([colour], progress=0, alpha=alpha)
    return colour_fn

# Colour by progress, which is a property on each fractal piece
def colour_by_progress(colours, alpha=1, snap=False):
    def colour_fn(piece):
        return get_colour(colours, piece.get_progress_value(), alpha, snap)
    return colour_fn

# Colour by a function of the piece's affine transformation (vector, matrix)
# tsfm(vect, matrix) should output a number
def colour_by_tsfm(min_val, max_val, colours, tsfm, alpha=1, snap=False):
    def colour_fn(piece):
        if not callable(tsfm):
            return BLACK
        this_val = tsfm(piece.get_vect(), piece.get_mx())
        tsfm_progress = (this_val - min_val) / (max_val - min_val)
        return get_colour(colours, tsfm_progress, alpha, snap)
    return colour_fn

# Colour by a function of the piece's affine transformation (vector, matrix)
# metric(matrix) should output a number
def colour_by_log2_size(min_val, max_val, colours, metric=metric_matrix_min_eig_val, alpha=1, snap=False):
    fn = lambda vect, mx: math.log(metric(mx), 2)
    return colour_by_tsfm(min_val, max_val, colours, fn, alpha, snap)

DEFAULT_COLOURING_FN = colour_by_progress([BLACK, BLUE])


# -------------------------------------
# Sorting functions for lists of fractal pieces
# Usage:
# fractal_system.piece_sorter = sort_function(arguments_if_needed)

# Sort pieces randomly
def sort_randomly():
    def sort_fn(piece):
        return random.random()
    return sort_fn
    
# Sort by function of the piece's affine transformation (vector, matrix)
# Random factor is optional
def sort_by_tsfm(tsfm, rand=False):
    def sort_fn(piece):
        random_factor, main_factor = 0, tsfm(piece.get_vect(), piece.get_mx())
        if rand:
            random_factor = random.random()
        return main_factor + random_factor
    return sort_fn
    
# Sort by z-coordinate (reversed), e.g. for 3D fractals
def sort_by_z():
    return sort_by_tsfm(lambda vect, mx: -vect[2])
    
# Sort by size
def sort_by_size():
    return sort_by_tsfm(lambda vect, mx: -metric_matrix_min_eig_val(mx))
    
