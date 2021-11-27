from pyautonifty.constants import DRAWING_SIZE, BLACK
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Draw straight lines that combine to create impression of curved lines
def curved_lines(drawing, n=20):
    # init drawing
    step = DRAWING_SIZE / n

    # do curved lines
    for i in range(n + 1):
        offset = i * step
        # do bottom left line
        drawing.add_straight_line(Pos(offset, DRAWING_SIZE), Pos(0, offset), BLACK, DRAWING_SIZE / (25 * n))
        # do top right
        drawing.add_straight_line(Pos(DRAWING_SIZE, offset), Pos(offset, 0), BLACK, DRAWING_SIZE / (25 * n))

    # do diagonal lines
    for i in range(n - 1):
        offset = (i + 1) * step
        # do top left line
        drawing.add_straight_line(Pos(offset, 0), Pos(0, offset), BLACK, DRAWING_SIZE / (25 * n))
        # do bottom right
        drawing.add_straight_line(Pos(DRAWING_SIZE, DRAWING_SIZE - offset), Pos(DRAWING_SIZE - offset, DRAWING_SIZE),
                                  BLACK, DRAWING_SIZE / (25 * n))

    # do middle diagonal
    drawing.add_straight_line(Pos(DRAWING_SIZE, 0), Pos(0, DRAWING_SIZE), BLACK, DRAWING_SIZE / (25 * n))

    return drawing


if __name__ == "__main__":
    example_drawing = curved_lines(Drawing())

    output_data = example_drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink

    print(f"Lines: {len(example_drawing)}, "
          f"Points: {sum([len(line['points']) for line in example_drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(example_drawing, filename="curved_lines_%Y_%m_%d_%H-%M-%S-%f.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10)
