import math

from constants import DRAWING_SIZE


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

    def rotate(self, rotation, origin=None):
        # get default centre
        if origin is None:
            origin = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)

        self -= origin
        x = self.x * math.cos(rotation) - self.y * math.sin(rotation)
        self.y = self.x * math.sin(rotation) + self.y * math.cos(rotation)
        self.x = x
        return self + origin

    def __add__(self, other):
        result = self.copy()
        result.x += other.x
        result.y += other.y
        return result

    def __sub__(self, other):
        result = self.copy()
        result.x -= other.x
        result.y -= other.y
        return result

    def __mul__(self, mult):
        result = self.copy()
        result.x *= mult
        result.y *= mult
        return result

    def __truediv__(self, div):
        result = self.copy()
        result.x /= div
        result.y /= div
        return result

    def __round__(self):
        result = self.copy()
        result.x = round(self.x)
        result.y = round(self.y)
        return result

    def __repr__(self):
        return f"({self.x}, {self.y})"
