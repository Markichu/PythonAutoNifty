class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def copy(self):
        return Vector2D(self.x, self.y)

    def __add__(self, obj):
        # TODO: Ought to check that obj is a Vector2D
        result = Vector2D()
        result.x = self.x + obj.x
        result.y = self.y + obj.y
        return result

    def __mul__(self, scale):
        # TODO: Ought to check that scale is numeric
        result = Vector2D()
        result.x = self.x * scale
        result.y = self.y * scale
        return result

    def __repr__(self):
        return f"[{self.x}; {self.y}]"
