import math
from PIL import Image

from pyautonifty.constants import DRAWING_SIZE, GOLDEN_RATIO
from pyautonifty.pos import Pos
from pyautonifty.drawing import Drawing
from pyautonifty.renderer import Renderer


# Draw an image using spiralling dots
def fibonacci_image(drawing, image_filename, n=1500):
    # load image from file
    image = Image.open(image_filename)

    # init result
    width, height = image.size

    for i in range(n):
        # calc radians of rotation and radius from centre
        radians = i * (2 - (2 / GOLDEN_RATIO)) * math.pi
        radius = math.sqrt(i + 1) * DRAWING_SIZE / math.sqrt(n)

        # calc position of dot
        pos = Pos.from_rotational(radians, radius)

        # calc size of dot from image brightness
        image_pos = round((pos.copy() / DRAWING_SIZE) * width)
        colour = list(image.getpixel((image_pos.x, image_pos.y)))
        colour.append(1)
        brightness = 1 - ((0.2126 * colour[0] + 0.7152 * colour[1] + 0.0722 * colour[2]) / 265)

        # draw dot
        drawing.add_point(pos, colour, brightness * DRAWING_SIZE / math.sqrt(n) / 2)

    return drawing


if __name__ == "__main__":
    example_drawing = fibonacci_image(Drawing(), "example.jpg")

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