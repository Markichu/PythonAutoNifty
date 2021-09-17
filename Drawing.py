import json
import random
import pygame
import os
import time
import numpy as np

from Pos import Pos
from helperFns import get_bezier_curve
from constants import DRAWING_SIZE, DEFAULT_BRUSH_RADIUS, MIN_BRUSH_RADIUS, BLACK, WHITE, TITLE_BAR_HEIGHT, BORDER_WIDTH


# The Drawing class contains all the code required to produce an output.txt file.
# Copy and paste contents of output.txt code (Javascript) into the web browser on the Create mode of Nifty Ink,
# and it will draw whatever you have coded onto the Nifty Ink canvas.
# Options exist to either overwrite existing canvas, or add a layer on top.

class Drawing:
    def __init__(self):
        self.object = {"lines": [],
                       "width": DRAWING_SIZE,
                       "height": DRAWING_SIZE}

    # Create a round dot / point at the desired location
    def add_point(self, pos, colour, brush_radius):
        point = pos.point()
        line = {"points": [point, point],
                "brushColor": "rgba({},{},{},{})".format(*colour),
                "brushRadius": brush_radius}
        self.object["lines"].append(line)

    # Use a large dot to colour the whole canvas
    def add_background(self, colour):
        # 0.71 is approx square root of 0.5
        self.add_point(Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2), colour, DRAWING_SIZE * 0.71)

    # Add a gradient between two points
    def add_gradient(self, pos1, pos2, colour1, colour2, divisions=30):
        r_step = (colour2[0] - colour1[0]) / divisions
        g_step = (colour2[1] - colour1[1]) / divisions
        b_step = (colour2[2] - colour1[2]) / divisions
        a_step = (colour2[3] - colour1[3]) / divisions
        size_step = (pos2.y - pos1.y) / divisions
        brush_radius = ((pos2.y - pos1.y) / (divisions - 1))

        for i in range(divisions + 1):
            colour = (colour1[0] + (r_step * i),
                      colour1[1] + (g_step * i),
                      colour1[2] + (b_step * i),
                      colour1[3] + (a_step * i))
            line_pos1 = Pos(pos1.x, pos1.y + (size_step * i))
            line_pos2 = Pos(pos2.x, pos1.y + (size_step * i))
            self.add_straight_line(line_pos1, line_pos2, colour, brush_radius)

    # Add a straight line between two positions on the canvas
    def add_straight_line(self, pos1, pos2, colour, brush_radius):
        point1 = pos1.point()
        point2 = pos2.point()
        line = {"points": [point1, point2],
                "brushColor": "rgba({},{},{},{})".format(*colour),
                "brushRadius": brush_radius}
        self.object["lines"].append(line)

    # Add a curved line between a list of points (Pos) on the canvas
    # Note - this line is curved on Nifty Ink
    def add_quadratic_bezier_curve(self, pos_list, colour, brush_radius, enclosed_path=False):
        points_list = []
        for pos in pos_list:
            points_list.append(pos.point())
        if enclosed_path:
            points_list.append(pos_list[0].point())
        line = {"points": points_list,
                "brushColor": "rgba({},{},{},{})".format(*colour),
                "brushRadius": brush_radius}
        self.object["lines"].append(line)

    # Add a series of straight line segments between a list of points (Pos) on the canvas
    def add_line(self, pos_list, colour, brush_radius, enclosed_path=False):
        # create points for square
        points_list = [pos_list[0].point()]
        for pos in pos_list[1:-1]:
            points_list.append(pos.point())
            points_list.append(pos.point())
        points_list.append(pos_list[-1].point())
        if enclosed_path:
            points_list.append(pos_list[-1].point())
            points_list.append(pos_list[0].point())
        line = {"points": points_list,
                "brushColor": "rgba({},{},{},{})".format(*colour),
                "brushRadius": brush_radius}
        self.object["lines"].append(line)

    # Add a pause to the canvas, using a point off the canvas
    def add_pause(self, length):
        point = {"x": -10, "y": -10}
        line = {"points": [point for _ in range(length)],
                "brushColor": "rgba({},{},{},{})".format(*(0, 0, 0, 0)),
                "brushRadius": 0}
        self.object["lines"].append(line)

    # Add a square to the canvas
    # The degree of roundedness of the corners is determined by the brush radius
    def add_rounded_square(self, centre_pos, width, colour, brush_radius=DEFAULT_BRUSH_RADIUS):
        # init corners to outer positions
        corners = [Pos(0, 0),
                   Pos(0, width),
                   Pos(width, width),
                   Pos(width, 0)]
        for i, corner in enumerate(corners):
            corners[i] = centre_pos - Pos(width / 2, width / 2) + corner

        # Checked (internal) brush radius should be larger than minimum in defaults,
        # and then smaller than half of the square width
        br2 = min(width / 2, max(MIN_BRUSH_RADIUS, brush_radius))

        # calculate line_count, this must be a whole number.
        line_count = round(width / (2 * br2))

        # calculate inner corners from outer and brush
        offsets = [Pos(br2, br2),
                   Pos(br2, -br2),
                   Pos(-br2, -br2),
                   Pos(-br2, br2)]
        for i, corner in enumerate(corners):
            corners[i] = corner + offsets[i]

        # do outer line
        result_corners = corners + [corners[0]]

        # do filling lines. line_step is approximately 2 * br2
        line_step = (width - br2 * 2) / line_count
        for i in range(1, line_count):
            result_corners.append(corners[0].copy() + Pos(line_step * i, 0) + Pos(0, br2))
            result_corners.append(corners[1].copy() + Pos(line_step * i, 0) + Pos(0, -br2))
        self.add_line(result_corners, colour, br2)

    # Write text onto the canvas using a custom font specified below
    def write(self, pos, lines, font_size, line_spacing=1.15, colour=BLACK):
        line_pos = pos.copy()
        y_offset = Pos(0, font_size * line_spacing)
        font = {"a": ([[Pos(0.1, 1), Pos(0.5, 0)],
                       [Pos(0.5, 0), Pos(0.9, 1)],
                       [Pos(0.2, 0.8), Pos(0.8, 0.8)]], 1),
                "b": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.1, 0.5)],
                       [Pos(0.1, 0.5), Pos(0.9, 0.5), Pos(0.9, 1), Pos(0.1, 1)]], 1),
                "c": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7)]], 1),
                "d": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 1), Pos(0.1, 1)]], 1),
                "e": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.1, 0.5), Pos(0.6, 0.5)],
                       [Pos(0.1, 1), Pos(0.9, 1)]], 1),
                "f": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.1, 0.5), Pos(0.6, 0.5)]], 1),
                "g": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7), Pos(0.9, 0.5)],
                       [Pos(0.5, 0.5), Pos(0.9, 0.5)]], 1),
                "h": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0.5), Pos(0.9, 0.5)],
                       [Pos(0.9, 0), Pos(0.9, 1)]], 1),
                "i": ([[Pos(0.1, 0), Pos(0.1, 1)]], 0.2),
                "j": ([[Pos(0.6, 0), Pos(0.6, 0.7), Pos(0.6, 0.7), Pos(0.6, 1), Pos(0.1, 1)]], 0.7),
                "k": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0.6), Pos(0.9, 0)],
                       [Pos(0.25, 0.5), Pos(0.9, 1)]], 1),
                "l": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 1), Pos(0.7, 1)]], 0.8),
                "m": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.6, 1)],
                       [Pos(0.6, 1), Pos(1.1, 0)],
                       [Pos(1.1, 0), Pos(1.1, 1)]], 1.2),
                "n": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 1)],
                       [Pos(0.9, 0), Pos(0.9, 1)]], 1),
                "o": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7), Pos(0.9, 0.3)]], 1),
                "p": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.1, 0.5)]], 1),
                "q": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7), Pos(0.9, 0.3)],
                       [Pos(0.7, 0.8), Pos(0.9, 1)]], 1),
                "r": ([[Pos(0.1, 0), Pos(0.1, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.1, 0.5)],
                       [Pos(0.6, 0.5), Pos(0.9, 1)]], 1),
                "s": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.5), Pos(0.9, 0.5), Pos(0.9, 1), Pos(0.1, 1),
                        Pos(0.1, 0.7)]], 1),
                "t": ([[Pos(0.5, 0), Pos(0.5, 1)],
                       [Pos(0.1, 0), Pos(0.9, 0)]], 1),
                "u": ([[Pos(0.1, 0), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.7), Pos(0.9, 0)]], 1),
                "v": ([[Pos(0.1, 0), Pos(0.5, 1)],
                       [Pos(0.5, 1), Pos(0.9, 0)]], 1),
                "w": ([[Pos(0.1, 0), Pos(0.4, 1)],
                       [Pos(0.4, 1), Pos(0.7, 0)],
                       [Pos(0.7, 0), Pos(1, 1)],
                       [Pos(1, 1), Pos(1.3, 0)]], 1.4),
                "x": ([[Pos(0.1, 0), Pos(0.9, 1)],
                       [Pos(0.1, 1), Pos(0.9, 0)]], 1),
                "y": ([[Pos(0.1, 0), Pos(0.5, 0.6)],
                       [Pos(0.5, 0.6), Pos(0.9, 0)],
                       [Pos(0.5, 0.6), Pos(0.5, 1)]], 1),
                "z": ([[Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.9, 0), Pos(0.1, 1)],
                       [Pos(0.1, 1), Pos(0.9, 1)]], 1),
                " ": ([], 0.75),
                "#": ([[Pos(0.1, 0.3), Pos(0.9, 0.3)],
                       [Pos(0.1, 0.7), Pos(0.9, 0.7)],
                       [Pos(0.2, 1), Pos(0.4, 0)],
                       [Pos(0.6, 1), Pos(0.8, 0)]], 1),
                "=": ([[Pos(0.1, 0.3), Pos(0.9, 0.3)],
                       [Pos(0.1, 0.7), Pos(0.9, 0.7)]], 1),
                "'": ([[Pos(0.1, 0), Pos(0.1, 0.4)]], 0.2),
                "\"": ([[Pos(0.1, 0), Pos(0.1, 0.4)],
                        [Pos(0.2, 0), Pos(0.2, 0.4)]], 0.3),
                ".": ([[Pos(0.1, 1), Pos(0.1, 1)]], 0.2),
                "!": ([[Pos(0.1, 0), Pos(0.1, 0.8)],
                       [Pos(0.1, 1), Pos(0.1, 1)]], 0.2),
                "1": ([[Pos(0.1, 1), Pos(0.9, 1)],
                       [Pos(0.5, 0), Pos(0.5, 1)],
                       [Pos(0.5, 0), Pos(0.1, 0.4)]], 1),
                "2": ([[Pos(0.1, 0.3), Pos(0.1, 0), Pos(0.8, 0), Pos(0.8, 0.4), Pos(0.1, 1)],
                       [Pos(0.1, 1), Pos(0.9, 1)]], 1),
                "3": ([[Pos(0.1, 0.2), Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.4, 0.5)],
                       [Pos(0.1, 0.8), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.5), Pos(0.4, 0.5)]], 1),
                "4": ([[Pos(0.1, 0.8), Pos(0.9, 0.8)],
                       [Pos(0.7, 0), Pos(0.7, 1)],
                       [Pos(0.1, 0.8), Pos(0.7, 0)]], 1),
                "5": ([[Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.1, 0.4), Pos(0.1, 0)],
                       [Pos(0.1, 0.4), Pos(0.9, 0.4), Pos(0.9, 1), Pos(0.1, 1), Pos(0.1, 0.8)]], 1),
                "6": ([[Pos(0.9, 0.2), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.4),
                        Pos(0.1, 0.6), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.5), Pos(0.1, 0.5), Pos(0.1, 0.6)]], 1),
                "7": ([[Pos(0.1, 0.2), Pos(0.1, 0)],
                       [Pos(0.1, 0), Pos(0.9, 0)],
                       [Pos(0.9, 0), Pos(0.4, 1)]], 1),
                "8": ([[Pos(0.5, 0.5), Pos(0.1, 0.5), Pos(0.1, 0), Pos(0.9, 0), Pos(0.9, 0.5), Pos(0.5, 0.5)],
                       [Pos(0.5, 0.5), Pos(0.1, 0.5), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.5), Pos(0.5, 0.5)]], 1),
                "9": ([[Pos(0.1, 0.8), Pos(0.1, 1), Pos(0.9, 1), Pos(0.9, 0.6),
                        Pos(0.9, 0.4), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.5), Pos(0.9, 0.5), Pos(0.9, 0.4)]], 1),
                "0": ([[Pos(0.9, 0.3), Pos(0.9, 0), Pos(0.1, 0), Pos(0.1, 0.3), Pos(0.1, 0.7), Pos(0.1, 1), Pos(0.9, 1),
                        Pos(0.9, 0.7), Pos(0.9, 0.3)],
                       [Pos(0.1, 0.3), Pos(0.9, 0.7)]], 1)}

        def write_char(pos, char):
            # resize char to font size
            this_char = []
            x_offset = Pos(font_size * font[char][1], 0)
            for line in font[char][0]:
                this_line = []
                for point in line:
                    this_line.append((point.copy() * font_size) + pos)
                this_char.append(this_line)

            # draw character
            for line in this_char:
                self.add_quadratic_bezier_curve(line, colour, font_size / 30)

            return pos + x_offset

        for line in lines:
            for char in line:
                if char.lower() in font:
                    pos = write_char(pos.copy(), char.lower())
            line_pos = line_pos + y_offset
            pos = line_pos.copy()

    # Randomly reorder the lines
    # Nifty Ink will animate in an interesting random order
    def shuffle_lines(self):
        random.shuffle(self.object["lines"])

    # Use this to make your drawings slightly less precise, but also reduce their size a lot
    # This can be useful if browser local storage limits start affecting your large drawings
    def round_floats(self):
        for line in self.object['lines']:
            line['brushRadius'] = round(line['brushRadius'])
            for point in line['points']:
                point['x'] = round(point['x'])
                point['y'] = round(point['y'])

    # Save raw drawing data to a file for later use.
    def export_raw_data(self, file_name, indent=4):
        with open(file_name, "w") as file:
            file.write(json.dumps(self.object, indent=indent))
        print(f"Exported raw data to {file_name}.")

    # Load a raw data file and replace the contents of this drawing.
    def import_raw_data(self, file_name):
        with open(file_name, "r") as file:
            drawing_data = json.loads(file.read())
        self.object = drawing_data
        print(f"Imported raw data from {file_name}.")

    # Adds a specified drawing as a new layer on top of this drawing
    # TODO: Handle canvas size scaling (which we currently don't change anyway)
    def add_layer(self, drawing):
        self.object['lines'].extend(drawing.object['lines'])

    # Adds a new layer to the drawing, loaded from a specified file.
    def add_layer_from_file(self, file_name):
        with open(file_name, "r") as file:
            drawing_data = json.loads(file.read())
        drawing = Drawing()
        drawing.object = drawing_data
        self.add_layer(drawing)
        print(f"Added {file_name} as a new layer.")

    # Shrink or expand all the stored lines using multiplication
    def __mul__(self, shrink_size):
        # origin for shrinking
        origin = Pos(DRAWING_SIZE / 2, DRAWING_SIZE / 2)

        # shrink each point
        for line_index in range(len(self.object["lines"])):
            line = self.object["lines"][line_index]
            for point_index in range(len(line["points"])):
                point = line["points"][point_index]
                point_pos = Pos(point["x"], point["y"])
                point_pos -= origin
                point_pos *= shrink_size
                point_pos += origin
                line["points"][point_index] = point_pos.point()
        return self

    # Render the lines to preview in Pygame
    def render(self, pygame_scale=None, headless=False, filename="output.png", simulate=False, speed=None,
               allow_transparency=False, fake_transparency=False, proper_line_thickness=False, draw_as_bezier=False,
               step_size=10):
        # Set a fake video driver to hide output
        if headless:
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
            # No screen to get the dimensions, just render at normal size
            if pygame_scale is None:
                pygame_scale = 1

        if step_size < 2:
            step_size = 2

        pygame.init()

        # Position the window perfectly if it's not headless
        if not headless:
            info_object = pygame.display.Info()
            smallest_dimension = min(info_object.current_w, info_object.current_h)

            x = round((info_object.current_w - (smallest_dimension - TITLE_BAR_HEIGHT - (BORDER_WIDTH * 2))) / 2)
            y = TITLE_BAR_HEIGHT + BORDER_WIDTH
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

            # Scale the window and drawing to the maximum square size
            if pygame_scale is None:
                pygame_scale = (smallest_dimension - TITLE_BAR_HEIGHT - (BORDER_WIDTH * 2)) / DRAWING_SIZE

        # Initialise the window with dimensions
        pygame_x = round(DRAWING_SIZE * pygame_scale)
        pygame_y = round(DRAWING_SIZE * pygame_scale)
        screen = pygame.display.set_mode((pygame_x, pygame_y))

        pygame.display.set_caption("Drawing Render")
        screen.fill(WHITE[:3])
        pygame.display.update()  # Show the background, (so the screen isn't black on drawings that are slow to process)

        def alpha_blend(a, bg, fg):
            return ((1 - a) * fg[0] + a * bg[0],
                    (1 - a) * fg[1] + a * bg[1],
                    (1 - a) * fg[2] + a * bg[2],
                    255)

        def draw_line(surface, colour, start_point, end_point, width, end_caps=False):
            if end_caps:
                pygame.draw.circle(surface, colour, start_point, width / 2)
                pygame.draw.circle(surface, colour, end_point, width / 2)
            if start_point == end_point:
                return
            np.seterr(divide='ignore', invalid='ignore')
            vec_start_point = np.array(start_point)
            vec_end_point = np.array(end_point)
            move_point = vec_end_point - vec_start_point
            norm_move = move_point / np.linalg.norm(move_point)

            rotated_vec = np.array((-norm_move[1], norm_move[0])) * width / 2
            start_point_1 = vec_start_point + rotated_vec
            start_point_2 = vec_start_point - rotated_vec
            end_point_1 = vec_end_point + rotated_vec
            end_point_2 = vec_end_point - rotated_vec

            pygame.draw.polygon(surface, colour, [start_point_1, start_point_2, end_point_2, end_point_1], width=0)

        def draw_lines(surface, colour, pts, width, end_caps=False):
            last_point = None
            for pt in pts:
                if last_point:
                    draw_line(surface, colour, last_point, pt, width, end_caps=end_caps)
                last_point = pt

        def get_midpoint(p1, p2):
            x = p1[0] + (p2[0] - p1[0]) / 2
            y = p1[1] + (p2[1] - p1[1]) / 2
            return [x, y]

        def draw_quadratic_bezier_curve_line(surface, colour, pts, width, end_caps=False, step_size=40):

            last_midpoint = pts[0]
            midpoint = last_midpoint
            p2 = last_midpoint

            for i in range(len(pts)):
                p1 = pts[i]
                try:
                    p2 = pts[i + 1]

                    midpoint = get_midpoint(p1, p2)
                    # TODO: Write some code to create an appropriate step_size, likely based on the bezier curve length
                    bezier_curve_points = get_bezier_curve((last_midpoint, p1, midpoint), step_size=step_size, end_point=True)
                    draw_lines(surface, colour, bezier_curve_points, width, end_caps=end_caps)

                    last_midpoint = midpoint
                except IndexError:  # Draw the last point as a straight line to finish
                    draw_line(surface, colour, midpoint, p2, width, end_caps=end_caps)

        for line in self.object["lines"]:
            brush_radius = line["brushRadius"] * pygame_scale
            colour = [float(cell) for cell in list(line["brushColor"][5:-1].split(","))]
            colour[3] *= 255  # Pygame expects an alpha between 0 and 255, not 0 and 1.

            points = []
            if colour[3] != 255 and allow_transparency:  # If the brushColour is transparent, draw with transparency
                target_surface = pygame.Surface((pygame_x, pygame_y))
                if colour[:-1] != [0,0,0]:
                    target_surface.set_colorkey(BLACK)
                else:  # Handle the black edge case
                    target_surface.set_colorkey(WHITE)
                    target_surface.fill((255,255,255,0))
                target_surface.set_alpha(round(colour[3]))
            else:  # If the brushColour is opaque, draw with no transparency
                if fake_transparency:
                    colour = alpha_blend(colour[3] / 255, colour[:-1], [255, 255, 255])
                target_surface = screen

            for index, point in enumerate(line["points"]):
                this_point = (point["x"] * pygame_scale, point["y"] * pygame_scale)
                points.append(this_point)
                if not proper_line_thickness:
                    pygame.draw.circle(target_surface, colour, this_point, int(brush_radius))
            if proper_line_thickness:
                if draw_as_bezier:
                    draw_quadratic_bezier_curve_line(target_surface, colour, points, brush_radius * 2, end_caps=True, step_size=step_size)
                else:
                    draw_lines(target_surface, colour, points, brush_radius * 2, end_caps=True)
            else:
                pygame.draw.lines(target_surface, colour, False, points, int(brush_radius * 2))

            if colour[3] != 255 and allow_transparency:  # Required for transparency
                screen.blit(target_surface, (0, 0))

            if simulate:  # Update the drawing line by line to see the drawing process
                pygame.display.update()
                if speed and speed != 0:
                    time.sleep(speed / 100)

            # Ensure that no events, such as pygame being closed are ignored.
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    # Exits before the image is finished, does not take screenshot.
                    return

        # update screen to render the final result of the drawing
        pygame.display.update()
        print(f"\nSaving {filename}")
        pygame.image.save(screen, filename)
        print("Saved.")

        # enter a loop to prevent pygame from ending
        running = True
        while running and not headless:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    running = False
                    break
            time.sleep(0.2)  # Sleep for a short time. Prevents continual use of CPU.

    # Nifty import method 1 - deprecated
    def to_nifty_show_import(self):
        return "drawingCanvas.current.loadSaveData(\"" + json.dumps(self.object).replace('"', '\\"') + "\", false)"

    # Nifty import method 2 - overwrite canvas
    def to_nifty_import(self):
        # Use a minified LZString
        # https://raw.githubusercontent.com/pieroxy/lz-string/master/libs/lz-string.min.js
        lz_string = """var LZString=function(){function o(o,r){if(!t[o]){t[o]={};for(var n=0;n<o.length;n++)t[o][o.charAt(n)]=n}return t[o][r]}var r=String.fromCharCode,n="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$",t={},i={compressToBase64:function(o){if(null==o)return"";var r=i._compress(o,6,function(o){return n.charAt(o)});switch(r.length%4){default:case 0:return r;case 1:return r+"===";case 2:return r+"==";case 3:return r+"="}},decompressFromBase64:function(r){return null==r?"":""==r?null:i._decompress(r.length,32,function(e){return o(n,r.charAt(e))})},compressToUTF16:function(o){return null==o?"":i._compress(o,15,function(o){return r(o+32)})+" "},decompressFromUTF16:function(o){return null==o?"":""==o?null:i._decompress(o.length,16384,function(r){return o.charCodeAt(r)-32})},compressToUint8Array:function(o){for(var r=i.compress(o),n=new Uint8Array(2*r.length),e=0,t=r.length;t>e;e++){var s=r.charCodeAt(e);n[2*e]=s>>>8,n[2*e+1]=s%256}return n},decompressFromUint8Array:function(o){if(null===o||void 0===o)return i.decompress(o);for(var n=new Array(o.length/2),e=0,t=n.length;t>e;e++)n[e]=256*o[2*e]+o[2*e+1];var s=[];return n.forEach(function(o){s.push(r(o))}),i.decompress(s.join(""))},compressToEncodedURIComponent:function(o){return null==o?"":i._compress(o,6,function(o){return e.charAt(o)})},decompressFromEncodedURIComponent:function(r){return null==r?"":""==r?null:(r=r.replace(/ /g,"+"),i._decompress(r.length,32,function(n){return o(e,r.charAt(n))}))},compress:function(o){return i._compress(o,16,function(o){return r(o)})},_compress:function(o,r,n){if(null==o)return"";var e,t,i,s={},p={},u="",c="",a="",l=2,f=3,h=2,d=[],m=0,v=0;for(i=0;i<o.length;i+=1)if(u=o.charAt(i),Object.prototype.hasOwnProperty.call(s,u)||(s[u]=f++,p[u]=!0),c=a+u,Object.prototype.hasOwnProperty.call(s,c))a=c;else{if(Object.prototype.hasOwnProperty.call(p,a)){if(a.charCodeAt(0)<256){for(e=0;h>e;e++)m<<=1,v==r-1?(v=0,d.push(n(m)),m=0):v++;for(t=a.charCodeAt(0),e=0;8>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1}else{for(t=1,e=0;h>e;e++)m=m<<1|t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t=0;for(t=a.charCodeAt(0),e=0;16>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1}l--,0==l&&(l=Math.pow(2,h),h++),delete p[a]}else for(t=s[a],e=0;h>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1;l--,0==l&&(l=Math.pow(2,h),h++),s[c]=f++,a=String(u)}if(""!==a){if(Object.prototype.hasOwnProperty.call(p,a)){if(a.charCodeAt(0)<256){for(e=0;h>e;e++)m<<=1,v==r-1?(v=0,d.push(n(m)),m=0):v++;for(t=a.charCodeAt(0),e=0;8>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1}else{for(t=1,e=0;h>e;e++)m=m<<1|t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t=0;for(t=a.charCodeAt(0),e=0;16>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1}l--,0==l&&(l=Math.pow(2,h),h++),delete p[a]}else for(t=s[a],e=0;h>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1;l--,0==l&&(l=Math.pow(2,h),h++)}for(t=2,e=0;h>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1;for(;;){if(m<<=1,v==r-1){d.push(n(m));break}v++}return d.join("")},decompress:function(o){return null==o?"":""==o?null:i._decompress(o.length,32768,function(r){return o.charCodeAt(r)})},_decompress:function(o,n,e){var t,i,s,p,u,c,a,l,f=[],h=4,d=4,m=3,v="",w=[],A={val:e(0),position:n,index:1};for(i=0;3>i;i+=1)f[i]=i;for(p=0,c=Math.pow(2,2),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;switch(t=p){case 0:for(p=0,c=Math.pow(2,8),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;l=r(p);break;case 1:for(p=0,c=Math.pow(2,16),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;l=r(p);break;case 2:return""}for(f[3]=l,s=l,w.push(l);;){if(A.index>o)return"";for(p=0,c=Math.pow(2,m),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;switch(l=p){case 0:for(p=0,c=Math.pow(2,8),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;f[d++]=r(p),l=d-1,h--;break;case 1:for(p=0,c=Math.pow(2,16),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;f[d++]=r(p),l=d-1,h--;break;case 2:return w.join("")}if(0==h&&(h=Math.pow(2,m),m++),f[l])v=f[l];else{if(l!==d)return null;v=s+s.charAt(0)}w.push(v),f[d++]=s+v.charAt(0),h--,s=v,0==h&&(h=Math.pow(2,m),m++)}}};return i}();"function"==typeof define&&define.amd?define(function(){return LZString}):"undefined"!=typeof module&&null!=module&&(module.exports=LZString);"""

        # Set up the json string
        json_string = "var json_string = \"" + json.dumps(self.object).replace("\"", "\\\"").replace(" ", "") + "\";"

        # Update the session storage with the escaped unicode point compressed json string
        local_storage = """window.localStorage.setItem("drawing", JSON.stringify(LZString.compress(json_string)));"""

        # Refresh the Create Ink page to show the new Canvas Ink
        refresh_page = "location.reload();"

        return lz_string + json_string + local_storage + refresh_page

    # Nifty import method 3 - add layer on top of canvas
    def to_nifty_add_layer_import(self):
        # Use a minified LZString
        # https://raw.githubusercontent.com/pieroxy/lz-string/master/libs/lz-string.min.js
        lz_string = """var LZString=function(){function o(o,r){if(!t[o]){t[o]={};for(var n=0;n<o.length;n++)t[o][o.charAt(n)]=n}return t[o][r]}var r=String.fromCharCode,n="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$",t={},i={compressToBase64:function(o){if(null==o)return"";var r=i._compress(o,6,function(o){return n.charAt(o)});switch(r.length%4){default:case 0:return r;case 1:return r+"===";case 2:return r+"==";case 3:return r+"="}},decompressFromBase64:function(r){return null==r?"":""==r?null:i._decompress(r.length,32,function(e){return o(n,r.charAt(e))})},compressToUTF16:function(o){return null==o?"":i._compress(o,15,function(o){return r(o+32)})+" "},decompressFromUTF16:function(o){return null==o?"":""==o?null:i._decompress(o.length,16384,function(r){return o.charCodeAt(r)-32})},compressToUint8Array:function(o){for(var r=i.compress(o),n=new Uint8Array(2*r.length),e=0,t=r.length;t>e;e++){var s=r.charCodeAt(e);n[2*e]=s>>>8,n[2*e+1]=s%256}return n},decompressFromUint8Array:function(o){if(null===o||void 0===o)return i.decompress(o);for(var n=new Array(o.length/2),e=0,t=n.length;t>e;e++)n[e]=256*o[2*e]+o[2*e+1];var s=[];return n.forEach(function(o){s.push(r(o))}),i.decompress(s.join(""))},compressToEncodedURIComponent:function(o){return null==o?"":i._compress(o,6,function(o){return e.charAt(o)})},decompressFromEncodedURIComponent:function(r){return null==r?"":""==r?null:(r=r.replace(/ /g,"+"),i._decompress(r.length,32,function(n){return o(e,r.charAt(n))}))},compress:function(o){return i._compress(o,16,function(o){return r(o)})},_compress:function(o,r,n){if(null==o)return"";var e,t,i,s={},p={},u="",c="",a="",l=2,f=3,h=2,d=[],m=0,v=0;for(i=0;i<o.length;i+=1)if(u=o.charAt(i),Object.prototype.hasOwnProperty.call(s,u)||(s[u]=f++,p[u]=!0),c=a+u,Object.prototype.hasOwnProperty.call(s,c))a=c;else{if(Object.prototype.hasOwnProperty.call(p,a)){if(a.charCodeAt(0)<256){for(e=0;h>e;e++)m<<=1,v==r-1?(v=0,d.push(n(m)),m=0):v++;for(t=a.charCodeAt(0),e=0;8>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1}else{for(t=1,e=0;h>e;e++)m=m<<1|t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t=0;for(t=a.charCodeAt(0),e=0;16>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1}l--,0==l&&(l=Math.pow(2,h),h++),delete p[a]}else for(t=s[a],e=0;h>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1;l--,0==l&&(l=Math.pow(2,h),h++),s[c]=f++,a=String(u)}if(""!==a){if(Object.prototype.hasOwnProperty.call(p,a)){if(a.charCodeAt(0)<256){for(e=0;h>e;e++)m<<=1,v==r-1?(v=0,d.push(n(m)),m=0):v++;for(t=a.charCodeAt(0),e=0;8>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1}else{for(t=1,e=0;h>e;e++)m=m<<1|t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t=0;for(t=a.charCodeAt(0),e=0;16>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1}l--,0==l&&(l=Math.pow(2,h),h++),delete p[a]}else for(t=s[a],e=0;h>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1;l--,0==l&&(l=Math.pow(2,h),h++)}for(t=2,e=0;h>e;e++)m=m<<1|1&t,v==r-1?(v=0,d.push(n(m)),m=0):v++,t>>=1;for(;;){if(m<<=1,v==r-1){d.push(n(m));break}v++}return d.join("")},decompress:function(o){return null==o?"":""==o?null:i._decompress(o.length,32768,function(r){return o.charCodeAt(r)})},_decompress:function(o,n,e){var t,i,s,p,u,c,a,l,f=[],h=4,d=4,m=3,v="",w=[],A={val:e(0),position:n,index:1};for(i=0;3>i;i+=1)f[i]=i;for(p=0,c=Math.pow(2,2),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;switch(t=p){case 0:for(p=0,c=Math.pow(2,8),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;l=r(p);break;case 1:for(p=0,c=Math.pow(2,16),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;l=r(p);break;case 2:return""}for(f[3]=l,s=l,w.push(l);;){if(A.index>o)return"";for(p=0,c=Math.pow(2,m),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;switch(l=p){case 0:for(p=0,c=Math.pow(2,8),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;f[d++]=r(p),l=d-1,h--;break;case 1:for(p=0,c=Math.pow(2,16),a=1;a!=c;)u=A.val&A.position,A.position>>=1,0==A.position&&(A.position=n,A.val=e(A.index++)),p|=(u>0?1:0)*a,a<<=1;f[d++]=r(p),l=d-1,h--;break;case 2:return w.join("")}if(0==h&&(h=Math.pow(2,m),m++),f[l])v=f[l];else{if(l!==d)return null;v=s+s.charAt(0)}w.push(v),f[d++]=s+v.charAt(0),h--,s=v,0==h&&(h=Math.pow(2,m),m++)}}};return i}();"function"==typeof define&&define.amd?define(function(){return LZString}):"undefined"!=typeof module&&null!=module&&(module.exports=LZString);"""

        # Raw json string
        raw_json_string = json.dumps(self.object).replace("\"", "\\\"").replace(" ", "")

        # Set up the json string of the new data
        json_object = "var json_object = JSON.parse(\"" + raw_json_string + "\");"

        # Save the canvas if there are any unsaved changes
        save_canvas = """var button = document.getElementsByTagName("button");
                         for (var i = 0; i < button.length; i++) {
                           if (button[i].innerHTML.includes("SAVE *")) {
                             button[i].click();
                           }
                         };"""

        # Get the current saved data from the localStorage
        local_storage_data = """var raw_storage = window.localStorage.getItem("drawing");"""

        # Scale all the points of the newly imported data to the current saved data canvas size
        update_data = """if (raw_storage == "" || raw_storage == "undefined") {
                            var json_string = JSON.stringify(json_object)
                         } else {
                            var decompressed_data = LZString.decompress(JSON.parse(raw_storage));
                            decompressed_data = JSON.parse(decompressed_data);
                            var saved_height = decompressed_data['height'];
                            var saved_width = decompressed_data['width'];
                            var imported_height = json_object['height'];
                            var imported_width = json_object['width'];

                            var scale_height = saved_height / imported_height;
                            var scale_width = saved_width / imported_width;
                            var scale_brush_radius = Math.max(scale_height, scale_width)

                            json_object['lines'].forEach(function(part, i) {
                              this[i]['brushRadius'] = this[i]['brushRadius']*scale_brush_radius;
                              this[i]['points'].forEach(function(part, j) {
                                this[j]['x'] = this[j]['x']*scale_width;
                                this[j]['y'] = this[j]['y']*scale_height;
                              }, this[i]['points']);
                            }, json_object['lines']);

                            decompressed_data['lines'] = decompressed_data['lines'].concat(json_object['lines']);
                            var json_string = JSON.stringify(decompressed_data);
                         };"""

        # Update the session storage with the escaped unicode point compressed json string
        local_storage = """window.localStorage.setItem("drawing", JSON.stringify(LZString.compress(json_string)));"""

        # Refresh the Create Ink page to show the new Canvas Ink Layer
        refresh_page = "location.reload();"

        return lz_string + json_object + save_canvas + local_storage_data + update_data + local_storage + refresh_page
