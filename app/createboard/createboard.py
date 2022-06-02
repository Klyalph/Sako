from .constants import *
from .fen2png import Board, DrawImage
from typing import Optional


def create_board(fen: str, name) -> Optional[str]:
    """Returns the path to the image created by the FEN notation"""
    fen = Board(fen.split())
    if fen.isvalid:
        board_image = DrawImage(fen, "png", "./app/createboard", name)
        board_image.create()
        board_image.to_image()
        return "{}/{}.png".format(os.path.dirname(__file__), board_image.fname)
