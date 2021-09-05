from constants import BLACK
from fractalHelperFns import DEFAULT_PLOTTING_FN, DEFAULT_COLOURING_FN


class FractalPlotter:
    def __init__(self):
        self.draws = True
        self.colouring_fn = DEFAULT_COLOURING_FN
        self.plotting_fn = DEFAULT_PLOTTING_FN

    def plot(self, drawing, piece):
        if not self.draws:
            return
        colour = self.colouring_fn(piece) if callable(self.colouring_fn) else BLACK
        if callable(self.plotting_fn):
            self.plotting_fn(drawing, piece, colour)

    def __repr__(self):
        return f"FP: draws {self.draws}"
