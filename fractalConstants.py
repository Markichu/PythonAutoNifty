import numpy as np

DEFAULT_MAX_DEFNS = 10000  # normally would use a lot fewer than this
DEFAULT_MIN_DIAMETER = 30
DEFAULT_MAX_PIECES = 10000
DEFAULT_MAX_ITERATIONS = 6
BREAK_AFTER_ITERATIONS = 1000  # stop the loop if this number of iterations is reached

DEFAULT_HULL_MAX_ITERATIONS = 20
DEFAULT_HULL_ACCURACY = 0.031415  # Acceptable accuracy for fractal roughly filling interval [-1, 1] in each direction

# This hull ought to have diameter 2 in the diameter-calculating algorithm being used
# Current algorithm is to find max-min x and y at 0, 30, 60 degrees (min of 6 values)
# This hull produces 2 under that algorithm.
DEFAULT_INITIAL_HULL = np.array(((1, 1), (-1, 0.5), (0.5, -1)))
