import chess
import nextcord

from ...createboard import create_board
from ...objects import Game, User

flags = {
    chess.WHITE: "<:flag_white:959942962920439818>",
    chess.BLACK: "<:flag_black:959942962902708737>",
}


async def upload_board(ctx, game: Game, board: chess.Board, user: User):
    board = chess.Board(fen=game.fen_notation)
    path_to_pic = create_board(board.fen(), game.id)
    file = nextcord.File(path_to_pic)
    msg = await ctx.send(file=file, embed=_board_embed(game, board))
    return msg


# Add more game information in this embed
# Calculate the number of whitspaes needed to make this clean.
def _board_embed(game: Game, board: chess.Board) -> nextcord.Embed:
    v = " " * 51
    return nextcord.Embed(
        title=f"Game {game.id} {v} \u200b"
        f"\n{game.moves} Move(s) Taken So Far",
        description="\u200b",
        color=0x2F3136,
    ).add_field(
        name=f"{flags[board.turn]} To Move" f"\nTime Left: {game.time_left()}",
        value="\u200b",
        inline=True,
    )


async def update_board(board, user_color, game, msg):
    path_to_pic = create_board(board.fen(), game.id)

    file = nextcord.File(path_to_pic)
    await msg.edit(file=file, embed=_board_embed(game, board))
