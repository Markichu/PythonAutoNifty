from FractalDefn2D import FractalDefn2D
from FractalPiece2D import FractalPiece2D


class FractalSystem2D:
    def __init__(self, max_iterations=4, min_radius=40, max_pieces=1000):
        self.defns = []
        self.max_iterations = max_iterations
        self.min_radius = min_radius
        self.max_pieces = max_pieces
        self.max_defns = 10000

    def add_defn(self, fractal_defn):
        self.defns.append(fractal_defn)
        return self
        
    def make_defns(self, n):
        if isinstance(n, int):
            if n > 0 and n <= self.max_defns:
                for i in range(0, n):
                    self.add_defn(FractalDefn2D())
        return self

    def iterate(self, fractal_piece_list):
        result = fractal_piece_list
        for i in range(0, self.max_iterations):
            result = self.get_next_iteration(result)
        return result

    def get_next_iteration(self, fractal_piece_list):
        result = []
        counter = 0
        for prev_piece in fractal_piece_list:
            counter += 1
            this_id = prev_piece.id
            this_defn = self.defns[this_id]
            this_size_px = this_defn.relative_size * prev_piece.radius()
            if this_size_px <= self.min_radius or self.max_pieces < counter:
                result.append(prev_piece)
            else:
                for child_piece in this_defn.children:
                    result.append(FractalPiece2D(child_piece.id, prev_piece.vect + prev_piece.mx * child_piece.vect,  prev_piece.mx * child_piece.mx))
        return result

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
                    progress = progress_counter / (piece_count_plot - 1)
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
