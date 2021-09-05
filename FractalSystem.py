import numpy as np
from scipy.spatial import ConvexHull

from FractalDefn import FractalDefn
from fractalConstants import DEFAULT_MAX_PIECES, DEFAULT_MAX_DEFNS
from fractalConstants import DEFAULT_INITIAL_HULL, DEFAULT_HULL_MAX_ITERATIONS, DEFAULT_HULL_MIN_LEN, BREAK_AFTER_ITERATIONS
from fractalHelperFns import DEFAULT_METRIC_FN, DEFAULT_ITERATION_FN

# There should only be 1 fractal system created,
# link all fractal definitions and pieces back to this system

class FractalSystem:
    def __init__(self, max_pieces=DEFAULT_MAX_PIECES):
        self.defns = []
        self.max_pieces = max_pieces
        self.max_defns = DEFAULT_MAX_DEFNS
        self.iteration_fn = DEFAULT_ITERATION_FN  # Function to tell a fractal piece if it should iterate or not
        self.metric_fn = DEFAULT_METRIC_FN  # Function mapping from affine transformation (vect, mx) of a piece, to a numeric value. Can override on the definition.
        self.initial_pieces = []  # Set this one to a list of Fractal Pieces
        self.iterated_pieces = []  # Do not set this one, call fs.do_iterations() to generate it automatically
        self.piece_sorter = None

    def lookup_defn(self, id):
        if isinstance(id, int) and id >= 0 and id < len(self.defns):
            return self.defns[id]
        else:
            # If id is not found, fail gracefully by returning None.
            # Should check for None and only take further action if a definition is returned.
            return None

    def add_defn(self, fractal_defn):
        self.defns.append(fractal_defn)
        fractal_defn.system = self  # Force definition to link back to this system
        return self
        
    def make_defns(self, n):
        if isinstance(n, int) and n > 0 and n <= self.max_defns:
            self.defns = []
            for i in range(n):
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

    # Probably ought to limit the hull size to 20 or less points (in 2D) or a specified number of point (in 3D)
    # and have a good algorithm to expand the hull slightly to find suitable fewer points

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
                    prev_hull = self.defns[id].hull
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
            print(f"Definition {j} has length {len(defn.hull)}")
        print("")
        return self

    def do_iterations(self):
        self.iterated_pieces = self.initial_pieces
        iteration_finished = False
        counter = 0
        while not iteration_finished:
            counter += 1
            print(f"Calculating iteration {counter} on {len(self.iterated_pieces)} piece{'' if len(self.iterated_pieces) == 1 else 's'}")
            iteration_finished = self.iterate_once()
            if BREAK_AFTER_ITERATIONS <= counter:
                print(f"Forced break after {counter} iterations")
                break
        print("")

    def iterate_once(self):
        iteration_finished = True  # Set to false if at least one piece was successfully iterated
        exceeded_max_pieces = False  # Set to true if we run out of storage space
        n = len(self.iterated_pieces)  # self.iterated_pieces is this iteration
        collect_next_iteration = []  # collect_next_iteration is next iteration, updated by .iterate function below
        for i in range(n):
            piece_to_iterate = self.iterated_pieces[i]
            if exceeded_max_pieces or self.max_pieces - (n - i) < len(collect_next_iteration):
                # Have run out of space, just keep the same pieces without iterating
                collect_next_iteration.append(piece_to_iterate)
                exceeded_max_pieces = True
                iteration_finished = True
            else: 
                was_iterated = piece_to_iterate.iterate(collect_next_iteration)  # returns Boolean, appends to collect_next_iteration
                if was_iterated:
                    iteration_finished = False  # keep going until no piece iterates any further
        if exceeded_max_pieces:
            print("Warning - max pieces exceeded")
        self.iterated_pieces = collect_next_iteration
        return iteration_finished

    def final_size(self):
        return len(self.iterated_pieces)

    def plot(self, drawing):
        if callable(self.piece_sorter):
            self.iterated_pieces.sort(key=self.piece_sorter)
        for piece_to_plot in self.iterated_pieces:
            piece_to_plot.plot(drawing)

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
