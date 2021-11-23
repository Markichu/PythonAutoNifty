from .constants import BLACK
from .fractal_helper_fns import DEFAULT_PLOTTING_FN, DEFAULT_COLOURING_FN

# A FractalPlotter object controls how a FractalPiece is plotted onto the canvas
# It contains a list of instructions for the plot method and the colour to plot

class FractalPlotter:
    def __init__(self):
        # Set this to false to prevent any drawing from taking place
        self.draws = True

        # Store a list of things to do when plotting
        # Format is:
        # [[plot_fn_1, colour_fn_1], [plot_fn_2, colour_fn_2], ...]
        # Use the `add` function to add a new pair to this list
        self.plot_list = []
    
    # Add an instruction to use a plot method with a particular colour
    # Each of these are functions that get evaluated in the context of a specific fractal piece
    # Plotting function is mandatory, examples include plotting a dot, or plotting a path (filled/outline, closed/open)
    # Colouring function is optional, if not specified then BLACK will be used.
    def add(self, plotting_fn, colouring_fn=None):
        self.plot_list.append([plotting_fn, colouring_fn])
    
    # Plot a specific fractal piece onto the drawing (canvas),
    # using the plot methods stored in this FractalPlotter
    def plot(self, drawing, piece):
        if not self.draws:
            return
        if len(self.plot_list) == 0:
            # If user has not specified any plotting behaviour, lazy-initialise it here
            self.add(DEFAULT_PLOTTING_FN, DEFAULT_COLOURING_FN)
        # Iterate through the list of plotting instructions
        # and execute each one for the fractal piece
        for plot_and_colour_fns in self.plot_list:
            plot_fn = plot_and_colour_fns[0]
            colour_fn = plot_and_colour_fns[1]
            colour = colour_fn(piece) if callable(colour_fn) else BLACK
            if callable(plot_fn):
                plot_fn(drawing, piece, colour)

    def __repr__(self):
        return f"FP: draws {self.draws}"
