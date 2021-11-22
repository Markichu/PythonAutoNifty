import datetime
import os
import time
import numpy as np

# Hide the Pygame support message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = str()
import pygame

from constants import BLACK, WHITE, DRAWING_SIZE, TITLE_BAR_HEIGHT, BORDER_WIDTH
from helper_fns import get_bezier_curve, alpha_blend


class Renderer:
    def __init__(self, headless=False, pygame_scale=None):
        self.pygame_scale = pygame_scale
        self.headless = headless

        # Set a fake video driver to hide output
        if headless:
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
            # No screen to get the dimensions, just render at normal size
            if pygame_scale is None:
                self.pygame_scale = 1

        # Init pygame
        pygame.init()

        # Reposition and change size of surface to account for title bar
        if not headless:
            info_object = pygame.display.Info()
            smallest_dimension = min(info_object.current_w, info_object.current_h)

            x = round((info_object.current_w - (smallest_dimension - TITLE_BAR_HEIGHT - (BORDER_WIDTH * 2))) / 2)
            y = TITLE_BAR_HEIGHT + BORDER_WIDTH
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

            # Scale the window and drawing to the maximum square size
            if pygame_scale is None:
                self.pygame_scale = (smallest_dimension - TITLE_BAR_HEIGHT - (BORDER_WIDTH * 2)) / DRAWING_SIZE

        # Initialise the window with dimensions
        self.pygame_x = round(DRAWING_SIZE * self.pygame_scale)
        self.pygame_y = round(DRAWING_SIZE * self.pygame_scale)
        self.screen = pygame.display.set_mode((self.pygame_x, self.pygame_y))
        pygame.display.set_caption("Drawing Render")



    # Render the lines to preview in Pygame
    def render(self, drawing, filename="output.png", simulate=False, speed=None,
               allow_transparency=False, fake_transparency=False, proper_line_thickness=False, draw_as_bezier=False,
               step_size=10, save_transparent_bg=False, green_screen_colour=(0, 177, 64, 255), timestamp=False,
               timestamp_format="%Y_%m_%d_%H_%M_%S_%f_"):

        if step_size < 2:
            step_size = 2

        if save_transparent_bg:
            self.screen.fill(green_screen_colour)
        else:
            self.screen.fill(WHITE)
        # self.screen.set_alpha(255)  CHECK NOT USED
        pygame.display.update()  # Show the background, (so the screen isn't black on drawings that are slow to process)

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
            x = (p1[0] + p2[0]) / 2
            y = (p1[1] + p2[1]) / 2
            return [x, y]

        def draw_quadratic_bezier_curve_line(surface, colour, pts, width, end_caps=False, step_size=40):
            if pts:
                last_midpoint = pts[0]
                midpoint = last_midpoint
                p2 = last_midpoint

                for i in range(len(pts)):
                    p1 = pts[i]
                    try:
                        p2 = pts[i + 1]

                        midpoint = get_midpoint(p1, p2)
                        # TODO: Write some code to create an appropriate step_size, likely based on the bezier curve length
                        bezier_curve_points = get_bezier_curve((last_midpoint, p1, midpoint), step_size=step_size,
                                                               end_point=True)
                        draw_lines(surface, colour, bezier_curve_points, width, end_caps=end_caps)

                        last_midpoint = midpoint
                    except IndexError:  # Draw the last point as a straight line to finish
                        draw_line(surface, colour, midpoint, p2, width, end_caps=end_caps)

        for line in drawing:
            brush_radius = line["brushRadius"] * self.pygame_scale
            if "rgba" in line["brushColor"]:
                colour = [float(cell) for cell in list(line["brushColor"][5:-1].split(","))]
                colour[3] *= 255
            else:
                colour = [float(cell) for cell in list(line["brushColor"][4:-1].split(","))]
                colour.append(255)

            points = []
            if colour[3] != 255 and allow_transparency:  # If the brushColour is transparent, draw with transparency
                target_surface = pygame.Surface((self.pygame_x, self.pygame_y), 0, 32)
                if colour[:-1] != [0, 0, 0]:
                    target_surface.set_colorkey(BLACK)
                else:  # Handle the black edge case
                    target_surface.set_colorkey(WHITE)
                    target_surface.fill((255, 255, 255, 0))
                target_surface.set_alpha(round(colour[3]))
            else:  # If the brushColour is opaque, draw with no transparency
                if fake_transparency:
                    colour = alpha_blend(colour[3] / 255, colour[:-1], [255, 255, 255])
                target_surface = self.screen

            for index, point in enumerate(line["points"]):
                this_point = (point.x * self.pygame_scale, point.y * self.pygame_scale)
                points.append(this_point)
                if not proper_line_thickness:
                    pygame.draw.circle(target_surface, colour, this_point, int(brush_radius))

            if proper_line_thickness:
                if draw_as_bezier:
                    draw_quadratic_bezier_curve_line(target_surface, colour, points, brush_radius * 2,
                                                     end_caps=True, step_size=step_size)
                else:
                    draw_lines(target_surface, colour, points, brush_radius * 2, end_caps=True)
            else:
                pygame.draw.lines(target_surface, colour, False, points, int(brush_radius * 2))

            # Required for transparency
            if colour[3] != 255 and allow_transparency:
                self.screen.blit(target_surface, (0, 0))

            # Update the drawing line by line to see the drawing process
            if simulate:
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

        time_str = datetime.datetime.now().strftime(timestamp_format) if timestamp else ""

        pygame.image.save(self.screen, time_str + filename)

        # TODO: Figure out if Pygame has a method to save a surface with a transparent background
        if save_transparent_bg:
            from PIL import Image
            image_string = pygame.image.tostring(self.screen, 'RGBA', False)
            img = Image.frombytes("RGBA", self.screen.get_size(), image_string)

            # https://stackoverflow.com/a/69814643
            def convert_png_transparent(image, dst_file, bg_color=(255, 255, 255)):
                array = np.array(image, dtype=np.ubyte)
                mask = (array[:, :, :3] == bg_color).all(axis=2)
                alpha = np.where(mask, 0, 255)
                array[:, :, -1] = alpha

                Image.fromarray(np.ubyte(array)).save(dst_file, "PNG")

            convert_png_transparent(img, f"{time_str}transparent_{filename}", [*green_screen_colour[:-1]])

        # enter a loop to prevent pygame from ending
        running = True
        while running and not self.headless:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    running = False
                    break
            time.sleep(0.2)  # Sleep for a short time. Prevents continual use of CPU.