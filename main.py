from Drawing import Drawing

from constants import DRAWING_SIZE, BLACK
# from originalDrawingMethods? import point_image, rotating_square, tiled_diagonals,\
#   fibonacci_dots, fibonacci_image, squared_circle, curved_lines,\
#   shrinking_circle_ring, square_fractal, big_text_boi

from Pos import Pos
from Vector2D import Vector2D
from Matrix2D import Matrix2D
from FractalPiece2D import FractalPiece2D
from FractalDefn2D import FractalDefn2D
from FractalSystem2D import FractalSystem2D


def main():

    # Set up parameters
    iteration_count = 5
    circle_radius_factor = 0.72
    circle_colour = BLACK
    offset = 10

    # Set up main fractal
    main_piece = FractalPiece2D()
    main_piece.id = 0
    main_piece.vect = Vector2D(DRAWING_SIZE/2, DRAWING_SIZE/2)
    main_piece.mx = Matrix2D(DRAWING_SIZE/2, 0, 0, DRAWING_SIZE/2)

    # Set up linked fractal system
    syst = FractalSystem2D()

    # Set up each definition in the system
    defn_0 = FractalDefn2D()
    syst.add_defn(defn_0)

    pc_0_0 = FractalPiece2D()
    pc_0_0.id = 0
    pc_0_0.vect = Vector2D(-0.5, -0.5)
    pc_0_0.mx = Matrix2D(0, -0.5, -0.5, 0)
    defn_0.add_child(pc_0_0)

    pc_0_1 = FractalPiece2D()
    pc_0_1.id = 0
    pc_0_1.vect = Vector2D(-0.5, 0.5)
    pc_0_1.mx = Matrix2D(0.5, 0, 0, 0.5)
    defn_0.add_child(pc_0_1)

    pc_0_2 = FractalPiece2D()
    pc_0_2.id = 0
    pc_0_2.vect = Vector2D(0.5, -0.5)
    pc_0_2.mx = Matrix2D(0, 0.5, -0.5, 0)
    # pc_0_2.mx = Matrix2D(0.5, 0, 0, 0.5)
    defn_0.add_child(pc_0_2)

    pc_0_3 = FractalPiece2D()
    pc_0_3.id = 0
    pc_0_3.vect = Vector2D(0.5, 0.5)
    pc_0_3.mx = Matrix2D(-0.25, 0, 0, 0.25)
    defn_0.add_child(pc_0_3)

    main_iterations = syst.iterate(main_piece, iteration_count)


    print("")
    print("")
    print(pc_0_0)
    print(pc_0_1)
    print(pc_0_2)
    # print(pc_1_0)
    # print(pc_1_1)
    print("")
    print(defn_0)
    # print(defn_1)
    print("")
    print(syst)
    print("")
    print(main_piece)
    print("")
    print(main_iterations)
    print("")
    print("")

    drawing = Drawing()

    for piece in main_iterations:
        pos = Pos(piece.vect.x, DRAWING_SIZE - piece.vect.y)
        circle_radius = circle_radius_factor * (piece.mx.a ** 2 + piece.mx.b ** 2 + piece.mx.c ** 2 + piece.mx.d ** 2)**0.5
        drawing.add_point(pos, circle_colour, circle_radius)



    # drawing = square_fractal(Drawing(), [1, 1, 1, 0], 5)
    # drawing = big_text_boi(Drawing())

    # scale down so it not touch edgy
    # drawing *= 0.95

    print(f"Lines: {len(drawing.object['lines'])}, Size: {len(drawing.to_nifty_import())}")
    with open("output.txt", "w") as file:
        file.write(drawing.to_nifty_import())


if __name__ == '__main__':
    main()

# lines, chars, seconds
# 2187, 351713, 134
# 760, 114419, 23
#
#
#
#
#
#
#
#
