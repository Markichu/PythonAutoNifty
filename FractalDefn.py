from FractalPlotter import FractalPlotter
from FractalPiece import FractalPiece


class FractalDefn:
    def __init__(self, system=None):
        self.iterates = True  # if False, do not iterate the FractalPiece further
        self.children = []  # Either a list, or a function that evaluates to a list
        self.plotter = FractalPlotter()  # used to control plotting of FractalPieces linked to this FractalDefn
        self.system = system  # the FractalSystem this FractalDefn is contained within

        # How big is this definition?
        self.relative_size = 1
        # for self.relative_size = n,
        # either definition occupies circle of radius n,
        # or definition occupies square of size [-n, n] x [-n, n]
    
    def get_children(self):
        return self.children() if callable(self.children) else self.children

    def get_plotter(self):
        return self.plotter

    def set_plotter(self, plotter):
        self.plotter = plotter

    def get_system(self):
        return self.system

    def set_system(self, system):
        self.system = system

    def add_child(self, fractal_piece):
        if isinstance(fractal_piece, FractalPiece):
            if callable(self.children):
                # If self.children is a function, remove the function and replace by list
                self.children = []
            self.children.append(fractal_piece)
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
