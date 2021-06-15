import math
import random
from helperFns import interpolate_colour
from constants import DRAWING_SIZE, BLACK
from Vector2D import Vector2D
from Pos import Pos


class FractalPlotter2D:
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
        # Calculate which colour to use, based on progress through piece list
        cols = self.colours
        len_col = len(cols) - 1
        prog2 = progress * len_col
        prog_rem = prog2 - math.floor(prog2)
        colour_start = cols[math.floor(prog2)]
        colour_end = cols[math.ceil(prog2)]
        colour_this = interpolate_colour(colour_start, colour_end, prog_rem, self.alpha)
        # Inner function to turn vector into Pos
        def vect_to_pos(v1, mx, v2):
            wobble_x = self.hand_wobble_px * (random.random() - 0.5)
            wobble_y = self.hand_wobble_px * (random.random() - 0.5)
            v3 = v1 + (mx * v2) * self.path_expand_factor + Vector2D(wobble_x, wobble_y)
            pos1 = Pos(v3.x, DRAWING_SIZE - v3.y)
            return pos1
        # Plot
        path_vects = self.path_vectors
        path_len = len(path_vects)
        if path_len > 1:
            # Plot path
            pos_list = []
            for i in range(0, path_len):
                pos_list.append(vect_to_pos(piece.vect, piece.mx, path_vects[i]))
            if self.path_close:
                pos_list.append(pos_list[0])
            drawing.add_line(pos_list, colour_this, self.path_width)
        else:
            # Plot dot
            v4 = Vector2D()
            if path_len == 1:
                v4 = path_vects[0]
            pos = vect_to_pos(piece.vect, piece.mx, v4)
            circle_radius = self.dot_expand_factor * piece.radius()
            drawing.add_point(pos, colour_this, circle_radius)

    def __repr__(self):
        return "FDO: (options)"
