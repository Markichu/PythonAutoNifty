import math

from .constants import DRAWING_SIZE


# This class Pos wraps an x and y coordinate.
# This class could potentially be refactored (and replaced) by numpy vectors,
# however there would be a lot of updates to make.

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_rotational(radians, radius, origin=None):
        if origin is None:
            origin = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)

        return Pos(math.cos(radians) * radius / 2, math.sin(radians) * radius / 2) + origin

    def point(self):
        return {"x": self.x, "y": self.y}

    def copy(self):
        return Pos(self.x, self.y)

    def irotate(self, rotation, origin=None):
        # get default centre
        if origin is None:
            origin = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)

        self -= origin
        x = self.x * math.cos(rotation) - self.y * math.sin(rotation)
        self.y = self.x * math.sin(rotation) + self.y * math.cos(rotation)
        self.x = x
        self += origin
        return self

    def rotate(self, rotation, origin=None):
        return self.copy().irotate(rotation, origin)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, mult):
        self.x *= mult
        self.y *= mult
        return self

    def __itruediv__(self, div):
        self.x /= div
        self.y /= div
        return self

    def __add__(self, other):
        result = self.copy()
        result += other
        return result

    def __sub__(self, other):
        result = self.copy()
        result -= other
        return result

    def __mul__(self, mult):
        result = self.copy()
        result *= mult
        return result

    def __truediv__(self, div):
        result = self.copy()
        result /= div
        return result

    def __round__(self, n_digits=None):
        result = self.copy()
        result.x = round(self.x, n_digits)
        result.y = round(self.y, n_digits)
        return result

    def __repr__(self):
        return f"({self.x}, {self.y})"
