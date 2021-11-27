from pyautonifty.helper_fns import rotate
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Draw a square that appears to rotate on the Nifty Ink canvas
def rotating_square(drawing):
    drawing.add_background((255, 255, 255, 1))
    p1 = Pos(200, 200)
    p2 = Pos(200, 800)
    p3 = Pos(800, 800)
    p4 = Pos(800, 200)
    for _ in range(500):
        drawing.add_line([p1, p2, p3, p4], (0, 0, 0, 1), 10, enclosed_path=True)
        drawing.add_pause(10)
        drawing.add_background((255, 255, 255, 1))
        p1 = rotate(p1, 0.1)
        p2 = rotate(p2, 0.1)
        p3 = rotate(p3, 0.1)
        p4 = rotate(p4, 0.1)
    drawing.add_line([p1, p2, p3, p4], (0, 0, 0, 1), 10, enclosed_path=True)
    return drawing


if __name__ == "__main__":
    example_drawing = rotating_square(Drawing())

    output_data = example_drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink

    print(f"Lines: {len(example_drawing)}, "
          f"Points: {sum([len(line['points']) for line in example_drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(example_drawing, filename="rotating_square_%Y_%m_%d_%H-%M-%S-%f.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10)
