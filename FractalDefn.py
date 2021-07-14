from FractalPlotter import FractalPlotter
from FractalPiece import FractalPiece


class FractalDefn:
    def __init__(self, system=None, metric_fn=None):
        self.iterates = True  # Either a Boolean, or a function that evaluates to a Boolean; if False, do not iterate the FractalPiece further
        self.system = system  # the FractalSystem this FractalDefn is contained within
        self.metric_fn = metric_fn  # Use this to override the metric function set at system level
        self.plotter = FractalPlotter()  # used to control plotting of FractalPieces linked to this FractalDefn
        self.children = []  # Either a list, or a function that evaluates to a list

        # How big is this definition?
        self.relative_size = 1
        # for self.relative_size = n,
        # either definition occupies circle of radius n,
        # or definition occupies square of size [-n, n] x [-n, n]
    
    def get_iterates(self):
        return self.iterates() if callable(self.iterates) else self.iterates

    def set_iterates(self, iterates):
        # iterates should be a Boolean, or a function that evaluates to a Boolean
        self.iterates = iterates
        return self

    def get_system(self):
        return self.system

    def set_system(self, system):
        # system should be a FractalSystem
        self.system = system
        return self

    def get_metric_fn(self):
        return self.get_system().get_metric_fn() if self.metric_fn is None else self.metric_fn

    def get_plotter(self):
        return self.plotter

    def set_plotter(self, plotter):
        # plotter should be a FractalPlotter
        self.plotter = plotter
        return self

    def get_children(self):
        return self.children() if callable(self.children) else self.children

    def create_child(self, id, vect, mx):
        piece = FractalPiece(system=self.get_system(), id=id, vect=vect, mx=mx)
        if callable(self.children):
            # If self.children is a function, remove the function and replace by list
            self.children = []
        self.children.append(piece)
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
