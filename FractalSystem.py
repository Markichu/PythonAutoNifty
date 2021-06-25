from FractalDefn import FractalDefn
from FractalPiece import FractalPiece
from fractalConstants import DEFAULT_MAX_ITERATIONS, DEFAULT_MIN_RADIUS, DEFAULT_MAX_PIECES, DEFAULT_MAX_DEFNS


class FractalSystem:
    def __init__(self, max_iterations=DEFAULT_MAX_ITERATIONS, min_radius=DEFAULT_MIN_RADIUS, max_pieces=DEFAULT_MAX_PIECES):
        self.defns = []
        self.max_iterations = max_iterations
        self.min_radius = min_radius
        self.max_pieces = max_pieces
        self.max_defns = DEFAULT_MAX_DEFNS
        self.initial_pieces = []  # Set this one to a list of Fractal Pieces
        self.iterated_pieces = []  # Do not set this one, call fs.do_iterations() to generate it automatically
    
    def is_id_valid(self, id):
        if isinstance(id, int):
            if id >= 0 and id < len(self.defns):
                return True
        return False

    def add_defn(self, fractal_defn):
        self.defns.append(fractal_defn)
        return self
        
    def make_defns(self, n):
        if isinstance(n, int):
            if n > 0 and n <= self.max_defns:
                for i in range(0, n):
                    self.add_defn(FractalDefn())
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
            this_radius = this_piece.get_radius()
            if self.is_id_valid(this_id):
                this_defn = self.defns[this_id]
                does_not_iterate = not this_defn.iterate
                this_size_px = this_defn.relative_size * this_radius
                if this_size_px <= self.min_radius or self.max_pieces < counter or does_not_iterate:
                    next_iterated_pieces.append(this_piece)
                else:
                    iteration_finished = False
                    for child_piece in this_defn.children:
                        child_id = child_piece.get_id()
                        child_vect = child_piece.get_vect()
                        child_mx = child_piece.get_mx()
                        next_iterated_pieces.append(FractalPiece(child_id, this_vect + this_mx @ child_vect, this_mx @ child_mx))
        self.iterated_pieces = next_iterated_pieces
        return iteration_finished

    def final_size(self):
        return len(self.iterated_pieces)

    def plot(self, drawing):
        if self.final_size() > 0:
            # Make a list of pieces to plot, excluding non-drawing pieces
            pieces_to_plot = []
            for piece1 in self.iterated_pieces:
                defn1 = self.defns[piece1.id]
                plotter1 = defn1.plotter
                if plotter1.draw == True:
                    pieces_to_plot.append(piece1)
            piece_count_plot = len(pieces_to_plot)
            if piece_count_plot > 0:
                # Plot them
                progress_counter = 0
                for piece2 in pieces_to_plot:
                    defn2 = self.defns[piece2.id]
                    plotter2 = defn2.plotter
                    if piece_count_plot > 1:
                        progress = progress_counter / (piece_count_plot - 1)
                    else:
                        progress = 0.5
                    progress_counter += 1
                    plotter2.plot(piece2, drawing, progress)

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
