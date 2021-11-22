from fractal_defn import FractalDefn
from fractal_constants import DEFAULT_MAX_PIECES, DEFAULT_MAX_DEFNS, BREAK_AFTER_ITERATIONS
from fractal_constants import DEFAULT_HULL_MAX_ITERATIONS, DEFAULT_INITIAL_HULL
from fractal_helper_fns import DEFAULT_METRIC_FN, DEFAULT_ITERATION_FN


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
        self.verbose = True  # Set to false to suppress printing output to console

    def lookup_defn(self, fid):
        if isinstance(fid, int) and fid >= 0 and fid < len(self.defns):
            return self.defns[fid]
        else:
            # If fractal id (fid) is not found, fail gracefully by returning None.
            # Should check for None and only take further action if a definition is returned.
            return None

    def add_defn(self, fractal_defn):
        self.defns.append(fractal_defn)
        fractal_defn.system = self  # Force definition to link back to this system
        return self

    def make_defns(self, n):
        if isinstance(n, int) and n > 0 and n <= self.max_defns:
            self.defns = []
            for fid in range(n):
                self.add_defn(FractalDefn(system=self, fid=fid))
        return self

    def log(self, text):
        if self.verbose:
            print(text)

    def calculate_hulls(self, max_iterations=DEFAULT_HULL_MAX_ITERATIONS, hull_accuracy=None, initial_hull=DEFAULT_INITIAL_HULL):
        # 1. Initialise hulls on all definitions
        self.log("")
        self.log("Initialising convex hull calculations")
        for defn in self.defns:
            defn.initialise_hull(hull_accuracy=hull_accuracy, initial_hull=initial_hull)
        # 2. Iteratively calculate all hulls in parallel (necessary since they interact)
        self.log("")
        self.log("Calculating convex hulls")
        for i in range(max_iterations):
            for defn in self.defns:
                defn.iterate_hull(iteration=i)
            self.log(f"- hulls iteration {i + 1}")
        self.log("")
        self.log("Calculating definition minimum diameters")
        for defn in self.defns:
            defn.calculate_diameter()

    def do_iterations(self):
        self.log("")
        self.log(f"Calculating fractal iterations")
        self.iterated_pieces = self.initial_pieces
        iteration_finished = False
        counter = 0
        while not iteration_finished:
            counter += 1
            self.log(f"- iteration {counter} on {len(self.iterated_pieces)} piece{'' if len(self.iterated_pieces) == 1 else 's'}")
            iteration_finished = self.iterate_once()
            if BREAK_AFTER_ITERATIONS <= counter:
                self.log(f"Forced break after {counter} iterations")
                break
        self.log("")

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
            self.log("Warning - max pieces exceeded")
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
        defn_fid = 0
        for defn in self.defns:
            if first:
                first = False
            else:
                result += ", "
            result += f"(Fractal ID {defn_fid} contains {defn})"
            defn_fid += 1
        return result
