import nextcord

from nextcord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = self.help_embed()
        await ctx.send(embed=embed)
        pass

    @staticmethod
    def help_embed() -> nextcord.Embed:
        return nextcord.Embed(
            title="Help",
            description="This is the help command.\n"
            "Use `?help` to see this message again.",
        )


def setup(client):
    client.add_cog(Help(client))