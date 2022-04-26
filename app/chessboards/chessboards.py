import os

import chess
import chess.svg
import nextcord
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
import time
import sys


class ChessBoards:
    @classmethod
    def board(cls, board: chess.Board, orientation, game_id: str) -> str:

        with open(f"app/chessboards/{game_id}.svg", "wt") as f:
            f.write(chess.svg.board(board, size=2048, orientation=orientation))
        drawing = svg2rlg(f"app/chessboards/{game_id}.svg")

        renderPM.drawToFile(
            drawing, f"app/chessboards/{game_id}.png", fmt="PNG"
        )

        return f"{os.getcwd()}/app/chessboards/{game_id}.png"

        os.remove(f"./chessboards/{game_id}.svg")
        os.remove(f"./chessboards/{game_id}.png")

    # @classmethod
    # def board_test(cls, board: chess.Board, orientation, game_id: str) -> str:

    #     with open(f"./{game_id}.svg", "wt") as f:
    #         f.write(chess.svg.board(board, size=2048, orientation=orientation))
    #     drawing = svg2rlg(f"./{game_id}.svg")

    #     renderPM.drawToFile(
    #         drawing, f"./{game_id}.png", fmt="PNG"
    #     )

    #     return f"{os.getcwd()}/app/chessboards/{game_id}.png"

    #     os.remove(f"./chessboards/{game_id}.svg")
    #     os.remove(f"./chessboards/{game_id}.png")


# TODO: Make function that can remove the images created

# now = time.time()
# for _ in range(1000):
#     ChessBoards.board_test(chess.Board(), chess.BLACK, str(now))

# #Print time
# print(time.time() - now)
