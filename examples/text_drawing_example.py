from pyautonifty.constants import DRAWING_SIZE
from pyautonifty.font import Font, default_value
from pyautonifty.helper_fns import hsva_to_rgba
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


def text_drawing_example(drawing, font_file_name=None, draw_bounding_box=False):
    drawing.add_gradient(Pos(0, 0), Pos(DRAWING_SIZE, DRAWING_SIZE), hsva_to_rgba(0, 0, 0.9), hsva_to_rgba(0, 0, 0.7),
                         200)
    drawing.add_gradient(Pos(150, 150), Pos(DRAWING_SIZE - 150, DRAWING_SIZE - 150), hsva_to_rgba(0, 0, 1),
                         hsva_to_rgba(0, 0, 1), 200)

    font = Font(font_file_name, size=50, unknown_character=default_value())
    font2 = Font(font_file_name, size=25, line_spacing=1.35, colour=(64, 64, 200, 1), unknown_character=default_value())

    # Examples of writing:
    # title text
    drawing.write(font, Pos(160, 170), lines=["Add a title", "here!"], draw_bounding_box=draw_bounding_box)
    # body text
    drawing.write(font2, Pos(160, 300), lines=["Add some interesting",
                                               "content and words",
                                               "here!"], draw_bounding_box=draw_bounding_box)

    return drawing


if __name__ == "__main__":
    example_drawing = text_drawing_example(Drawing(), "fonts/OpenSans-Regular.ttf")

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
