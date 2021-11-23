from fontTools import ttLib
from collections import defaultdict

from constants import BLACK
from pos import Pos


class Character:
    def __init__(self, char, char_name, char_data, bounding_box, left_side_bearing, horizontal_advanced_width):
        self.char = char
        self.char_name = char_name

        character_width = bounding_box[1].x - bounding_box[0].x
        character_height = bounding_box[2].y - bounding_box[3].y

        self.character_width = character_width
        self.character_height = character_height
        self.bounding_box = bounding_box
        self.char_data = char_data
        self.left_side_bearing = left_side_bearing
        self.horizontal_advanced_width = horizontal_advanced_width


def default_value():
    return Character('�', 'uniFFFD', [[Pos(0.712890625, -0.08537946428571436), Pos(0.712890625, -0.08537946428571436), Pos(0.712890625, -0.08537946428571436), Pos(1.3685825892857144, 0.5689174107142857), Pos(1.3685825892857144, 0.5689174107142857), Pos(1.3685825892857144, 0.5689174107142857), Pos(0.712890625, 1.2225167410714286), Pos(0.712890625, 1.2225167410714286), Pos(0.712890625, 1.2225167410714286), Pos(0.05859375000000001, 0.5689174107142857), Pos(0.05859375000000001, 0.5689174107142857), Pos(0.05859375000000001, 0.5689174107142857)], [Pos(0.7582310267857143, 0.7440011160714286), Pos(0.7582310267857143, 0.7440011160714286), Pos(0.7582310267857143, 0.7440011160714286), Pos(0.7582310267857143, 0.7112165178571428), Pos(0.7582310267857143, 0.7112165178571428), Pos(0.7582310267857143, 0.7112165178571428), Pos(0.7582310267857143, 0.6763392857142857), Pos(0.7735770089285714, 0.6536690848214286), Pos(0.7735770089285714, 0.6536690848214286), Pos(0.7735770089285714, 0.6536690848214286), Pos(0.7889229910714286, 0.6309988839285714), Pos(0.8342633928571429, 0.5968191964285714), Pos(0.8342633928571429, 0.5968191964285714), Pos(0.8342633928571429, 0.5968191964285714), Pos(0.9061104910714286, 0.5396205357142857), Pos(0.9315708705357144, 0.4956752232142857), Pos(0.9315708705357144, 0.4956752232142857), Pos(0.9315708705357144, 0.4956752232142857), Pos(0.9570312500000001, 0.4517299107142857), Pos(0.9570312500000001, 0.3903459821428571), Pos(0.9570312500000001, 0.3903459821428571), Pos(0.9570312500000001, 0.3903459821428571), Pos(0.9570312500000001, 0.2961774553571428), Pos(0.8918108258928572, 0.2424665178571428), Pos(0.8918108258928572, 0.2424665178571428), Pos(0.8918108258928572, 0.2424665178571428), Pos(0.8265904017857143, 0.1887555803571428), Pos(0.7114955357142858, 0.1887555803571428), Pos(0.7114955357142858, 0.1887555803571428), Pos(0.7114955357142858, 0.1887555803571428), Pos(0.6563895089285715, 0.1887555803571428), Pos(0.5915178571428572, 0.2082868303571428), Pos(0.5915178571428572, 0.2082868303571428), Pos(0.5915178571428572, 0.2082868303571428), Pos(0.5266462053571429, 0.22781808035714282), Pos(0.47712053571428575, 0.2571149553571428), Pos(0.47712053571428575, 0.2571149553571428), Pos(0.47712053571428575, 0.2571149553571428), Pos(0.5343191964285715, 0.38127790178571425), Pos(0.5343191964285715, 0.38127790178571425), Pos(0.5343191964285715, 0.38127790178571425), Pos(0.6459263392857143, 0.3254743303571428), Pos(0.7087053571428572, 0.3254743303571428), Pos(0.7087053571428572, 0.3254743303571428), Pos(0.7087053571428572, 0.3254743303571428), Pos(0.7526506696428572, 0.3254743303571428), Pos(0.7742745535714286, 0.34570312499999994), Pos(0.7742745535714286, 0.34570312499999994), Pos(0.7742745535714286, 0.34570312499999994), Pos(0.7958984375, 0.3659319196428571), Pos(0.7958984375, 0.3987165178571428), Pos(0.7958984375, 0.3987165178571428), Pos(0.7958984375, 0.3987165178571428), Pos(0.7958984375, 0.4356863839285714), Pos(0.77880859375, 0.46184430803571425), Pos(0.77880859375, 0.46184430803571425), Pos(0.77880859375, 0.46184430803571425), Pos(0.76171875, 0.4880022321428571), Pos(0.7114955357142858, 0.5256696428571428), Pos(0.7114955357142858, 0.5256696428571428), Pos(0.7114955357142858, 0.5256696428571428), Pos(0.6529017857142858, 0.5731026785714285), Pos(0.63232421875, 0.6121651785714286), Pos(0.63232421875, 0.6121651785714286), Pos(0.63232421875, 0.6121651785714286), Pos(0.6117466517857143, 0.6512276785714286), Pos(0.6117466517857143, 0.7028459821428571), Pos(0.6117466517857143, 0.7028459821428571), Pos(0.6117466517857143, 0.7028459821428571), Pos(0.6117466517857143, 0.7440011160714286), Pos(0.6117466517857143, 0.7440011160714286), Pos(0.6117466517857143, 0.7440011160714286)], [Pos(0.5929129464285715, 0.9358258928571429), Pos(0.5929129464285715, 0.9358258928571429), Pos(0.5929129464285715, 0.9358258928571429), Pos(0.5929129464285715, 0.9797712053571429), Pos(0.61767578125, 1.0048828125), Pos(0.61767578125, 1.0048828125), Pos(0.61767578125, 1.0048828125), Pos(0.6424386160714286, 1.0299944196428572), Pos(0.6912667410714286, 1.0299944196428572), Pos(0.6912667410714286, 1.0299944196428572), Pos(0.6912667410714286, 1.0299944196428572), Pos(0.7373046875, 1.0299944196428572), Pos(0.7627650669642858, 1.0045340401785714), Pos(0.7627650669642858, 1.0045340401785714), Pos(0.7627650669642858, 1.0045340401785714), Pos(0.7882254464285715, 0.9790736607142857), Pos(0.7882254464285715, 0.9358258928571429), Pos(0.7882254464285715, 0.9358258928571429), Pos(0.7882254464285715, 0.9358258928571429), Pos(0.7882254464285715, 0.8911830357142857), Pos(0.7631138392857144, 0.86572265625), Pos(0.7631138392857144, 0.86572265625), Pos(0.7631138392857144, 0.86572265625), Pos(0.7380022321428572, 0.8402622767857143), Pos(0.6912667410714286, 0.8402622767857143), Pos(0.6912667410714286, 0.8402622767857143), Pos(0.6912667410714286, 0.8402622767857143), Pos(0.6410435267857143, 0.8402622767857143), Pos(0.6169782366071429, 0.8653738839285714), Pos(0.6169782366071429, 0.8653738839285714), Pos(0.6169782366071429, 0.8653738839285714), Pos(0.5929129464285715, 0.8904854910714286)]], [Pos(0.0, 1.2225167410714286), Pos(1.4285714285714286, 1.2225167410714286), Pos(1.4285714285714286, -0.08537946428571436), Pos(0.0, -0.08537946428571436)], 0.041015625, 0.0419921875)


class Font:

    def __init__(self, file_name, size=12, weight=None, line_spacing=1.35, colour=BLACK, unknown_character=None):
        self.font = ttLib.TTFont(file_name)
        self.units_per_em = self.font['head'].unitsPerEm
        self.character_ascii_map = self.font.getBestCmap()

        self.size = size
        self.weight = weight
        self.line_spacing = line_spacing
        self.colour = colour

        if not unknown_character:
            unknown_character = Character('�', 'uniFFFD', [], [Pos(0.0, 1.2225167410714286), Pos(1.4285714285714286, 1.2225167410714286), Pos(1.4285714285714286, -0.08537946428571436), Pos(0.0, -0.08537946428571436)], 0.041015625, 0.0419921875)
        self.default_value = unknown_character
        self.font_character_map = defaultdict(self.load_character)

    def __getitem__(self, key):
        if key in self.font_character_map:
            return self.font_character_map[key]
        else:
            return self.load_character(key)

    def __setitem__(self, key, value):
        self.font_character_map[key] = value

    def load_character(self, key):
        try:
            char_name = self.character_ascii_map[key]
            return Character(chr(key), char_name, *self.get_segment_coordinates(char_name))
        except KeyError:
            return self.default_value

    def get_segment_coordinates(self, glyph_name):
        glyph_table = self.font["glyf"]
        glyph = glyph_table.glyphs.get(glyph_name)
        if glyph is None:
            return None
        glyph.expand(glyph_table)
        glyph.recalcBounds(glyph_table)

        # Add phantom points for (left, right, top, bottom) positions.
        horizontal_advance_width, left_side_bearing = self.font["hmtx"].metrics[glyph_name]

        adjusted_horizontal_advanced_width = horizontal_advance_width - glyph.xMax
        adjusted_left_side_bearing = left_side_bearing

        normalised_horizontal_advanced_width = (horizontal_advance_width - glyph.xMax) / self.units_per_em
        normalised_left_side_bearing = left_side_bearing / self.units_per_em

        # Bounding box including the character spacing
        bounding_box = [(glyph.xMin - adjusted_left_side_bearing, -glyph.yMin),
                        (glyph.xMax + adjusted_horizontal_advanced_width, -glyph.yMin),
                        (glyph.xMax + adjusted_horizontal_advanced_width, -glyph.yMax),
                        (glyph.xMin - adjusted_left_side_bearing, -glyph.yMax)]

        total_x = self.units_per_em * 0.7
        total_y = self.units_per_em * 0.7
        y_offset = self.units_per_em * 0.7

        segments = []
        segment = []
        compressed_points, end_points, point_flags = glyph.getCoordinates(glyph_table)

        bounding_box = [Pos(x / total_x, (y + y_offset) / total_y) for (x, y) in bounding_box]

        # TODO: It seems either the flags are being handled incorrectly, \
        #       or the on curve/off curves are being calculated incorrectly \
        #       With fonts like OpenSans, it occurs visibly for letters such as A, B and D

        if len(compressed_points) > 1:
            for index, point in enumerate(compressed_points):
                point = (Pos((point[0]) / total_x, (-point[1] + y_offset) / total_y), point_flags[index])
                segment.append(point)

                if point_flags[index] == 1:
                    segment.append(point)
                    segment.append(point)

                # If two off points in a row, add an on point at their midpoint
                try:
                    if point_flags[index + 1] == 0 and point_flags[index] == 0 and index not in end_points:
                        x_pos = (compressed_points[index + 1][0]) / total_x
                        y_pos = (-compressed_points[index + 1][1] + y_offset) / total_y
                        end_point = Pos(x_pos, y_pos)
                        midpoint = ((end_point + point[0]) / 2, 1)
                        segment.append(midpoint)
                        segment.append(midpoint)
                        segment.append(midpoint)
                except IndexError:
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
