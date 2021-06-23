import numpy as np

from FractalPiece import FractalPiece
from FractalSystem import FractalSystem
from fractalHelperFns import rand_id, rand_mx_square, rand_mx_triangle, rand_mx_dihedral, rand_mx_rotation, rand_mx_circle, rand_vect_cts
from constants import DRAWING_SIZE, BLACK, BLUE, LIGHT_BLUE, RED, GREEN, YELLOW, CYAN, MAGENTA, ORANGE, LIGHT_GREEN, SPRING_GREEN, PURPLE, PINK


def fractalRunner(drawing):

    # Use this file to set up a FractalSystem
    # which contains a list of FractalDefn (linked fractals)
    # which each contain a list of FractalPiece (controlling next iteration)
    # as well as a FractalPlotter to control how each fractal definition is drawn

    # Number of fractal definition slots set up
    number_of_defns = 10  # Total number of fractal definitions in the linked fractal system

    # Iteration control parameters
    max_iterations = 10  # Maximum iterations
    min_radius = 10  # px, smallest iteration allowed
    max_pieces = 100000  # Stop iterating after this number of fractal pieces calculated

    # Set up which fractal is drawn, and its position and orientation
    margin_factor = 0.98  # if less than 1, leaves a small gap around the outside of canvas
    init_defn_id = 2  # between 0 and number_of_defns - 1
    init_vect = Vector2D(1, 1) * (DRAWING_SIZE / 2)
    init_mx = Matrix2D(1, 0, 0, 1) * (DRAWING_SIZE / 2) * margin_factor

    # Set up linked fractal system
    fs = FractalSystem(max_iterations, min_radius, max_pieces)
    fs.make_defns(number_of_defns)

    # --------------------

    # Definition #0 - iterates to nothing
    fd0 = fs.defns[0]
    # no children
    fp0 = fd0.plotter
    fp0.draw = False
    fp0.colours = [RED]

    # Definition #1 - iterates to itself
    fd1 = fs.defns[1]
    fd1.add_child(FractalPiece(1, Vector2D(), Matrix2D()))
    fd1.iterate = False
    fp1 = fd1.plotter
    fp1.colours = [LIGHT_GREEN]
    fp1.draw = False

    # Definition #2 - use as wrapper to display 1 or more other fractals
    fd2 = fs.defns[2]
    scv = 0.5
    scm = 0.45
    fd2.add_child(FractalPiece(3, Vector2D(-1, -1) * scv, Matrix2D() * scm))
    fd2.add_child(FractalPiece(4, Vector2D(1, -1) * scv, Matrix2D() * scm))
    fd2.add_child(FractalPiece(5, Vector2D(-1, 1) * scv, Matrix2D() * scm))
    fd2.add_child(FractalPiece(6, Vector2D(1, 1) * scv, Matrix2D() * scm))
    fd2.add_child(FractalPiece(7, Vector2D(-0.5, -0.8) * scv, Matrix2D.rotd(30) * 0.5 * scm))

    # Definition #3 - demo Sierpinski Sieve
    fd3 = fs.defns[3]
    sc = 0.5
    fd3.add_child(FractalPiece(3, Vector2D(-1, 1) * sc, Matrix2D() * sc))
    fd3.add_child(FractalPiece(3, Vector2D(-1, -1) * sc, Matrix2D() * sc))
    fd3.add_child(FractalPiece(3, Vector2D(1, -1) * sc, Matrix2D() * sc))
    fd3.relative_size = 1  # occupies [-1, 1] x [-1, 1] so "radius" = 1
    fd3.iterate = True
    # Set up plotter
    fp3 = fd3.plotter
    fp3.colours = [BLACK, ORANGE, ORANGE, ORANGE, ORANGE]
    fp3.add_path_vectors([Vector2D(-1, 1), Vector2D(-1, -1), Vector2D(1, -1)])
    fp3.path_close = True

    # Definition #4 - demo of random square matrix transformations
    fd4 = fs.defns[4]
    sc = 0.5
    fd4.add_child(FractalPiece(4, Vector2D(-1, -1) * sc, Matrix2D() * sc))
    fd4.add_child(FractalPiece(4, Vector2D(1, -1) * sc, Matrix2D() * sc))
    fd4.add_child(FractalPiece(4, Vector2D(-1, 1) * sc, rand_mx_square(sc ** 1.3)))
    fd4.add_child(FractalPiece(4, Vector2D(1, 1) * sc, rand_mx_square(sc ** 1.7)))
    # Set up plotter
    fp4 = fd4.plotter
    fp4.colours = [BLACK, BLACK, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE]
    fp4.hand_wobble_px = 2
    fp4.add_path_vectors([Vector2D(-1, 0), Vector2D(-1, -1), Vector2D(1, -1), Vector2D(1, 0), Vector2D(0, 1)])
    fp4.path_close = True
    fp4.path_expand_factor = 1.1
    fp4.path_width = 2

    # Definition #5 - demo of random hexagon dot fractal
    fd5 = fs.defns[5]
    sc = 1/3
    h = 3 ** 0.5
    id_list = [1, 5, 5, 5, 5]
    fd5.add_child(FractalPiece(rand_id(id_list), Vector2D(2, 0) * sc, rand_mx_circle(sc)))
    fd5.add_child(FractalPiece(rand_id(id_list), Vector2D(1, h) * sc, rand_mx_circle(sc)))
    fd5.add_child(FractalPiece(rand_id(id_list), Vector2D(-1, h) * sc, rand_mx_circle(sc)))
    fd5.add_child(FractalPiece(rand_id(id_list), Vector2D(-2, 0) * sc, rand_mx_circle(sc)))
    fd5.add_child(FractalPiece(rand_id(id_list), Vector2D(-1, -h) * sc, rand_mx_circle(sc)))
    fd5.add_child(FractalPiece(rand_id(id_list), Vector2D(1, -h) * sc, rand_mx_circle(sc)))
    fd5.add_child(FractalPiece(rand_id(id_list), Vector2D(0, 0) * sc, rand_mx_circle(sc)))
    # Set up plotter
    fp5 = fd5.plotter
    fp5.colours = [BLACK, BLACK, BLACK, PINK, PINK]

    # Definition #6 - demo of random vector shift
    fd6 = fs.defns[6]
    sc = 0.5
    fd6.add_child(FractalPiece(6, Vector2D(-1, -1) * sc, Matrix2D() * sc))
    fd6.add_child(FractalPiece(6, Vector2D(1, -1) * sc, Matrix2D() * sc))
    fd6.add_child(FractalPiece(6, rand_vect_cts(-sc, sc, sc, sc), Matrix2D() * sc))
    # Set up plotter
    fp6 = fd6.plotter
    fp6.colours = [BLACK, BLACK, BLACK, BLACK, GREEN]
    fp6.dot_expand_factor = 1.5  # make dots overlap

    # Definition #7 - Dragon curve
    fd7 = fs.defns[7]
    sc = 0.5 ** 0.5
    fd7.add_child(FractalPiece(7, Vector2D(-0.5, 0.5), Matrix2D.rotd(-45) * sc))
    fd7.add_child(FractalPiece(7, Vector2D(0.5, 0.5), Matrix2D.rotd(-135) * sc))
    # Set up plotter
    fp7 = fd7.plotter
    fp7.colours = [BLACK, BLACK, BLACK, BLACK, BLACK, RED]
    fp7.add_path_vectors([Vector2D(-1, 0), Vector2D(1, 0)])
    fp7.path_width = 3


    # --------------------

    # Provide a little output
    print("")
    print("Fractal System:")
    print(fs)
    print("")

    # Calculate the iterations
    init_fractal_piece = FractalPiece(init_defn_id, init_vect, init_mx)
    init_fractal_piece_list = [init_fractal_piece]
    iterated_fractal_piece_list = fs.iterate(init_fractal_piece_list)
    print(f"After iteration, there are {len(iterated_fractal_piece_list)} pieces")
    print("")
    
    # Plot iterations to drawing
    fs.plot(iterated_fractal_piece_list, drawing)
    print("Fractal System plotted successfully")
    print("")

    return drawing
