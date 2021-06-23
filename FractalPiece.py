from numpyHelperFns import array_rms_metric


class FractalPiece:
    def __init__(self, id, vect, mx):
        self.id = id  # Integer list index (0, 1, 2...) in fractal system, or callback that returns an index
        self.vect = vect  # Vector, or callback that returns a vector
        self.mx = mx  # Matrix, or callback that returns a matrix

    # If instance variable is callable, then return var()
    # Otherwise, return var
    # This allows things like randomisation to be carried out
    # each time the getter is called
    def _get_instance_var(self, arg):
        result = arg
        if callable(result):
            result = result()
        return result

    def get_id(self):
        return self._get_instance_var(self.id)

    def get_vect(self):
        return self._get_instance_var(self.vect)

    def get_mx(self):
        return self._get_instance_var(self.mx)

    def get_radius(self):
        return array_rms_metric(self.get_mx())

    def __repr__(self):
        mxprint = f"{self.mx}".replace("\n", ",")
        return f"(id {self.id}, vect {self.vect}, mx {mxprint})"
