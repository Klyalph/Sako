import os

PIECES = set("RNBKQPrnbkqp")
FEN_PIECES = {i: ("b" if i.islower() else "w") + i.lower() for i in PIECES}
BOARD_DIMENSIONS = 640
BOARD_SIZE = (BOARD_DIMENSIONS, BOARD_DIMENSIONS)
SQUARE_SIZE = 80
PIECE_SIZE = (SQUARE_SIZE, SQUARE_SIZE)
RESOURCES = f"{os.path.dirname(__file__)}/resources/"
