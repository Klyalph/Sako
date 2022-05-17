import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from ..objects import Game, UsersCollection
from ..utils.emojis import EMOJI
from .cog_utils.check import check_user
from .cog_utils.parse import parse_user

TIMEOUT = 80

# Represents the 'accept' and 'reject' button
class Choice(nextcord.ui.View):
    def __init__(self, contender: nextcord.Member):
        super().__init__(timeout=TIMEOUT)
        self.response = None
        self.contender = contender

    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.green)
    async def accept(self, button, interaction: Interaction):
        if interaction.user.id == self.contender.id:
            self.response = True
            self.stop()

    @nextcord.ui.button(label="Decline", style=nextcord.ButtonStyle.red)
    async def decline(self, button, interaction: Interaction):
        if interaction.user.id == self.contender.id:
            self.response = False
            self.stop()


class CreateChallenge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def challenge(self, ctx, contender):
        if ctx.channel.type == nextcord.ChannelType.private:
            return

        con = parse_user(self, ctx, contender)
        if con is None:
            msg = await ctx.send(
                "Please Enter A Valid Username To Challenge Someone!"
            )
            return

        await check_user(ctx.author)
        await check_user(con)

        challenger_user = UsersCollection.get_user(ctx.author.id)
        contender_user = UsersCollection.get_user(con.id)
        challenger_user.pending_command = str(ctx.message.id)

        if len(challenger_user.ongoing_games) >= 10:
            await ctx.send(
                f"{ctx.author.mention} "
                "You Have Reached The Maximum Number Of Ongoing Games!"
            )
            return
        elif len(contender_user.ongoing_games) >= 10:
            await ctx.send(
                f"{con.name} Have Reached The Maximum Number Of Ongoing Games!"
            )
            return

        challenge_embed = self._create_challenge_embed(
            challenger_user, contender_user, ctx, con
        )

        view = Choice(con)
        msg = await ctx.send(embed=challenge_embed, view=view)
        await view.wait()

        if challenger_user.pending_command != str(ctx.message.id):
            await msg.edit(
                "This Invite Is No Longer Valid", embed=None, view=None
            )
            return

        if view.response is None:
            await msg.edit(
                "Contender Did Not Respond In Time", embed=None, view=None
            )
            return

        if view.response:
            game = Game(challenger_user, contender_user)
            embed = self._create_acceptance_embed(ctx, con)
            await msg.edit(embed=embed, view=None)

        elif not view.response:
            embed = self._create_rejection_embed(ctx, con)
            await msg.edit(embed=embed, view=None)

    @commands.command()
    async def ch(self, ctx, opponent):
        await self.challenge(ctx, opponent)

    @commands.command()
    async def play(self, ctx, opponent):
        await self.challenge(ctx, opponent)

    @staticmethod
    def _create_acceptance_embed(ctx, contender) -> nextcord.Embed:
        return (
            nextcord.Embed(
                title=f"{EMOJI['checkmark']} {contender.name} "
                "Has Accepted The Challenge!",
                description=f"{ctx.author.name} Vs. {contender.name}",
                color=0x66A543,
            )
            .add_field(
                name=f"Each Player Has 24 Hours To Respond With A Move",
                value="\u200b",
                inline=False,
            )
            .set_footer(
                text=f"Write ?mm {ctx.author.name} To Make The First Move!",
                icon_url=contender.display_avatar,
            )
        )

    @staticmethod
    def _create_rejection_embed(ctx, contender) -> nextcord.Embed:
        return nextcord.Embed(
            title=f"{EMOJI['x']} Challenge Rejected By " f"{contender.name}",
            description=f"{ctx.author.name} Vs. {contender.name}",
            color=0xCC1634,
        )

    @staticmethod
    def _create_challenge_embed(
        challenger_user, contender_user, ctx, contender
    ) -> nextcord.Embed:
        return (
            nextcord.Embed(
                title=f"{EMOJI['pawn']} Daily Chess",
                description="{} Has Challenged {} To A Game Of Chess!".format(
                    ctx.author.name, contender.name
                ),
                color=0x2F3136,
            )
            .set_author(
                name=f"\u265b {ctx.author.name} Has Challenged "
                f"{contender.name} \u265a",
                icon_url=ctx.author.display_avatar,
            )
            .add_field(
                name=f"{EMOJI['black_flag']} {ctx.author.name} "
                f"({challenger_user.compute_win_percentage()}% Winrate)",
                value=f"{EMOJI['chart']} {challenger_user.elo} Elo"
                f"\n{EMOJI['trophy']} {challenger_user.wins} Wins "
                f"\n{EMOJI['anger']} {challenger_user.losses} Losses"
                f"\n{EMOJI['shake']} {challenger_user.stalemates} Stalemates"
                f"\n\n   {challenger_user.format_elo(contender_user)}",
                inline=True,
            )
            .add_field(
                name=f"{EMOJI['white_flag']} {contender.name} "
                f"({contender_user.compute_win_percentage()}% Winrate)",
                value=f"{EMOJI['chart']} {contender_user.elo} Elo"
                f"\n{EMOJI['trophy']} {contender_user.wins} Wins"
                f"\n{EMOJI['anger']} {contender_user.losses} Losses"
                f"\n{EMOJI['shake']} {contender_user.stalemates} Stalemates"
                f"\n\n   {contender_user.format_elo(challenger_user)}",
                inline=True,
            )
        )


def setup(client):
    client.add_cog(CreateChallenge(client))
