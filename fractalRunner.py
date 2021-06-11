from constants import DRAWING_SIZE, BLACK, BLUE, RED, GREEN, YELLOW, CYAN, MAGENTA
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
    initial_id = 0
    min_radius = 20
    max_iterations = 8
    circle_colour_list = [BLUE, RED, MAGENTA, GREEN, YELLOW]
    circle_radius_factor = 0.5 ** 0.5  # just touching
    # circle_radius_factor = 1 # overlapping

    # Initialisation of fractal
    main_piece = FractalPiece2D()
    main_piece.id = initial_id
    main_piece.vect = Vector2D(DRAWING_SIZE/2, DRAWING_SIZE/2)
    main_piece.mx = Matrix2D(DRAWING_SIZE/2, 0, 0, DRAWING_SIZE/2)

    # Set up linked fractal system
    fract_sys = FractalSystem2D()

    # Add 1, 2 or more definitions to the system
    defn_0 = FractalDefn2D()
    defn_1 = FractalDefn2D()
    defn_2 = FractalDefn2D()
    fract_sys.add_defn(defn_0)
    fract_sys.add_defn(defn_1)
    fract_sys.add_defn(defn_2)
    # optionally set defn.radius_factor
    # for each defn using a suitable formula
    # based on vectors and matrices in each defn
    # which is potentially automatable
    # using convex hulls

    # Set up definition 0
    pc_0_0 = FractalPiece2D()
    pc_0_0.id = 0
    pc_0_0.vect = Vector2D(-1, -1) * 0.5
    pc_0_0.mx = Matrix2D(1, 0, 0, 1) * 0.5
    defn_0.add_child(pc_0_0)

    pc_0_1 = FractalPiece2D()
    pc_0_1.id = 1
    pc_0_1.vect = Vector2D(-1, 1) * 0.5
    pc_0_1.mx = Matrix2D(0, 1, -1, 0) * 0.5
    defn_0.add_child(pc_0_1)

    pc_0_2 = FractalPiece2D()
    pc_0_2.id = 2
    pc_0_2.vect = Vector2D(1, -1) * 0.5
    pc_0_2.mx = Matrix2D(1, 0, 0, 1) * 0.5
    defn_0.add_child(pc_0_2)

    # Set up definition 1
    pc_1_0 = FractalPiece2D()
    pc_1_0.id = 0
    pc_1_0.vect = Vector2D(-1, -1) * 0.5
    pc_1_0.mx = Matrix2D(1, 0, 0, 1) * 0.5
    defn_1.add_child(pc_1_0)

    pc_1_1 = FractalPiece2D()
    pc_1_1.id = 0
    pc_1_1.vect = Vector2D(-1, 1) * 0.5
    pc_1_1.mx = Matrix2D(1, 0, 0, 1) * 0.5
    defn_1.add_child(pc_1_1)

    pc_1_2 = FractalPiece2D()
    pc_1_2.id = 0
    pc_1_2.vect = Vector2D(1, -1) * 0.5
    pc_1_2.mx = Matrix2D(1, 0, 0, 1) * 0.5
    defn_1.add_child(pc_1_2)

    # Set up definition 2
    pc_2_0 = FractalPiece2D()
    pc_2_0.id = 0
    pc_2_0.vect = Vector2D(1, -1) * 0.25
    pc_2_0.mx = Matrix2D(-1, 0, 0, 1) * 0.75
    defn_2.add_child(pc_2_0)

    pc_2_1 = FractalPiece2D()
    pc_2_1.id = 0
    pc_2_1.vect = Vector2D(-1, -1) * 0.75
    pc_2_1.mx = Matrix2D(1, 0, 0, 1) * 0.25
    defn_2.add_child(pc_2_1)

    # Calculate the iterations here using the system
    main_iterations = fract_sys.iterate(main_piece, max_iterations, min_radius)

    # Smoke test via a few console prints
    print("")
    print("")
    print(pc_0_0)
    print("")
    print(defn_0)
    print("")
    print(fract_sys)
    print("")
    print("")
    
    # Turn main_iterations into a list of Pos
    # and print to drawing using any relevant options
    for piece in main_iterations:
        pos = Pos(piece.vect.x, DRAWING_SIZE - piece.vect.y)
        circle_radius = circle_radius_factor * piece.radius()
        circle_colour = circle_colour_list[piece.id % len(circle_colour_list)]
        drawing.add_point(pos, circle_colour, circle_radius)

    return drawing
