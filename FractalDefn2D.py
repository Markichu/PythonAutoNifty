from FractalPlotter2D import FractalPlotter2D
from FractalPiece2D import FractalPiece2D


class FractalDefn2D:
    def __init__(self):
        self.children = []
        self.plotter = FractalPlotter2D()

        # How big is this definition?
        self.relative_size = 1
        # for self.relative_size = n,
        # either definition occupies circle of radius n,
        # or definition occupies square of size [-n, n] x [-n, n]

    def add_child(self, fractal_piece):
        if isinstance(fractal_piece, FractalPiece2D):
            self.children.append(fractal_piece)
        return self

    def __repr__(self):
        result = "FD: ["
        first = True
        for child in self.children:
            if first:
                first = False
            else:
                result += ", "
            result += f"{child}"
        result += "]"
        return result
