import random
from FractalPlotter import FractalPlotter
from FractalPiece import FractalPiece
from fractalHullHelperFns import iterate_defn_hull, calculate_hull_diameter
from fractalConstants import DEFAULT_HULL_ACCURACY


class FractalDefn:
    def __init__(self, system, id):
        self.system = system  # Link back to the system
        self.id = id  # The definition id number within the system

        # Fractal system contains default metric and iteration functions.
        # Override here at the definition level if needed.
        self.metric_fn = None
        self.iteration_fn = None

        self.plotter = FractalPlotter()  # used to control plotting of FractalPieces linked to this FractalDefn
        self.hull = None  # Convex Hull; set of coordinates describing shape of definition at vector (0, 0), matrix ((1, 0), (0, 1))
        self.hull_accuracy = DEFAULT_HULL_ACCURACY  # hull coordinates will be combined if they are nearer than this (small) number

        # Children should be either a list of abstract Fractal Pieces, or a function returning a list of abstract Fractal Pieces
        # If a function, it should accept an optional FractalPiece as context for evaluation.
        self.children = []

        # What is the minimum diameter of the convex hull of a piece calculated
        # on this definition with identity transformation (vect(0, 0), mx_id())?
        # (Note that if shear or stretch transformations are used then we really ought to calculate
        # diameter directly on the convex hull of each individual piece.)
        # For now, allow this value to be overridden, since perhaps in some situations the convex hull cannot be calculated.
        self.relative_diameter = 2
        # Default value of 2 means that under some rotation the fractal can be fitted between two planes 2 units apart.
        # or that approximately the fractal fits inside the 2x2 square [-1, 1] x [-1, 1]

    def get_metric_fn(self):
        return self.system.metric_fn if self.metric_fn is None else self.metric_fn

    def should_piece_iterate(self, piece):
        iteration_fn = self.system.iteration_fn if self.iteration_fn is None else self.iteration_fn
        return iteration_fn(piece)

    def get_piece_minimum_diameter(self, piece):
        # An alternative to the current method is calculating it directly
        # on the convex hull from this definition
        # transformed by the transformation on an individual piece.
        # This would cope well with stretches and shears.
        metric_fn = self.get_metric_fn()
        return self.relative_diameter * metric_fn(piece)

    def get_children(self, context_piece=None):
        # If self.children is not a function, it should be a list of FractalPieces, so return this list directly
        if not callable(self.children):
            return self.children
        # Otherwise, self.children is a function that should return a list of FractalPieces,
        # and accept an optional context_piece as context for evaluation
        # (The function should be able to cope with and without the context_piece,
        # since for fractal iteration the piece is supplied, but for convex hull it is not.)
        return self.children(context_piece)

    def create_child(self, id, vect, mx, reverse_progress=False, reset_progress=False):
        # This will be an "Abstract" fractal piece
        piece = FractalPiece(system=self.system, id=id, vect=vect, mx=mx, reverse_progress=reverse_progress, reset_progress=reset_progress)
        if callable(self.children):
            # If self.children is a function, remove the function and replace by list
            # Could alternatively raise an error if try to create_child on a fractal defn with fn for children
            self.children = []
        self.children.append(piece)
        return self

    def count_children(self):
        return 0 if callable(self.children) else len(self.children)

    def shuffle_children(self):
        if not callable(self.children):
            random.shuffle(self.children)
        return self

    def remove_child(self, position=None):
        # If position not specified, will remove the last child
        if not callable(self.children):
            if position is None:
                self.children.pop()
            else:
                self.children.pop(position)
        return self

    def plot(self, drawing, piece):
        self.plotter.plot(drawing, piece)

    def initialise_hull(self, hull_accuracy, initial_hull):
        self.hull_accuracy = hull_accuracy
        self.hull = initial_hull.copy()

    def iterate_hull(self, iteration):
        iterate_defn_hull(system=self.system, defn=self, iteration=iteration)

    def calculate_diameter(self):
        # TODO: Setting self.relative_diameter is only accurate in all cases for translations, rotations, reflections
        # If transformation is stretch or shear, this ought to be recalculated at the piece level!
        calculate_hull_diameter(system=self.system, defn=self)

    def __repr__(self):
        result = "FD: ["
        first = True
        if callable(self.children):
            result += "function"
        else:
            for child in self.children:
                if first:
                    first = False
                else:
                    result += ", "
                result += f"{child}"
        result += "]"
        return result
