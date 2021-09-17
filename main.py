from Drawing import Drawing
from helperFns import random_seed, set_random_seed
from constants import DRAWING_SIZE, BLACK
from drawingMethods import point_image, square_image, rotating_square, tiled_diagonals, \
    fibonacci_dots, fibonacci_image, squared_circle, curved_lines, \
    shrinking_circle_ring, square_fractal, text_drawing_example, square_example, rectangle_example, \
    alpha_example, star_example

from fractalRunner import fractalRunner


def main():
    # # Optional - Make a new random seed, set it and print it. Used in drawings with randomness
    # # This technically changes the random seed, but should not matter unless you put code above this.
    seed = random_seed()

    # # Optional - Change the random seed. Use this to reproduce the same random drawing.
    # set_random_seed(seed)

    # ---------------
    # # Pick a method to use here that draws something nice on the canvas
    # # Uncomment out a single line to run that function
    # # Most of the methods and examples are in file drawingMethods.py
    # # For the general fractal examples, set it up in fractalRunner.py

    # drawing = point_image(Drawing(), "temp_image.png", do_a_shuffle=False)  # Example of how to reproduce a small image (PNG, JPG supported) on the canvas
    # drawing = square_image(Drawing(), "temp_image.png", do_a_shuffle=False)  # Alternative image drawing method with sharp pixel corners
    # drawing = text_drawing_example(Drawing())  # Example of how to draw text on the canvas
    drawing = fractalRunner(Drawing())  # Generalised fractal drawing methods
    # drawing = square_fractal(Drawing(), [1, 1, 1, 0], 5)  # Simple square fractal drawing tool
    # drawing = square_example(Drawing())  # Draws some basic squares with different brush sizes
    # drawing = rectangle_example(Drawing())  # Draws some basic rectangles with different brush sizes
    # drawing = alpha_example(Drawing())  # Shows an example of using alpha values, make sure pygame has alpha enabled too!
    # drawing = star_example(Drawing())  # Draws a spiralling pattern inside a black circle

    # ---------------

    # # Optional - Reduce scale to prevent drawing from touching the edge
    # drawing *= 0.95

    # # Optional - Reduce size of your drawing but at the cost of precision.
    # drawing.round_floats()

    # # Optional - Save the raw drawing data to a file
    # drawing.export_raw_data("drawing.ink", indent=4)

    # # Optional - Load raw drawing data from a file, overwrites the drawing it is loaded into.
    # drawing.import_raw_data("drawing.ink")

    # # Optional - Add a layer from another drawing, adds to the top of the drawing.
    # drawing.add_layer(drawing2)

    # # Optional - Load a layer from a file, adds to the top of the drawing.
    # drawing.add_layer_from_file("drawing.ink")

    # # Select an import method for the output data
    output_data = drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink
    # output_data = drawing.to_nifty_add_layer_import()  # Keep previous canvas contents, write a layer on top
    # output_data = drawing.to_nifty_show_import() # Show the import and replace previous canvas contents in Nifty.Ink

    # # Write the drawing to output file
    # # that can be pasted into the console
    # # in the Developer pane on Nifty Ink website
    print(f"Lines: {len(drawing.object['lines'])}, Size: {(len(output_data)/1024.0**2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # # Optional - Render and save the image in pygame,\
    # #   increase pygame_scale for higher RES output images,\
    # #   enable headless if image will be larger than the screen,\
    # #   filename specifies the name and format of the image
    # #   simulate specifies whether to show the drawing process
    # #   speed specifies the speed a simulated drawing should be drawn, 3 is roughly equal to the speed that nifty uses
    # #   allow_transparency can be used to enable or disable transparency in the render, it is faster disabled
    # #   fake_transparency is used as an illusion of transparency but only works well with 1 effective layer, very fast
    # #   draw_as_bezier is used to show lines drawn in the exact same method as nifty.ink, slower
    # #   step_size determines the bezier curves effective resolution, higher is slower but often looks better

    # Render in a very accurate (but slower) way.
    drawing.render(pygame_scale=None, headless=False, filename="screenshot.png",
                   simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True, step_size=10)

    # Render the traditional way (faster).
    # drawing.render(pygame_scale=None, headless=False, filename="screenshot.png")


if __name__ == '__main__':
    main()
