from FractalPiece import FractalPiece
from FractalSystem import FractalSystem
from constants import DRAWING_SIZE, BLACK, BLUE, LIGHT_BLUE, RED, GREEN, YELLOW, CYAN, MAGENTA, ORANGE, LIGHT_GREEN, SPRING_GREEN, PURPLE, PINK
from numpyHelperFns import mx_angle, vect, mx_id, mx_rotd, mx_sq
from fractalHelperFns import colour_by_log2_size, wobble_square, plot_dot, plot_path, colour_by_progress, colour_by_tsfm,\
    defngen_rand_small_squares, idgen_rand, vectgen_rand, mxgen_rand_sq, mxgen_rand_circ


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
    init_defn_id = 2  # between 0 and number_of_defns - 1
    init_scale = DRAWING_SIZE / 2
    margin_factor = 0.98  # if less than 1, leaves a small gap around the outside of canvas
    init_vect = vect(1, 1) * init_scale
    init_mx = mx_id(2) * (init_scale * margin_factor)
    # This is setup for 2-dimensional fractal

    # Set up linked fractal system
    fs = FractalSystem(max_iterations, min_radius, max_pieces)
    fs.make_defns(number_of_defns)

    # Choose a sort order for final list of fractal pieces, which affects drawing order.
    # Examples:
    # fs.piece_sorter = sort_by_tsfm(lambda vect, mx: -vect[0])  # Draw by x-coord descending, e.g. from right to left
    # fs.piece_sorter = sort_by_size()  # Draw from largest at back, to smallest at front
    # fs.piece_sorter = sort_by_z()  # Draw from furthest back to furthest forward (3D only)
    # fs.piece_sorter = sort_randomly()  # Draw in a random order
    
    # --------------------

    # Definition #0 - empty fractal
    id = 0
    fd = fs.defns[id]
    # no children, iterates to nothing
    fp = fd.plotter
    fp.draws = False  # specify to prevent drawing
    # if it did draw, it would use default plotting function `plot_dot`
    fp.colouring_fn = colour_by_progress([RED])  # if it did draw, it would be a red dot

    # Definition #1 - identity fractal (doesn't change upon iteration)
    id = 1
    fd = fs.defns[id]
    fd.add_child(FractalPiece(id, vect(0, 0), mx_id()))  # this is the identity. Not actually used, since iteration prevented.
    fd.iterates = False  # specify to prevent further calculation of iterations
    fp = fd.plotter
    fp.draws = False
    fp.colouring_fn = colour_by_progress([LIGHT_GREEN])

    # Definition #2 - use as wrapper to display 1 or more other fractals
    id = 2
    fd = fs.defns[id]
    scv = 0.5
    scm = 0.45
    fd.add_child(FractalPiece(3, vect(-1, -1) * scv, mx_id() * scm))
    fd.add_child(FractalPiece(4, vect(1, -1) * scv, mx_id() * scm))
    fd.add_child(FractalPiece(5, vect(-1, 1) * scv, mx_id() * scm * 0.8))
    fd.add_child(FractalPiece(6, vect(1, 1) * scv, mx_id() * scm))
    fd.add_child(FractalPiece(7, vect(-1.2, -0.3) * scv, mx_rotd(30) * 0.4 * scm))
    fd.add_child(FractalPiece(8, vect(-0.3, -0.5) * scv, mx_id() * 0.45 * scm))
    # keep default plotting setup, this definition likely won't plot
    # since it iterates to other things

    # Definition #3 - demo Sierpinski Sieve
    id = 3
    fd = fs.defns[id]
    sc = 0.5
    fd.add_child(FractalPiece(id, vect(-1, -1) * sc, mx_id() * sc))
    fd.add_child(FractalPiece(id, vect(-1, 1) * sc, mx_id() * sc))
    fd.add_child(FractalPiece(id, vect(1, -1) * sc, mx_sq(1) * sc))
    fd.relative_size = 1  # this controls size vs min_radius during calculation; fractal occupies [-1, 1] x [-1, 1] so "radius" = 1
    fd.iterates = True  # this is default value, so this line is optional
    # Set up plotter
    fp = fd.plotter
    x_minus_y = lambda vect, mx: vect[0] - vect[1]
    fp.colouring_fn = colour_by_tsfm(-150, 150, x_minus_y, [RED, BLACK])
    fp.plotting_fn = plot_path(closed=True, vector_list=[vect(-1, 1), vect(-1, -1), vect(1, -1)])

    # Definition #4 - demo of random square matrix transformations
    id = 4
    fd = fs.defns[id]
    sc = 0.5
    fd.add_child(FractalPiece(id, vect(-1, -1) * sc, mx_id() * sc))
    fd.add_child(FractalPiece(id, vect(1, -1) * sc, mx_id() * sc))
    fd.add_child(FractalPiece(id, vect(-1, 1) * sc, mxgen_rand_sq(sc ** 1.3)))
    fd.add_child(FractalPiece(id, vect(1, 1) * sc, mxgen_rand_sq(sc ** 1.7)))
    # Set up plotter
    fp = fd.plotter
    fp.colouring_fn = colour_by_log2_size(2, 3, [GREEN, BLUE])
    fp.plotting_fn = plot_path(
        closed=True,
        width=2,
        expand_factor=1.1,
        wobble_fn=wobble_square(pixels=3),
        vector_list=[vect(-1, 0), vect(-1, -1), vect(1, -1), vect(1, 0), vect(0, 1)]
    )

    # Definition #5 - demo of random hexagon dot fractal
    id_exit = 1
    id_iterate = 5
    fd = fs.defns[id_iterate]
    sc = 1/3
    h = 3 ** 0.5
    id_list = [id_exit, id_iterate, id_iterate, id_iterate, id_iterate]
    id_callback = idgen_rand(id_list)
    mx_callback = mxgen_rand_circ(sc)
    fd.add_child(FractalPiece(id_callback, vect(2, 0) * sc, mx_callback))
    fd.add_child(FractalPiece(id_callback, vect(1, h) * sc, mx_callback))
    fd.add_child(FractalPiece(id_callback, vect(-1, h) * sc, mx_callback))
    fd.add_child(FractalPiece(id_callback, vect(-2, 0) * sc, mx_callback))
    fd.add_child(FractalPiece(id_callback, vect(-1, -h) * sc, mx_callback))
    fd.add_child(FractalPiece(id_callback, vect(1, -h) * sc, mx_callback))
    fd.add_child(FractalPiece(id_callback, vect(0, 0) * sc, mx_callback))
    # Set up plotter
    fp = fd.plotter
    fp.colouring_fn = colour_by_progress([BLACK, PINK, LIGHT_BLUE, GREEN, YELLOW, BLACK])
    fp.plotting_fn = plot_dot(expand_factor=0.65)  # make dots distinct

    # Definition #6 - demo of random vector shift
    id = 6
    fd = fs.defns[id]
    sc = 0.5
    fd.add_child(FractalPiece(id, vect(-1, -1) * sc, mx_id() * sc))
    fd.add_child(FractalPiece(id, vect(1, -1) * sc, mx_id() * sc))
    fd.add_child(FractalPiece(id, vectgen_rand([-sc, sc], [sc, sc]), mx_id() * sc))
    # Set up plotter
    fp = fd.plotter
    distance_from_700_700 = lambda vect, mx: ((vect[0]-700) ** 2 + (vect[1]-700) ** 2) ** 0.5
    fp.colouring_fn = colour_by_tsfm(50, 250, distance_from_700_700, [MAGENTA, YELLOW, CYAN])
    fp.plotting_fn = plot_dot(expand_factor=1.5, wobble_fn=wobble_square(pixels=5))  # make dots overlap

    # Definition #7 - Dragon curve
    id = 7
    fd = fs.defns[id]
    sc = 0.5 ** 0.5
    fd.add_child(FractalPiece(id, vect(-0.5, 0.5), mx_rotd(-45) * sc))
    fd.add_child(FractalPiece(id, vect(0.5, 0.5), mx_rotd(-135) * sc))
    # Set up plotter
    fp = fd.plotter
    piece_angle = lambda vect, mx: mx_angle(mx)
    fp.colouring_fn = colour_by_tsfm(-90, 270, piece_angle, [RED, YELLOW, GREEN, BLUE])
    fp.plotting_fn = plot_path(width=3, vector_list=[vect(-1, 0), vect(1, 0)])

    # Definition #8 - Random Sierpinski Carpet - 7 out of 9 little squares, in 3x3 big square
    idr = 8
    fd = fs.defns[idr]
    fd.children = defngen_rand_small_squares(id=idr, m=7, n=3)  # Definition children is dynamically calculated by callback
    fp = fd.plotter
    distance_from_origin = lambda vect, mx: ((vect[0]) ** 2 + (vect[1]) ** 2) ** 0.5
    fp.colouring_fn = colour_by_tsfm(450, 700, distance_from_origin, [BLACK, RED, BLUE])
    fp.plotting_fn = plot_path(closed=True, width=1, expand_factor=0.8, vector_list=[vect(-1, 1), vect(-1, -1), vect(1, -1), vect(1, 0), vect(0, 0)])

    # --------------------

    # Provide a little output
    print("")
    print("Fractal System:")
    print(fs)
    print("")

    # Calculate the iterations
    fs.initial_pieces = [FractalPiece(init_defn_id, init_vect, init_mx)]
    fs.do_iterations()
    print(f"After iteration, there are {fs.final_size()} pieces")
    print("")

    # Plot iterations to drawing
    fs.plot(drawing)
    print("Fractal System plotted successfully")
    print("")

    return drawing
