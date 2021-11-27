import random

from pyautonifty.constants import DRAWING_SIZE, YELLOW, BLACK, MAGENTA, BLUE
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


def smiley_face(drawing):
    # Set a background colour to be used for the drawing
    background_colour = MAGENTA

    # Add a blue square that is not filled in around where the smiley face will be
    square_position = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)
    square_width = DRAWING_SIZE / 1.5
    square_colour = BLUE
    square_brush_radius = DRAWING_SIZE / 64
    square_filled = False

    # Set the position of the yellow face itself in the middle of the drawing (typically 500, 500)
    face_position = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)
    face_radius = DRAWING_SIZE / 4  # 250
    face_colour = YELLOW  # Yellow in RGBA (255, 255, 0, 1)

    # Create the eyes
    eye_horizontal_offset = DRAWING_SIZE / 10
    eye_vertical_offset = DRAWING_SIZE / 16
    left_eye_position = face_position - Pos(eye_horizontal_offset, eye_vertical_offset)
    right_eye_position = face_position - Pos(-eye_horizontal_offset, eye_vertical_offset)
    eye_radius = DRAWING_SIZE / 32
    eye_colour = BLACK  # Black in RGBA (0, 0, 0, 1)

    # Create the curve for the smile
    smile_horizontal_offset = DRAWING_SIZE / 8
    smile_vertical_offset = DRAWING_SIZE / 12
    smile_starting_point = face_position + Pos(-smile_horizontal_offset, smile_vertical_offset)
    smile_control_point = face_position + Pos(0, smile_vertical_offset * 3)
    smile_ending_point = face_position + Pos(smile_horizontal_offset, smile_vertical_offset)
    smile_points = [smile_starting_point, smile_control_point, smile_ending_point]
    smile_brush_radius = DRAWING_SIZE / 64
    smile_colour = BLACK  # Black in RGBA (0, 0, 0, 1)

    # Put it all together in a drawing using chained methods
    drawing.add_background(background_colour) \
           .add_rounded_square(square_position, square_width, square_colour, square_brush_radius, square_filled) \
           .add_point(face_position, face_colour, face_radius) \
           .add_point(left_eye_position, eye_colour, eye_radius) \
           .add_point(right_eye_position, eye_colour, eye_radius) \
           .add_general_bezier_curve(smile_points, smile_colour, smile_brush_radius)

    return drawing


if __name__ == "__main__":
    example_drawing = smiley_face(Drawing())

    output_data = example_drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink

    print(f"Lines: {len(example_drawing)}, "
          f"Points: {sum([len(line['points']) for line in example_drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(example_drawing, filename="smiley_face_%Y_%m_%d_%H-%M-%S-%f.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10)
