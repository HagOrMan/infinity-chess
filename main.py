import os
import pygame
import sys

pygame.init()

# paths for different assets
can_go_image = os.path.join("assets", "CanGoCircle.png")
empty_square_image = os.path.join("assets", "EmptySquare.png")
black_rook_image = os.path.join("assets", "b_rook.png")
white_rook_image = os.path.join("assets", "w_rook.png")
black_knight_image = os.path.join("assets", "b_knight.png")
white_knight_image = os.path.join("assets", "w_knight.png")
black_bishop_image = os.path.join("assets", "b_bishop.png")
white_bishop_image = os.path.join("assets", "w_bishop.png")
black_queen_image = os.path.join("assets", "b_queen.png")
white_queen_image = os.path.join("assets", "w_queen.png")
black_king_image = os.path.join("assets", "b_king.png")
white_king_image = os.path.join("assets", "w_king.png")
black_pawn_image = os.path.join("assets", "b_pawn.png")
white_pawn_image = os.path.join("assets", "w_pawn.png")

# Colours for different aspects of the game.
Color = {
    "light_blue": (152, 180, 209),
    "dark_blue": (97, 130, 152),
    "can_kill": (43, 180, 14),
    "chosen": (27, 174, 219),
    "in_check": (240, 30, 30),
    "grid_lines": (112, 112, 112),
    "white": (255, 255, 255)
}

word_font = pygame.font.Font("freesansbold.ttf", 20)

# Sets up window.
win_width = 530
gap = 26
win_height = 600
win_colour = (0, 0, 0)
WIN = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Infinity Chess")

square_width = (win_width - gap) / 8

clock = pygame.time.Clock()

# Variables for the game itself
white_win = True
white_turn = True
game_over = False
promoting_pawn = False
choosing_piece = True

# Specifically for en passant.
wPawnJustMoved, bPawnJustMoved = [False for r in range(8)], [False for r in range(8)]

# Images needed for the game.
goCircle = pygame.image.load(can_go_image)
passantCircle = pygame.image.load(can_go_image)
castleCircle = pygame.image.load(can_go_image)
emptySquare = pygame.image.load(empty_square_image)

# Variables for the chosen square and resetting squares to their original colours.
chosenRow, chosenCol = 0, 0
chosenText = 'p'
chosen_colour = Color['light_blue']
check_back_colour = Color['light_blue']


# The Piece class contains all the knowledge about a specific piece on the board.
class Piece:
    def __init__(self, team='None', piece='None', image=empty_square_image, moved=False):
        self.team = team
        self.piece = piece
        self.image = pygame.image.load(image)
        self.moved = moved


# Class for all the squares on the board.
class Square:
    def __init__(self, row, col, bgn_colour, movable, piece, killable, checkmate_image):
        self.row = row
        self.col = col
        self.bgn_colour = bgn_colour
        self.movable = movable
        self.piece = piece
        self.killable = killable
        self.y = int(row * square_width)
        self.x = int(col * square_width) + gap
        self.checkmate_image = checkmate_image

    # Draws itself by drawing a rectangle and a piece if necessary.
    def draw(self):
        pygame.draw.rect(WIN, self.bgn_colour, (self.x, self.y, square_width, square_width))
        if self.piece.image != emptySquare:
            WIN.blit(self.piece.image, (self.x, self.y))


# Variable representing whichever piece was last chosen.
chosenPiece = Piece('w', 'r', white_rook_image, False)

# All the squares on the board.
A8 = Square(0, 0, Color["light_blue"], False, Piece('b', 'r', black_rook_image), False, empty_square_image)
B8 = Square(0, 1, Color["dark_blue"], False, Piece('b', 'n', black_knight_image), False, empty_square_image)
C8 = Square(0, 2, Color["light_blue"], False, Piece('b', 'b', black_bishop_image), False, empty_square_image)
D8 = Square(0, 3, Color["dark_blue"], False, Piece('b', 'q', black_queen_image), False, empty_square_image)
E8 = Square(0, 4, Color["light_blue"], False, Piece('b', 'k', black_king_image), False, empty_square_image)
F8 = Square(0, 5, Color["dark_blue"], False, Piece('b', 'b', black_bishop_image), False, empty_square_image)
G8 = Square(0, 6, Color["light_blue"], False, Piece('b', 'n', black_knight_image), False, empty_square_image)
H8 = Square(0, 7, Color["dark_blue"], False, Piece('b', 'r', black_rook_image), False, empty_square_image)

A7 = Square(1, 0, Color["dark_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
B7 = Square(1, 1, Color["light_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
C7 = Square(1, 2, Color["dark_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
D7 = Square(1, 3, Color["light_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
E7 = Square(1, 4, Color["dark_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
F7 = Square(1, 5, Color["light_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
G7 = Square(1, 6, Color["dark_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
H7 = Square(1, 7, Color["light_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)

A6 = Square(2, 0, Color["light_blue"], False, Piece(), False, empty_square_image)
B6 = Square(2, 1, Color["dark_blue"], False, Piece(), False, empty_square_image)
C6 = Square(2, 2, Color["light_blue"], False, Piece(), False, empty_square_image)
D6 = Square(2, 3, Color["dark_blue"], False, Piece(), False, empty_square_image)
E6 = Square(2, 4, Color["light_blue"], False, Piece(), False, empty_square_image)
F6 = Square(2, 5, Color["dark_blue"], False, Piece(), False, empty_square_image)
G6 = Square(2, 6, Color["light_blue"], False, Piece(), False, empty_square_image)
H6 = Square(2, 7, Color["dark_blue"], False, Piece(), False, empty_square_image)

A5 = Square(3, 0, Color["dark_blue"], False, Piece(), False, empty_square_image)
B5 = Square(3, 1, Color["light_blue"], False, Piece(), False, empty_square_image)
C5 = Square(3, 2, Color["dark_blue"], False, Piece(), False, empty_square_image)
D5 = Square(3, 3, Color["light_blue"], False, Piece(), False, empty_square_image)
E5 = Square(3, 4, Color["dark_blue"], False, Piece(), False, empty_square_image)
F5 = Square(3, 5, Color["light_blue"], False, Piece(), False, empty_square_image)
G5 = Square(3, 6, Color["dark_blue"], False, Piece(), False, empty_square_image)
H5 = Square(3, 7, Color["light_blue"], False, Piece(), False, empty_square_image)

A4 = Square(4, 0, Color["light_blue"], False, Piece(), False, empty_square_image)
B4 = Square(4, 1, Color["dark_blue"], False, Piece(), False, empty_square_image)
C4 = Square(4, 2, Color["light_blue"], False, Piece(), False, empty_square_image)
D4 = Square(4, 3, Color["dark_blue"], False, Piece(), False, empty_square_image)
E4 = Square(4, 4, Color["light_blue"], False, Piece(), False, empty_square_image)
F4 = Square(4, 5, Color["dark_blue"], False, Piece(), False, empty_square_image)
G4 = Square(4, 6, Color["light_blue"], False, Piece(), False, empty_square_image)
H4 = Square(4, 7, Color["dark_blue"], False, Piece(), False, empty_square_image)

A3 = Square(5, 0, Color["dark_blue"], False, Piece(), False, empty_square_image)
B3 = Square(5, 1, Color["light_blue"], False, Piece(), False, empty_square_image)
C3 = Square(5, 2, Color["dark_blue"], False, Piece(), False, empty_square_image)
D3 = Square(5, 3, Color["light_blue"], False, Piece(), False, empty_square_image)
E3 = Square(5, 4, Color["dark_blue"], False, Piece(), False, empty_square_image)
F3 = Square(5, 5, Color["light_blue"], False, Piece(), False, empty_square_image)
G3 = Square(5, 6, Color["dark_blue"], False, Piece(), False, empty_square_image)
H3 = Square(5, 7, Color["light_blue"], False, Piece(), False, empty_square_image)

A2 = Square(6, 0, Color["light_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
B2 = Square(6, 1, Color["dark_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
C2 = Square(6, 2, Color["light_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
D2 = Square(6, 3, Color["dark_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
E2 = Square(6, 4, Color["light_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
F2 = Square(6, 5, Color["dark_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
G2 = Square(6, 6, Color["light_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
H2 = Square(6, 7, Color["dark_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)

A1 = Square(7, 0, Color["dark_blue"], False, Piece('w', 'r', white_rook_image), False, empty_square_image)
B1 = Square(7, 1, Color["light_blue"], False, Piece('w', 'n', white_knight_image), False, empty_square_image)
C1 = Square(7, 2, Color["dark_blue"], False, Piece('w', 'b', white_bishop_image), False, empty_square_image)
D1 = Square(7, 3, Color["light_blue"], False, Piece('w', 'q', white_queen_image), False, empty_square_image)
E1 = Square(7, 4, Color["dark_blue"], False, Piece('w', 'k', white_king_image), False, empty_square_image)
F1 = Square(7, 5, Color["light_blue"], False, Piece('w', 'b', white_bishop_image), False, empty_square_image)
G1 = Square(7, 6, Color["dark_blue"], False, Piece('w', 'n', white_knight_image), False, empty_square_image)
H1 = Square(7, 7, Color["light_blue"], False, Piece('w', 'r', white_rook_image), False, empty_square_image)

# The board which is full of all the squares.
Board = [[Square(0, 0, Color['light_blue'], False, Piece(), False, empty_square_image) for _ in range(8)] for __ in range(8)]

# Variables for the squares which will be changed when the player is promoting a pawn.
promote1, promote2, promote3 = Board[0][0].piece.image, Board[0][0].piece.image, Board[0][0].piece.image


# Used to make sure that pieces can go through the left and right side of the board.
def infinite_edge(inf_col):
    if inf_col < 0:
        return 8 + inf_col
    else:
        return inf_col % 8


def reset_board():
    Board[0][2] = Square(0, 2, Color["light_blue"], False, Piece('b', 'b', black_bishop_image), False, empty_square_image)
    Board[0][3] = Square(0, 3, Color["dark_blue"], False, Piece('b', 'q', black_queen_image), False, empty_square_image)
    Board[0][0] = Square(0, 0, Color["light_blue"], False, Piece('b', 'r', black_rook_image), False, empty_square_image)
    Board[0][4] = Square(0, 4, Color["light_blue"], False, Piece('b', 'k', black_king_image), False, empty_square_image)
    Board[0][5] = Square(0, 5, Color["dark_blue"], False, Piece('b', 'b', black_bishop_image), False, empty_square_image)
    Board[0][6] = Square(0, 6, Color["light_blue"], False, Piece('b', 'n', black_knight_image), False, empty_square_image)
    Board[0][7] = Square(0, 7, Color["dark_blue"], False, Piece('b', 'r', black_rook_image), False, empty_square_image)
    Board[0][1] = Square(0, 1, Color["dark_blue"], False, Piece('b', 'n', black_knight_image), False, empty_square_image)

    Board[1][0] = Square(1, 0, Color["dark_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
    Board[1][1] = Square(1, 1, Color["light_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
    Board[1][2] = Square(1, 2, Color["dark_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
    Board[1][3] = Square(1, 3, Color["light_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
    Board[1][4] = Square(1, 4, Color["dark_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
    Board[1][5] = Square(1, 5, Color["light_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
    Board[1][6] = Square(1, 6, Color["dark_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)
    Board[1][7] = Square(1, 7, Color["light_blue"], False, Piece('b', 'p', black_pawn_image), False, empty_square_image)

    Board[2][0] = Square(2, 0, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[2][1] = Square(2, 1, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[2][2] = Square(2, 2, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[2][3] = Square(2, 3, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[2][4] = Square(2, 4, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[2][5] = Square(2, 5, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[2][6] = Square(2, 6, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[2][7] = Square(2, 7, Color["dark_blue"], False, Piece(), False, empty_square_image)

    Board[3][0] = Square(3, 0, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[3][1] = Square(3, 1, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[3][2] = Square(3, 2, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[3][3] = Square(3, 3, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[3][4] = Square(3, 4, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[3][5] = Square(3, 5, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[3][6] = Square(3, 6, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[3][7] = Square(3, 7, Color["light_blue"], False, Piece(), False, empty_square_image)

    Board[4][0] = Square(4, 0, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[4][1] = Square(4, 1, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[4][2] = Square(4, 2, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[4][3] = Square(4, 3, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[4][4] = Square(4, 4, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[4][5] = Square(4, 5, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[4][6] = Square(4, 6, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[4][7] = Square(4, 7, Color["dark_blue"], False, Piece(), False, empty_square_image)

    Board[5][0] = Square(5, 0, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[5][1] = Square(5, 1, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[5][2] = Square(5, 2, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[5][3] = Square(5, 3, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[5][4] = Square(5, 4, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[5][5] = Square(5, 5, Color["light_blue"], False, Piece(), False, empty_square_image)
    Board[5][6] = Square(5, 6, Color["dark_blue"], False, Piece(), False, empty_square_image)
    Board[5][7] = Square(5, 7, Color["light_blue"], False, Piece(), False, empty_square_image)

    Board[6][0] = Square(6, 0, Color["light_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
    Board[6][1] = Square(6, 1, Color["dark_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
    Board[6][2] = Square(6, 2, Color["light_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
    Board[6][3] = Square(6, 3, Color["dark_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
    Board[6][4] = Square(6, 4, Color["light_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
    Board[6][5] = Square(6, 5, Color["dark_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
    Board[6][6] = Square(6, 6, Color["light_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)
    Board[6][7] = Square(6, 7, Color["dark_blue"], False, Piece('w', 'p', white_pawn_image), False, empty_square_image)

    Board[7][0] = Square(7, 0, Color["dark_blue"], False, Piece('w', 'r', white_rook_image), False, empty_square_image)
    Board[7][1] = Square(7, 1, Color["light_blue"], False, Piece('w', 'n', white_knight_image), False, empty_square_image)
    Board[7][2] = Square(7, 2, Color["dark_blue"], False, Piece('w', 'b', white_bishop_image), False, empty_square_image)
    Board[7][3] = Square(7, 3, Color["light_blue"], False, Piece('w', 'q', white_queen_image), False, empty_square_image)
    Board[7][4] = Square(7, 4, Color["dark_blue"], False, Piece('w', 'k', white_king_image), False, empty_square_image)
    Board[7][5] = Square(7, 5, Color["light_blue"], False, Piece('w', 'b', white_bishop_image), False, empty_square_image)
    Board[7][6] = Square(7, 6, Color["dark_blue"], False, Piece('w', 'n', white_knight_image), False, empty_square_image)
    Board[7][7] = Square(7, 7, Color["light_blue"], False, Piece('w', 'r', white_rook_image), False, empty_square_image)


def fill_board():
    Board[0][0] = A8
    Board[0][1] = B8
    Board[0][2] = C8
    Board[0][3] = D8
    Board[0][4] = E8
    Board[0][5] = F8
    Board[0][6] = G8
    Board[0][7] = H8

    Board[1][0] = A7
    Board[1][1] = B7
    Board[1][2] = C7
    Board[1][3] = D7
    Board[1][4] = E7
    Board[1][5] = F7
    Board[1][6] = G7
    Board[1][7] = H7

    Board[2][0] = A6
    Board[2][1] = B6
    Board[2][2] = C6
    Board[2][3] = D6
    Board[2][4] = E6
    Board[2][5] = F6
    Board[2][6] = G6
    Board[2][7] = H6

    Board[3][0] = A5
    Board[3][1] = B5
    Board[3][2] = C5
    Board[3][3] = D5
    Board[3][4] = E5
    Board[3][5] = F5
    Board[3][6] = G5
    Board[3][7] = H5

    Board[4][0] = A4
    Board[4][1] = B4
    Board[4][2] = C4
    Board[4][3] = D4
    Board[4][4] = E4
    Board[4][5] = F4
    Board[4][6] = G4
    Board[4][7] = H4

    Board[5][0] = A3
    Board[5][1] = B3
    Board[5][2] = C3
    Board[5][3] = D3
    Board[5][4] = E3
    Board[5][5] = F3
    Board[5][6] = G3
    Board[5][7] = H3

    Board[6][0] = A2
    Board[6][1] = B2
    Board[6][2] = C2
    Board[6][3] = D2
    Board[6][4] = E2
    Board[6][5] = F2
    Board[6][6] = G2
    Board[6][7] = H2

    Board[7][0] = A1
    Board[7][1] = B1
    Board[7][2] = C1
    Board[7][3] = D1
    Board[7][4] = E1
    Board[7][5] = F1
    Board[7][6] = G1
    Board[7][7] = H1


# Draws lines between squares to make the board look nicer.
def draw_grid():
    for r in range(8):
        pygame.draw.line(WIN, Color['grid_lines'], (gap, r * square_width), (win_width, r * square_width))
        for c in range(8):
            pygame.draw.line(WIN, Color['grid_lines'], (c * square_width + gap, 0), (c * square_width + gap, 504))


# Draws letters and numbers for the game on the board.
def write_nums():

    # All the letters.
    AWrd = word_font.render(str('A'), False, Color["white"])
    BWrd = word_font.render(str('B'), False, Color["white"])
    CWrd = word_font.render(str('C'), False, Color["white"])
    DWrd = word_font.render(str('D'), False, Color["white"])
    EWrd = word_font.render(str('E'), False, Color["white"])
    FWrd = word_font.render(str('F'), False, Color["white"])
    GWrd = word_font.render(str('G'), False, Color["white"])
    HWrd = word_font.render(str('H'), False, Color["white"])

    # Adds letters to window.
    WIN.blit(AWrd, (gap - 5 + int(square_width / 2), win_width - 15))
    WIN.blit(BWrd, (gap - 5 + int(square_width / 2) + square_width, win_width - 15))
    WIN.blit(CWrd, (gap - 5 + int(square_width / 2) + square_width * 2, win_width - 15))
    WIN.blit(DWrd, (gap - 5 + int(square_width / 2) + square_width * 3, win_width - 15))
    WIN.blit(EWrd, (gap - 5 + int(square_width / 2) + square_width * 4, win_width - 15))
    WIN.blit(FWrd, (gap - 5 + int(square_width / 2) + square_width * 5, win_width - 15))
    WIN.blit(GWrd, (gap - 5 + int(square_width / 2) + square_width * 6, win_width - 15))
    WIN.blit(HWrd, (gap - 5 + int(square_width / 2) + square_width * 7, win_width - 15))

    # All the numbers.
    Wrd1 = word_font.render(str('1'), False, Color["white"])
    Wrd2 = word_font.render(str('2'), False, Color["white"])
    Wrd3 = word_font.render(str('3'), False, Color["white"])
    Wrd4 = word_font.render(str('4'), False, Color["white"])
    Wrd5 = word_font.render(str('5'), False, Color["white"])
    Wrd6 = word_font.render(str('6'), False, Color["white"])
    Wrd7 = word_font.render(str('7'), False, Color["white"])
    Wrd8 = word_font.render(str('8'), False, Color["white"])

    # Adds numbers to window.
    WIN.blit(Wrd8, (8, -6 + int(square_width / 2)))
    WIN.blit(Wrd7, (8, -6 + int(square_width / 2) + square_width))
    WIN.blit(Wrd6, (8, -6 + int(square_width / 2) + square_width * 2))
    WIN.blit(Wrd5, (8, -6 + int(square_width / 2) + square_width * 3))
    WIN.blit(Wrd4, (8, -6 + int(square_width / 2) + square_width * 4))
    WIN.blit(Wrd3, (8, -6 + int(square_width / 2) + square_width * 5))
    WIN.blit(Wrd2, (8, -6 + int(square_width / 2) + square_width * 6))
    WIN.blit(Wrd1, (8, -6 + int(square_width / 2) + square_width * 7))


# Draws the board.
def draw_board():

    # Draws squares.
    for rows in Board:
        for cols in rows:
            cols.draw()

    # Draws lines which outline the squares and letters/numbers.
    draw_grid()
    write_nums()

    # Draws button to restart the game.
    restartFont = pygame.font.SysFont('timesnewroman', 26)
    restart_txt = restartFont.render(str('Restart Game'), False, Color['white'])
    WIN.blit(restart_txt, (win_width - square_width * 3, win_height - 50))

    # Draws a surrounding outline for the restart game 'button'.
    pygame.draw.line(WIN, Color['white'], (win_width - square_width * 3 - 10, win_height - 50),
                     (win_width - 40, win_height - 50))
    pygame.draw.line(WIN, Color['white'], (win_width - square_width * 3 - 10, win_height - 20),
                     (win_width - 40, win_height - 20))
    pygame.draw.line(WIN, Color['white'], (win_width - square_width * 3 - 10, win_height - 20),
                     (win_width - square_width * 3 - 10, win_height - 50))
    pygame.draw.line(WIN, Color['white'], (win_width - 40, win_height - 20),
                     (win_width - 40, win_height - 50))


# Checks if they clicked on the restart button and restarts if so.
def clicked_restart(pos):
    x, y = pos

    if win_width - square_width * 3 - 10 < x < win_width - 40 and win_height - 50 < y < win_height - 20:

        # Resets everything.
        reset_kill()
        reset_background()
        reset_pawn_moves()
        reset_board()
        global game_over, white_turn, promoting_pawn
        game_over = False
        promoting_pawn = False
        white_turn = True


# Gets the square at a specific position on the board that was clicked.
def get_square(posit):
    rows, cols = 0, 0
    x, y = posit
    rows = y // square_width
    cols = (x - gap) // square_width
    return int(rows), int(cols)


# Checks if a pawn at its starting position just moved.
def pawn_just_moved(rows, cols):

    # Ensures that the piece being checked is a pawn.
    if Board[rows][cols].piece.piece == 'p':

        # If the pawn is at the row that it starts at and just moved 2, its position in the list is set to true.
        if chosenRow == 6 and rows == 4 and is_white(rows, cols):
            wPawnJustMoved[chosenCol] = True
        if chosenRow == 1 and rows == 3 and not is_white(rows, cols):
            bPawnJustMoved[chosenCol] = True


# Does an en passant.
def en_passant(rows, cols):

    # Creates a vertical multiplier for if the piece is white or black.
    verMult = -1
    if is_white(chosenRow, chosenCol):
        verMult = 1

    # Resets the square that the piece moved from and adds the piece to its new square.
    Board[chosenRow][chosenCol].bgn_colour = chosen_colour
    Board[chosenRow][chosenCol].piece = Piece('None', 'None', empty_square_image, False)
    Board[rows][cols].piece = chosenPiece

    # Takes away the piece that was captured.
    Board[rows + verMult][cols].piece = Piece('None', 'None', empty_square_image, False)

    global white_turn, choosing_piece
    white_turn = not white_turn
    choosing_piece = True


# Marks the places that the pawn can go.
def pawn_moves():

    global chosenCol, chosenRow

    # Checks if they are white and makes a vertical multiplier from it, since black moves down and white up.
    verMult = 1
    if is_white(chosenRow, chosenCol):
        verMult = -1

    # Checks if the piece can move 1 space up.
    if not is_occupied(chosenRow + verMult, chosenCol):
        # Ensures that moving here will not result in check.
        if will_not_check(chosenRow + verMult, chosenCol):
            Board[chosenRow + verMult][chosenCol].piece.image = goCircle

        if on_board(chosenRow + 2 * verMult, chosenCol):
            # Checks if the piece can move up 2 or down 2.
            if not is_occupied(chosenRow + 2 * verMult, chosenCol) and Board[chosenRow][chosenCol].row == 6:
                # Ensures that moving here will not result in check.
                if will_not_check(chosenRow + 2 * verMult, chosenCol):
                    Board[chosenRow + 2 * verMult][chosenCol].piece.image = goCircle
            if not is_occupied(chosenRow + 2 * verMult, chosenCol) and Board[chosenRow][chosenCol].row == 1:
                # Ensures that moving here will not result in check.
                if will_not_check(chosenRow + 2 * verMult, chosenCol):
                    Board[chosenRow + 2 * verMult][chosenCol].piece.image = goCircle

    # Checks if the piece can capture to its left or right.
    if is_occupied(chosenRow + verMult, infinite_edge(chosenCol + 1)):
        if white_turn != is_white(chosenRow + verMult, infinite_edge(chosenCol + 1)):
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol + 1)):
                Board[chosenRow + verMult][infinite_edge(chosenCol + 1)].bgn_colour = Color['can_kill']
    if is_occupied(chosenRow + verMult, infinite_edge(chosenCol - 1)):
        if white_turn != is_white(chosenRow + verMult, infinite_edge(chosenCol - 1)):
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol - 1)):
                Board[chosenRow + verMult][infinite_edge(chosenCol - 1)].bgn_colour = Color['can_kill']

    # Checks if the piece can en passant, exiting the method if they aren't at the right row.
    if is_white(chosenRow, chosenCol) and chosenRow != 3:
        return
    if not is_white(chosenRow, chosenCol) and chosenRow != 4:
        return

    # Checks en passant for white pieces.
    if is_white(chosenRow, chosenCol):
        if bPawnJustMoved[infinite_edge(chosenCol - 1)]:
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol - 1)):
                Board[chosenRow + verMult][infinite_edge(chosenCol - 1)].piece.image = passantCircle
        if bPawnJustMoved[infinite_edge(chosenCol + 1)]:
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol + 1)):
                Board[chosenRow + verMult][infinite_edge(chosenCol + 1)].piece.image = passantCircle
    # Checks en passant for black pieces.
    else:
        if wPawnJustMoved[infinite_edge(chosenCol - 1)]:
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol - 1)):
                Board[chosenRow + verMult][infinite_edge(chosenCol - 1)].piece.image = passantCircle
        if wPawnJustMoved[infinite_edge(chosenCol + 1)]:
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol + 1)):
                Board[chosenRow + verMult][infinite_edge(chosenCol + 1)].piece.image = passantCircle


# Marks the places that the rook can go.
def rook_moves():

    # List of all the possible moves for the rook.
    rook_move = [[[chosenRow + x, chosenCol] for x in range(1, 8)],
                 [[chosenRow, infinite_edge(chosenCol - x)] for x in range(1, 8)],
                 [[chosenRow - x, chosenCol] for x in range(1, 8)],
                 [[chosenRow, infinite_edge(chosenCol + x)] for x in range(1, 8)]]

    # Loops through all possible moves.
    for horizontal in rook_move:
        for position in horizontal:

            # Sets row and col to the values in the position being checked.
            rows, cols = position[0], position[1]
            if on_board(rows, cols):

                # Checks if the place we are checking is one that the rook can move to or capture at.
                if is_occupied(rows, cols):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(chosenRow, chosenCol) != is_white(rows, cols):
                        # Ensures that moving here will not result in check.
                        if will_not_check(rows, cols):
                            Board[rows][cols].bgn_colour = Color['can_kill']
                    break
                else:
                    # Ensures that moving here will not result in check.
                    if will_not_check(rows, cols):
                        Board[rows][cols].piece.image = goCircle


# Marks the places that the bishop can go.
def bishop_moves():

    # List of all the possible moves for the bishop.
    bish_move = [[[chosenRow + x, infinite_edge(chosenCol + x)] for x in range(1, 8)],
                 [[chosenRow + x, infinite_edge(chosenCol - x)] for x in range(1, 8)],
                 [[chosenRow - x, infinite_edge(chosenCol + x)] for x in range(1, 8)],
                 [[chosenRow - x, infinite_edge(chosenCol - x)] for x in range(1, 8)]]

    # Goes through each of the options where the bishop can move.
    for diagonal in bish_move:
        for position in diagonal:

            # Sets row and col to the values in the position being checked.
            rows, cols = position[0], position[1]
            if on_board(rows, cols):

                # Checks if the place we are checking is one that the bishop can move to or capture at.
                if is_occupied(rows, cols):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(chosenRow, chosenCol) != is_white(rows, cols):
                        # Ensures that moving here will not result in check.
                        if will_not_check(rows, cols):
                            Board[rows][cols].bgn_colour = Color['can_kill']
                    break
                else:
                    # Ensures that moving here will not result in check.
                    if will_not_check(rows, cols):
                        Board[rows][cols].piece.image = goCircle


# Marks the places that the knight can go.
def knight_moves():

    # Goes through a 4 by 4 grid marking each place where the knight can move.
    for x in range(-2, 3):
        for y in range(-2, 3):

            # Since knights move in a 2-1 fashion, or L shape, this ensures that an L shape is being made.
            if x ** 2 + y ** 2 == 5:

                rows, cols = chosenRow + x, infinite_edge(chosenCol + y)
                if on_board(rows, cols):

                    # Checks if the place we are checking is one that the knight can move to or capture at.
                    if is_occupied(rows, cols):
                        # If it is occupied, ensures that they are not taking their own piece.
                        if is_white(chosenRow, chosenCol) != is_white(rows, cols):
                            # Ensures that moving here will not result in check.
                            if will_not_check(rows, cols):
                                Board[rows][cols].bgn_colour = Color['can_kill']
                    else:
                        # Ensures that moving here will not result in check.
                        if will_not_check(rows, cols):
                            Board[rows][cols].piece.image = goCircle


# Marks the places that the queen can go.
def queen_moves():
    bishop_moves()
    rook_moves()


# Marks the places that the king can go.
def king_moves():

    # Goes through each square a 3 by 3 grid surrounding the king, checking which squares it can move to.
    for x in range(3):
        for y in range(3):

            # Sets rows and cols to the rows and column being checked.
            rows = chosenRow - 1 + x
            cols = infinite_edge(chosenCol - 1 + y)

            # Ensures that we are checking a place on the board.
            if on_board(rows, cols):

                # Checks if the place we are checking is one that the king can move to or capture at.
                if is_occupied(rows, cols):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(chosenRow, chosenCol) != is_white(rows, cols):
                        # Ensures that moving here will not result in check.
                        if will_not_check(rows, cols):
                            Board[rows][cols].bgn_colour = Color['can_kill']
                else:
                    # Ensures that moving here will not result in check.
                    if will_not_check(rows, cols):
                        Board[rows][cols].piece.image = goCircle

    mark_castling()


# Castles the player's king.
def castling(rows, cols):

    global white_turn, choosing_piece

    # If the king castles with H1 rook.
    if rows == 7 and cols == 6:

        # Saves the rook at the place that it is castling from.
        rook_piece = Board[7][7].piece

        # Resets the spot they moved from to a blank square, and puts it in its new spot.
        Board[chosenRow][chosenCol].bgn_colour = chosen_colour
        Board[chosenRow][chosenCol].piece = Piece('None', 'None', empty_square_image, False)
        Board[rows][cols].piece = chosenPiece

        # Resets the spot the rook moved from to a blank square, and puts it in its new spot.
        Board[7][7].piece = Piece('None', 'None', empty_square_image, False)
        Board[7][5].piece = rook_piece

        # Shows that they moved.
        Board[rows][cols].piece.moved = True
        Board[7][5].piece.moved = True

    # If the king castles with A1 rook.
    if rows == 7 and cols == 2:
        # Saves the rook at the place that it is castling from.
        rook_piece = Board[7][0].piece

        # Resets the spot they moved from to a blank square, and puts it in its new spot.
        Board[chosenRow][chosenCol].bgn_colour = chosen_colour
        Board[chosenRow][chosenCol].piece = Piece('None', 'None', empty_square_image, False)
        Board[rows][cols].piece = chosenPiece

        # Resets the spot the rook moved from to a blank square, and puts it in its new spot.
        Board[7][0].piece = Piece('None', 'None', empty_square_image, False)
        Board[7][3].piece = rook_piece

        # Shows that they moved.
        Board[rows][cols].piece.moved = True
        Board[7][3].piece.moved = True

    # If the king castles with A8 rook.
    if rows == 0 and cols == 2:
        # Saves the rook at the place that it is castling from.
        rook_piece = Board[0][0].piece

        # Resets the spot they moved from to a blank square, and puts it in its new spot.
        Board[chosenRow][chosenCol].bgn_colour = chosen_colour
        Board[chosenRow][chosenCol].piece = Piece('None', 'None', empty_square_image, False)
        Board[rows][cols].piece = chosenPiece

        # Resets the spot the rook moved from to a blank square, and puts it in its new spot.
        Board[0][0].piece = Piece('None', 'None', empty_square_image, False)
        Board[0][3].piece = rook_piece

        # Shows that they moved.
        Board[rows][cols].piece.moved = True
        Board[0][3].piece.moved = True

    # If the king castles with H8 rook.
    if rows == 0 and cols == 6:
        # Saves the rook at the place that it is castling from.
        rook_piece = Board[0][7].piece

        # Resets the spot they moved from to a blank square, and puts it in its new spot.
        Board[chosenRow][chosenCol].bgn_colour = chosen_colour
        Board[chosenRow][chosenCol].piece = Piece('None', 'None', empty_square_image, False)
        Board[rows][cols].piece = chosenPiece

        # Resets the spot the rook moved from to a blank square, and puts it in its new spot.
        Board[0][7].piece = Piece('None', 'None', empty_square_image, False)
        Board[0][5].piece = rook_piece

        # Shows that they moved.
        Board[rows][cols].piece.moved = True
        Board[0][5].piece.moved = True

    # Changes who's move it is, and resets variables.
    white_turn = not white_turn
    choosing_piece = True
    reset_background()
    reset_pawn_moves()


# Marks where the player can castle.
def mark_castling():

    # Returns if the king is in check as they cannot castle.
    if chosen_colour == Color['in_check']:
        return

    if is_white(chosenRow, chosenCol):

        # Checks castling with A1 rook.
        if not (Board[7][0].piece.moved or Board[7][4].piece.moved or is_occupied(7, 1) or is_occupied(7, 2) or is_occupied(7, 3)):
            if Board[7][0].piece.piece == 'r' and Board[7][4].piece.piece == 'k':
                if will_not_check(7, 2):
                    Board[7][2].piece.image = castleCircle

        # Checks castling with H1 rook.
        if not (Board[7][4].piece.moved or Board[7][7].piece.moved or is_occupied(7, 5) or is_occupied(7, 6)):
            if Board[7][7].piece.piece == 'r' and Board[7][4].piece.piece == 'k':
                if will_not_check(7, 6):
                    Board[7][6].piece.image = castleCircle
    else:

        # Checks castling with A8 rook.
        if not (Board[0][0].piece.moved or Board[0][4].piece.moved or is_occupied(0, 1) or is_occupied(0, 2) or is_occupied(0, 3)):
            if Board[0][0].piece.piece == 'r' and Board[0][4].piece.piece == 'k':
                if will_not_check(0, 2):
                    Board[0][2].piece.image = castleCircle

        # Checks castling with H8 rook.
        if not (Board[0][4].piece.moved or Board[0][7].piece.moved or is_occupied(0, 5) or is_occupied(0, 6)):
            if Board[0][4].piece.piece == 'k' and Board[0][7].piece.piece == 'r':
                if will_not_check(0, 6):
                    Board[0][6].piece.image = castleCircle


# Marks the places that the pawn can capture.
def check_pawn_moves(rows, cols):

    # Checks if they are white and makes a vertical multiplier from it, since black moves down and white up.
    verMult = 1
    if is_white(rows, cols):
        verMult = -1

    # Checks if the piece can capture to its left or right.
    if is_occupied(rows + verMult, infinite_edge(cols + 1)):
        if is_white(rows, cols) != is_white(rows + verMult, infinite_edge(cols + 1)):
            Board[rows + verMult][infinite_edge(cols + 1)].killable = True
    if is_occupied(rows + verMult, infinite_edge(cols - 1)):
        if is_white(rows, cols) != is_white(rows + verMult, infinite_edge(cols - 1)):
            Board[rows + verMult][infinite_edge(cols - 1)].killable = True


# Marks the places that the rook can capture.
def check_rook_moves(rows, cols):

    # Goes through all the possible moves for the rook.
    rook_move = [[[rows + x, cols] for x in range(1, 8)],
                 [[rows, infinite_edge(cols - x)] for x in range(1, 8)],
                 [[rows - x, cols] for x in range(1, 8)],
                 [[rows, infinite_edge(cols + x)] for x in range(1, 8)]]

    for horizontal in rook_move:
        for position in horizontal:

            # Sets row and col to the values in the position being checked.
            r, c = position[0], position[1]
            if on_board(r, c):

                # Checks if the place we are checking is one that the rook can move to or capture at.
                if is_occupied(r, c):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(rows, cols) != is_white(r, c):
                        Board[r][c].killable = True
                    break
                else:
                    Board[r][c].killable = True


# Marks the places that the bishop can capture.
def check_bishop_moves(rows, cols):

    # Goes through all the possible moves for the bishop.
    bish_move = [[[rows + x, infinite_edge(cols + x)] for x in range(1, 8)],
                 [[rows + x, infinite_edge(cols - x)] for x in range(1, 8)],
                 [[rows - x, infinite_edge(cols + x)] for x in range(1, 8)],
                 [[rows - x, infinite_edge(cols - x)] for x in range(1, 8)]]

    # Goes through each of the options where the bishop can move.
    for diagonal in bish_move:
        for position in diagonal:

            # Sets row and col to the values in the position being checked.
            r, c = position[0], position[1]
            if on_board(r, c):

                # Checks if the place we are checking is one that the bishop can move to or capture at.
                if is_occupied(r, c):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(rows, cols) != is_white(r, c):
                        Board[r][c].killable = True
                    break
                else:
                    Board[r][c].killable = True


# Marks the places that the knight can capture.
def check_knight_moves(rows, cols):

    # Goes through a 4 by 4 grid marking each place where the knight can move.
    for x in range(-2, 3):
        for y in range(-2, 3):

            # Since knights move in a 2-1 fashion, or L shape, this ensures that an L shape is being made.
            if x ** 2 + y ** 2 == 5:

                r, c = rows + x, infinite_edge(cols + y)
                if on_board(r, c):

                    # Checks if the place we are checking is one that the knight can move to or capture at.
                    if is_occupied(r, c):
                        # If it is occupied, ensures that they are not taking their own piece.
                        if is_white(rows, cols) != is_white(r, c):
                            Board[r][c].killable = True
                    else:
                        Board[r][c].killable = True


# Marks the places that the queen can capture.
def check_queen_moves(rows, cols):
    check_rook_moves(rows, cols)
    check_bishop_moves(rows, cols)


# Marks the places that the king can capture.
def check_king_moves(rows, cols):

    # Goes through each square a 3 by 3 grid surrounding the king, checking which squares it can move to.
    for x in range(3):
        for y in range(3):

            # Sets row and col to the row and column being checked.
            r = rows - 1 + x
            c = infinite_edge(cols - 1 + y)

            # Ensures that we are checking a place on the board.
            if on_board(r, c):

                # Checks if the place we are checking is one that the king can move to or capture at.
                if is_occupied(r, c):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(r, c) != is_white(rows, cols):
                        Board[r][c].killable = True
                else:
                    Board[r][c].killable = True


# Returns if the pawn can move to any possible position, which signifies that it is not checkmate.
def mate_pawn_moves():

    # Checks if they are white and makes a vertical multiplier from it, since black moves down and white up.
    verMult = 1
    if is_white(chosenRow, chosenCol):
        verMult = -1

    # Checks if the piece can move 1 space up.
    if not is_occupied(chosenRow + verMult, chosenCol):
        # Ensures that moving here will not result in check.
        if will_not_check(chosenRow + verMult, chosenCol):
            return True

        if on_board(chosenRow + 2 * verMult, chosenCol):
            # Checks if the piece can move up 2 or down 2.
            if not is_occupied(chosenRow + 2 * verMult, chosenCol) and Board[chosenRow][chosenCol].row == 6:
                # Ensures that moving here will not result in check.
                if will_not_check(chosenRow + 2 * verMult, chosenCol):
                    return True
            if not is_occupied(chosenRow + 2 * verMult, chosenCol) and Board[chosenRow][chosenCol].row == 1:
                # Ensures that moving here will not result in check.
                if will_not_check(chosenRow + 2 * verMult, chosenCol):
                    return True

    # Checks if the piece can capture to its left or right.
    if is_occupied(chosenRow + verMult, infinite_edge(chosenCol + 1)):
        if white_turn != is_white(chosenRow + verMult, infinite_edge(chosenCol + 1)):
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol + 1)):
                return True
    if is_occupied(chosenRow + verMult, infinite_edge(chosenCol - 1)):
        if white_turn != is_white(chosenRow + verMult, infinite_edge(chosenCol - 1)):
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol - 1)):
                return True

    # Checks if the piece can en passant, exiting the method if they aren't at the right row.
    if is_white(chosenRow, chosenCol) and chosenRow != 3:
        return False
    if not is_white(chosenRow, chosenCol) and chosenRow != 4:
        return False

    # Checks en passant for white pieces.
    if is_white(chosenRow, chosenCol):
        if bPawnJustMoved[infinite_edge(chosenCol - 1)]:
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol - 1)):
                return True
        if bPawnJustMoved[infinite_edge(chosenCol + 1)]:
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol + 1)):
                return True

    # Checks en passant for black pieces.
    else:
        if wPawnJustMoved[infinite_edge(chosenCol - 1)]:
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol - 1)):
                return True
        if wPawnJustMoved[infinite_edge(chosenCol + 1)]:
            # Ensures that moving here will not result in check.
            if will_not_check(chosenRow + verMult, infinite_edge(chosenCol + 1)):
                return True

    # They could not move at all, so returns false
    return False


# Returns if the rook can move to any possible position, which signifies that it is not checkmate.
def mate_rook_moves():

    # Goes through all the possible moves for the rook.
    rook_move = [[[chosenRow + x, chosenCol] for x in range(1, 8)],
                 [[chosenRow, infinite_edge(chosenCol - x)] for x in range(1, 8)],
                 [[chosenRow - x, chosenCol] for x in range(1, 8)],
                 [[chosenRow, infinite_edge(chosenCol + x)] for x in range(1, 8)]]

    for horizontal in rook_move:
        for position in horizontal:

            # Sets row and col to the values in the position being checked.
            rows, cols = position[0], position[1]
            if on_board(rows, cols):

                # Checks if the place we are checking is one that the rook can move to or capture at.
                if is_occupied(rows, cols):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(chosenRow, chosenCol) != is_white(rows, cols):
                        # Ensures that moving here will not result in check.
                        if will_not_check(rows, cols):
                            return True
                    break
                else:
                    # Ensures that moving here will not result in check.
                    if will_not_check(rows, cols):
                        return True

    # Can't move, so returns false.
    return False


# Returns if the bishop can move to any possible position, which signifies that it is not checkmate.
def mate_bishop_moves():

    # Goes through all the possible moves for the bishop.
    bish_move = [[[chosenRow + x, infinite_edge(chosenCol + x)] for x in range(1, 8)],
                 [[chosenRow + x, infinite_edge(chosenCol - x)] for x in range(1, 8)],
                 [[chosenRow - x, infinite_edge(chosenCol + x)] for x in range(1, 8)],
                 [[chosenRow - x, infinite_edge(chosenCol - x)] for x in range(1, 8)]]

    # Goes through each of the options where the bishop can move.
    for diagonal in bish_move:
        for position in diagonal:

            # Sets row and col to the values in the position being checked.
            rows, cols = position[0], position[1]
            if on_board(rows, cols):

                # Checks if the place we are checking is one that the bishop can move to or capture at.
                if is_occupied(rows, cols):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(chosenRow, chosenCol) != is_white(rows, cols):
                        # Ensures that moving here will not result in check.
                        if will_not_check(rows, cols):
                            return True
                    break
                else:
                    # Ensures that moving here will not result in check.
                    if will_not_check(rows, cols):
                        return True

    # Can't move, so returns false
    return False


# Returns if the knight can move to any possible position, which signifies that it is not checkmate.
def mate_knight_moves():

    # Goes through a 4 by 4 grid marking each place where the knight can move.
    for x in range(-2, 3):
        for y in range(-2, 3):

            # Since knights move in a 2-1 fashion, or L shape, this ensures that an L shape is being made.
            if x ** 2 + y ** 2 == 5:

                rows, cols = chosenRow + x, infinite_edge(chosenCol + y)
                if on_board(rows, cols):

                    # Checks if the place we are checking is one that the knight can move to or capture at.
                    if is_occupied(rows, cols):
                        # If it is occupied, ensures that they are not taking their own piece.
                        if is_white(chosenRow, chosenCol) != is_white(rows, cols):
                            # Ensures that moving here will not result in check.
                            if will_not_check(rows, cols):
                                return True
                    else:
                        # Ensures that moving here will not result in check.
                        if will_not_check(rows, cols):
                            return True

    # Can't move, so returns false.
    return False


# Returns if the queen can move to any possible position, which signifies that it is not checkmate.
def mate_queen_moves():
    if mate_bishop_moves() or mate_rook_moves():
        return True
    else:
        return False


# Returns if the king can move to any possible position, which signifies that it is not checkmate.
def mate_king_moves():

    # Goes through each square a 3 by 3 grid surrounding the king, checking which squares it can move to.
    for x in range(3):
        for y in range(3):

            # Sets rows and cols to the rows and column being checked.
            rows = chosenRow - 1 + x
            cols = infinite_edge(chosenCol - 1 + y)

            # Ensures that we are checking a place on the board.
            if on_board(rows, cols):

                # Checks if the place we are checking is one that the king can move to or capture at.
                if is_occupied(rows, cols):
                    # If it is occupied, ensures that they are not taking their own piece.
                    if is_white(chosenRow, chosenCol) != is_white(rows, cols):
                        # Ensures that moving here will not result in check.
                        if will_not_check(rows, cols):
                            return True
                else:
                    # Ensures that moving here will not result in check.
                    if will_not_check(rows, cols):
                        return True

    # Returns false if no move was found.
    return False


# Dictionary of possible move methods that can be called.
moves = {
    'p': pawn_moves, 'r': rook_moves, 'b': bishop_moves, 'n': knight_moves, 'q': queen_moves, 'k': king_moves
}

# Dictionary of possible move methods that can be called when checking if the king is in check.
check_moves = {
    'p': check_pawn_moves, 'r': check_rook_moves,
    'b': check_bishop_moves, 'n': check_knight_moves,
    'q': check_queen_moves, 'k': check_king_moves
}

# Dictionary of possible move methods that can be called when checking if it is checkmate.
mate_moves = {
    'p': mate_pawn_moves, 'r': mate_rook_moves,
    'b': mate_bishop_moves, 'n': mate_knight_moves,
    'q': mate_queen_moves, 'k': mate_king_moves
}


# Calls the specific method which marks all possible moves for a piece.
def mark_movable():
    global chosenText
    moves[chosenText]()


# Called whenever the user is choosing which piece to use.
def choose_piece(rows, cols):

    # Doesn't let the user choose a new piece if the game is over or the user is promoting a pawn.
    if game_over or promoting_pawn:
        return

    # Ensures that the square which was clicked is occupied.
    if is_occupied(rows, cols):

        # Ensures that the correct player is choosing which piece to move.
        global white_turn, chosenRow, chosenCol, choosing_piece, chosen_colour, chosenPiece, chosenText
        if is_white(rows, cols) != white_turn:
            return

        # Saves the values of the square that was chosen.
        chosenRow, chosenCol = rows, cols
        chosen_colour = Board[rows][cols].bgn_colour
        chosenPiece = Board[rows][cols].piece
        chosenText = Board[rows][cols].piece.piece

        # Shows that the square here is chosen by changing the colour, and sets choosing piece to false.
        Board[rows][cols].bgn_colour = Color['chosen']
        choosing_piece = False

        # Marks where this piece that was chosen can go.
        mark_movable()


# Called whenever the user is moving a piece as they have already chosen one.
def move_piece(rows, cols):
    global choosing_piece, chosenPiece, white_turn

    # Resets the choosing variables if they clicked on the same square they originally did.
    if rows == chosenRow and cols == chosenCol:
        Board[rows][cols].bgn_colour = chosen_colour
        choosing_piece = True

        reset_background()
        in_check()

    # Selects the user's new piece if they clicked on another one of their pieces.
    elif Board[rows][cols].piece.team == Board[chosenRow][chosenCol].piece.team:
        Board[rows][cols].bgn_colour = chosen_colour
        reset_background()
        choose_piece(rows, cols)

    # If the user is doing an en passant.
    if Board[rows][cols].piece.image is passantCircle:
        en_passant(rows, cols)
        reset_background()
        reset_pawn_moves()
        Board[rows][cols].piece.moved = True

    if Board[rows][cols].piece.image is castleCircle:
        castling(rows, cols)
        reset_background()
        reset_pawn_moves()
        Board[rows][cols].piece.moved = True

    # If the user is moving/capturing another piece.
    if Board[rows][cols].bgn_colour == Color['can_kill'] or Board[rows][cols].piece.image is goCircle:

        # Resets the spot they moved from to a blank square, and puts it in its new spot.
        Board[chosenRow][chosenCol].bgn_colour = chosen_colour
        Board[chosenRow][chosenCol].piece = Piece('None', 'None', empty_square_image, False)
        Board[rows][cols].piece = chosenPiece

        # Changes who's move it is, and resets variables.
        white_turn = not white_turn
        choosing_piece = True
        reset_background()
        reset_pawn_moves()
        show_promote_pawn(rows, cols)
        pawn_just_moved(rows, cols)
        Board[rows][cols].piece.moved = True

    # Ensures that after showing the promote pawn options, we aren't checking if the king is in check.
    if not promoting_pawn:
        # Checks if the move made the king go into check.
        if not (chosen_colour == Color['in_check'] and Board[chosenRow][chosenCol].piece == 'k'):
            in_check()


# Called whenever a square is clicked and forms the basic logic of the game.
def square_clicked(rows, cols):

    # If the user is promoting a pawn, lets them.
    if promoting_pawn:
        promote_pawn(rows, cols)

    # Uses the correct logic for whenever the user is doing anything.
    global choosing_piece

    if choosing_piece:
        choose_piece(rows, cols)
    else:
        move_piece(rows, cols)


# Ensures that a move is one that is on the board.
def on_board(rows, cols):
    return 0 <= rows < 8 and 0 <= cols < 8


# Resets the background from any circles or colours.
def reset_background():
    for rows in Board:
        for cols in rows:
            if cols.piece.image == goCircle or cols.piece.image == passantCircle or cols.piece.image == castleCircle:
                cols.piece.image = emptySquare
            if (cols.row + cols.col) % 2 == 0:
                cols.bgn_colour = Color['light_blue']
            else:
                cols.bgn_colour = Color['dark_blue']


# Resets the pawn just moved lists after a move has been done because this did not 'just' move.
def reset_pawn_moves():
    global wPawnJustMoved, bPawnJustMoved
    wPawnJustMoved, bPawnJustMoved = [False for r in range(8)], [False for r in range(8)]


# Promotes a pawn.
def promote_pawn(rows, cols):

    global promoting_pawn

    # Ensures that a square which contains a possible promotion piece was clicked.
    if Board[rows][cols].bgn_colour != Color['white']:
        return

    # Variables for if the piece is white/black, and where it is on the board.
    verMult = -1
    prom_row = 7
    if is_white(rows, cols):
        verMult = 1
        prom_row = 0

    # Saves the piece chosen in new piece, and replaces everything back to how it was before.
    new_piece = Board[rows][cols].piece
    Board[prom_row][cols].piece = new_piece
    Board[prom_row + verMult][cols].piece = promote1
    Board[prom_row + verMult * 2][cols].piece = promote2
    Board[prom_row + verMult * 3][cols].piece = promote3

    # Changes promoting pawn and resets the background.
    promoting_pawn = not promoting_pawn
    reset_background()

    in_check()


# Checks if a pawn made it to the end and needs to be promoted, showing the promotion options.
def show_promote_pawn(rows, cols):

    # Exits the method if the piece being checked is not a pawn or is not at the end.
    if Board[rows][cols].piece.piece != 'p':
        return
    elif rows != 0 and rows != 7:
        return

    global promote1, promote2, promote3

    # Checks the colour of the pawn that just moved and if it is at the end of where it can go.
    if is_white(rows, cols) and rows == 0:

        # Saves the pieces below the one being changed on the board so that they can be reset after.
        promote1 = Board[rows + 1][cols].piece
        promote2 = Board[rows + 2][cols].piece
        promote3 = Board[rows + 3][cols].piece

        # Replaces the pieces at the current row and 3 below it with the options that the user has for promotion.
        Board[rows][cols].piece = Piece('w', 'q', white_queen_image, False)
        Board[rows + 1][cols].piece = Piece('w', 'r', white_rook_image, False)
        Board[rows + 2][cols].piece = Piece('w', 'b', white_bishop_image, False)
        Board[rows + 3][cols].piece = Piece('w', 'n', white_knight_image, False)

        # Change the background colour of the possible promotion pieces.
        Board[rows][cols].bgn_colour = Color['white']
        Board[rows + 1][cols].bgn_colour = Color['white']
        Board[rows + 2][cols].bgn_colour = Color['white']
        Board[rows + 3][cols].bgn_colour = Color['white']

    elif not is_white(rows, cols) and rows == 7:

        # Saves the pieces below the one being changed on the board so that they can be reset after.
        promote1 = Board[rows - 1][cols].piece
        promote2 = Board[rows - 2][cols].piece
        promote3 = Board[rows - 3][cols].piece

        # Replaces the pieces at the current row and 3 below it with the options that the user has for promotion.
        Board[rows][cols].piece = Piece('b', 'q', black_queen_image, False)
        Board[rows - 1][cols].piece = Piece('b', 'r', black_rook_image, False)
        Board[rows - 2][cols].piece = Piece('b', 'b', black_bishop_image, False)
        Board[rows - 3][cols].piece = Piece('b', 'n', black_knight_image, False)

        # Change the background colour of the possible promotion pieces.
        Board[rows][cols].bgn_colour = Color['white']
        Board[rows - 1][cols].bgn_colour = Color['white']
        Board[rows - 2][cols].bgn_colour = Color['white']
        Board[rows - 3][cols].bgn_colour = Color['white']

    # Changes promoting pawn to true since they're choosing what to promote to.
    global promoting_pawn
    promoting_pawn = not promoting_pawn


# Checks which squares any white piece can kill at.
def find_w_pieces():

    # Looks through board.
    for r in range(8):
        for c in range(8):

            # Uses methods which mark killable squares on the board for all white pieces.
            if is_occupied(r, c):
                if is_white(r, c):
                    check_moves[Board[r][c].piece.piece](r, c)


# Checks which squares any black piece can kill at.
def find_b_pieces():

    # Looks through board.
    for r in range(8):
        for c in range(8):

            # Uses methods which mark killable squares on the board for all white pieces.
            if is_occupied(r, c):
                if not is_white(r, c):
                    check_moves[Board[r][c].piece.piece](r, c)


# Checks if either king is in check.
def in_check():

    global check_back_colour

    # Finds both kings.
    for rows in range(8):
        for cols in range(8):

            # Checks if the piece at this rows and cols is a king, and sees which one it is.
            if Board[rows][cols].piece.piece == 'k':

                # Calls methods for the opposing colour's pieces, checking if any one of them can kill the king.
                if is_white(rows, cols):
                    find_b_pieces()

                    check_back_colour = Board[rows][cols].bgn_colour

                    # If the king can be killed, changes their background colour, if not resets it.
                    if Board[rows][cols].killable:
                        Board[rows][cols].bgn_colour = Color['in_check']

                        reset_kill()

                        # Checks if they are in checkmate.
                        checkmate(True, rows, cols)
                    else:
                        Board[rows][cols].bgn_colour = check_back_colour

                    reset_kill()

                else:
                    find_w_pieces()

                    check_back_colour = Board[rows][cols].bgn_colour

                    # If the king can be killed, changes their background colour, if not resets it.
                    if Board[rows][cols].killable:
                        Board[rows][cols].bgn_colour = Color['in_check']

                        reset_kill()

                        # Checks if they are in checkmate.
                        checkmate(False, rows, cols)
                    else:
                        Board[rows][cols].bgn_colour = check_back_colour

                    reset_kill()


# Ensures that moving a piece to this place will not result in check for its king.
def will_not_check(rows, cols):

    white = is_white(chosenRow, chosenCol)

    # Resets the spot they moved from to a blank square.
    Board[chosenRow][chosenCol].piece = Piece('None', 'None', empty_square_image, False)

    # Saves the info of the piece being replaced, and then replaces it.
    check_piece = Board[rows][cols].piece
    Board[rows][cols].piece = chosenPiece

    # Finds the kings, calls the proper methods for their opponent's pieces, and displays if they are in check.
    for r in range(8):
        for c in range(8):

            # Ensures that we are looking at a king.
            if Board[r][c].piece.piece == 'k':

                # Calls proper methods for the opponent's pieces.
                if is_white(r, c) and white:
                    find_b_pieces()

                    # Puts the pieces back where they should be.
                    Board[chosenRow][chosenCol].piece = chosenPiece
                    Board[rows][cols].piece = check_piece

                    # If the king can be killed, returns false since they should not move there.
                    if Board[r][c].killable:
                        reset_kill()
                        return False
                    else:
                        reset_kill()
                        return True

                elif (not is_white(r, c)) and (not white):
                    find_w_pieces()

                    # Puts the pieces back where they should be.
                    Board[chosenRow][chosenCol].piece = chosenPiece
                    Board[rows][cols].piece = check_piece

                    # If the king can be killed, returns false since they should not move there.
                    if Board[r][c].killable:
                        reset_kill()
                        return False
                    else:
                        reset_kill()
                        return True


# Displays the winner on the board.
def show_winner():

    # Sets the text to be displayed on the board.
    winner_str = ''
    if white_win:
        winner_str = 'White '
    else:
        winner_str = 'Black '
    winner_str += 'has won the game!'

    # Displays the winner on the board.
    winner_txt = word_font.render(winner_str, False, Color["white"])
    WIN.blit(winner_txt, (20, win_height - 40))


# Checks if a king is in checkmate.
def checkmate(white, rows, cols):

    global chosenRow, chosenCol, chosenText, chosenPiece

    # Goes through all white/black pieces and checks if any can move, exiting the method if they can.
    for r in range(8):
        for c in range(8):

            # Ensures that we are looking at the pieces of the correct player.
            if is_occupied(r, c) and is_white(r, c) == white:

                # Sets the global fields.
                chosenRow, chosenCol = r, c
                chosenText = str(Board[r][c].piece.piece)
                chosenPiece = Board[r][c].piece
                # print('checking ' + chosenText + ' at ' + str(chosenRow) + ', ' + str(chosenCol))

                # Checks if the piece has any moves, exiting if they do because then it isn't checkmate.
                if mate_moves[chosenText]():
                    return

    # The method was not exited so a winner was found, and is displayed.
    global game_over, white_win
    game_over, white_win = True, not white
    reset_background()

    # Puts the king's background colour back to the in check colour.
    Board[rows][cols].bgn_colour = Color['in_check']


# Resets killable attribute on board.
def reset_kill():

    for rows in range(8):
        for cols in range(8):
            Board[rows][cols].killable = False


# Checks if a piece at a square is white.
def is_white(rows, cols):
    return Board[rows][cols].piece.team == 'w'


# Checks if a square is occupied.
def is_occupied(rows, cols):
    return Board[rows][cols].piece.team != 'None'


# Fills the board up properly before beginning the game.
fill_board()


# The logic which is used while the game is running.
while True:
    clock.tick(50)
    keysPressed = pygame.key.get_pressed()

    # When the user exits the game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Test thing for resetting the board.
        if keysPressed[pygame.K_DOWN]:
            reset_board()

        # Gets the row and column of the button which was clicked.
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_square(pos)

            # Calls button method using row and column.
            if row < 8 and col >= 0:
                square_clicked(row, col)
            else:
                # If they clicked outside of the board on the restart button.
                clicked_restart(pos)

    # Draws everything on the board
    WIN.fill(win_colour)
    draw_board()

    # Shows the winner if the game ended.
    if game_over:
        show_winner()

    pygame.display.flip()
