import nextcord
from discord import SlashOption
from nextcord.ext import commands

from ..objects import GamesCollection, User, UsersCollection
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
        await ctx.send(embed=embed)

    @staticmethod
    def _create_profile_embed(user: User, ctx) -> nextcord.Embed:
        return (
            nextcord.Embed(
                title=f"User Statistics For {ctx.author.name}",
                color=nextcord.Color.from_rgb(0, 0, 0),
            )
            .set_author(
                name=f"{ctx.author.name}'s Sako Profile",
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
                self.current_game_string(ctx, user, opponent, opponent_profile)
            )

        return embed.add_field(
            name=f"{EMOJI['pawn']} Ongoing Games:",
            value="\n".join(str_games),
            inline=False,
        )

    @staticmethod
    def current_game_string(ctx, user, opponent, opponent_profile):
        return (
            f"{ctx.author.name} "
            f"vs. {opponent.name} ({opponent_profile.elo})"
        )


def setup(client):
    client.add_cog(UserProfile(client))
