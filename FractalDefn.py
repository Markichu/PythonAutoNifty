from FractalPlotter import FractalPlotter
from FractalPiece import FractalPiece


class FractalDefn:
    def __init__(self):
        self.iterates = True
        self.children = []
        self.plotter = FractalPlotter()

        # How big is this definition?
        self.relative_size = 1
        # for self.relative_size = n,
        # either definition occupies circle of radius n,
        # or definition occupies square of size [-n, n] x [-n, n]

    def add_child(self, fractal_piece):
        if isinstance(fractal_piece, FractalPiece):
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
