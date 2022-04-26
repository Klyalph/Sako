import chess
import nextcord

from ...chessboards import ChessBoards
from ...objects import Game, User


async def upload_board(ctx, game: Game, board: chess.Board, user: User):
    user_color = game.get_user_color(user.id)
    board = chess.Board(fen=game.fen_notation)
    path_to_pic = ChessBoards.board(board, user_color, game.id)
    file = nextcord.File(path_to_pic)
    msg = await ctx.send(file=file)
    return msg, user_color


async def update_board(board, user_color, game, msg):
    path_to_pic = ChessBoards.board(board, user_color, game.id)
    file = nextcord.File(path_to_pic)
    await msg.edit(file=file)
