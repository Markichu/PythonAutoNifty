import math
import random
import numpy as np

from .pos import Pos
from .constants import DRAWING_SIZE, BLACK, BLUE
from .fractal_constants import DEFAULT_MIN_DIAMETER, DEFAULT_MAX_ITERATIONS, BASE_SCALE_WIDTH
from .helper_fns import interpolate_colour
from .numpy_helper_fns import vect, vect_len, mx_rotd, metric_matrix_min_eig_val, metric_matrix_rms, metric_matrix_x_coord


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
# Internal helpers for plotting functions

# Helper function to shrink a single point (q) by a specified brush radius (width)
# How it shrinks depends on the points before and after (p, r)
def shrink_2D_vect(p, q, r, width, mx):
    # Numpy vector arithmetic used here
    # mx ought to be a 90 degree rotation either to left or to right
    # L1 is line from p to q
    # L2 is line from q to r
    # Goal is to shift both L1 and L2 sideways by `width`, then calculate their intersection
    # which is the shrunk coordinate

    # Peturb p, q, r infinitesimally here to avoid potential divisions by zero later on
    delta_v = 0.000001
    def peturb_vector(sc):
        return np.array((sc * (-0.5 + random.random()), sc * (-0.5 + random.random())))
    p = p + peturb_vector(delta_v)
    q = q + peturb_vector(delta_v)
    r = r + peturb_vector(delta_v)

    # Calculate shift vectors to move each line L1, L2 by width, in direction of mx
    sv1_0 = mx @ (q - p)
    sv2_0 = mx @ (r - q)
    sv1 = sv1_0 * (width / vect_len(sv1_0))
    sv2 = sv2_0 * (width / vect_len(sv2_0))

    # Calculate vectors shifted by width here
    ps1 = p + sv1
    qs1 = q + sv1
    qs2 = q + sv2
    rs2 = r + sv2

    # Convert to individual components
    # Now LA is L1 shifted by width, LA is between (x1, y1) and (x2, y2)
    # and LB is L2 shifted by width, LB is between (x3, y3) and (x4, y4)
    x_1 = ps1[0]
    y_1 = ps1[1]
    x_2 = qs1[0]
    y_2 = qs1[1]
    x_3 = qs2[0]
    y_3 = qs2[1]
    x_4 = rs2[0]
    y_4 = rs2[1]

    # Due to x<->y symmetry in line definition, define a function that can obtain either
    def get_coord(x1, x2, x3, x4, y1, y2, y3, y4):
        A = y4 - y3
        B = y2 - y1
        C = y1 - y3
        D = x4 - x3
        E = x2 - x1
        F = (1/(B*D) - 1/(A*E))
        x0 = C/(A*B) + x3/(B*D) - x1/(A*E)
        x = x0 / F
        return x
    
    # Use function to obtain both x and y coords, and return result
    x = get_coord(x_1, x_2, x_3, x_4, y_1, y_2, y_3, y_4)
    y = get_coord(y_1, y_2, y_3, y_4, x_1, x_2, x_3, x_4)
    return np.array((x, y))


# Helper function to shrink 2D path (vect_list) by a specified brush radius (width)
def shrink_2D_vects(piece, vect_list, width):
    result_list = []
    count_vect = len(vect_list)
    # 1. Check we have at least 3 vectors in list to shrink
    if count_vect < 3:
        return vect_list
    # 2. If piece is too small, reduce the shrink amount (width)
    width_from_piece = 0.5 * piece.get_minimum_diameter()
    if width_from_piece < width:
        width = width_from_piece
    # 3. Get the average vector in the list
    av_vect = vect_list[0]
    for i in range(1, count_vect):
        av_vect = av_vect + vect_list[i]
    av_vect = av_vect * (1/count_vect)
    # 4. Check normal (constructed using mx) to line between first two vectors
    # is pointing in same direction as the vector from middle of line to middle of shape
    mx = mx_rotd(angle=90, scale=1)
    p = vect_list[0]
    q = vect_list[1]
    v1 = mx @ (q-p)
    v2 = av_vect * 2 - p - q
    dot_product = sum(v1 * v2)
    if dot_product < 0:
        mx = mx_rotd(angle=-90, scale=1)  # Reverse the orientation
    # 5. Shrink the vector list by specified width, in correct orientation mx
    for i in range(count_vect):
        p = vect_list[(i-1) % count_vect]
        q = vect_list[i]
        r = vect_list[(i+1) % count_vect]
        shrunk_q = shrink_2D_vect(p, q, r, width, mx)
        result_list.append(shrunk_q)
    return result_list


# Helper function to calculate a 2D planar spiral filling path from an outline or convex hull
def spiral_2D_path_fill(vect_list, width):
    n = len(vect_list)  # hull length
    avg_vect = vect_list[0] * 0  # Going to spiral in towards this point
    for i in range(n):
        avg_vect += vect_list[i]
    avg_vect /= n  # turn sum to (mean) average
    max_distance_from_avg = 0
    for i in range(n):
        max_distance_from_avg = max(max_distance_from_avg, vect_len(vect_list[i] - avg_vect))
    # Calculate m, number of spirals in to the centre
    # width is brush radius, so x2
    # Add 2 to ensure overlapping, round to integer number of spirals
    m = round(2 + max_distance_from_avg / (2 * width))
    # Construct list of vectors to plot
    mid_boundary_point = (vect_list[-2] + vect_list[-1]) * 0.5
    spiral_list = [mid_boundary_point, vect_list[-1]] + vect_list  # standard array concatenation
    for i in range(m):
        for j in range(n):
            spiral_list.append(((m - (i + 1)) * vect_list[j] + (i + 1) * avg_vect) * (1 / m))
    spiral_list.append(avg_vect)
    final_draw_list = spiral_list[::-1]  # Reverse order to spiral outwards
    return final_draw_list

# Helper function to do the drawing based on a wide range of criteria
def basic_plot_path(drawing, piece, vector_list, width, scale_width, shrink, colour, fill, closed, curved, expand_factor, wobble_fn):
    piece_vect = piece.get_vect()
    piece_mx = piece.get_mx()

    # 1. Calculate draw_list, which is the path to draw
    draw_list = []
    # 1.1. Transform vector list to draw list
    for i in range(len(vector_list)):
        wobble_vect = wobble_fn() if callable(wobble_fn) else piece_vect * 0
        draw_vect = piece_vect + wobble_vect + (piece_mx @ vector_list[i]) * expand_factor
        draw_list.append(draw_vect)
    # 1.2. If scale_width option used, scale the width up or down based on piece diameter relative to the base scale width
    if scale_width:
        width *= piece.get_minimum_diameter() / BASE_SCALE_WIDTH
    # 1.3. Shrink a bit (due to finite brush radius) if shrink option is selected
    if shrink:
        draw_list = shrink_2D_vects(piece, draw_list, width)
    # 1.4. Deal with both filled and closed shapes
    if fill and len(draw_list) > 2:
        draw_list = spiral_2D_path_fill(vect_list=draw_list, width=width)
        # if filling, shape is automatically closed
    elif closed:
        draw_list.append(draw_list[0])
    
    # 2. Convert to pos_list, a list of Pos objects
    pos_list = []
    for vect in draw_list:
        pos_list.append(get_canvas_pos_from_vect(vect))
    
    # 3. Choose either a straight line or a curved path function to do the drawing
    if curved:
        drawing.add_quadratic_bezier_curve(pos_list, colour, width)
    else:
        drawing.add_line(pos_list, colour, width)


# -------------------------------------
# Plotting functions

# Plot a dot (small circle) for each fractal piece
# Optional parameters:
# expand_factor is to fine-tune control of dot size
# offset_vect is to offset the dot by a specified amount
# wobble_fn returns a random pixel displacement to simulate drawing by hand
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


# Plot a path (optionally filled, or closed) for each fractal piece separately
# 1. If vector_list is specified, use that for the path
# 2. Else if convex hull is calculated, use that
# 3. Otherwise fall back to a unit square, making sure it is closed
def plot_path(vector_list=None, fill=False, closed=False, curved=False, width=1, scale_width=False, shrink=False, expand_factor=1, wobble_fn=None):
    def plot_fn(drawing, piece, colour=BLACK):
        use_closed = closed
        vect_list = vector_list
        if vect_list is None:
            vect_list = piece.get_defn().hull
        if vect_list is None:
            vect_list = [vect(0, 1), vect(-1, 1), vect(-1, -1), vect(1, -1), vect(1, 1)]
            use_closed = True
        basic_plot_path(drawing=drawing, piece=piece, vector_list=vect_list, wobble_fn=wobble_fn, closed=use_closed, colour=colour, width=width, scale_width=scale_width, shrink=shrink, curved=curved, expand_factor=expand_factor, fill=fill)

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
