import numpy as np
from scipy.spatial import ConvexHull

from numpyHelperFns import mx_rotd


# To make a convex hull in 2D:
# 1. Start with any 2D shape (e.g. a triangle around the origin) for a hull for each definition
# 2. At each calculation iteration, for each definition, take union of previous hulls under fractal maps
# 3. Scale coordinates up (e.g. multiple by 1/0.05) and round to integer, which will deduplicate points close to each other
# 4. Use a convex hull algorithm to remove all interior points (scipy package used here)
# 5. Replace previous hull points with new hull points, and iterate several times

# Note on 2. - currently "vect" is actually not a column vector, but is a row coordinate
# which mean that premultiplying by matrix -> postmultiplying by matrix transpose
# (all the matrix arithmetic is backwards!)
# This probably ought to be fixed later on...

# Also note that for random fractals the hull may not converge so nicely
# This could be alleviated by using multiple (random) copies of the hull points at each stage
# or in some cases by making random fractals (with no context piece supplied) evaluate in the largest possible way

def iterate_defn_hull(system, defn, iteration):
    children = defn.get_children()
    len_children = len(children)
    if len_children < 1:
        return
    next_points = None
    for child in children:
        # FractalDefn contains abstract FractalPieces. These can have fid, vect, mx all functions.
        # Evaluate without any context_piece. These functions should return the largest possible orientation
        # so that convex hull is too big, rather than too small.
        fid = child.get_fid()
        vect = child.get_vect()
        mx = child.get_mx()
        prev_hull = system.lookup_defn(fid).hull
        next_points_partial = prev_hull @ np.transpose(mx) + vect  # Backwards arithmetic here (*)
        if next_points is None:
            next_points = next_points_partial
        else:
            next_points = np.concatenate((next_points, next_points_partial))
    # Not actually going to find convex hull on these points, but on a rounded and scaled version of them
    # which can significantly reduce the number of points in the hull (good for drawing and calculation speed)
    scaled_integer_points = np.rint(next_points * (1 / defn.hull_accuracy))
    hull = ConvexHull(scaled_integer_points)  # object
    vertices = hull.vertices  # array of point indices
    # Now can do lookup on original points (next_points) rather than the approximate and scaled points (scaled_integer_points)
    defn.hull = next_points[vertices]
    # TODO: fix error if hull accuracy is too big then we don't get enough points to make a convex hull, and the method from scipy breaks
    # system.log(f"Hull iteration {iteration} of definition {defn.fid} has length {len(defn.hull)}")


degrees_30 = mx_rotd(angle=30, scale=1)
degrees_60 = mx_rotd(angle=60, scale=1)


def calculate_hull_diameter(system, defn):
    # Calculates minimum diameter over a total of 6 directions: 0, 30, 60, 90, 120, 150 degrees
    hull = defn.hull

    def get_square_min_diam(the_hull):
        x_min, y_min = 10 ** 10, 10 ** 10
        x_max, y_max = -10 ** 10, -10 ** 10
        for point in the_hull:
            x_min = min(x_min, point[0])
            x_max = max(x_max, point[1])
            y_min = min(y_min, point[0])
            y_max = max(y_max, point[1])
        square_diam = min(abs(x_max - x_min), abs(y_max - y_min))
        return square_diam

    def get_min_diam_30_degrees(the_hull):
        d0 = get_square_min_diam(the_hull)
        d30 = get_square_min_diam(the_hull @ degrees_30)
        d60 = get_square_min_diam(the_hull @ degrees_60)
        return min(d0, d30, d60)

    diam = get_min_diam_30_degrees(hull)
    defn.relative_diameter = diam
    system.log(f"- hull {defn.fid} has {len(hull)} points, {diam:.2f} min diameter")
