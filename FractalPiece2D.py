from Vector2D import Vector2D
from Matrix2D import Matrix2D

dummyVect = Vector2D()
dummyMx = Matrix2D()


class FractalPiece2D:
    def __init__(self, id=0, vect=dummyVect, mx=dummyMx):
        if isinstance(id, int):
            if id >= 0:
                self.id = id
            else:
                self.id = 0
        else:
            self.id = 0
        
        if isinstance(vect, Vector2D):
            self.vect = vect
        else:
            self.vect = Vector2D() # need new object here, not the dummy object

        if isinstance(mx, Matrix2D):
            self.mx = mx
        else:
            self.mx = Matrix2D() # need new object

    def copy(self):
        return FractalPiece2D(self.id, self.vect.copy(), self.mx.copy())

    def radius(self):
        return self.mx.rms_metric()

    def __repr__(self):
        return f"(id {self.id}, vect {self.vect}, mx {self.mx})"
