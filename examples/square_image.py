from PIL import Image

from pyautonifty.constants import DRAWING_SIZE
from pyautonifty.helper_fns import rotate
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Draw an image from file using square pixels
def square_image(drawing, image_name, brush_radius=1, do_a_shuffle=False,
                 width=DRAWING_SIZE, height=DRAWING_SIZE,
                 position=Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2), keep_aspect_ratio=False, rotation=None):
    # load image from file
    image = Image.open(image_name)

    # convert the image to RGBA values
    rgba_image = image.convert('RGBA')

    # init width and height
    pixel_width, pixel_height = image.size

    if keep_aspect_ratio:  # keep the images original shape
        square_pixel_width = width / max(pixel_width, pixel_height)
        square_pixel_height = height / max(pixel_width, pixel_height)

        # Centre the image if it isn't a square
        x_offset = abs(max(pixel_width, pixel_height) - pixel_width) / 2
        y_offset = abs(max(pixel_width, pixel_height) - pixel_height) / 2
    else:  # stretch the image to be a square
        square_pixel_width = width / pixel_width
        square_pixel_height = height / pixel_height

        x_offset = 0
        y_offset = 0

    for x in range(pixel_width):
        for y in range(pixel_height):
            colour = list(rgba_image.getpixel((x, y)))
            colour[3] /= 255

            # Do the initial position calculation
            px = (x + 0.5 + x_offset) * square_pixel_width
            py = (y + 0.5 + y_offset) * square_pixel_height

            # Adjust the position of the image
            px += position.x - (width / 2)
            py += position.y - (height / 2)

            pos = Pos(px, py)

            # Rotate the position
            if rotation:
                pos = rotate(pos, rotation, origin=position)

            drawing.add_rounded_rectangle(centre_pos=pos, width=square_pixel_width, height=square_pixel_height,
                                          colour=colour, brush_radius=brush_radius)

    if do_a_shuffle:
        drawing.shuffle_lines()

    return drawing


if __name__ == "__main__":
    example_drawing = square_image(Drawing(), image_name="example.jpg")

    output_data = example_drawing.to_nifty_import()  # Replace previous canvas contents in Nifty.Ink

    print(f"Lines: {len(example_drawing)}, "
          f"Points: {sum([len(line['points']) for line in example_drawing])}, "
          f"Size: {(len(output_data) / 1024.0 ** 2):.2f}MB")
    with open("output.txt", "w") as file:
        file.write(output_data)

    # Init render class.
    renderer = Renderer()

    # Render in a very accurate (but slower) way.
    renderer.render(example_drawing, filename="square_image_%Y_%m_%d_%H-%M-%S-%f.png",
                    simulate=True, allow_transparency=True, proper_line_thickness=True, draw_as_bezier=True,
                    step_size=10)
