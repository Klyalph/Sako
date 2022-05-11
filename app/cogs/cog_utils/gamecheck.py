from __future__ import annotations

import chess

from .processresults import process_draw, process_win


async def game_check(self_, ctx, game, msg, board: chess.Board):
    if board.is_checkmate():
        await process_win(self_, ctx, game, msg, board)
        return True
    elif board.is_stalemate() or board.is_insufficient_material():
        await process_draw(self_, ctx, game, msg, board)
        return True
