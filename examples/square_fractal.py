from pyautonifty.constants import DRAWING_SIZE
from pyautonifty.font import Font, default_value
from pyautonifty.helper_fns import hsva_to_rgba
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Draw a square fractal which splits a square into 4 more squares (2x2), and iterates on 3 out of 4 smaller squares.
# Note - this is Markichu's original fractal drawing method for square fractals
# It was derived from davidryan59/niftymaestro drawings on Nifty Ink
# Subsequently, davidryan59 implemented more generalised fractal drawing methods, see fractalRunner, FractalSystem etc.
def square_fractal(drawing, master_key, iterations=5):
    # add gradient background
    drawing.add_gradient(Pos(0, 0), Pos(DRAWING_SIZE, DRAWING_SIZE), hsva_to_rgba(0, 0, 0.9), hsva_to_rgba(0, 0, 0.7), 200)
    drawing *= 1 / 0.95

    # Add text
    font = Font("fonts/OpenSans-Regular.ttf", size=50, unknown_character=default_value())
    drawing.write(font, Pos(600, 125), ["Square", "Fractal", f'#{"".join([str(key) for key in master_key[:3]])}', f"n={iterations}"])

    def rotate_left(ext_key):
        rotate_left_dict = {0: 0,
                            1: 2,
                            2: 3,
                            3: 4,
                            4: 1,
                            5: 6,
                            6: 7,
                            7: 8,
                            8: 5}
        modified_key = [rotate_left_dict[i] for i in ext_key]
        return [modified_key[1], modified_key[3], modified_key[0], modified_key[2]]

    def mirror(ext_key):
        mirror_dict = {0: 0,
                       1: 7,
                       2: 6,
                       3: 5,
                       4: 8,
                       5: 3,
                       6: 2,
                       7: 1,
                       8: 4}
        modified_key = [mirror_dict[i] for i in ext_key]
        return [modified_key[2], modified_key[3], modified_key[0], modified_key[1]]

    def next_ext_key(ext_key, this_key):
        if this_key == 1:
            return ext_key
        elif this_key == 2:
            return rotate_left(ext_key)
        elif this_key == 3:
            return rotate_left(rotate_left(ext_key))
        elif this_key == 4:
            return rotate_left(rotate_left(rotate_left(ext_key)))
        elif this_key == 5:
            return mirror(rotate_left(rotate_left(ext_key)))
        elif this_key == 6:
            return mirror(rotate_left(ext_key))
        elif this_key == 7:
            return mirror(ext_key)
        elif this_key == 8:
            return mirror(rotate_left(rotate_left(rotate_left(ext_key))))

    def square_fractal_recursive(drawing, ext_key, square_pos_corners, iterations):
        pos = (square_pos_corners[0] + square_pos_corners[1]) / 2
        size = (square_pos_corners[1].x - square_pos_corners[0].x) / 2
        if iterations > 0:
            # call recursively for all inner cells
            avg_pos = (square_pos_corners[0] + square_pos_corners[1]) / 2
            subdivisions = [[Pos(square_pos_corners[0].x, avg_pos.y), Pos(avg_pos.x, square_pos_corners[1].y)],
                            [square_pos_corners[0].copy(), avg_pos.copy()],
                            [avg_pos.copy(), square_pos_corners[1].copy()],
                            [Pos(avg_pos.x, square_pos_corners[0].y), Pos(square_pos_corners[1].x, avg_pos.y)]]
            for this_key, subdiv in zip(ext_key, subdivisions):
                if this_key != 0:
                    # draw transparent circle
                    # colour = hsva_to_rgba(0, 0, 0.4 - 0.4 * (pos.y / DRAWING_SIZE), 0.05)
                    # drawing.add_point(pos, colour, size)

                    square_fractal_recursive(drawing, next_ext_key(master_key, this_key), subdiv, iterations - 1)
        else:
            # draw dot in this cell
            colour = hsva_to_rgba(0, 0, 0.4 - 0.4 * (pos.y / DRAWING_SIZE))
            drawing.add_point(pos, colour, size)
        return drawing

    return square_fractal_recursive(drawing, master_key, [Pos(0, 0), Pos(DRAWING_SIZE, DRAWING_SIZE)], iterations)


if __name__ == "__main__":
    example_drawing = square_fractal(Drawing(), [1, 1, 1, 0], 5)

    output_data = example_drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink

    print(f"Lines: {len(example_drawing)}, "
          f"Points: {sum([len(line['points']) for line in example_drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(example_drawing, filename="screenshot.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10,
                    timestamp=True)