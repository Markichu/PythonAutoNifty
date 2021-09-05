from fractalHelperFns import DEFAULT_ITERATION_FN

# Consider splitting FractalPiece class into concrete and abstract subclasses
#
# Abstract fractal pieces are the ones inside a fractal definition, and can have values or functions for id, vect, matrix
# Must use get_id, get_vect, get_mx for these.
#
# Concrete fractal pieces can only have values (and not functions) for id, vect, matrix
# Fractal system should have concrete initial pieces, and concrete iterated pieces
# This is mentioned in comments on the 'iterate' method below.
# For concrete, it would still be encouraged to use the getters, even though self.id, self.vect, self.mx would work.

class FractalPiece:
    def __init__(self, system, id, vect, mx, iteration=0, progress=None, reverse_progress=False, reset_progress=False):
        self.system = system

        # Keep track of what iteration this piece is on
        self.iteration = iteration

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
    
    def get_progress_value(self):
        return 0.5 * (self.progress[0] + self.progress[1])

    # Return array of n intervals representing progress interval of this piece split into n chunks
    # n should be a positive integer
    def split_progress_interval(self, n):
        prog_start = self.progress[0]
        prog_end = self.progress[1]
        prog_step = (prog_end - prog_start) / n
        result = [None] * n
        for i in range(n):
            result[i] = [prog_start + i * prog_step, prog_start + (i+1) * prog_step]
        return result

    def get_defn(self):
        return self.system.lookup_defn(self.get_id())

    # If instance variable is callable, then return var(context_piece)
    # Otherwise, return var
    # This allows things like randomisation to be carried out
    # each time the getter is called
    # The context piece will be the outer piece using this piece to iterate
    def _get_instance_var(self, arg, context_piece=None):
        result = arg
        if callable(result):
            # Evaluate the function on the context, i.e. this fractal piece
            result = result(context_piece)
        return result

    def get_id(self, context_piece=None):
        return self._get_instance_var(self.id, context_piece)

    def get_vect(self, context_piece=None):
        return self._get_instance_var(self.vect, context_piece)

    def get_mx(self, context_piece=None):
        return self._get_instance_var(self.mx, context_piece)
        
    def get_minimum_diameter(self):
        return self.get_defn().get_piece_minimum_diameter(self)
    
    def plot(self, drawing):
        self.get_defn().plot(drawing, self)

    def iterate(self, collect_next_iteration):
        was_iterated = False
        this_defn = self.get_defn()
        if this_defn is None:
            # If defn cannot be found, this piece should not be added to collect_next_iteration
            pass
        else:
            if not this_defn.should_piece_iterate(self):
                # Do not iterate, but keep piece inside the list collect_next_iteration
                collect_next_iteration.append(self)
            else:
                was_iterated = True
                # 'This' piece (self) is concrete, so id, vect, mx ought to be values, not functions.
                # Use getters anyway, but don't supply context
                this_vect = self.get_vect()
                this_mx = self.get_mx()
                # defn.children might be a function. Use the getter with this piece (self) as context.
                defn_child_pieces = this_defn.get_children(self)
                count_children = len(defn_child_pieces)
                if 0 < count_children:
                    progress_intervals = self.split_progress_interval(count_children)
                    for i in range(count_children):
                        defn_child_piece = defn_child_pieces[i]
                        # 'Defn child' piece on a fractal definition is abstract,
                        # so id, vect, mx could be values or functions.
                        # Therefore need to use the getters, evaluated in the context of this piece (self).
                        defn_child_id = defn_child_piece.get_id(self)
                        defn_child_vect = defn_child_piece.get_vect(self)
                        defn_child_mx = defn_child_piece.get_mx(self)
                        # 'Next' piece will be concrete, and will be constructed with values (not functions) for id, vect, mx.
                        next_id = defn_child_id
                        next_vect = this_vect + this_mx @ defn_child_vect
                        next_mx = this_mx @ defn_child_mx
                        next_progress = progress_intervals[i]
                        if defn_child_piece.reverse_progress:
                            next_progress = [next_progress[1], next_progress[0]]
                        if defn_child_piece.reset_progress:
                            next_progress = [0, 1]
                        next_piece = FractalPiece(system=self.system, id=next_id, vect=next_vect, mx=next_mx, iteration=self.iteration + 1, progress=next_progress)
                        collect_next_iteration.append(next_piece)
        return was_iterated


    def __repr__(self):
        id = "function" if callable(self.id) else self.id
        vect = "function" if callable(self.vect) else self.vect
        mx = "function" if callable(self.mx) else self.mx
        mxprint = f"{mx}".replace("\n", ",")
        return f"(id {id}, vect {vect}, mx {mxprint})"
