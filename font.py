import os
from fontTools import ttLib
from collections import defaultdict

from Pos import Pos
from fontConstants import default_value

# Useful for information, https://github.com/fonttools/fonttools/blob/main/Lib/fontTools/ttLib/tables/_g_l_y_f.py
# Inspired by https://github.com/fonttools/fonttools/blob/main/Snippets/interpolate.py


def get_segment_coordinates(font, glyph_name, units_per_em):
    glyph_table = font["glyf"]
    glyph = glyph_table.glyphs.get(glyph_name)
    if glyph is None:
        return None
    glyph.expand(glyph_table)
    glyph.recalcBounds(glyph_table)

    # Add phantom points for (left, right, top, bottom) positions.
    horizontal_advance_width, left_side_bearing = font["hmtx"].metrics[glyph_name]

    adjusted_horizontal_advanced_width = horizontal_advance_width - glyph.xMax
    adjusted_left_side_bearing = left_side_bearing

    normalised_horizontal_advanced_width = (horizontal_advance_width - glyph.xMax) / units_per_em
    normalised_left_side_bearing = left_side_bearing / units_per_em

    # Bounding box including the character spacing
    bounding_box = [(glyph.xMin - adjusted_left_side_bearing, -glyph.yMin),
                    (glyph.xMax + adjusted_horizontal_advanced_width, -glyph.yMin),
                    (glyph.xMax + adjusted_horizontal_advanced_width, -glyph.yMax),
                    (glyph.xMin - adjusted_left_side_bearing, -glyph.yMax)]

    total_x = units_per_em*0.7

    total_y = units_per_em*0.7

    # largest_x = glyph.xMax
    y_offset = units_per_em*0.7

    segments = []
    segment = []
    compressed_points, end_points, point_flags = glyph.getCoordinates(glyph_table)

    bounding_box = [Pos(x / total_x, (y+y_offset) / total_y) for (x, y) in bounding_box]

    if len(compressed_points) > 1:
        for index, point in enumerate(compressed_points):
            point = (Pos((point[0]) / total_x, (-point[1]+y_offset) / total_y), point_flags[index])
            segment.append(point)

            if point_flags[index] == 1:
                segment.append(point)
                segment.append(point)

            # If two off points in a row, add an on point at their midpoint
            try:
                if point_flags[index+1] == 0 and point_flags[index] == 0 and index not in end_points:
                    end_point = Pos((compressed_points[index + 1][0]) / total_x, (-compressed_points[index + 1][1]+y_offset) / total_y)
                    midpoint = ((end_point+point[0])/2, 1)
                    segment.append(midpoint)
                    segment.append(midpoint)
                    segment.append(midpoint)
            except Exception:
                pass

            if index in end_points:  # Last point in this segment, close the loop and extend segments
                # If the first point is not on the curve,
                # get the last point that was on curve
                # and use that instead
                if segment[0][1] != 1:
                    true_starting_point = None
                    # TODO: Might be slow for large characters, maybe use the index in reverse
                    for pt in segment[::-1]:
                        if pt[1] == 1:
                            true_starting_point = pt
                            break
                    segment = [true_starting_point] + segment

                segments.append(segment)  # Add the segment to the segments
                segment = []  # Clear the segment

    # TODO: It's possible to keep this but then the default font would need to be updated to include "on/off" curves
    # Remove the on/off curve data as we no longer need it
    segments = [[point for (point, on) in segment] for segment in segments]

    return segments, bounding_box, normalised_left_side_bearing, normalised_horizontal_advanced_width


def get_reduced_font_character_map(text, file_name):
    tt = ttLib.TTFont(file_name)
    units_per_em = tt['head'].unitsPerEm
    character_ascii_map = tt.getBestCmap()

    font_character_map = defaultdict(default_value)

    unique_used_characters = set(char for char in text)

    # Only returns a character map of characters that are going to be used, should be much faster
    for char in unique_used_characters:
        try:
            char_name = character_ascii_map[ord(char)]

            char_data, bounding_box, adjusted_left_side_bearing, adjusted_horizontal_advanced_width = get_segment_coordinates(tt, char_name, units_per_em)
            character_width = bounding_box[1].x - bounding_box[0].x
            character_height = bounding_box[2].y - bounding_box[3].y
            font_character_map[ord(char)] = [char, char_name, character_width, character_height, bounding_box, char_data, adjusted_left_side_bearing, adjusted_horizontal_advanced_width]
        except Exception:  # This character isn't in the font, the default character will be used
            pass

    return font_character_map


def get_font_character_map(file_name):
    font = ttLib.TTFont(file_name)
    units_per_em = font['head'].unitsPerEm
    character_ascii_map = font.getBestCmap()

    font_character_map = defaultdict(default_value)

    glyph_count = len(character_ascii_map)
    font_file_size = os.path.getsize(file_name)

    if glyph_count > 1000:
        print(f"Loading a large font ({glyph_count} glyphs), this may take a while.")
    if font_file_size > 1024.0**2:
        print(f"Loading a large sized font ({font_file_size/(1024.0**2):.2f}MB), this may take a while.")

    for ascii_char, char_name in character_ascii_map.items():
        char_data,bounding_box,adjusted_left_side_bearing,adjusted_horizontal_advanced_width = get_segment_coordinates(font, char_name, units_per_em)
        character_width = bounding_box[1].x - bounding_box[0].x
        character_height = bounding_box[2].y - bounding_box[3].y
        font_character_map[ascii_char] = [chr(ascii_char), char_name, character_width, character_height, bounding_box, char_data, adjusted_left_side_bearing, adjusted_horizontal_advanced_width]

    return font_character_map


# Gives an example of the character data for common ascii characters, and will give missing characters as '�'
if __name__ == '__main__':
    character_map = get_font_character_map('fonts/OpenSans-Regular.ttf')

    example_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[];',./{}:\\\"<>?~`|1234567890"
    for character in example_text:
        ascii_value = ord(character)
        print(character_map[ascii_value])

    print("".join(character_map[ord(character)][0] for character in example_text))