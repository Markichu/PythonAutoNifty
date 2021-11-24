import numpy as np

from pyautonifty.constants import DRAWING_SIZE
from pyautonifty.helper_fns import hsva_to_rgba
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Squared Circle example
def squared_circle(drawing, n=8):
    # init step and drawing
    step = 90 / n
    current_h = 0.8

    for i in range(n):
        # get degrees around circle and position
        degrees = i * step + (step / 2)

        # get pos for corners
        pos1 = Pos.from_rotational(np.radians(degrees), DRAWING_SIZE).rotate(np.radians(45))
        pos2 = Pos(pos1.x, DRAWING_SIZE - pos1.y).rotate(np.radians(45))
        pos3 = Pos(DRAWING_SIZE - pos1.x, DRAWING_SIZE - pos1.y).rotate(np.radians(45))
        pos4 = Pos(DRAWING_SIZE - pos1.x, pos1.y).rotate(np.radians(45))

        # do colour
        colour = hsva_to_rgba(current_h, 0.8, 0.85)
        current_h -= 0.7 / n

        # add square
        drawing.add_line([pos1, pos2, pos3, pos4], colour, DRAWING_SIZE / (25 * n))

    return drawing


if __name__ == "__main__":
    example_drawing = squared_circle(Drawing(), n=100)

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