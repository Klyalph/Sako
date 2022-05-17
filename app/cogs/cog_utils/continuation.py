from __future__ import annotations

import asyncio

import chess

from ...objects import Game, UsersCollection, User
from .gamecheck import game_check
from .movecheck import create_move_check
from .uploadboard import update_board
from .processresults import process_resignation
import nextcord


# TODO: add support for draw
# Update board command doesn't work for some reason when it is send in available moves in dm


async def game_continuation(
    self_, ctx, game, msg, board: chess.Board, opponent: nextcord.Member
) -> None:

    user = UsersCollection.get_user(str(ctx.author.id))
    opponent_user = UsersCollection.get_user(str(opponent.id))
    while 1:
        if await wait_for_move(self_, ctx, game, msg, board, user):
            break

        if await wait_for_move(self_, ctx, game, msg, board, opponent_user):
            break


async def wait_for_move(
    self_, ctx, game: Game, msg, board: chess.Board, user: User
) -> bool:
    current_moves = [str(move) for move in board.legal_moves]
    user_color = game.get_user_color(str(user.id))

    user.pending_command = str(msg.id)
    check = create_move_check(ctx, user, current_moves)

    try:
        move = await self_.client.wait_for("message", check=check, timeout=100)
    except asyncio.TimeoutError:
        return True

    if user.pending_command != str(msg.id):
        return True

    if move.content == "resign":
        await process_resignation(self_, ctx, game, msg, board)
        return True

    board.push_san(move.content)
    game.move(board.fen())

    try:
        await move.delete()
    except Exception:
        pass

    await update_board(self_.client, board, user_color, game, msg)

    if await game_check(self_, ctx, game, msg, board):
        return True

    return False
