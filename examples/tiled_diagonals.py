import random

from pyautonifty.constants import DRAWING_SIZE
from pyautonifty.helper_fns import hsva_to_rgba
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Draw a pattern involving a lot of diagonal lines
def tiled_diagonals(drawing, n=50):
    cell_size = DRAWING_SIZE / n
    for x in range(n):
        for y in range(n):
            if random.getrandbits(1):
                pos1 = Pos(x * cell_size, y * cell_size)
                pos2 = Pos((x + 1) * cell_size, (y + 1) * cell_size)
            else:
                pos1 = Pos((x + 1) * cell_size, y * cell_size)
                pos2 = Pos(x * cell_size, (y + 1) * cell_size)
            colour = hsva_to_rgba(random.random(), 0.5, 1)
            drawing.add_straight_line(pos1, pos2, colour, DRAWING_SIZE / n / 10)
    drawing.shuffle_lines()
    return drawing


if __name__ == "__main__":
    example_drawing = tiled_diagonals(Drawing())

    output_data = example_drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink

    print(f"Lines: {len(example_drawing)}, "
          f"Points: {sum([len(line['points']) for line in example_drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(example_drawing, filename="tiled_diagonals_%Y_%m_%d_%H-%M-%S-%f.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10)
