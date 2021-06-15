from constants import DRAWING_SIZE, BLACK, BLUE, RED, GREEN, YELLOW, CYAN, MAGENTA
from Vector2D import Vector2D
from Matrix2D import Matrix2D
from FractalPiece2D import FractalPiece2D
from FractalSystem2D import FractalSystem2D


def fractalRunner(drawing):

    # Use this file to set up a FractalSystem2D
    # which contains a list of FractalDefn2D (linked fractals)
    # which each contain a list of FractalPiece2D (controlling next iteration)
    # as well as a FractalPlotter2D to control how each fractal definition is drawn

    # Number of fractal definition slots set up
    number_of_defns = 10  # Total number of fractal definitions in the linked fractal system

    # Iteration control parameters
    max_iterations = 8  # Maximum iterations
    min_radius = 20  # px, smallest iteration allowed
    max_pieces = 10000  # Stop iterating after this number of fractal pieces calculated

    # Set up which fractal is drawn, and its position and orientation
    margin_factor = 0.95  # if less than 1, leaves a small gap around the outside of canvas
    init_defn_id = 2  # between 0 and number_of_defns - 1
    init_vect = Vector2D(1, 1) * (DRAWING_SIZE / 2)
    init_mx = Matrix2D(1, 0, 0, 1) * (DRAWING_SIZE / 2) * margin_factor

    # Set up linked fractal system
    fs = FractalSystem2D(max_iterations, min_radius, max_pieces)
    fs.make_defns(number_of_defns)

    # --------------------

    # Set up 0th definition - Sierpinski sieve, with lines
    fd0 = fs.defns[0]
    fd0.add_child(FractalPiece2D(0, Vector2D(-0.5, 0.5), Matrix2D.sq(1) * 0.5))
    fd0.add_child(FractalPiece2D(0, Vector2D(-0.5, -0.5), Matrix2D.sq(1) * 0.5))
    fd0.add_child(FractalPiece2D(0, Vector2D(0.5, -0.5), Matrix2D.sq(1) * 0.5))
    fd0.relative_size = 1  # fractal definition occupies area [-1, 1] x [-1, 1]
    # Set up 0th plotter
    fp0 = fd0.plotter
    fp0.draw = True
    fp0.colours = [BLACK, RED, YELLOW, BLACK, GREEN, BLUE, BLACK]
    fp0.alpha = 1
    fp0.hand_wobble_px = 5
    fp0.add_path_vectors([Vector2D(-1, 0), Vector2D(-1, -1), Vector2D(1, -1), Vector2D(-1, 1)])
    fp0.path_close = True
    fp0.path_expand_factor = 1.2
    fp0.path_width = 2

    # Set up 1st definition - square fractal, with dots
    fd1 = fs.defns[1]
    fd1.add_child(FractalPiece2D(1, Vector2D(-1, 1), Matrix2D.sq(1) * 0.5))
    fd1.add_child(FractalPiece2D(1, Vector2D(-1, -1), Matrix2D.sq(1) * 0.5))
    fd1.add_child(FractalPiece2D(1, Vector2D(1, -1), Matrix2D.sq(2) * 0.5))
    fd1.relative_size = 2  # fractal definition occupies area [-2, 2] x [-2, 2]
    # Set up 1st plotter
    fp1 = fd1.plotter
    fp1.draw = True
    fp1.colours = [BLACK, CYAN, MAGENTA, YELLOW]
    fp1.hand_wobble_px = 4
    fp1.dot_expand_factor = 2.5

    # Set up 2nd definition - a wrapper to draw definitions 0 and 1
    fd2 = fs.defns[2]
    fd2.add_child(FractalPiece2D(0, Vector2D(0, 0), Matrix2D.sq(1)))
    fd2.add_child(FractalPiece2D(1, Vector2D(0.5, 0.5), Matrix2D.rotd(-10) * 0.19))
    # Set up 2nd plotter
    fd2.plotter.draw = False

    # --------------------

    # Provide a little output
    print("")
    print("Fractal System:")
    print(fs)
    print("")

    # Calculate the iterations
    init_fractal_piece = FractalPiece2D(init_defn_id, init_vect, init_mx)
    init_fractal_piece_list = [init_fractal_piece]
    iterated_fractal_piece_list = fs.iterate(init_fractal_piece_list)
    print(f"After iteration, there are {len(iterated_fractal_piece_list)} pieces")
    print("")
    
    # Plot iterations to drawing
    fs.plot(iterated_fractal_piece_list, drawing)
    print("Fractal System plotted successfully")
    print("")

    return drawing
