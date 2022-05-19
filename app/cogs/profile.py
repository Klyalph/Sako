import nextcord
from nextcord.ext import commands

from ..objects import (
    GamesCollection,
    User,
    UsersCollection,
    PreviousGamesCollection,
)
from ..utils.emojis import EMOJI
from .cog_utils.check import check_user


class UserProfile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def profile(self, ctx):
        if ctx.channel.type == nextcord.ChannelType.private:
            return

        await check_user(ctx.author)

        user_profile = UsersCollection.get_user(str(ctx.author.id))
        embed = self._create_profile_embed(user_profile, ctx)
        embed = self._add_current_games_to_embed(ctx, user_profile, embed)
        embed = self._add_previous_games_to_embed(ctx, user_profile, embed)
        await ctx.send(embed=embed)

    @commands.command()
    async def p(self, ctx):
        await self.profile(ctx)

    @staticmethod
    def _create_profile_embed(user: User, ctx) -> nextcord.Embed:
        return (
            nextcord.Embed(
                title=f"User Statistics For {ctx.author.name}",
                color=0x2F3136,
            )
            .set_author(
                name=f"{ctx.author.name}'s Chess Profile",
                icon_url=ctx.author.display_avatar,
            )
            .add_field(
                name=f"{EMOJI['star']} {user.compute_win_percentage()}% winrate"
                f"\n{EMOJI['chart']} {user.elo} elo",
                value="\u200b",
                inline=False,
            )
            .add_field(
                name=f"{EMOJI['trophy']} {user.wins} Wins",
                value="\u200b",
                inline=True,
            )
            .add_field(
                name=f"{EMOJI['anger']} {user.losses} Losses",
                value="\u200b",
                inline=True,
            )
            .add_field(
                name=f"{EMOJI['shake']} {user.stalemates} Stalemates",
                value="\u200b",
                inline=True,
            )
        )

    def _add_current_games_to_embed(
        self, ctx, user: User, embed: nextcord.Embed
    ) -> nextcord.Embed:
        games = GamesCollection.get_games_by_user_id(user.id)
        if not games:
            return embed

        str_games = []

        for game in games:
            opponent_profile = game.get_opponent_profile(user.id)
            opponent = self.client.get_user(int(opponent_profile.id))
            str_games.append(
                self._current_game_string(
                    ctx, user, opponent, opponent_profile, game
                )
            )

        return embed.add_field(
            name=f"{EMOJI['pawn']} Ongoing Games: \n \u200b",
            value="\n".join(str_games) + "\n \u200b",
            inline=False,
        )

    @staticmethod
    def _current_game_string(ctx, user, opponent, opponent_profile, game):
        return (
            f"**{ctx.author.name} "
            f"vs. {opponent.name}** ({opponent_profile.elo}) (id: {game.id})"
        )

    def _add_previous_games_to_embed(
        self, ctx, user: User, embed: nextcord.Embed
    ):
        previous_games = PreviousGamesCollection.get_previous_games(user.id)
        if not previous_games:
            return embed

        str_games = []

        for previous_game in previous_games[:10]:
            opponent_profile = UsersCollection.get_user(
                previous_game.opponent_id
            )
            opponent_disc_profile = self.client.get_user(
                int(opponent_profile.id)
            )
            str_games.append(
                self._previous_game_string(
                    ctx, opponent_disc_profile, previous_game
                )
            )

        return embed.add_field(
            name=f"{EMOJI['pawn']} Previous Games: \n \u200b",
            value="\n".join(str_games) + "\n \u200b",
            inline=False,
        )

    @staticmethod
    def _previous_game_string(ctx, opponent_disc_profile, previous_game):
        result = [
            "Lost",
            "Stalemate",
            "Won",
        ][previous_game.result]

        return f"**vs. {opponent_disc_profile.name}:** {result} (game ended {previous_game.time} UTC)"


def setup(client):
    client.add_cog(UserProfile(client))
