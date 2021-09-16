import numpy as np
import random
from FractalPiece import FractalPiece
from FractalSystem import FractalSystem
from constants import DRAWING_SIZE, WHITE, LIGHT_GREY, GREY, DARK_GREY, BLACK, RED, ORANGE, YELLOW, LIGHT_GREEN, GREEN, SPRING_GREEN, CYAN, LIGHT_BLUE, BLUE, PURPLE, MAGENTA, PINK
from numpyHelperFns import vect, vect_len, mx_angle, mx_id, mx_scale, mx_diag, mx_rotd, mx_sq
from fractalHelperFns import colour_fixed, colour_by_progress, colour_by_tsfm, colour_by_log2_size
from fractalHelperFns import plot_dot, plot_path, plot_hull_outline, plot_hull_filled
from fractalHelperFns import sort_by_tsfm, grid_generator, wobble_square
from fractalHelperFns import get_iteration_fn_standard, get_iteration_fn_stop
from fractalGeneratorFns import gen_children_rand_small_squares, gen_children_fade_out, gen_id_rand
from fractalGeneratorFns import gen_vect_rand, gen_mx_rand_sq, gen_mx_rand_circ

def fractalRunner(drawing):

    # Use this file to set up a FractalSystem
    # which contains a list of FractalDefn (linked fractals)
    # which each contain a list of FractalPiece (controlling next iteration)
    # as well as a FractalPlotter to control how each fractal definition is drawn

    # Set up fractal system
    max_iterations = 20  # Maximum iterations
    min_diameter = 15  # px, fractal pieces will stop iterating if they are smaller than this diameter on at least 1 direction
    max_pieces = 100000  # Stop iterating after this number of fractal pieces calculated
    number_of_defns = 50  # Total number of fractal definitions in the linked fractal system

    # Set up which fractal is drawn, and its position and orientation
    init_defn_id = 2  # between 0 and number_of_defns-1
    init_scale = DRAWING_SIZE / 2
    margin_factor = 0.98  # if less than 1, leaves a small gap around the outside of canvas
    init_vect = vect(
        x = 1,
        y = 1,
        scale = init_scale
    )
    init_mx = mx_scale(
        dim = 2,
        scale = init_scale * margin_factor
    )
    # This is setup for 2-dimensional fractal

    # Create linked fractal system
    fs = FractalSystem(max_pieces=max_pieces)
    # Function to control when pieces stop iterating
    fs.iteration_fn = get_iteration_fn_standard(min_diameter=min_diameter, max_iterations=max_iterations)
    # Create the required number of fractal definitions
    fs.make_defns(number_of_defns)

    # Choose a sort order for final list of fractal pieces, which affects drawing order.
    # Examples:
    # fs.piece_sorter = sort_randomly()  # Draw in a random order
    sort_len = 100
    sort_pow = 4
    sort_vect = init_vect
    fs.piece_sorter = sort_by_tsfm(tsfm=lambda vect, mx: vect_len(vect=vect-sort_vect, power=sort_pow)/sort_len, rand=True)  # Draw by distance from sort_vect, with sort_len pixel random boundary
    # fs.piece_sorter = sort_by_z()  # Draw from furthest back to furthest forward (3D only)
    # fs.piece_sorter = sort_by_size()  # Draw from largest at back, to smallest at front

    # In order to recreate a given fractal precisely, any randomness it contains must be generated from a fixed random seed.
    # Enable/disable this section to turn seeding on or off.
    random_seed = "My fractal 002"  # Try incrementing this number! Controls the fractal via which randomness it uses.
    random.seed(random_seed)  # Comment this out if you don't want to control the seeding
    
    # --------------------

    # Definition #0 - empty fractal
    id = 0
    fd = fs.lookup_defn(id)
    # no children, iterates to nothing
    fp = fd.plotter
    fp.draws = False  # specify to prevent drawing
    # if it did draw, it would use default plotting function `plot_dot`
    fp.colouring_fn = colour_by_progress(colours=[RED])  # if it did draw, it would be a red dot

    # Definition #1 - identity fractal (doesn't change upon iteration)
    id = 1
    fd = fs.lookup_defn(id)
    fd.create_child(id, vect(0, 0), mx_id())  # this is the identity. Not actually used, since iteration prevented.
    fd.iteration_fn = get_iteration_fn_stop()  # specify to prevent further calculation of iterations
    fp = fd.plotter
    fp.draws = False  # In this demo, defn id=1 is used, but not drawn. You can show it if you want.
    fp.colouring_fn = colour_by_progress(colours=[LIGHT_GREEN])

    # Definition #2 - use as wrapper to display 1 or more other fractals
    # Since this is a wrapper, reset the progress on each inner fractal
    # to reset things like colouring schemes
    id = 2
    fd = fs.lookup_defn(id)
    scv = 0.5
    scm = 0.45
    fd.create_child(3, vect(-1, -1) * scv, mx_scale(scm), reset_progress=True)
    fd.create_child(4, vect(1, -1) * scv, mx_scale(scm), reset_progress=True)
    fd.create_child(5, vect(-0.8, 1) * scv, mx_scale(scm * 0.8), reset_progress=True)
    fd.create_child(6, vect(-0.4, -0.6) * scv, mx_scale(0.45 * scm), reset_progress=True)
    fd.create_child(7, vect(-1.5, 1.6) * scv, mx_rotd(angle=-60, scale=0.35 * scm), reset_progress=True)
    fd.create_child(8, vect(1, 1) * scv, mx_scale(scm), reset_progress=True)
    fd.create_child(9, vect(-1, 0.2) * scv, mx_rotd(angle=20, scale=scm * 1.15) @ np.array(((1, 0), (0, -1))), reset_progress=True)
    # keep default plotting setup, this definition likely won't plot
    # since it iterates to other things

    # Definition #3 - demo Sierpinski Sieve
    id = 3
    fd = fs.lookup_defn(id)
    n = 2
    sc = 1/n
    grid = grid_generator(x_steps=n, y_steps=n)  # Defaults from -1 to +1 in both x and y directions
    # Grid generator generates coordinates at square midpoints from -1 to 1, total steps 2
    # grid(0, 0) = (-0.5, -0.5)
    # grid(1, 0) = (0.5, -0.5)
    # etc
    fd.create_child(id, grid(0, 0), mx_id() * sc)  # Same scale matrix result, three ways of writing
    fd.create_child(id, grid(0, 1), mx_scale(sc))
    fd.create_child(id, grid(1, 0), mx_sq(num=1, scale=sc))

    # Showing here a manual assignment of relative diameter to fractal definition.
    # This is redundant since 2 is the default value, but larger or smaller values will affect drawing and iteration.
    # Min diameter 2 means in some orientation the defn fits between planes 2 units apart, for a piece with identity transformation (vect(0, 0), mx_id())
    fd.relative_diameter = 2
    fd.iteration_fn = get_iteration_fn_standard(min_diameter=10, max_iterations=5)
    
    fp = fd.plotter
    x_minus_y = lambda vect, mx: vect[0] - vect[1]
    fp.colouring_fn = colour_by_tsfm(-150, 150, tsfm=x_minus_y, colours=[RED, BLACK])

    # # Plot method 1: set the corner points manually, plot a path
    # fp.plotting_fn = plot_path(closed=True, vector_list=[vect(-1, 1), vect(-1, -1), vect(1, -1)])
    # # Plot method 2: outline using convex hull, must call fs.calculate_hulls after definitions complete
    # fp.plotting_fn = plot_hull_outline(width=1.5, expand_factor=1.00)
    # Plot method 3: fill using convex hull, must call fs.calculate_hulls
    fp.plotting_fn = plot_hull_filled(width=1, expand_factor=1.00)

    # Definition #4 - demo of random square matrix transformations
    id = 4
    fd = fs.lookup_defn(id)
    n = 2
    sc = 1/n
    grid = grid_generator(x_steps=n, y_steps=n)
    fd.create_child(id, grid(0, 0), mx_scale(sc))
    fd.create_child(id, grid(1, 0), mx_scale(sc))
    fd.create_child(id, grid(0, 1), gen_mx_rand_sq(scale=sc**1.3))
    fd.create_child(id, grid(1, 1), gen_mx_rand_sq(scale=sc**1.7))
    fp = fd.plotter
    fp.colouring_fn = colour_by_log2_size(0, 4, colours=[GREEN, BLUE])
    fp.plotting_fn = plot_path(
        closed=True,
        width=2,
        expand_factor=1.1,
        wobble_fn=wobble_square(pixels=3),
        vector_list=[vect(-1, 0), vect(-1, -1), vect(1, -1), vect(1, 0), vect(0, 1)],
        curved=True
    )
    # fp.plotting_fn = plot_hull_filled()  # Alternative plot method, using defaults

    # Definition #5 - demo of random hexagon fractal
    id_exit = 1
    id_iterate = 5
    fd = fs.lookup_defn(id_iterate)
    sc = 1/3
    h = 3 ** 0.5
    id_list = [id_exit, id_iterate, id_iterate, id_iterate, id_iterate]
    id_fn = gen_id_rand(id_list)
    mx_fn = gen_mx_rand_circ(sc)
    fd.create_child(id_fn, vect(2, 0) * sc, mx_fn)
    fd.create_child(id_fn, vect(1, h) * sc, mx_fn)
    fd.create_child(id_fn, vect(-1, h) * sc, mx_fn)
    fd.create_child(id_fn, vect(-2, 0) * sc, mx_fn)
    fd.create_child(id_fn, vect(-1, -h) * sc, mx_fn)
    fd.create_child(id_fn, vect(1, -h) * sc, mx_fn)
    fd.create_child(id_fn, vect(0, 0) * sc, mx_fn)
    fp = fd.plotter
    fp.colouring_fn = colour_by_progress(colours=[BLACK, PINK, LIGHT_BLUE, GREEN, YELLOW, BLACK])
    # fp.plotting_fn = plot_dot(expand_factor=0.5)  # expand_factor < 1 makes dots distinct
    # fp.plotting_fn = plot_hull_outline(width=1.5, expand_factor=0.5)  # alternative plotting method
    fp.plotting_fn = plot_hull_filled(expand_factor=0.5)

    # Definition #6 - demo of random vector shift
    id = 6
    fd = fs.lookup_defn(id)
    sc = 0.5
    fd.create_child(id, vect(-1, -1) * sc, mx_scale(sc))  # Two versions of same scale matrix here
    fd.create_child(id, vect(1, -1) * sc, mx_diag(sc, sc))
    fd.create_child(id, gen_vect_rand([-sc, sc], [sc, sc]), mx_scale(sc))
    fp = fd.plotter
    distance_from_origin = lambda vect, mx: ((vect[0]) ** 2 + (vect[1]) ** 2) ** 0.5
    fp.colouring_fn = colour_by_tsfm(500, 580, tsfm=distance_from_origin, colours=[PURPLE, YELLOW, PINK])
    fp.plotting_fn = plot_dot(expand_factor=1.5, wobble_fn=wobble_square(pixels=5))  # make dots overlap

    # Definition #7 - Standard (2D) dragon curve
    id = 7
    fd = fs.lookup_defn(id)
    sc = 0.5 ** 0.5
    fd.create_child(id, vect(-0.5, 0.5), mx_rotd(angle=-45, scale=sc))
    fd.create_child(id, vect(0.5, 0.5), mx_rotd(angle=-135, scale=sc))
    fp = fd.plotter
    piece_angle = lambda vect, mx: mx_angle(mx)
    fp.colouring_fn = colour_by_tsfm(-90, 270, tsfm=piece_angle, colours=[RED, YELLOW, GREEN, BLUE])
    fp.plotting_fn = plot_path(width=3, vector_list=[vect(-1, 0), vect(1, 0)])

    # Definition #8 - Random Sierpinski Carpet
    # gen_children_rand_small_squares - 7 out of 9 little squares, in 3x3 big square
    # gen_children_fade_out - Iterate with a probability depending on how far fractal piece is from a specified point
    idr = 8
    fd = fs.lookup_defn(idr)
    # fd.children = gen_children_rand_small_squares(system=fs, id=idr, m=7, n=3)  # Definition children is dynamically calculated by callback
    fd.children = gen_children_fade_out(system=fs, id=idr, n=3, centre_vect=vect(750, 750), cutoff_diameter=50, d1=75, d2=225, p1=1, p2=0)
    fp = fd.plotter
    x, y = 650, 650
    distance_from_pt = lambda vect, mx: ((vect[0]-x) ** 2 + (vect[1]-y) ** 2) ** 0.5
    fp.colouring_fn = colour_by_tsfm(50, 350, tsfm=distance_from_pt, colours=[MAGENTA, YELLOW, CYAN])
    fp.plotting_fn = plot_path(closed=True, width=2, expand_factor=0.8, vector_list=[vect(-1, 1), vect(-1, -1), vect(1, -1), vect(1, 0), vect(0, 0)])

    # Definition #9 - Modified dragon curve with fractal dimension varying from 1 to 2, from one end to the other
    def gen_children_variable_dragon(system, id):
        def calc_children(context_piece=None):
            progress = 1
            if context_piece is not None:
                progress = context_piece.get_progress_value()
            x = 0
            y = progress
            x1 = 0.5*(-1+x)
            x2 = 0.5*(1+x)
            y1 = 0.5 * y
            y2 = 0.5 * y
            piece1 = FractalPiece(system=system, id=id, vect=vect(x1, y1), mx=np.array(((x-x1, y1-y), (y-y1, x-x1))))
            piece2 = FractalPiece(system=system, id=id, vect=vect(x2, y2), mx=np.array(((x-x2, y2-y), (y-y2, x-x2))))
            piece2.reverse_progress = True  # Needed to get linear colouring and iteration! Try removing it...
            children = [piece1, piece2]
            return children
        return calc_children
    id = 9
    fd = fs.lookup_defn(id)
    sc = 0.5 ** 0.5
    fd.children = gen_children_variable_dragon(fs, id)
    fd.iteration_fn = get_iteration_fn_standard(min_diameter=20, max_iterations=20)
    fp = fd.plotter
    fp.colouring_fn = colour_by_progress([BLUE, RED, ORANGE])
    # fp.colouring_fn = colour_fixed(CYAN, alpha=0.75) # Alternative fixed colouring method
    fp.plotting_fn = plot_path(width=2, vector_list=[vect(-1, 0), vect(1, 0)])
    # fp.plotting_fn = plot_path(width=1, closed=True, vector_list=[vect(-1, 0), vect(0, -1), vect(1, 0), vect(0, 1)])  # Alternative plot method
    
    # --------------------

    # TODO: Convex Hulls only currently works for 2D. Can it work for 3D too?
    # Calculate Convex Hulls after fractal definitions completed
    # Need to do this if plot_hull_outline method used, can comment out this section otherwise
    fs.calculate_hulls(hull_accuracy=0.1, max_iterations=10)

    # --------------------

    # # Examine the fractal system setup
    # fs.log("")
    # fs.log("Fractal System:")
    # fs.log(fs)
    # fs.log("")

    # Calculate the iterations
    initial_piece = FractalPiece(system=fs, id=init_defn_id, vect=init_vect, mx=init_mx)
    fs.initial_pieces = [initial_piece]
    fs.do_iterations()
    fs.log(f"After iteration, there are {fs.final_size()} pieces")
    fs.log("")

    # Plot iterations to drawing
    fs.plot(drawing)
    fs.log("Fractal System plotted successfully")
    fs.log("")

    return drawing
