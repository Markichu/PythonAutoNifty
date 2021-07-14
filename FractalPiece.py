class FractalPiece:
    def __init__(self, system, id, vect, mx):
        if not system.is_fractal_system():
            # Can remove this eventually, at the moment it catches any previous code that omitted the system
            raise TypeError("Must supply a FractalSystem to create a FractalPiece")
        self.system = system
        self.id = id  # Integer list index (0, 1, 2...) in fractal system, or callback that returns an index
        self.vect = vect  # Vector, or callback that returns a vector
        self.mx = mx  # Matrix, or callback that returns a matrix

    def get_system(self):
        return self.system

    def get_defn(self):
        return self.get_system().get_defn(self.get_id())

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

    def get_metric_fn(self):
        return self.get_defn().get_metric_fn()

    def get_metric(self):
        metric_fn = self.get_metric_fn()
        return metric_fn(self)

    def __repr__(self):
        id = "function" if callable(self.id) else self.id
        vect = "function" if callable(self.vect) else self.vect
        mx = "function" if callable(self.mx) else self.mx
        mxprint = f"{mx}".replace("\n", ",")
        return f"(id {id}, vect {vect}, mx {mxprint})"
