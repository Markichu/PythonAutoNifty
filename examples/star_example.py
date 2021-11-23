import math
import random

from pyautonifty.constants import DRAWING_SIZE, BLACK
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


def star_example(drawing, lines=10, line_segments=100, draw_points=False, transparency=False, curved_lines=False, enclosed_path=False):
    all_points = []
    drawing.add_point(Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2), BLACK, 500)
    num = random.randint(2, 10)
    rot = random.random() * 1 + random.randint(0, 1)
    for j in range(random.randint(2, lines)):
        line_points = []
        for i in range(random.randint(2, line_segments)):
            # calc position of dot
            pos = Pos.from_rotational(rot * math.pi * i * j, num * j * i)
            # draw dot
            line_points.append(pos)

        colour = [random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 1]
        if transparency:
            colour[-1] = random.random()
        brush_radius = 1
        if curved_lines:
            drawing.add_quadratic_bezier_curve(line_points, colour, brush_radius, enclosed_path=True)
        else:
            drawing.add_line(line_points, colour, brush_radius, enclosed_path=enclosed_path)

        all_points.extend(line_points)

    if draw_points:
        for pnt in all_points:
            colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 1]
            if transparency:
                colour[-1] = random.random()
            brush_radius = random.randint(10, 20)
            position = pnt + Pos(0.5, 0.5)
            drawing.add_point(position, colour, brush_radius)
        for pnt in all_points:
            colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 1]
            if transparency:
                colour[-1] = random.random()
            brush_radius = random.randint(3, 9)
            position = pnt + Pos(0.5, 0.5)
            drawing.add_point(position, colour, brush_radius)
    return drawing


if __name__ == "__main__":
    example_drawing = star_example(Drawing())

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