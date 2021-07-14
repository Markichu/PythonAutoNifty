from FractalDefn import FractalDefn
from FractalPiece import FractalPiece
from fractalConstants import DEFAULT_MAX_ITERATIONS, DEFAULT_MIN_RADIUS, DEFAULT_MAX_PIECES, DEFAULT_MAX_DEFNS
from fractalHelperFns import DEFAULT_METRIC_FN


class FractalSystem:
    def __init__(self, max_iterations=DEFAULT_MAX_ITERATIONS, min_radius=DEFAULT_MIN_RADIUS, max_pieces=DEFAULT_MAX_PIECES):
        self.defns = []
        self.max_iterations = max_iterations
        self.min_radius = min_radius
        self.max_pieces = max_pieces
        self.max_defns = DEFAULT_MAX_DEFNS
        self.metric_fn = DEFAULT_METRIC_FN  # Function from piece to number (metric, radius, size). Can override on the definition.
        self.initial_pieces = []  # Set this one to a list of Fractal Pieces
        self.iterated_pieces = []  # Do not set this one, call fs.do_iterations() to generate it automatically
        self.piece_sorter = None

    def is_fractal_system(self):
        return True
    
    def get_defn(self, id):
        return self.defns[id]

    def get_metric_fn(self):
        return self.metric_fn

    def set_metric_fn(self, metric_fn):
        # metric_fn should be a function that maps from FractalPieces to numeric
        self.metric_fn = metric_fn
        return self

    def is_id_valid(self, id):
        if isinstance(id, int):
            if id >= 0 and id < len(self.defns):
                return True
        return False

    def add_defn(self, fractal_defn):
        self.defns.append(fractal_defn)
        # Make sure that definition is linked to this Fractal System,
        # overwriting any previous link
        if fractal_defn.get_system() != self:
            fractal_defn.set_system(self)
        return self
        
    def make_defns(self, n):
        if isinstance(n, int):
            if n > 0 and n <= self.max_defns:
                for i in range(0, n):
                    self.add_defn(FractalDefn(system=self))
        return self

    def do_iterations(self):
        self.iterated_pieces = self.initial_pieces
        for i in range(0, self.max_iterations):
            iteration_finished = self.iterate_once()
            if iteration_finished:
                break

    def iterate_once(self):
        iteration_finished = True
        next_iterated_pieces = []
        counter = 0
        for this_piece in self.iterated_pieces:
            counter += 1
            this_id = this_piece.get_id()
            this_vect = this_piece.get_vect()
            this_mx = this_piece.get_mx()
            this_metric = this_piece.get_metric()
            if self.is_id_valid(this_id):
                this_defn = self.get_defn(this_id)
                does_not_iterate = not this_defn.get_iterates()
                this_size_px = this_defn.relative_size * this_metric
                if this_size_px <= self.min_radius or self.max_pieces < counter or does_not_iterate:
                    next_iterated_pieces.append(this_piece)
                else:
                    iteration_finished = False
                    for child_piece in this_defn.get_children():
                        child_id = child_piece.get_id()
                        child_vect = child_piece.get_vect()
                        child_mx = child_piece.get_mx()
                        next_vect = this_vect + this_mx @ child_vect
                        next_mx = this_mx @ child_mx
                        next_piece = FractalPiece(system=self, id=child_id, vect=next_vect, mx=next_mx)
                        next_iterated_pieces.append(next_piece)
        if self.max_pieces < counter:
            iteration_finished = True
            print("Warning - max pieces exceeded")
        self.iterated_pieces = next_iterated_pieces
        return iteration_finished

    def final_size(self):
        return len(self.iterated_pieces)

    def plot(self, drawing):
        pieces_to_plot = self.iterated_pieces
        total_pieces = self.final_size()
        if callable(self.piece_sorter):
            pieces_to_plot.sort(key=self.piece_sorter)
        progress_counter = 0
        for piece_to_plot in pieces_to_plot:
            plotter = self.get_defn(piece_to_plot.id).get_plotter()
            plotter.plot(piece_to_plot, drawing, progress_counter, total_pieces)
            progress_counter += 1

    def __repr__(self):
        result = "FS: "
        first = True
        defn_id = 0
        for defn in self.defns:
            if first:
                first = False
            else:
                result += ", "
            result += f"(ID {defn_id} contains {defn})"
            defn_id += 1
        return result
