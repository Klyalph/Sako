import asyncio

import chess
import nextcord
from app.objects.gamescollection import GamesCollection
from nextcord.ext import commands

from ..chessboards import ChessBoards
from ..objects import User, UsersCollection
from .cog_utils.check import check_user
from .cog_utils.move_check import create_move_check
from .cog_utils.parse import parse_user
from .cog_utils.process_results import process_draw, process_win
from .cog_utils.upload_board import update_board, upload_board


class MakeMove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mm(self, ctx, opponent):
        if ctx.channel.type == nextcord.ChannelType.private:
            return

        opponent = parse_user(self, ctx, opponent)
        if opponent is None:
            await ctx.send(
                "Please Enter A Valid Username To Challenge Someone!"
            )
            return

        await check_user(ctx.author)
        await check_user(opponent)

        user = UsersCollection.get_user(ctx.author.id)
        user.pending_command = str(ctx.message.id)

        game = self.get_game(user.id, opponent)

        if game is None:
            msg = await ctx.send("You Have No Turns")
            return

        board = chess.Board(fen=game.fen_notation)
        msg, user_color = await upload_board(ctx, game, board, user)

        available_moves = [str(move) for move in board.legal_moves]
        check = create_move_check(ctx, available_moves)

        try:
            move = await self.client.wait_for(
                "message", check=check, timeout=60
            )
        except asyncio.TimeoutError:
            await ctx.send("It Took You Too Long To Make A Move!")
            return

        if user.pending_command != str(ctx.message.id):
            return

        board.push_san(move.content)
        game.move(board.fen())

        await move.add_reaction("✅")

        await update_board(board, user_color, game, msg)

        if board.is_checkmate():
            await process_win(self, ctx, game, msg, board)
            return

        elif (
            board.is_stalemate()
            or board.is_insufficient_material()
            or board.is_repetition(count=3)
        ):
            await process_draw(self, ctx, game, msg, board)
            return

    @staticmethod
    def get_game(id: str, opponent):
        games = [
            game
            for game in GamesCollection.get_games_by_user_id(id)
            if game.is_user_turn(id)
            and (
                game.user1_id.id == str(opponent.id)
                or game.user2_id.id == str(opponent.id)
            )
        ]
        if len(games) == 0:
            return None

        return games[0]


def setup(client):
    client.add_cog(MakeMove(client))
