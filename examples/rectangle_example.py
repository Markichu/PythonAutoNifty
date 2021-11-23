from pyautonifty.constants import BLACK
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Draw four black rectangles nearly filling the canvas, with different rounding on each corner
def rectangle_example(drawing):
    drawing.add_rounded_rectangle(centre_pos=Pos(250, 250), width=400, height=200, colour=BLACK, brush_radius=0.1)
    drawing.add_rounded_rectangle(centre_pos=Pos(750, 250), width=200, height=400, colour=BLACK, brush_radius=2)
    drawing.add_rounded_rectangle(centre_pos=Pos(250, 750), width=400, height=200, colour=BLACK, brush_radius=40)
    drawing.add_rounded_rectangle(centre_pos=Pos(750, 750), width=200, height=400, colour=BLACK, brush_radius=1000)
    return drawing


if __name__ == "__main__":
    example_drawing = rectangle_example(Drawing())

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