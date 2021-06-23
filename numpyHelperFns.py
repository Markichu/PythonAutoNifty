import numpy as np


# Find a metric for vector or matrix
# = square root of sum of all entries in the vector or matrix
def array_rms_metric(mx):
    return np.sum(mx * mx) ** 0.5

# Easy syntax for generating 2D or 3D vectors
def vect(x, y, z=None):
    if z == None:
        return np.array((x, y))
    else:
        return np.array((x, y, z))

# Easy syntax for generating matrix identity
# Defaults to 2D matrix
def mx_id(n=2):
    return np.identity(n)

# 2D clockwise rotation matrix, angle in radians
def mx_rotr(angle_in_radians):
    angle_anticlock = -angle_in_radians
    c, s = np.cos(angle_anticlock), np.sin(angle_anticlock)
    return np.array(((c, -s), (s, c)))

# 2D clockwise rotation matrix, angle in degrees
def mx_rotd(angle_in_degrees):
    return mx_rotr(np.radians(angle_in_degrees))

# 2D reflection matrix in x-axis
def mx_refl_x():
    return np.array(((-1, 0), (0, 1)))

# 2D reflection matrix in y-axis
def mx_refl_y():
    return np.array(((1, 0), (0, -1)))

# Dihedral group of regular polygon 2, 3, 4, 5, 6...
# (rectangle, triangle, square, pentagon, hexagon...)
# where bottom edge is horizontal (so horizontal reflection)
# dh(5, 1) for identity
# dh(5, 2) for 72 degree rotation anticlockwise
# dh(5, 6) for horizontal reflection
# dh(8, 6) for 225 (45 * 5) degree rotation anticlockwise
def mx_dh(sides, num):
    if not isinstance(sides, int):
        raise TypeError("Number of sides must be an integer")
    if sides < 2:
        raise TypeError("Number of sides must be at least 2")
    if not isinstance(num, int):
        raise TypeError("Transformation number must be an integer")
    if num < 1:
        raise TypeError("Transformation number must be at least 1")
    if num > sides * 2:
        raise TypeError(
            f"Transformation number must be at most {sides * 2}")
    rotation_num = (num - 1) % sides  # 0, 1, 2, ..., sides - 1
    reflection_num = ((num - 1) - rotation_num) / sides  # 0, 1
    rotation_mx = mx_rotd((-360/sides) * rotation_num)
    refl_x_mx = np.array( (((-1) ** reflection_num, 0), (0, 1)) )
    result = rotation_mx @ refl_x_mx
    return result

# Square transformations 1 to 8
# sq(1) for identity
# sq(2) for 90 degree rotation anticlockwise
# sq(5) for *vertical* reflection (should have been horizontal... but already published on Nifty Ink)
def mx_sq(num):
    if not isinstance(num, int):
        raise TypeError("Argument is not integer")
    if num < 1:
        raise TypeError("Argument must be at least 1")
    if num > 8:
        raise TypeError("Argument must be at most 8")
    rotation_num = (num - 1) % 4  # 0, 1, 2, 3
    reflection_num = ((num - 1) - rotation_num) / 4  # 0, 1
    rotation_mx = mx_rotd((-90) * rotation_num)
    refl_y_mx = np.array(((1, 0), (0, (-1) ** reflection_num)))
    result = rotation_mx @ refl_y_mx
    return result
