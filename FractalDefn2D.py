from FractalPlotter2D import FractalPlotter2D
from FractalPiece2D import FractalPiece2D


class FractalDefn2D:
    def __init__(self):
        self.children = []
        self.plotter = FractalPlotter2D()
        self.relative_size = 1  # How big is this definition relative to square [-1, 1] x [-1, 1]?

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
