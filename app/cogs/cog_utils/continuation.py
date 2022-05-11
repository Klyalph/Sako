from __future__ import annotations

import asyncio

import chess
from nextcord.ext import commands

from ...objects import Game, UsersCollection
from .gamecheck import game_check
from .movecheck import create_move_check
from .uploadboard import update_board
from .processresults import process_resignation


# TODO: add support for resign and draw
# print a message of sorts if one of the users don't respond


async def game_continuation(
    self_, ctx, game, msg, board: chess.Board, opponent
):

    while 1:

        if await wait_for_user_move(self_, ctx, game, msg, board):
            break

        if await wait_for_opponent_move(
            self_, ctx, game, msg, board, opponent
        ):
            break


async def wait_for_opponent_move(
    self_, ctx, game: Game, msg, board: chess.Board, opponent
) -> bool:
    current_moves = [str(move) for move in board.legal_moves]

    user = UsersCollection.get_user(str(opponent.id))
    user.pending_command = str(msg.id)

    user_color = game.get_user_color(str(opponent.id))

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

    await update_board(board, user_color, game, msg)

    if await game_check(self_, ctx, game, msg, board):
        return True

    return False


async def wait_for_user_move(
    self_, ctx, game, msg, board: chess.Board
) -> bool:
    current_moves = [str(move) for move in board.legal_moves]
    user_color = game.get_user_color(str(ctx.author.id))

    user = UsersCollection.get_user(str(ctx.author.id))
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

    await update_board(board, user_color, game, msg)

    if await game_check(self_, ctx, game, msg, board):
        return True

    return False
