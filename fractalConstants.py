import numpy as np

DEFAULT_MAX_DEFNS = 10000  # normally would use a lot fewer than this
DEFAULT_MIN_DIAMETER = 30
DEFAULT_MAX_PIECES = 10000
DEFAULT_MAX_ITERATIONS = 6
BREAK_AFTER_ITERATIONS = 1000  # stop the loop if this number of iterations is reached

DEFAULT_HULL_MAX_ITERATIONS = 20
DEFAULT_HULL_MIN_LEN = 0.037
DEFAULT_INITIAL_HULL = np.array(((1, 1), (-1, 0.5), (0.5, -1)))
