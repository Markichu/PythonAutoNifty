from constants import BLACK, BLUE
from fractalHelperFns import colour_by_progress, plot_dot


class FractalPlotter:
    def __init__(self):
        self.draw = True
        self.colouring_fn = colour_by_progress([BLACK, BLUE])
        self.plotting_fn = plot_dot()

    def plot(self, piece, drawing, progress_counter, total_pieces):
        if not self.draw:
            return
        progress = progress_counter / total_pieces
        this_colour = self.colouring_fn(piece, progress) if callable(self.colouring_fn) else BLACK
        if callable(self.plotting_fn):
            self.plotting_fn(drawing, piece, this_colour)

    def __repr__(self):
        return f"FP: draw {self.draw}, dot rel. size {self.dot_expand_factor}, path width {self.path_width}, path vectors {self.path_vectors}"
