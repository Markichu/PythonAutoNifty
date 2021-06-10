class FractalDefn2D:
    def __init__(self):
        self.children = []

    def add_child(self, fractal_piece):
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
