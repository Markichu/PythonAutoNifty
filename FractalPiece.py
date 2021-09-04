class FractalPiece:
    def __init__(self, system, id, vect, mx, progress=None, reverse_progress=False, reset_progress=False):
        if not system.is_fractal_system():
            # Can remove this eventually, at the moment it catches any previous code that omitted the system
            raise TypeError("Must supply a FractalSystem to create a FractalPiece")
        self.system = system

        # Keep track of "progress" through the fractal iteration using an interval [start, end]
        # Default interval is [0, 1]. Interval is a list of [start, end] values of progress.
        # When iterating, this interval should be subdivided and become smaller and smaller within [0, 1].
        self.progress = progress if progress is not None else [0, 1]  # use None above and [0, 1] here to get new list each time

        # In a fractal definition, for a child fractal, set reverse_progress directly to True
        # if you want progress to be flipped when iterating.
        # An example of when this is useful is for a dragon fractal, to get linear colouring.
        self.reverse_progress = reverse_progress

        # In a fractal definition, for a child fractal, set reset_progress directly to True
        # if you want progress to revert back to [0, 1] on this fractal piece
        # For example, if using an outer fractal to generate a lot of inner fractals,
        # might want to reset the progress on each one. This could for example reset the colouring scheme on each inner fractal.
        # Probably don't have reset_progress true for any fractal that iterates to itself.
        self.reset_progress = reset_progress

        # These should be either a value of the specified type, or a function returning suitable value
        # Function should accept an optional FractalPiece as context for evaluation.
        self.id = id  # Should be a non-negative integer 0, 1, 2... representing definition position in fractal system
        self.vect = vect  # Numpy vector (or is it coordinate?)
        self.mx = mx  # Numpy matrix

    def get_system(self):
        return self.system
    
    def get_progress_value(self):
        return 0.5 * (self.progress[0] + self.progress[1])

    # Return array of n intervals representing progress interval of this piece split into n chunks
    def split_progress_interval(self, n):
        prog_start = self.progress[0]
        prog_end = self.progress[1]
        prog_step = (prog_end - prog_start) / n
        result = [None] * n
        for i in range(n):
            result[i] = [prog_start + i * prog_step, prog_start + (i+1) * prog_step]
        return result

    def get_defn(self):
        return self.get_system().get_defn(self.get_id())

    # If instance variable is callable, then return var()
    # Otherwise, return var
    # This allows things like randomisation to be carried out
    # each time the getter is called
    def _get_instance_var(self, arg):
        result = arg
        if callable(result):
            # Evaluate the function on the context, i.e. this fractal piece
            result = result(self)
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
