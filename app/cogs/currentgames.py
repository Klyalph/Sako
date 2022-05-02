from __future__ import annotations

import asyncio

import chess
import nextcord
from nextcord.ext import commands

from typing import List
from ..objects import Game, GamesCollection, UsersCollection
from ..utils.emojis import EMOJI
from .cog_utils.check import check_user
from .cog_utils.move_check import create_move_check
from .cog_utils.process_results import process_draw, process_win
from .cog_utils.upload_board import update_board, upload_board

# TODO: ADD EMBEDS

# Check if person wants to resign
# Check if game is over, and then
# IN what way the game is over
# And distribute points
# And add them to previous games to both of the profiles
# checking if game over should be done after a move, in the LS
# CHeck if a game is lost by checking if the time is over.


class GameDropdown(nextcord.ui.Select):
    def __init__(
        self, options: List[nextcord.SelectOption], view, user_id: int
    ):
        # Required some workarounds...
        self._view = view
        self.user_id = user_id
        super().__init__(
            placeholder="🌟 Choose A Game",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id == self.user_id:
            self._view.value = self.values[0]
            return self._view.stop()


class GameDropdownView(nextcord.ui.View):
    def __init__(self, options: List[nextcord.SelectOption], user_id: int):
        self.value = None
        super().__init__(timeout=10)
        self.add_item(
            GameDropdown(options, self, user_id),
        )


class ListMoves(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ls(self, ctx):
        await check_user(ctx.author)
        games = [
            game
            for game in GamesCollection.get_games_by_user_id(
                str(ctx.author.id)
            )
            if game.is_user_turn(str(ctx.author.id))
        ]
        if len(games) == 0:
            await ctx.reply("No Turns Available")
            return

        user_profile = UsersCollection.get_user(str(ctx.author.id))
        user_profile.pending_command = str(ctx.message.id)

        options = self.create_game_dropdowns(ctx, games)

        view = GameDropdownView(options, ctx.author.id)
        msg = await ctx.send(view=view)

        await view.wait()

        # If the user don't respond in time
        if view.value is None:
            await msg.delete()
            await ctx.reply("You took too long to respond")
            return

        game = GamesCollection.get_game(view.value)

        if user_profile.pending_command != str(ctx.message.id):
            msg.delete()
            return

        await msg.delete()
        board = chess.Board(fen=game.fen_notation)
        msg, user_color = await upload_board(ctx, game, board, user_profile)

        available_moves = [str(move) for move in board.legal_moves]
        check = create_move_check(ctx, available_moves)

        try:
            move = await self.client.wait_for(
                "message", check=check, timeout=60
            )
        except asyncio.TimeoutError:
            await ctx.send("It took you too long to make a move!")
            return

        if user_profile.pending_command != str(ctx.message.id):
            return

        board.push_san(move.content)
        game.move(board.fen())

        await move.add_reaction("✅")

        # Update board with move taken
        await update_board(board, user_color, game, msg)

        # Check if the game is over
        if board.is_checkmate():
            await process_win(self, ctx, game, msg, board)
            return

        elif (
            board.is_stalemate()
            or board.is_insufficient_material()
        ):
            await process_draw(self, ctx, game, msg, board)
            return

    def create_game_dropdowns(self, ctx, games: List[Game]):
        options = []
        for game in games:
            opponent_profile = game.get_opponent_profile(str(ctx.author.id))
            opponent = self.client.get_user(int(opponent_profile.id))
            options.append(
                nextcord.SelectOption(
                    label=f"Vs. {opponent.name}"
                    f" ({opponent_profile.elo} elo)",
                    description=f"Time Left To Respond: "
                    f"{game.time_left()} | {game.moves} Move(s) Made So Far",
                    value=str(game.id),
                    emoji="☀️",
                )
            )
        return options


def setup(client):
    client.add_cog(ListMoves(client))
