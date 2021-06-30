import numpy as np


# ---------------------------------------
# General helper methods such as easily generate a vector or identity matrix

# Get dimension of vector or matrix
def np_dim(np_obj):
    return np_obj.shape[0]

# Find a metric for vector or matrix
# where identity matrix in 2D or 3D has metric 1
def array_rms_metric(mx):
    return np.sum(mx * mx * (1/np_dim(mx)) ) ** 0.5

# Easy syntax for generating 2D or 3D vectors
def vect(x=0, y=0, z=None):
    if z is None:
        return np.array((x, y))
    return np.array((x, y, z))

# Easy syntax for generating matrix identity
# Defaults to 2D matrix
def mx_id(n=2):
    return np.identity(n)


# ---------------------------------------
# Generate rotation matrices in 2D or 3D

# 2D clockwise rotation matrix in XY plane, angle in degrees, +1° rotates Y towards X
def mx_rotd(angle_in_degrees):
    angle_in_radians = np.radians(angle_in_degrees)
    c, s = np.cos(angle_in_radians), np.sin(angle_in_radians)
    return np.array(((c, s), (-s, c)))

# 3D clockwise rotation matrix in XY plane, angle in degrees, +1° rotates Y towards X
def mx_rotd_XY(angle_in_degrees):
    angle_in_radians = np.radians(angle_in_degrees)
    c, s = np.cos(angle_in_radians), np.sin(angle_in_radians)
    return np.array(((c, s, 0), (-s, c, 0), (0, 0, 1)))

# 3D clockwise rotation matrix in XZ plane, angle in degrees, +1° rotates Z towards X
def mx_rotd_XZ(angle_in_degrees):
    angle_in_radians = np.radians(angle_in_degrees)
    c, s = np.cos(angle_in_radians), np.sin(angle_in_radians)
    return np.array(((c, 0, s), (0, 1, 0), (-s, 0, c)))

# 3D clockwise rotation matrix in YZ plane, angle in degrees, +1° rotates Z towards Y
def mx_rotd_YZ(angle_in_degrees):
    angle_in_radians = np.radians(angle_in_degrees)
    c, s = np.cos(angle_in_radians), np.sin(angle_in_radians)
    return np.array(((1, 0, 0), (0, c, s), (0, -s, c)))

# Utility method to do an XY rotation, then a XZ rotation, then an optional scale
# Applying a matrix transformation is _pre_multiplication, so XZ goes first.
# Scaling is commutative, so can go anywhere.
# Angles are in degrees
def mx_rotd_3D(ang_xy, ang_xz, scale=1):
    return mx_rotd_XZ(ang_xz) @ (mx_rotd_XY(ang_xy) * scale)


# ---------------------------------------
# Generate reflection matrices in 2D or 3D

# Reflection matrix in x-axis
def mx_refl_X(n=2):
    if n == 3:
        return np.array(((-1, 0, 0), (0, 1, 0), (0, 0, 1)))
    return np.array(((-1, 0), (0, 1)))

# Reflection matrix in y-axis
def mx_refl_Y(n=2):
    if n == 3:
        return np.array(((1, 0, 0), (0, -1, 0), (0, 0, 1)))
    return np.array(((1, 0), (0, -1)))

# Reflection matrix in z-axis
def mx_refl_Z():
    return np.array(((1, 0, 0), (0, 1, 0), (0, 0, -1)))


# ---------------------------------------
# Discrete symmetry groups

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
