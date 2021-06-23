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

    def iterate(self, fractal_piece_list):
        result = fractal_piece_list
        for i in range(0, self.max_iterations):
            iteration_result = self.get_next_iteration(result)
            iteration_finished = iteration_result[0]
            result = iteration_result[1]
            if iteration_finished:
                break
        return result

    def get_next_iteration(self, fractal_piece_list):
        iteration_finished = True
        result = []
        counter = 0
        for this_piece in fractal_piece_list:
            counter += 1
            this_id = this_piece.get_id()
            this_vect = this_piece.get_vect()
            this_mx = this_piece.get_mx()
            this_radius = this_piece.get_radius()
            if self.is_id_valid(this_id) and isinstance(this_vect, Vector2D) and isinstance(this_mx, Matrix2D):
                this_defn = self.defns[this_id]
                does_not_iterate = not this_defn.iterate
                this_size_px = this_defn.relative_size * this_radius
                if this_size_px <= self.min_radius or self.max_pieces < counter or does_not_iterate:
                    result.append(this_piece)
                else:
                    iteration_finished = False
                    for child_piece in this_defn.children:
                        child_id = child_piece.get_id()
                        child_vect = child_piece.get_vect()
                        child_mx = child_piece.get_mx()
                        result.append(FractalPiece(child_id, this_vect + this_mx * child_vect, this_mx * child_mx))
        iteration_result = [iteration_finished, result]
        return iteration_result

    def plot(self, fractal_piece_list_all, drawing):
        piece_count_all = len(fractal_piece_list_all)
        if piece_count_all > 0:
            # Make a list of pieces to plot, excluding non-drawing pieces
            fractal_piece_list_plot = []
            for piece1 in fractal_piece_list_all:
                defn1 = self.defns[piece1.id]
                plotter1 = defn1.plotter
                if plotter1.draw == True:
                    fractal_piece_list_plot.append(piece1)
            piece_count_plot = len(fractal_piece_list_plot)
            if piece_count_plot > 0:
                # Plot them
                progress_counter = 0
                for piece2 in fractal_piece_list_plot:
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
