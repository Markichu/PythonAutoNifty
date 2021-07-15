from Drawing import Drawing

from fractalRunner import fractalRunner
from originalDrawingMethods import point_image, rotating_square, tiled_diagonals,\
  fibonacci_dots, fibonacci_image, squared_circle, curved_lines,\
  shrinking_circle_ring, square_fractal, big_text_boi

def main():

    # ---------------
    # # Pick a drawing to run here
    # # (Uncomment out a single line to run that function)

    # drawing = square_fractal(Drawing(), [1, 1, 1, 0], 5)
    # drawing = big_text_boi(Drawing())
    drawing = fractalRunner(Drawing())
    # drawing = point_image(Drawing(), "stars.jpg", do_a_shuffle=False)
    # ---------------

    # # Optional - Reduce scale to prevent drawing from touching the edge
    # drawing *= 0.95

    # # Select an import method for the output data
    output_data = drawing.to_nifty_fast_import()  # Replace previous canvas contents in Nifty.Ink
    # output_data = drawing.to_nifty_add_layer_import()  # Keep previous canvas contents, write a layer on top

    # # Write the drawing to output file
    # # that can be pasted into the console
    # # in the Developer pane on Nifty Ink website
    print(f"Lines: {len(drawing.object['lines'])}, Size: {len(output_data)}")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # # Optional - Render and save the image in pygame,\
    # #   increase pygame_scale for higher RES output images,\
    # #   enable headless if image will be larger than the screen,\
    # #   filename specifies the name and format of the image
    drawing.render(pygame_scale=None,headless=False,filename="screenshot.png")

if __name__ == '__main__':
    main()
