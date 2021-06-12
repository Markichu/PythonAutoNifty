import math

from Vector2D import Vector2D
from helperFns import deg_to_rad


# A Matrix2D is a matrix of this form:
# [a, b]
# [c, d]

class Matrix2D:
    def __init__(self, a=1, b=0, c=0, d=1):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    # Clockwise rotation, angle in radians
    @classmethod
    def rotr(cls, angle):
        a = math.cos(angle)
        b = math.sin(angle)
        return cls(a, b, -b, a)

    # Clockwise rotation, angle in degrees
    @classmethod
    def rotd(cls, angle):
        return cls.rotr(deg_to_rad(angle))

    # Dihedral group of regular polygon 2, 3, 4, 5, 6...
    # (rectangle, triangle, square, pentagon, hexagon...)
    # where bottom edge is horizontal (so horizontal reflection)
    # Matrix2D.dh(5, 1) for identity
    # Matrix2D.dh(5, 2) for 72 degree rotation anticlockwise
    # Matrix2D.dh(5, 6) for horizontal reflection
    # Matrix2D.dh(8, 6) for 225 (45 * 5) degree rotation anticlockwise
    @classmethod
    def dh(cls, sides, num):
        if not isinstance(sides, int):
            raise TypeError("Number of sides must be an integer")
        if sides < 2:
            raise TypeError("Number of sides must be at least 2")
        if not isinstance(num, int):
            raise TypeError("Transformation number must be an integer")
        if num < 1:
            raise TypeError("Transformation number must be at least 1")
        if num > sides * 2:
            raise TypeError(f"Transformation number must be at most {sides * 2}")
        rotation = ((num - 1) % sides)  # 0, 1, 2, ..., sides - 1
        reflection = ((num - 1) - rotation) / sides  # 0, 1
        rotation_mx = cls.rotd((-360/sides) * rotation)
        reflection_mx = cls((-1) ** reflection, 0, 0, 1)
        return rotation_mx * reflection_mx

    # Square transformations 1 to 8
    # Matrix2D.sq(1) for identity
    # Matrix2D.sq(2) for 90 degree rotation anticlockwise
    # Matrix2D.sq(5) for *vertical* reflection (should have been horizontal... but already published on Nifty Ink)
    @classmethod
    def sq(cls, num):
        if not isinstance(num, int):
            raise TypeError("Argument is not integer")
        if num < 1:
            raise TypeError("Argument must be at least 1")
        if num > 8:
            raise TypeError("Argument must be at most 8")
        rotation = ((num - 1) % 4)  # 0, 1, 2, 3
        reflection = ((num - 1) - rotation) / 4  # 0, 1
        rotation_mx = cls.rotd((-90) * rotation)
        reflection_mx = cls(1, 0, 0, (-1) ** reflection)
        return rotation_mx * reflection_mx

    def copy(self):
        return Matrix2D(self.a, self.b, self.c, self.d)

    # Give an order of magnitude size for this matrix
    def rms_metric(self):
        return (0.5 * (self.a ** 2 + self.b ** 2 + self.c ** 2 + self.d ** 2)) ** 0.5
    
    def __mul__(self, obj):
        if isinstance(obj, (int, float)):
            result = Matrix2D()
            result.a = self.a * obj
            result.b = self.b * obj
            result.c = self.c * obj
            result.d = self.d * obj
            return result
        elif isinstance(obj, Vector2D):
            result = Vector2D()
            result.x = self.a * obj.x + self.b * obj.y
            result.y = self.c * obj.x + self.d * obj.y
            return result
        elif isinstance(obj, Matrix2D):
            result = Matrix2D()
            result.a = self.a * obj.a + self.b * obj.c
            result.b = self.a * obj.b + self.b * obj.d
            result.c = self.c * obj.a + self.d * obj.c
            result.d = self.c * obj.b + self.d * obj.d
            return result
        else:
            raise TypeError("Argument for matrix multiplication is not of a supported type")

    def __repr__(self):
        return f"[{self.a}, {self.b}; {self.c}, {self.d}]"
