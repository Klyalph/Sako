from __future__ import annotations

from typing import List

import chess
import nextcord
from nextcord.ext import commands

from ..objects import Game, GamesCollection, UsersCollection
from .cog_utils.check import check_user
from .cog_utils.continuation import game_continuation, wait_for_move
from .cog_utils.uploadboard import upload_board


class GameDropdown(nextcord.ui.Select):
    def __init__(
        self, options: List[nextcord.SelectOption], view, user_id: int
    ):
        # Required some workarounds...
        self._view = view
        self.user_id = user_id
        super().__init__(
            placeholder="☀️ Choose A Game",
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
        super().__init__(timeout=25)
        self.add_item(
            GameDropdown(options, self, user_id),
        )


class ListMoves(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def availablemoves(self, ctx):

        if ctx.channel.type == nextcord.ChannelType.private:
            return

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

        options = self.create_game_dropdown_options(ctx, games)

        view = GameDropdownView(options, ctx.author.id)
        msg = await ctx.send(view=view)

        await view.wait()

        # If the user don't respond in time
        if view.value is None:
            await msg.delete()
            if user_profile.pending_command == str(ctx.message.id):
                await ctx.reply("It Took You Too Long To Respond")
            return

        game = GamesCollection.get_game(view.value)
        opponent = self.client.get_user(
            int(game.get_opponent_profile(str(ctx.author.id)).id)
        )

        if user_profile.pending_command != str(ctx.message.id):
            await msg.delete()
            return

        await msg.delete()
        board = chess.Board(fen=game.fen_notation)
        msg = await upload_board(self.client, ctx, game, board, user_profile)

        if ctx.channel.type == nextcord.ChannelType.private:
            await wait_for_move(self, ctx, game, msg, board, user_profile)
        else:
            await game_continuation(self, ctx, game, msg, board, opponent)

    @commands.command()
    async def am(self, ctx):
        await self.availablemoves(ctx)

    def create_game_dropdown_options(self, ctx, games: List[Game]):
        options = []
        for game in games:
            opponent_profile = game.get_opponent_profile(str(ctx.author.id))
            opponent = self.client.get_user(int(opponent_profile.id))
            options.append(
                nextcord.SelectOption(
                    label=f"Vs. {opponent.name}"
                    f" ({opponent_profile.elo} elo) (id: {game.id})",
                    description=f"Time Left To Respond: "
                    f"{game.time_left()} | {game.moves} Move(s) Made So Far",
                    value=str(game.id),
                    emoji="☀️",
                )
            )
        return options


def setup(client):
    client.add_cog(ListMoves(client))
