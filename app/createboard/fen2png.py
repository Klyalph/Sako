from .constants import (
    PIECES,
    FEN_PIECES,
    BOARD_SIZE,
    PIECE_SIZE,
    RESOURCES,
    SQUARE_SIZE,
)
from PIL import Image


class DrawImage:
    def __init__(self, board, fmt, dest, fname):

        if board.move == "w":
            self.result = Image.open(RESOURCES + "board.png").resize(
                BOARD_SIZE
            )
        else:
            self.result = Image.open(RESOURCES + "boardb.png").resize(
                BOARD_SIZE
            )
        self.board = board.board
        self.fmt = fmt
        self.fname = fname
        self.dest = dest

    @staticmethod
    def open_image(piece):
        try:
            im = Image.open(RESOURCES + "{}.png".format(piece))
            return im.resize(PIECE_SIZE)
        except:
            print(piece + ".png", "does not exist.")

    def insert(self, piece, square):  # square is tuple (r,c)
        R = square[0] * SQUARE_SIZE
        C = square[1] * SQUARE_SIZE
        self.result.paste(piece, (R, C), piece)

    def create(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    piece = self.open_image(self.board[i][j])
                    self.insert(piece, (i, j))

    def to_image(self):
        self.result.save("{}/{}.{}".format(self.dest, self.fname, self.fmt))


class Board:
    def __init__(self, fen):
        self.fen = fen
        self.isvalid = self.is_valid_fen()
        self.board = None
        self.move = fen[1]
        if self.isvalid:
            self.board = self.fen_to_board()

    def is_valid_fen(self):
        board, move, castle, enpassant, half_move, full_move = self.fen
        return (
            self.is_valid_board(board)
            and self.is_valid_move(move)
            and self.is_valid_enpassant(enpassant)
            and self.is_int(half_move)
            and self.is_int(full_move)
        )

    def fen_to_board(self):
        board = [["" for _ in range(8)] for _ in range(8)]
        board_str = self.fen[0].split("/")
        for i, rank in enumerate(board_str):
            pos = 0
            for square in rank:
                if self.is_int(square):
                    pos += int(square)
                else:
                    board[pos][i] = FEN_PIECES[square]
                    pos += 1

        if self.move == "b":
            for i in range(4):
                for j in range(8):
                    board[i][j], board[8 - i - 1][8 - j - 1] = (
                        board[8 - i - 1][8 - j - 1],
                        board[i][j],
                    )
        return board

    @staticmethod
    def is_int(value):
        return value.isnumeric()

    def is_valid_enpassant(self, square):
        return self.is_valid_square(square) or square == "-"

    @staticmethod
    def is_valid_square(square):
        if len(square) > 2:
            return False
        return square[0] in "abcdefgh" and square[1] in "12345678"

    @staticmethod
    def is_valid_move(move):
        return move == "w" or move == "b"

    def is_valid_board(self, board):
        board = board.split("/")
        if len(board) != 8:
            return False
        for rank in board:
            length = 0
            for piece in rank:
                if self.is_int(piece):
                    length += int(piece)
                elif piece in PIECES:
                    length += 1
                else:
                    return False
            if length != 8:
                return False
        return True
