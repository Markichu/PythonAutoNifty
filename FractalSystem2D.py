from FractalPiece2D import FractalPiece2D


class FractalSystem2D:
    def __init__(self):
        self.defns = []

    def add_defn(self, fractal_defn):
        self.defns.append(fractal_defn)
        return self

    def iterate(self, fractal_piece, iterations=0):
        result = [fractal_piece]
        for i in range(0, iterations):
            result = self.get_next_iteration(result)
        return result

    def get_next_iteration(self, fractal_piece_list):
        result = []
        for prev_piece in fractal_piece_list:
            this_id = prev_piece.id
            this_defn = self.defns[this_id]
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
