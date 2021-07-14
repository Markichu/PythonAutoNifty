import random

from FractalPiece import FractalPiece
from numpyHelperFns import vect, mx_scale, mx_rotd, mx_refl_X, mx_sq, mx_dh
    

# -------------------------------------
# Methods to calculate callback for children on fractal definitions

# For a square [-1, 1] x [-1, 1]
# split it into n^2 tiles (nxn)
# and then keep m out of n^2 at random
def defngen_rand_small_squares(system, id, m, n):
    sc = 1 / n
    def callback():
        children = []
        n0 = n - 1
        for x0 in range(n):
            for y0 in range(n):
                x1 = 2 * x0 - n0
                y1 = 2 * y0 - n0
                piece = FractalPiece(system=system, id=id, vect=vect(x1, y1, scale=sc), mx=mx_scale(sc))
                children.append(piece)
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
        mx = mx_rotd(
            angle=random.uniform(0, 360),
            scale=scale
        )
        if reflect and (random.random() < 0.5):
            mx = mx @ mx_refl_X()
        return mx
    return callback

# Any rotation or reflection in a square with a flat edge down
def mxgen_rand_sq(scale=1, reflect=True):
    max_num = 4
    if reflect:
        max_num = 8
    def callback():
        return mx_sq(
            num=random.randint(1, max_num),
            scale=scale
        )
    return callback

# Any rotation or reflection in a triangle with a flat edge down
def mxgen_rand_tri(scale=1, reflect=True):
    max_num = 3
    if reflect:
        max_num = 6
    def callback():
        return mx_dh(
            sides=3,
            num=random.randint(1, max_num),
            scale=scale
        )
    return callback

# Any rotation or reflection in a <sides>-sided polygon with a flat edge down
def mxgen_rand_dihedral(sides, scale=1, reflect=True):
    max_num = sides
    if reflect:
        max_num = sides * 2
    def callback():
        return mx_dh(
            sides=sides,
            num=random.randint(1, max_num),
            scale=scale
        )
    return callback
