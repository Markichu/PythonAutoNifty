from Vector2D import Vector2D
from Matrix2D import Matrix2D


class FractalPiece2D:
    def __init__(self):
        self.id = 0
        self.vect = Vector2D()
        self.mx = Matrix2D()

    def copy(self):
        result = FractalPiece2D()
        result.id = self.id
        result.vect = self.vect
        result.mx = self.mx
        return result

    def radius(self):
        return self.mx.rms_metric()

    def __repr__(self):
        return f"(id {self.id}, vect {self.vect}, mx {self.mx})"
