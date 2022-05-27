import nextcord
from nextcord.ext import commands

from .cog_utils.check import check_user
from typing import List
from ..objects import UsersCollection, GamesCollection, Game
from ..utils.emojis import EMOJI


class GameList(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gamelist(self, ctx):
        await check_user(ctx.author)

        user_chess_profile = UsersCollection.get_user(str(ctx.author.id))

        games = GamesCollection.get_games_by_user_id(str(ctx.author.id))
        if len(games) == 0:
            await ctx.send(embed=self.no_ongoing_games_embed(ctx))
            return

        await ctx.send(embed=self.ongoing_games_embed(ctx, games))

    @staticmethod
    def no_ongoing_games_embed(ctx) -> nextcord.Embed:
        return nextcord.Embed(
            title="You Have No Current Ongoing Games",
            description="Challenge Someone To A Game Of Chess"
            " By Typing **?ch <username>**!",
            color=0x2F3136,
        ).set_author(
            name=f"{ctx.author.name}",
            icon_url=ctx.author.display_avatar,
        )

    def ongoing_games_embed(self, ctx, games: List[Game]):
        embed = nextcord.Embed(
            title=f"You Currently have {len(games)} Ongoing Game(s)",
            color=0x2F3136,
        ).set_author(
            name=f"{ctx.author.name}",
            icon_url=ctx.author.display_avatar,
        )

        games_str = []
        for game in games:
            opponent = game.get_opponent_profile(str(ctx.author.id))
            opponent_disc_profile = self.client.get_user(int(opponent.id))

            games_str.append(
                self.create_game_string(
                    ctx,
                    opponent_disc_profile,
                    game,
                    game.is_user_turn(str(ctx.author.id)),
                )
            )

        embed.add_field(name="\u200b", value="\n".join(games_str))

        return embed

    @staticmethod
    def create_game_string(
        ctx,
        opponent_disc_profile: nextcord.Member,
        game: Game,
        is_user_turn: bool,
    ) -> str:
        if is_user_turn:
            v = "Your turn"
        else:
            v = f"{opponent_disc_profile.name}'s turn"

        return (
            f"{EMOJI['pawn']} **{v}: game versus {opponent_disc_profile.name}\n "
            f"{EMOJI['chart']} (opponent elo: "
            f"{game.get_opponent_profile(str(ctx.author.id)).elo}) "
            f"(time left: {game.time_left()})** \n\n"
        )


def setup(client):
    client.add_cog(GameList(client))
