# A Vector2D is a vector of this form:
# [x]
# [y]

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def copy(self):
        return Vector2D(self.x, self.y)

    def __add__(self, obj):
        if isinstance(obj, Vector2D):
            result = Vector2D()
            result.x = self.x + obj.x
            result.y = self.y + obj.y
            return result
        else:
            raise TypeError("Non-vector argument for vector addition")

    def __mul__(self, scale):
        if isinstance(scale, (int, float)):
            result = Vector2D()
            result.x = self.x * scale
            result.y = self.y * scale
            return result
        else:
            raise TypeError("Non-numeric argument for vector scaling")

    def __repr__(self):
        return f"[{self.x}; {self.y}]"
