import json
import math
import random
import pygame
import os
import time
import numpy as np
import datetime

from Pos import Pos
from font import get_font_character_map, get_reduced_font_character_map
from helperFns import get_bezier_curve, rotate
from constants import DRAWING_SIZE, DEFAULT_BRUSH_RADIUS, MIN_BRUSH_RADIUS, BLACK, WHITE, TITLE_BAR_HEIGHT, BORDER_WIDTH, RED
from fontConstants import DEFAULT_FONT


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

    # This function is only really useful for fonts. TrueTypeFonts have compressed bezier curves.
    # These curves are not in the same form as the midpoint based bezier curves of Nifty.ink
    # This function serves as a "close enough" approximation of converting them to nifty bezier curves, without the slow
    # and wasteful iterative approach which would make fonts draw far slower and not be consistently smooth with curves.
    def add_modified_quadratic_bezier_curve(self, pos_list, colour, brush_radius, enclosed_path=False):

        max_index = len(pos_list)-1

        new_pos_list = []

        for index, point in enumerate(pos_list):
            if index == 0:
                new_pos_list.append(point)
            if index < max_index:
                next_point = pos_list[index+1]
                midpoint = Pos((next_point.x+point.x)/2,(next_point.y+point.y)/2)
                new_pos_list.append(midpoint)
            else:
                # This is the last point in the segment
                if enclosed_path:
                    next_point = pos_list[0]
                    midpoint = Pos((next_point.x + point.x) / 2, (next_point.y + point.y) / 2)
                    new_pos_list.append(midpoint)
                    new_pos_list.append(next_point)
                else:
                    new_pos_list.append(point)
        self.add_quadratic_bezier_curve(new_pos_list, colour, brush_radius, enclosed_path=False)

    # Add a series of straight line segments between a list of points (Pos) on the canvas
    def add_line(self, pos_list, colour, brush_radius, enclosed_path=False):
        # create points for square
        if pos_list:
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

    # Add a bezier curve that is quadratic if you give 3 points, cubic if you give 4 points and so on.
    def add_general_bezier_curve(self, control_points, colour, brush_radius, step_size=40, enclosed_path=False):
        if step_size < 2:
            step_size = 2
        tuple_control_points = [(point.x, point.y) for point in control_points]
        points = get_bezier_curve(tuple_control_points, step_size, end_point=True)
        pos_points = [Pos(point[0], point[1]) for point in points]
        self.add_line(pos_points, colour, brush_radius, enclosed_path=enclosed_path)

    # Add a pause to the canvas, using a point off the canvas
    def add_pause(self, length):
        point = {"x": -10, "y": -10}
        line = {"points": [point for _ in range(length)],
                "brushColor": "rgba({},{},{},{})".format(*(0, 0, 0, 0)),
                "brushRadius": 0}
        self.object["lines"].append(line)

    # Add a square to the canvas
    # The degree of roundedness of the corners is determined by the brush radius
    def add_rounded_square(self, centre_pos, width, colour, brush_radius=DEFAULT_BRUSH_RADIUS, filled=True):
        self.add_rounded_rectangle(centre_pos, width, width, colour, brush_radius=brush_radius, filled=filled)

    # # Add a rectangle to the canvas
    # # The degree of roundedness of the corners is determined by the brush radius
    def add_rounded_rectangle(self, centre_pos, width, height, colour, brush_radius=DEFAULT_BRUSH_RADIUS, filled=True):
        rotate_rectangle = False
        if width > height:
            width, height = height, width
            rotate_rectangle = True

        # init corners to outer positions
        corners = [Pos(0, 0),
                   Pos(0, height),
                   Pos(width, height),
                   Pos(width, 0)]
        for i, corner in enumerate(corners):
            corners[i] = centre_pos - Pos(width / 2, height / 2) + corner

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

        if filled:
            # do filling lines. line_step is approximately 2 * br2
            line_step = (width - br2 * 2) / line_count
            for i in range(1, line_count):
                result_corners.append(corners[0].copy() + Pos(line_step * i, 0) + Pos(0, br2))
                result_corners.append(corners[1].copy() + Pos(line_step * i, 0) + Pos(0, -br2))

        if rotate_rectangle:
            result_corners = [rotate(point, math.pi/2, centre_pos) for point in result_corners]
        self.add_line(result_corners, colour, br2)

    # Write text onto the canvas using a custom font specified below
    def write(self, pos, lines, font_size, font_weight=None, line_spacing=1.35, colour=BLACK, font_file_name=None, show_points=False, draw_bounding_box=False):
        line_pos = pos.copy()
        y_offset = Pos(0, font_size * line_spacing)

        if not font_weight:
            if not font_file_name:
                font_weight = font_size / 30  # The default font looks a bit better thicker as it isn't outline based like all other fonts.
            else:
                font_weight = font_size / 60

        if font_file_name:
            # TODO: Figure out how to fill
            # TODO: Anti-aliasing for Pygame

            # Very slow, only use the following function if you need the character map for every single character in the font
            # character_map = get_font_character_map(font_file_name)

            # Much faster, near instant if not many unique characters are used
            character_map = get_reduced_font_character_map("".join(lines), font_file_name)
        else:
            character_map = DEFAULT_FONT

        def write_char(pos, char, char_num):

            if not font_file_name:
                char = char.upper()

            x_offset = Pos(font_size * character_map[ord(char)][2], 0)

            # horizontal_advanced_width = Pos(character_map[ord(char)][7], 0)
            # Bounding box including the character spacing

            current_left_side_bearing = Pos(0, 0)
            # If first character, remove left side bearing
            if char_num == 0:
                current_left_side_bearing = Pos(character_map[ord(char)][6], 0)
                x_offset -= current_left_side_bearing * font_size

            char_data = character_map[ord(char)][5]
            this_char_bounding_box = [((point.copy() - current_left_side_bearing) * font_size) + pos for point in character_map[ord(char)][4]]

            if draw_bounding_box:
                self.add_line(this_char_bounding_box, colour, font_weight, enclosed_path=True)
                full_char_bounding_box = [Pos(0.0, 0.0), Pos((this_char_bounding_box[1].x - pos.x)/font_size, 0.0), Pos((this_char_bounding_box[2].x - pos.x)/font_size, 1.0), Pos(0.0, 1.0)]
                full_char_bounding_box = [(point.copy() * font_size) + pos for point in full_char_bounding_box]
                self.add_line(full_char_bounding_box, RED, font_weight, enclosed_path=True)

            for index, segment in enumerate(char_data):
                this_char_segment = [(point.copy() * font_size) + pos - (current_left_side_bearing * font_size) for point in segment]
                if font_file_name:
                    self.add_modified_quadratic_bezier_curve(this_char_segment, colour, font_weight, enclosed_path=True)
                else:
                    self.add_quadratic_bezier_curve(this_char_segment, colour, font_weight)

            return pos + x_offset

        for line in lines:
            for index, char in enumerate(line):
                pos = write_char(pos.copy(), char, index)
            line_pos = line_pos + y_offset
            pos = line_pos.copy()

    # Randomly reorder the lines
    # Nifty Ink will animate in an interesting random order
    def shuffle_lines(self):
        random.shuffle(self.object["lines"])

    # Use this to make your drawings slightly less precise, but also reduce their size a lot
    # This can be useful if browser local storage limits start affecting your large drawings
    def round_floats(self, round_colours=False):
        for line in self.object['lines']:
            if round_colours:
                r, g, b, a = [float(x) for x in line['brushColor'][5:-1].split(",")]
                if a == 1:
                    line['brushColor'] = "rgb(" + ",".join([str(round(r)), str(round(g)), str(round(b))]) + ")"
                else:
                    line['brushColor'] = "rgba(" + ",".join([str(round(r)), str(round(g)), str(round(b)), str(a)]) + ")"
            line['brushRadius'] = round(line['brushRadius'])
            for point in line['points']:
                point['x'] = round(point['x'])
                point['y'] = round(point['y'])

    # Reverse the drawing order of all the lines, this will mess up the final appearance if lines overlap!
    def __reversed__(self):
        self.object['lines'] = list(reversed(self.object['lines']))
        return self

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
               step_size=10, save_transparent_bg=False, green_screen_colour=(0,177,64,255), timestamp=False, timestamp_format="%Y_%m_%d_%H_%M_%S_%f_"):
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
        screen = pygame.display.set_mode((pygame_x, pygame_y), 0, 32)

        pygame.display.set_caption("Drawing Render")

        if save_transparent_bg:
            screen.fill(green_screen_colour)
        else:
            screen.fill(WHITE)
        screen.set_alpha(255)
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
                        bezier_curve_points = get_bezier_curve((last_midpoint, p1, midpoint), step_size=step_size, end_point=True)
                        draw_lines(surface, colour, bezier_curve_points, width, end_caps=end_caps)

                        last_midpoint = midpoint
                    except IndexError:  # Draw the last point as a straight line to finish
                        draw_line(surface, colour, midpoint, p2, width, end_caps=end_caps)

        for line in self.object["lines"]:
            brush_radius = line["brushRadius"] * pygame_scale
            if "rgba" in line["brushColor"]:
                colour = [float(cell) for cell in list(line["brushColor"][5:-1].split(","))]
            else:
                colour = [float(cell) for cell in list(line["brushColor"][4:-1].split(","))]

            try:
                colour[3] *= 255  # Pygame expects an alpha between 0 and 255, not 0 and 1.
            except:
                colour.append(255)

            points = []
            if colour[3] != 255 and allow_transparency:  # If the brushColour is transparent, draw with transparency
                target_surface = pygame.Surface((pygame_x, pygame_y), 0, 32)
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

        time_str = datetime.datetime.now().strftime(timestamp_format) if timestamp else ""

        print(f"\nSaving {time_str+filename}")
        pygame.image.save(screen, time_str+filename)
        print("Saved.")

        # TODO: Figure out if Pygame has a method to save a surface with a transparent background
        if save_transparent_bg:
            image_string = pygame.image.tostring(screen, 'RGBA', False)

            from PIL import Image

            img = Image.frombytes("RGBA", screen.get_size(), image_string)

            # https://stackoverflow.com/questions/765736/how-to-use-pil-to-make-all-white-pixels-transparent
            def convert_png_transparent(image, dst_file, bg_color=(255, 255, 255)):
                array = np.array(image, dtype=np.ubyte)
                mask = (array[:, :, :3] == bg_color).all(axis=2)
                alpha = np.where(mask, 0, 255)
                array[:, :, -1] = alpha

                print(f"Saving {dst_file}")
                Image.fromarray(np.ubyte(array)).save(dst_file, "PNG")
                print("Saved.")

                # # save a version with white pixels where the green screen was
                # for y in range(image.size[1]):
                #     for x in range(image.size[0]):
                #         if [*image.getpixel((x, y))[:-1]] == bg_color:
                #             image.putpixel((x, y), (255, 255, 255, 255))

            convert_png_transparent(img, f"{time_str}transparent_{filename}", [*green_screen_colour[:-1]])

            # # Directly save the PIL image (no alpha sadly)
            # img.save("pil_screenshot.png")
            # print("Saved.")

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
