from constants import DRAWING_SIZE, BLACK, BLUE, RED, GREEN, YELLOW, CYAN, MAGENTA
from helperFns import interpolate_colour
from Pos import Pos
from Vector2D import Vector2D
from Matrix2D import Matrix2D
from FractalPiece2D import FractalPiece2D
from FractalDefn2D import FractalDefn2D
from FractalSystem2D import FractalSystem2D


def fractalRunner(drawing):

    # Use this file to set up a FractalSystem2D
    # which contains a list of FractalDefn2D (linked fractals)
    # which each contain a list of FractalPiece2D (controlling next iteration)

    # Set up whatever control parameters are required
    init_id = 0
    min_radius = 26
    max_iterations = 8
    circle_colours = [\
        [BLUE, CYAN],\
        [RED, MAGENTA],\
        [GREEN, YELLOW]]
    circle_radius_factor = 0.5 ** 0.5  # just touching
    # circle_radius_factor = 1 # overlapping

    # Initialisation of fractal
    sc = DRAWING_SIZE / 2  # main scale
    init_fractal_piece = FractalPiece2D(init_id, Vector2D(1, 1) * sc, Matrix2D(1, 0, 0, 1) * sc)

    # Set up linked fractal system
    fs = FractalSystem2D()
    fs.add_n_defns(3)

    fs.add_child(0, FractalPiece2D(0, Vector2D(-1, -1) * 0.5, Matrix2D(1, 0, 0, 1) * 0.5))
    fs.add_child(0, FractalPiece2D(1, Vector2D(-1, 1) * 0.5, Matrix2D(0, 1, -1, 0) * 0.5))
    fs.add_child(0, FractalPiece2D(2, Vector2D(1, -1) * 0.5, Matrix2D(1, 0, 0, 1) * 0.5))

    fs.add_child(1, FractalPiece2D(0, Vector2D(-1, -1) * 0.5, Matrix2D(1, 0, 0, 1) * 0.5))
    fs.add_child(1, FractalPiece2D(0, Vector2D(-1, 1) * 0.5, Matrix2D(1, 0, 0, 1) * 0.5))
    fs.add_child(1, FractalPiece2D(0, Vector2D(1, -1) * 0.5, Matrix2D(1, 0, 0, 1) * 0.5))

    fs.add_child(2, FractalPiece2D(0, Vector2D(-3, -1) * 0.25, Matrix2D(1, 0, 0, 1) * 0.25))
    fs.add_child(2, FractalPiece2D(0, Vector2D(1, -1) * 0.25, Matrix2D(-1, 0, 0, 1) * 0.75))

    # Calculate the iterations here using the system
    main_iterations = fs.iterate(init_fractal_piece, max_iterations, min_radius)

    # Smoke test via console print
    print("")
    print("Fractal System:")
    print(fs)
    print("")
    
    # Turn main_iterations into a list of Pos
    # and print to drawing using any relevant options
    main_size = len(main_iterations)
    if main_size > 0:
        progress_factor = 1 / (main_size - 1)
        progress_counter = 0
        for piece in main_iterations:
            progress = progress_factor * progress_counter
            pos = Pos(piece.vect.x, DRAWING_SIZE - piece.vect.y)
            circle_radius = circle_radius_factor * piece.radius()
            circle_colour_start = circle_colours[piece.id % len(circle_colours)][0]
            circle_colour_end = circle_colours[piece.id % len(circle_colours)][1]
            circle_colour = interpolate_colour(circle_colour_start, circle_colour_end, progress)
            drawing.add_point(pos, circle_colour, circle_radius)
            progress_counter += 1

    return drawing
