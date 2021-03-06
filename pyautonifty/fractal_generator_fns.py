import random

from .fractal_piece import FractalPiece
from .fractal_helper_fns import grid_generator
from .numpy_helper_fns import vect, vect_len, mx_scale, mx_rotd, mx_refl_X, mx_sq, mx_dh


# -------------------------------------
# Some fractal parameters are either values or functions
# Use this file to store some common functions that return suitable values
# Usually the function takes a fractal piece in as an optional parameter
# to fine-tune the behaviour.

# For a square [-1, 1] x [-1, 1]
# split it into n^2 tiles (nxn)
# and then keep m out of n^2 at random
def gen_children_rand_small_squares(system, fid, m, n):
    grid = grid_generator(x_steps=n, y_steps=n)

    def calc_children(context_piece=None):
        # This function is probabilistic, so context piece is not used. Still need the parameter available!
        children = []
        for x in range(n):
            for y in range(n):
                piece = FractalPiece(system=system, fid=fid, vect=grid(x, y), mx=mx_scale(1 / n))
                children.append(piece)
        return random.sample(children, m)

    return calc_children


# For a square [-1, 1] x [-1, 1]
# split it into n^2 tiles (nxn)
# and keep each tile with probability between p1 and p2
# depending on its distance from vect
# For large pieces, iterate them with probability 1,
# only apply the probabilistic iteration to scales (metrics) below the cutoff.
def gen_children_fade_out(system, fid, n, centre_vect, cutoff_diameter, d1=0, d2=2000, p1=1, p2=0):
    grid = grid_generator(x_steps=n, y_steps=n)

    def calc_children(context_piece=None):
        p = 1  # Default is to include all children, unless context is supplied and size (metric) is below cutoff
        if context_piece is not None:
            if context_piece.get_minimum_diameter() < cutoff_diameter:
                outer_vect = context_piece.get_vect()
                d = vect_len(outer_vect - centre_vect)
                d_progress_1_to_2 = max(0, min(1, (d - d1) / (d2 - d1)))
                p = p1 + d_progress_1_to_2 * (p2 - p1)
        children = []
        for x in range(n):
            for y in range(n):
                if (random.random() < p):
                    piece = FractalPiece(system=system, fid=fid, vect=grid(x, y), mx=mx_scale(1 / n))
                    children.append(piece)
        return children

    return calc_children


# -------------------------------------
# Methods to calculate a random fractal id

# Select an fractal id (fid) at random from a list, equal weights
def gen_fid_rand(list_of_fids):
    def calc_id(context_piece=None):
        return random.choice(list_of_fids)

    return calc_id


# -------------------------------------
# 2D or 3D methods to calculate a random vector

# Calculate a random continuous 2D or 3D vector in (x1, x2) x (y1, y2) [x (z1, z2)]
# Example: gen_vect_rand([1, 2], [3, 4], [5, 6])
def gen_vect_rand(x_range, y_range, z_range=None):
    def calc_vect(context_piece=None):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        if z_range is None:
            return vect(x, y)
        z = random.uniform(z_range[0], z_range[1])
        return vect(x, y, z)

    return calc_vect


# -------------------------------------
# 2D methods to calculate a random matrix

# Any rotation or reflection in the circle
def gen_mx_rand_circ(scale=1, reflect=True):
    def calc_mx(context_piece=None):
        mx = mx_rotd(
            angle=random.uniform(0, 360),
            scale=scale
        )
        if reflect and (random.random() < 0.5):
            mx = mx @ mx_refl_X()
        return mx

    return calc_mx


# Any rotation or reflection in a square with a flat edge down
def gen_mx_rand_sq(scale=1, reflect=True):
    max_num = 4
    if reflect:
        max_num = 8

    def calc_mx(context_piece=None):
        return mx_sq(
            num=random.randint(1, max_num),
            scale=scale
        )

    return calc_mx


# Any rotation or reflection in a triangle with a flat edge down
def gen_mx_rand_tri(scale=1, reflect=True):
    max_num = 3
    if reflect:
        max_num = 6

    def calc_mx(context_piece=None):
        return mx_dh(
            sides=3,
            num=random.randint(1, max_num),
            scale=scale
        )

    return calc_mx


# Any rotation or reflection in a <sides>-sided polygon with a flat edge down
def gen_mx_rand_dihedral(sides, scale=1, reflect=True):
    max_num = sides
    if reflect:
        max_num = sides * 2

    def calc_mx(context_piece=None):
        return mx_dh(
            sides=sides,
            num=random.randint(1, max_num),
            scale=scale
        )

    return calc_mx
