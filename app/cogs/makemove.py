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
    async def makemove(self, ctx, opponent, *args):
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

        if time_left := (user.is_on_cooldown()):
            await ctx.send(
                f"{EMOJI['hourglass']} "
                f"| **{ctx.author.name}!** Please wait **{time_left}s** "
            )
            return

        game = self.get_game(user.id, opponent)

        if game is None:
            msg = await ctx.send("You Have No Turns")
            return

        board = chess.Board(fen=game.fen_notation)
        msg = await upload_board(self.client, ctx, game, board, user)

        await game_continuation(self, ctx, game, msg, board, opponent)

    # @commands.command()
    # async def makemove(self, ctx, opponent):
    #     await self.m(ctx, opponent)

    # @commands.command()
    # async def mm(self, ctx, opponent):
    #     await self.m(ctx, opponent)

    @staticmethod
    def get_game(id: str, opponent):
        # Fetches the games where it is the user's turn
        games = [
            game
            for game in GamesCollection.get_games_by_user_id(id)
            if game.is_user_turn(id)
            and (
                game.user1_id.id == str(opponent.id)
                or game.user2_id.id == str(opponent.id)
            )
        ]
        if len(games):
            return games[0]


def setup(client):
    client.add_cog(MakeMove(client))
