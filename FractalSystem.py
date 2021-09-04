import numpy as np
from scipy.spatial import ConvexHull

from FractalDefn import FractalDefn
from FractalPiece import FractalPiece
from fractalConstants import DEFAULT_MAX_ITERATIONS, DEFAULT_MIN_RADIUS, DEFAULT_MAX_PIECES, DEFAULT_MAX_DEFNS
from fractalConstants import DEFAULT_INITIAL_HULL, DEFAULT_HULL_MAX_ITERATIONS, DEFAULT_HULL_MIN_LEN
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

    # To make a convex hull
    # 1. Start with any 2D shape (e.g. a triangle around the origin) for a hull for each definition
    # 2. At each calculation iteration, for each definition, take union of previous hulls under fractal maps
    # 3. Use a convex hull algorithm to remove all interior points
    # 4. Replace previous hull points with new hull points, and iterate several times

    # Note (*) - currently "vect" is actually not a column vector, but is a row coordinate
    # which mean that premultiplying by matrix -> postmultiplying by matrix transpose
    # (all the matrix arithmetic is backwards!)
    # This probably ought to be fixed later on...

    # Also note that for random fractals the hull will not converge so nicely
    # This could be alleviated by using multiple (random) copies of the hull points at each stage

    # Since the min_len introduces rounding into the coords, it would be possible to stop early
    # if the previous and next rounded coords were identical

    def calculate_hulls(self, max_iterations=DEFAULT_HULL_MAX_ITERATIONS, min_len=DEFAULT_HULL_MIN_LEN, initial_hull=DEFAULT_INITIAL_HULL):
        # Initialise all defns
        for defn in self.defns:
            # Initialise convex hull to at least 3 points around the origin, must use a 2D shape for ConvexHull algorithm 1st iteration
            defn.hull = initial_hull
            defn._next_hull = None
        # Iteratively work out the convex hull
        for i in range(max_iterations):
            # Calculate next hulls
            for j in range(len(self.defns)):
                defn = self.defns[j]
                children = defn.get_children()
                if len(children) < 1:
                    continue
                next_points = None
                for child in children:
                    id = child.get_id()
                    vect = child.get_vect()
                    mx = child.get_mx()
                    prev_hull = self.defns[id].get_hull()
                    next_points_partial = prev_hull @ np.transpose(mx) + vect  # Backwards arithmetic here (*)
                    if next_points is None:
                        next_points = next_points_partial
                    else:
                        next_points = np.concatenate((next_points, next_points_partial))
                scaled_integer_points = np.rint(next_points * (1/min_len))
                hull = ConvexHull(scaled_integer_points)  # object
                vertices = hull.vertices  # array of point indices
                defn._next_hull = next_points[vertices] # next_points and scaled_integer_points have same order
            # Store next hulls
            for defn in self.defns:
                if defn._next_hull is not None:
                    defn.hull = defn._next_hull
                    defn._next_hull = None
        print("")
        print(f"Results of Convex Hull calculations:")
        for j in range(len(self.defns)):
            defn = self.defns[j]
            children = defn.get_children()
            if len(children) < 1:
                continue
            print(f"Definition {j} has length {len(defn.get_hull())}")
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
                does_not_iterate = not this_defn.get_iterates(this_piece)
                this_size_px = this_defn.relative_size * this_metric
                if this_size_px <= self.min_radius or self.max_pieces < counter or does_not_iterate:
                    next_iterated_pieces.append(this_piece)
                else:
                    iteration_finished = False
                    for child_piece in this_defn.get_children(this_piece):
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
