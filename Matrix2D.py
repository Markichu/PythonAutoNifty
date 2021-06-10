from Vector2D import Vector2D


# 2D Matrix of this form:
# [a, b]
# [c, d]

class Matrix2D:
    def __init__(self, a=1, b=0, c=0, d=1):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def copy(self):
        return Matrix2D(self.a, self.b, self.c, self.d)

    def __mul__(self, obj):
        if isinstance(obj, Vector2D):
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
            raise TypeError("Passes object for multiplication is not a supported type.")

    def __repr__(self):
        return f"[{self.a}, {self.b}; {self.c}, {self.d}]"
