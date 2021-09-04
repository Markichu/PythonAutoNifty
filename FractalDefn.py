import random
from FractalPlotter import FractalPlotter
from FractalPiece import FractalPiece


class FractalDefn:
    def __init__(self, system=None, metric_fn=None):
        self.system = system  # the FractalSystem this FractalDefn is contained within
        self.metric_fn = metric_fn  # Use this to override the metric function set at system level
        self.plotter = FractalPlotter()  # used to control plotting of FractalPieces linked to this FractalDefn
        self.hull = None  # Convex Hull; set of coordinates describing shape of definition at vector (0, 0), matrix ((1, 0), (0, 1))
        self._next_hull = None  # Temporary variable for calculating next iteration of convex hull

        # These should be either a value, or a function returning suitable value
        # Function should accept an optional FractalPiece as context for evaluation.
        self.iterates = True  # Boolean (or function)
        self.children = []  # List of FractalPieces (or function)

        # How big is this definition?
        self.relative_size = 1
        # for self.relative_size = n,
        # either definition occupies circle of radius n,
        # or definition occupies square of size [-n, n] x [-n, n]
    
    def get_system(self):
        return self.system

    def set_system(self, system):
        # system should be a FractalSystem
        self.system = system
        return self

    def get_metric_fn(self):
        return self.get_system().get_metric_fn() if self.metric_fn is None else self.metric_fn

    def set_metric_fn(self, metric_fn=None):
        # metric_fn should be a function that maps from FractalPieces to numeric
        # Supply no argument to clear this metric function, and use the default in the system
        self.metric_fn = metric_fn
        return self

    def get_plotter(self):
        return self.plotter

    def set_plotter(self, plotter):
        # plotter should be a FractalPlotter
        self.plotter = plotter
        return self

    def get_hull(self):
        return self.hull

    def get_iterates(self, context_piece=None):
        # If self.iterates is not a function, it should be a Boolean value, so return that value directly
        if not callable(self.iterates):
            return self.iterates
        # Otherwise, self.iterates is a function that accepts an optional context piece and returns a Boolean
        # Currently the context piece should always be supplied.
        return self.iterates(context_piece)

    def set_iterates(self, iterates):
        # iterates should be a Boolean, or a function that accepts an optional context piece and evaluates to a Boolean
        self.iterates = iterates
        return self

    def get_children(self, context_piece=None):
        # If self.children is not a function, it should be a list of FractalPieces, so return this list directly
        if not callable(self.children):
            return self.children
        # Otherwise, self.children is a function that should return a list of FractalPieces,
        # and accept an optional context_piece as context for evaluation
        # (The function should be able to cope with and without the context_piece,
        # since for fractal iteration the piece is supplied, but for convex hull it is not.)
        return self.children(context_piece)

    def create_child(self, id, vect, mx):
        piece = FractalPiece(system=self.get_system(), id=id, vect=vect, mx=mx)
        if callable(self.children):
            # If self.children is a function, remove the function and replace by list
            self.children = []
        self.children.append(piece)
        return self

    def count_children(self):
        return 0 if callable(self.children) else len(self.children)

    def shuffle_children(self):
        if not callable(self.children):
            random.shuffle(self.children)
        return self

    def remove_child(self, position=None):
        # If position not specified, will remove the last child
        if not callable(self.children):
            if position is None:
                self.children.pop()
            else:
                self.children.pop(position)
        return self

    def __repr__(self):
        result = "FD: ["
        first = True
        if callable(self.children):
            result += "function"
        else:
            for child in self.children:
                if first:
                    first = False
                else:
                    result += ", "
                result += f"{child}"
        result += "]"
        return result
