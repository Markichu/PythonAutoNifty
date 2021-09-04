from constants import BLACK, BLUE
from fractalHelperFns import colour_by_progress, plot_dot


class FractalPlotter:
    def __init__(self):
        self.draws = True
        self.colouring_fn = colour_by_progress([BLACK, BLUE])
        self.plotting_fn = plot_dot()

    def plot(self, drawing, piece):
        if not self.draws:
            return
        colour = self.colouring_fn(piece) if callable(self.colouring_fn) else BLACK
        if callable(self.plotting_fn):
            self.plotting_fn(drawing, piece, colour)

    def __repr__(self):
        return f"FP: draws {self.draws}"
