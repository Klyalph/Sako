import nextcord

from nextcord.ext import commands
from ..utils.emojis import EMOJI


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = self.help_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command()
    async def h(self, ctx):
        await self.help(ctx)

    @staticmethod
    def help_embed(ctx) -> nextcord.Embed:
        return (
            nextcord.Embed(
                description="Here is a list of commands!",
                color=0xFFFFFF,
            )
            .set_author(
                name="Command List",
                icon_url=ctx.author.display_avatar,
            )
            .add_field(
                name=f"{EMOJI['star']} `?help` | `?h`",
                value="Shows this message \n \u200b",
                inline=False,
            )
            .add_field(
                name=f"{EMOJI['pawn']} `?makemove` | `?move` | `?mm`",
                value="Make a move in one of your current chess games \n \u200b",
                inline=False,
            )
            .add_field(
                name=f"{EMOJI['fire']} `?createchallenge` | `?challenge` | `?ch` "
                f"\n Argument: `@user` | `user`",
                value="Challenge a user to a game of chess \n \u200b",
                inline=False,
            )
            .add_field(
                name=f"{EMOJI['shake']} `?profile` | `?p`",
                value="View your chess profile \n \u200b",
                inline=False,
            )
            .add_field(
                name=f"{EMOJI['chart']} `?availablemoves` | `?am` | `?moves`",
                value="Choose between games"
                " where it's your turn to make a move",
                inline=False,
            )
        )


def setup(client):
    client.add_cog(Help(client))
