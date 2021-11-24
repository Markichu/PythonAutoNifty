from pyautonifty import helper_fns, constants
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.fractal_runner import fractalRunner
from pyautonifty.renderer import Renderer

from examples.alpha_example import alpha_example
from examples.curved_lines import curved_lines
from examples.fibonacci_dots import fibonacci_dots
from examples.point_image import point_image
from examples.rectangle_example import rectangle_example
from examples.rotating_square import rotating_square
from examples.shrinking_circle_ring import shrinking_circle_ring
from examples.square_example import square_example
from examples.square_fractal import square_fractal
from examples.square_image import square_image
from examples.squared_circle import squared_circle
from examples.star_example import star_example
from examples.text_drawing_example import text_drawing_example
from examples.tiled_diagonals import tiled_diagonals


# Below you can create your own custom drawing programmatically!
def custom_drawing_method(drawing):
    colour = (255, 0, 0, 0.2)  # RED with an alpha value of 0.2
    drawing.add_rounded_rectangle(Pos(500, 500), 600, 500, colour, 50, filled=True)

    line_points = [Pos(370, 342), Pos(637, 503), Pos(370, 663)]

    mid_point_x = sum(pos.x for pos in line_points) / len(line_points)
    mid_point_y = sum(pos.y for pos in line_points) / len(line_points)
    mid_point = Pos(mid_point_x, mid_point_y)

    line_points.append(line_points[0])
    line_points.append(mid_point)
    line_points.append(line_points[1])
    line_points.append(mid_point)
    line_points.append(line_points[2])

    colour = (255, 255, 255, 0.5)  # WHITE with an alpha value of 0.5

    drawing.add_line(line_points, colour, 50)
    return drawing


def main():
    # # Optional - Make a new random seed, set it and print it. Used in drawings with randomness
    # # This technically changes the random seed, but should not matter unless you put code above this.
    seed = helper_fns.random_seed()
    print("Random seed:", seed)

    # # Optional - Change the random seed. Use this to reproduce the same random drawing.
    # helper_fns.set_random_seed(seed)
    # print("Random changed to:", seed)

    # ---------------
    # # Pick a method to use here that draws something nice on the canvas
    # # Uncomment out a single line to run that function
    # # Most of the methods and examples are in file drawing_methods.py
    # # For the general fractal examples, set it up in fractal_runner.py

    # drawing = point_image(Drawing(), "temp_image.png", do_a_shuffle=False)  # Small image (PNG, JPG supported)
    # drawing = square_image(Drawing(), "temp_image.png", do_a_shuffle=False)  # Sharp pixel corners drawing
    # drawing = text_drawing_example(Drawing(), font_file_name='fonts/OpenSans-Regular.ttf')  # Text with TTF font file
    drawing = fractalRunner(Drawing())  # Generalised fractal drawing methods
    # drawing = square_fractal(Drawing(), [1, 1, 1, 0], 5)  # Simple square fractal drawing tool
    # drawing = square_example(Drawing())  # Draws some basic squares with different brush sizes
    # drawing = rectangle_example(Drawing())  # Draws some basic rectangles with different brush sizes
    # drawing = alpha_example(Drawing())  # Shows an example of using alpha values, ensure correct pygame settings
    # drawing = star_example(Drawing())  # Draws a spiralling pattern inside a black circle

    # drawing = custom_drawing_method(Drawing())

    # ---------------

    # # Optional - Reduce scale to prevent drawing from touching the edge
    # drawing *= 0.95

    # # Optional - Reduce size of your drawing but at the cost of precision.
    # round(drawing)

    # # Optional - Save the raw drawing data to a file
    # drawing.export_raw_data("drawing.ink", indent=4)

    # # Optional - Load raw drawing data from a file, overwrites the drawing it is loaded into.
    # drawing.import_raw_data("drawing.ink")

    # # Optional - Add a layer from another drawing, adds to the top of the drawing.
    # drawing + drawing2

    # # Optional - Reverse the drawing order of a drawing
    # reversed(drawing)

    # # Select an import method for the output data
    output_data = drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink
    # output_data = drawing.to_nifty_add_layer_import()  # Keep previous canvas contents, write a layer on top
    # output_data = drawing.to_nifty_show_import() # Show the import and replace previous canvas contents in Nifty.Ink

    # # Write the drawing to output file
    # # that can be pasted into the console
    # # in the Developer pane on Nifty Ink website
    print(f"Lines: {len(drawing)}, "
          f"Points: {sum([len(line['points']) for line in drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # # Optional - Render and save the image in pygame
    # #   increase pygame_scale for higher RES output images
    # #   enable headless if image will be larger than the screen
    # #   filename specifies the name and format of the image
    # #   simulate specifies whether to show the drawing process
    # #   speed specifies the speed a simulated drawing should be drawn, 3 is roughly equal to the speed that nifty uses
    # #   allow_transparency can be used to enable or disable transparency in the render, it is faster disabled
    # #   fake_transparency is used as an illusion of transparency but only works well with 1 effective layer, very fast
    # #   draw_as_bezier is used to show lines drawn in the exact same method as nifty.ink, slower
    # #   step_size determines the bezier curves effective resolution, higher is slower but often looks better
    # #   save_transparent_bg transparent bg in the pygame screenshot, doesn't work well with transparent lines
    # #   green_screen_colour the colour to use as a green screen for transparent bg, use a colour not in your drawing!
    # #   timestamp_format provides access to a custom timestamp format, refer to datetime's strftime format codes

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(drawing, filename="screenshot_%Y_%m_%d_%H-%M-%S-%f.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10)

    # Render the traditional way (faster).
    # renderer.render(drawing, filename="screenshot.png")


if __name__ == '__main__':
    main()
