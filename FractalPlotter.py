from constants import BLACK
from Vector2D import Vector2D
from fractalHelperFns import vect_to_pos, get_colour


class FractalPlotter:
    def __init__(self):
        self.draw = True
        self.colours = [BLACK]
        self.alpha = 1
        self.hand_wobble_px = 0
        self.dot_expand_factor = 1
        self.path_vectors = []
        self.path_width = 1
        self.path_expand_factor = 1
        self.path_close = False
    
    def add_path_vector(self, vect):
        if isinstance(vect, Vector2D):
            self.path_vectors.append(vect)
        return self
    
    def add_path_vectors(self, vect_list):
        for vect in vect_list:
            self.add_path_vector(vect)
        return self

    def plot(self, piece, drawing, progress):
        this_colour = get_colour(self.colours, progress, self.alpha)
        # Plot
        path_vects = self.path_vectors
        path_len = len(path_vects)
        if path_len > 1:
            # Plot path
            pos_list = []
            for i in range(0, path_len):
                pos_list.append(vect_to_pos(piece.get_vect(), piece.get_mx(), path_vects[i], self.hand_wobble_px, self.path_expand_factor))
            if self.path_close:
                pos_list.append(pos_list[0])
            drawing.add_line(pos_list, this_colour, self.path_width)
        else:
            # Plot dot
            v4 = Vector2D()
            if path_len == 1:
                v4 = path_vects[0]
            pos = vect_to_pos(piece.get_vect(), piece.get_mx(), v4, self.hand_wobble_px, 1)
            circle_radius = self.dot_expand_factor * piece.get_radius()
            drawing.add_point(pos, this_colour, circle_radius)

    def __repr__(self):
        return f"FP: draw {self.draw}, dot rel. size {self.dot_expand_factor}, path width {self.path_width}, path vectors {self.path_vectors}, colours {self.colours}"
