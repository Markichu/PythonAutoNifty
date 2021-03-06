import numpy as np
import random

from .fractal_piece import FractalPiece
from .fractal_system import FractalSystem
from .helper_fns import hex_list_to_rgba
from .constants import DRAWING_SIZE, WHITE, LIGHT_GREY, GREY, DARK_GREY, BLACK, RED, ORANGE, YELLOW, LIGHT_GREEN, GREEN, SPRING_GREEN, CYAN, LIGHT_BLUE, BLUE, PURPLE, MAGENTA, PINK
from .numpy_helper_fns import vect, vect_len, mx_angle, mx_id, mx_scale, mx_diag, mx_rotd, mx_sq
from .fractal_helper_fns import colour_fixed, colour_by_progress, colour_by_tsfm, colour_by_log2_size
from .fractal_helper_fns import plot_dot, plot_path
from .fractal_helper_fns import sort_by_tsfm, grid_generator, wobble_square
from .fractal_helper_fns import get_iteration_fn_standard, get_iteration_fn_stop
from .fractal_generator_fns import gen_children_rand_small_squares, gen_children_fade_out, gen_fid_rand
from .fractal_generator_fns import gen_vect_rand, gen_mx_rand_sq, gen_mx_rand_circ


def fractalRunner(drawing):
    # Use this file to set up a FractalSystem
    # which contains a list of FractalDefn (linked fractals)
    # which each contain a list of FractalPiece (controlling next iteration)
    # as well as a FractalPlotter to control how each fractal definition is drawn

    # ----------------------
    # First, create a fractal system and its definitions
    max_pieces = 100000  # Stop iterating after this number of fractal pieces calculated
    number_of_defns = 50  # Total number of fractal definitions in the linked fractal system

    # Create linked fractal system
    fs = FractalSystem(max_pieces=max_pieces)
    # Create the required number of fractal definitions
    fs.make_defns(number_of_defns)

    # ----------------------
    # Then set parameters that are important for how fractal displays

    # Control randomisation by setting a specific seed
    # This allows pseudorandom fractals to be precisely recreated later on
    random_seed = "My fractal 002"  # Any text here, every text will make a different fractal
    random.seed(random_seed)  # Comment this out if you don't want to control the seeding

    # Initialisation of fractal, its fractal id (fid), position (vector), and orientation (matrix)
    init_defn_fid = 2  # between 0 and number_of_defns-1
    margin_factor = 0.98  # if less than 1, leaves a small gap around the outside of canvas
    init_scale = DRAWING_SIZE / 2
    init_vect = vect(
        x=1,
        y=1,
        scale=init_scale
    )
    init_mx = mx_scale(
        dim=2,
        scale=init_scale * margin_factor
    )
    # This is setup for 2-dimensional fractal

    # Choose a sort order for final list of fractal pieces, which affects drawing order.
    # Examples:
    # fs.piece_sorter = sort_randomly()  # Draw in a random order
    sort_len = 100
    sort_pow = 4
    sort_vect = init_vect
    fs.piece_sorter = sort_by_tsfm(tsfm=lambda vect, mx: vect_len(vect=vect - sort_vect, power=sort_pow) / sort_len, rand=True)  # Draw by distance from sort_vect, with sort_len pixel random boundary
    # fs.piece_sorter = sort_by_z()  # Draw from furthest back to furthest forward (3D only)
    # fs.piece_sorter = sort_by_size()  # Draw from largest at back, to smallest at front

    # Control default iteration function in fractal system
    sys_max_iterations = 20  # Maximum iterations
    sys_min_diameter = 30  # px, fractal pieces will stop iterating if they are smaller than this diameter on at least 1 direction

    # --------------------

    # Definition #0 - empty fractal
    fid = 0
    fd = fs.lookup_defn(fid)
    # no children, iterates to nothing
    fp = fd.plotter
    fp.draws = False  # specify to prevent drawing


    # Definition #1 - identity fractal (doesn't change upon iteration)
    fid = 1
    fd = fs.lookup_defn(fid)
    fd.create_child(fid, vect(0, 0), mx_id())  # this is the identity. Not actually used, since iteration prevented.
    fd.iteration_fn = get_iteration_fn_stop()  # specify to prevent further calculation of iterations
    fp = fd.plotter
    fp.draws = False


    # Definition #2 - use as wrapper to display 1 or more other fractals
    # Since this is a wrapper, reset the progress on each inner fractal
    # to reset things like colouring schemes
    fid = 2
    fd = fs.lookup_defn(fid)
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
    fid = 3
    fd = fs.lookup_defn(fid)
    n = 2
    sc = 1 / n
    grid = grid_generator(x_steps=n, y_steps=n)  # Defaults from -1 to +1 in both x and y directions
    # Grid generator generates coordinates at square midpoints from -1 to 1, total steps 2
    # grid(0, 0) = (-0.5, -0.5)
    # grid(1, 0) = (0.5, -0.5)
    # etc
    fd.create_child(fid, grid(0, 0), mx_id() * sc)  # Same scale matrix result, three ways of writing
    fd.create_child(fid, grid(0.05, 1), mx_scale(sc))
    fd.create_child(fid, grid(1, 0.05), mx_sq(num=1, scale=sc))

    # Showing here a manual assignment of relative diameter to fractal definition.
    # This is redundant since 2 is the default value, but larger or smaller values will affect drawing and iteration.
    # Min diameter 2 means in some orientation the defn fits between planes 2 units apart, for a piece with identity transformation (vect(0, 0), mx_id())
    fd.relative_diameter = 2
    fd.iteration_fn = get_iteration_fn_standard(min_diameter=60, max_iterations=4)

    fp = fd.plotter
    x_minus_y = lambda vect, mx: vect[0] - vect[1]
    fill_colour_fn = colour_by_tsfm(-150, 150, tsfm=x_minus_y, colours=[RED, BLUE], alpha=0.5)
    outline_colour_fn = colour_fixed(colour=BLACK, alpha=0.75)
    # Plotting method: uses convex hull on definition by default, override by specifying vector_list = [vect(x, y)...]
    # Setting shrink=True (overriding default value of False) moves the shape's vectors inwards
    # to try and draw strictly inside the original shape using the specified brush radius (width).
    # If shape is too small, compared with brush radius, then the lines drawn will overlap the boundary anyway.
    fill_plot_fn = plot_path(width=5, expand_factor=1.00, fill=True, shrink=True)
    outline_plot_fn = plot_path(width=3, fill=False, closed=True, shrink=False)
    # Composite drawing method: do a translucent fill first, then a nearly solid outline
    # The fill uses the shrink method, the outline does not, which gives some interesting effects at the boundaries.
    fp.add(fill_plot_fn, fill_colour_fn)
    fp.add(outline_plot_fn, outline_colour_fn)


    # Definition #4 - demo of random square matrix transformations
    fid = 4
    fd = fs.lookup_defn(fid)
    n = 2
    sc = 1 / n
    grid = grid_generator(x_steps=n, y_steps=n)
    fd.create_child(fid, grid(0, 0), mx_scale(sc))
    fd.create_child(fid, grid(1, 0), mx_scale(sc))
    fd.create_child(fid, grid(0, 1), gen_mx_rand_sq(scale=sc ** 1.3))
    fd.create_child(fid, grid(1, 1), gen_mx_rand_sq(scale=sc ** 1.7))
    fp = fd.plotter
    colouring_fn = colour_by_log2_size(2, 4, colours=[GREEN, BLUE])
    plotting_fn = plot_path(
        closed=True,
        width=2,
        expand_factor=1.1,
        wobble_fn=wobble_square(pixels=3),
        vector_list=[vect(-1, 0), vect(-1, -1), vect(1, -1), vect(1, 0), vect(0, 1)],
        curved=True
    )
    fp.add(plotting_fn, colouring_fn)


    # Definition #5 - demo of random hexagon fractal
    fid_exit = 1
    fid_iterate = 5
    fd = fs.lookup_defn(fid_iterate)
    sc = 1 / 3
    h = 3 ** 0.5
    id_list = [fid_exit, fid_iterate, fid_iterate, fid_iterate, fid_iterate]
    fid_fn = gen_fid_rand(id_list)
    mx_fn = gen_mx_rand_circ(sc)
    fd.create_child(fid_fn, vect(2, 0) * sc, mx_fn)
    fd.create_child(fid_fn, vect(1, h) * sc, mx_fn)
    fd.create_child(fid_fn, vect(-1, h) * sc, mx_fn)
    fd.create_child(fid_fn, vect(-2, 0) * sc, mx_fn)
    fd.create_child(fid_fn, vect(-1, -h) * sc, mx_fn)
    fd.create_child(fid_fn, vect(1, -h) * sc, mx_fn)
    fd.create_child(fid_fn, vect(0, 0) * sc, mx_fn)
    fp = fd.plotter
    colouring_fn = colour_by_progress(colours=[BLACK, PINK, LIGHT_BLUE, GREEN, YELLOW, BLACK])
    # plotting_fn = plot_dot(expand_factor=0.5)  # expand_factor < 1 makes dots distinct
    plotting_fn = plot_path(expand_factor=0.5, fill=True)
    fp.add(plotting_fn, colouring_fn)


    # Definition #6 - demo of random vector shift
    fid = 6
    fd = fs.lookup_defn(fid)
    sc = 0.5
    fd.create_child(fid, vect(-1, -1) * sc, mx_scale(sc))  # Two versions of same scale matrix here
    fd.create_child(fid, vect(1, -1) * sc, mx_diag(sc, sc))
    fd.create_child(fid, gen_vect_rand([-sc, sc], [sc, sc]), mx_scale(sc))
    fp = fd.plotter
    distance_from_origin = lambda vect, mx: ((vect[0]) ** 2 + (vect[1]) ** 2) ** 0.5
    colouring_fn = colour_by_tsfm(500, 580, tsfm=distance_from_origin, colours=[PURPLE, YELLOW, PINK])
    plotting_fn = plot_dot(expand_factor=1.5, wobble_fn=wobble_square(pixels=5))  # make dots overlap
    fp.add(plotting_fn, colouring_fn)


    # Definition #7 - Standard (2D) dragon curve
    fid = 7
    fd = fs.lookup_defn(fid)
    sc = 0.5 ** 0.5
    fd.create_child(fid, vect(-0.5, 0.5), mx_rotd(angle=-45, scale=sc))
    fd.create_child(fid, vect(0.5, 0.5), mx_rotd(angle=-135, scale=sc))
    fp = fd.plotter
    piece_angle = lambda vect, mx: mx_angle(mx)
    colouring_fn = colour_by_tsfm(-90, 270, tsfm=piece_angle, colours=[RED, YELLOW, GREEN, BLUE])
    plotting_fn = plot_path(width=3, vector_list=[vect(-1, 0), vect(1, 0)])
    fp.add(plotting_fn, colouring_fn)


    # Definition #8 - Random Sierpinski Carpet
    # gen_children_rand_small_squares - 7 out of 9 little squares, in 3x3 big square
    # gen_children_fade_out - Iterate with a probability depending on how far fractal piece is from a specified point
    fidr = 8
    fd = fs.lookup_defn(fidr)
    # fd.children = gen_children_rand_small_squares(system=fs, fid=fidr, m=7, n=3)  # Definition children is dynamically calculated by callback
    fd.children = gen_children_fade_out(system=fs, fid=fidr, n=3, centre_vect=vect(750, 750), cutoff_diameter=50, d1=75, d2=225, p1=1, p2=0)
    fp = fd.plotter
    x, y = 650, 650
    distance_from_pt = lambda vect, mx: ((vect[0] - x) ** 2 + (vect[1] - y) ** 2) ** 0.5
    colouring_fn = colour_by_tsfm(50, 350, tsfm=distance_from_pt, colours=[MAGENTA, YELLOW, CYAN])
    plotting_fn = plot_path(fill=True, width=3, expand_factor=0.6, vector_list=[vect(-1, 1), vect(-1, -1), vect(1, -1), vect(1, 0), vect(0, 0)])
    fp.add(plotting_fn, colouring_fn)


    # Definition #9 - Modified dragon curve with fractal dimension varying from 1 to 2, from one end to the other
    def gen_children_variable_dragon(system, fid):
        def calc_children(context_piece=None):
            progress = 1
            if context_piece is not None:
                progress = context_piece.get_progress_value()
            x = 0
            y = progress
            x1 = 0.5 * (-1 + x)
            x2 = 0.5 * (1 + x)
            y1 = 0.5 * y
            y2 = 0.5 * y
            piece1 = FractalPiece(system=system, fid=fid, vect=vect(x1, y1), mx=np.array(((x - x1, y1 - y), (y - y1, x - x1))))
            piece2 = FractalPiece(system=system, fid=fid, vect=vect(x2, y2), mx=np.array(((x - x2, y2 - y), (y - y2, x - x2))))
            piece2.reverse_progress = True  # Needed to get linear colouring and iteration! Try removing it...
            children = [piece1, piece2]
            return children

        return calc_children

    fid = 9
    fd = fs.lookup_defn(fid)
    sc = 0.5 ** 0.5
    fd.children = gen_children_variable_dragon(fs, fid)
    fd.iteration_fn = get_iteration_fn_standard(min_diameter=20, max_iterations=20)
    fp = fd.plotter
    colouring_fn = colour_by_progress([BLUE, RED, ORANGE])
    # colouring_fn = colour_fixed(CYAN, alpha=0.75) # Alternative fixed colouring method
    plotting_fn = plot_path(width=2, vector_list=[vect(-1, 0), vect(1, 0)])
    # plotting_fn = plot_path(width=1, closed=True, vector_list=[vect(-1, 0), vect(0, -1), vect(1, 0), vect(0, 1)])  # Alternative plot method
    fp.add(plotting_fn, colouring_fn)


    # --------------------

    # Default function to control when pieces stop iterating
    # This can be overwritten at the fractal definition level
    fs.iteration_fn = get_iteration_fn_standard(min_diameter=sys_min_diameter, max_iterations=sys_max_iterations)

    # --------------------

    # TODO: Convex Hulls only currently works for 2D. Can it work for 3D too?
    # Calculate Convex Hulls after fractal definitions completed
    # If this is not done, plot_path will not have hulls available for drawing,
    # and will fall back to unit squares if a path (vector_list) is not supplied
    fs.calculate_hulls(hull_accuracy=0.1, max_iterations=10)

    # --------------------

    # # Examine the fractal system setup
    # fs.log("")
    # fs.log("Fractal System:")
    # fs.log(fs)
    # fs.log("")

    # Calculate the iterations
    initial_piece = FractalPiece(system=fs, fid=init_defn_fid, vect=init_vect, mx=init_mx)
    fs.initial_pieces = [initial_piece]
    fs.do_iterations()
    fs.log(f"After iteration, there are {fs.final_size()} pieces")
    fs.log("")

    # Plot iterations to drawing
    fs.plot(drawing)
    fs.log("Fractal System plotted successfully")
    fs.log("")

    return drawing
