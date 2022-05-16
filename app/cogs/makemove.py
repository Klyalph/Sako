import chess
import nextcord
from app.objects.gamescollection import GamesCollection
from nextcord.ext import commands

from ..objects import UsersCollection
from .cog_utils.check import check_user
from .cog_utils.continuation import game_continuation
from .cog_utils.parse import parse_user
from .cog_utils.uploadboard import upload_board
from ..utils.emojis import EMOJI


# Write to just find the first game where the person hasn't made a move.
class MakeMove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def makemove(self, ctx):
        if ctx.channel.type == nextcord.ChannelType.private:
            return

        await check_user(ctx.author)

        user = UsersCollection.get_user(str(ctx.author.id))
        user.pending_command = str(ctx.message.id)

        if time_left := (user.is_on_cooldown()):
            await ctx.send(
                f"{EMOJI['hourglass']} "
                f"| **{ctx.author.name}!** Please wait **{time_left}s** "
            )
            return

        game = self.get_game(user.id)

        if game is None:
            msg = await ctx.send("You Have No Turns")
            return

        board = chess.Board(fen=game.fen_notation)
        msg = await upload_board(self.client, ctx, game, board, user)
        opponent_profile = UsersCollection.get_user(
            game.get_opponent_profile(user.id).id
        )

        opponent_disc_profile = self.client.get_user(int(opponent_profile.id))
        await game_continuation(
            self, ctx, game, msg, board, opponent_disc_profile
        )

    @commands.command()
    async def makemove(self, ctx):
        await self.makemove(ctx)

    @commands.command()
    async def mm(self, ctx):
        await self.makemove(ctx)

    @staticmethod
    def get_game(id: str):
        # Fetches the games where it is the user's turn
        games = [
            game
            for game in GamesCollection.get_games_by_user_id(id)
            if game.is_user_turn(id)
        ]
        if len(games):
            return games[0]


def setup(client):
    client.add_cog(MakeMove(client))
