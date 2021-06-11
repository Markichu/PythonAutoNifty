from FractalDefn2D import FractalDefn2D
from FractalPiece2D import FractalPiece2D


class FractalSystem2D:
    def __init__(self):
        self.defns = []

    def add_defn(self, fractal_defn):
        self.defns.append(fractal_defn)
        return self
        
    def add_n_defns(self, n):
        if isinstance(n, int):
            if n > 0:
                for i in range(0, n):
                    self.add_defn(FractalDefn2D())
        return self

    def add_child(self, id, fractal_piece):
        self.defns[id].add_child(fractal_piece)
        return self

    def iterate(self, fractal_piece, max_iterations=0, min_radius=1):
        result = [fractal_piece]
        for i in range(0, max_iterations):
            result = self.get_next_iteration(result, min_radius)
        return result

    def get_next_iteration(self, fractal_piece_list, min_radius):
        result = []
        for prev_piece in fractal_piece_list:
            this_id = prev_piece.id
            this_defn = self.defns[this_id]
            this_size_px = this_defn.radius_factor * prev_piece.radius()
            if this_size_px <= min_radius:
                result.append(prev_piece)
            else:
                for child_piece in this_defn.children:
                    next_piece = FractalPiece2D()
                    next_piece.id = child_piece.id
                    next_piece.vect = prev_piece.vect + prev_piece.mx * child_piece.vect
                    next_piece.mx = prev_piece.mx * child_piece.mx
                    result.append(next_piece)
        return result

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
