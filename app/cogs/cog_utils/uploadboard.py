import chess
import nextcord
import os

from ...createboard import create_board
from ...objects import Game, User

flags = {
    chess.WHITE: "<:flag_white:959942962920439818>",
    chess.BLACK: "<:flag_black:959942962902708737>",
}


async def upload_board(
    client: nextcord.Client, ctx, game: Game, board: chess.Board, user: User
):
    board = chess.Board(fen=game.fen_notation)
    path_to_pic = create_board(board.fen(), game.id)
    file = nextcord.File(path_to_pic)
    msg = await ctx.send(file=file, embed=_board_embed(client, game, board))
    os.remove(path_to_pic)
    return msg


# Add more game information in this embed
# Calculate the number of whitspaes needed to make this clean. ➣ ➣ ➣
def _board_embed(
    client: nextcord.Client, game: Game, board: chess.Board
) -> nextcord.Embed:
    user_disc_one = client.get_user(int(game.user1_id.id))
    user_disc_two = client.get_user(int(game.user2_id.id))
    text_len = len(f"Game {game.id} \u200b")
    v = " " * (63 - text_len)

    return nextcord.Embed(
        title=f"Game {game.id} {v} \u200b"
        f"\n{game.moves} Move(s) Taken So Far"
        f"\n{user_disc_two.name} vs {user_disc_one.name}",
        description="\u200b",
        color=0x2F3136,
    ).add_field(
        name=f"{flags[board.turn]} To Move" f"\nTime Left: {game.time_left()}",
        value="\u200b",
        inline=True,
    )


async def update_board(client: nextcord.Client, board, user_color, game, msg):
    path_to_pic = create_board(board.fen(), game.id)

    file = nextcord.File(path_to_pic)
    await msg.edit(file=file, embed=_board_embed(client, game, board))
    os.remove(path_to_pic)
