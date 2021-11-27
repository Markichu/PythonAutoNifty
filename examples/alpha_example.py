import random

from pyautonifty.constants import DRAWING_SIZE
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


def alpha_example(drawing):
    for i in range(random.randint(0, 100)):
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.random())
        position = Pos(random.randint(0, DRAWING_SIZE), random.randint(0, DRAWING_SIZE))
        brush_radius = random.randint(1, 500)
        drawing.add_point(position, colour, brush_radius)
        line_points = []
        for j in range(random.randint(2, 20)):
            line_points.append(Pos(random.randint(0, DRAWING_SIZE), random.randint(0, DRAWING_SIZE)))
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.random())
        brush_radius = random.randint(1, 10)
        drawing.add_quadratic_bezier_curve(line_points, colour, brush_radius)
    return drawing


if __name__ == "__main__":
    example_drawing = alpha_example(Drawing())

    output_data = example_drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink

    print(f"Lines: {len(example_drawing)}, "
          f"Points: {sum([len(line['points']) for line in example_drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(example_drawing, filename="alpha_example_%Y_%m_%d_%H-%M-%S-%f.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10)
