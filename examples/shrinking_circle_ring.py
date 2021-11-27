import math

from pyautonifty.constants import DRAWING_SIZE, WHITE
from pyautonifty.helper_fns import hsva_to_rgba
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Draw concentric rings of circles getting smaller
def shrinking_circle_ring(drawing, n=20, m=36):
    radians_step = 2 * math.pi / m
    current_h = 0
    big_radius = DRAWING_SIZE / 2
    for _ in range(n):
        # calc current radius
        big_radius = (m * big_radius) / (m + 2 * math.pi)
        small_radius = (math.pi * big_radius) / m

        # do colour
        colour = hsva_to_rgba(current_h, 0.8, 0.9)
        current_h -= 1 / n

        # draw circles around radius
        for i in range(m):
            pos = Pos.from_rotational(radians_step * i, big_radius)
            drawing.add_point(pos, colour, small_radius)
            drawing.add_point(pos, WHITE, small_radius / 3)

    drawing *= 2

    return drawing


if __name__ == "__main__":
    example_drawing = shrinking_circle_ring(Drawing())

    output_data = example_drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink

    print(f"Lines: {len(example_drawing)}, "
          f"Points: {sum([len(line['points']) for line in example_drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(example_drawing, filename="shrinking_circle_ring_%Y_%m_%d_%H-%M-%S-%f.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10)
