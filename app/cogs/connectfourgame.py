import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import Button

from .cog_utils.check import check_user
from typing import List
from ..objects import UsersCollection, GamesCollection, Game, ConnectFour
from .cog_utils.parse import parse_user
from ..utils.emojis import EMOJI


class ConnectFourChoices(nextcord.ui.View):
    # The user is the person who's turn it is
    def __init__(self, user_id: nextcord.Member):
        super().__init__(timeout=30)
        self.response = None
        self.user_id = user_id

    # MUST be a better way to do this
    @nextcord.ui.button(label="1", style=nextcord.ButtonStyle.primary)
    async def button1(self, button, interaction: Interaction):
        self.response = int(button.label)
        self.stop()

    @nextcord.ui.button(label="2", style=nextcord.ButtonStyle.primary)
    async def button2(self, button, interaction: Interaction):
        if interaction.user.id == self.user_id:
            self.response = int(button.label)
            self.stop()

    @nextcord.ui.button(label="3", style=nextcord.ButtonStyle.primary)
    async def button3(self, button, interaction: Interaction):
        if interaction.user.id == self.user_id:
            self.response = int(button.label)
            self.stop()

    @nextcord.ui.button(label="4", style=nextcord.ButtonStyle.primary)
    async def button4(self, button, interaction: Interaction):
        if interaction.user.id == self.user_id:
            self.response = int(button.label)
            self.stop()

    @nextcord.ui.button(label="5", style=nextcord.ButtonStyle.primary)
    async def button5(self, button, interaction: Interaction):
        if interaction.user.id == self.user_id:
            self.response = int(button.label)
            self.stop()

    @nextcord.ui.button(label="6", style=nextcord.ButtonStyle.primary)
    async def button6(self, button, interaction: Interaction):
        if interaction.user.id == self.user_id:
            self.response = int(button.label)
            self.stop()

    @nextcord.ui.button(label="7", style=nextcord.ButtonStyle.primary)
    async def button7(self, button, interaction: Interaction):
        if interaction.user.id == self.user_id:
            self.response = int(button.label)
            self.stop()


class ConnectFourGame(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def connectfour(self, ctx, opponent):
        opponent_disc_profile = parse_user(self, ctx, opponent)

        if opponent_disc_profile is None:
            await ctx.send(f"**{opponent}** is not a valid user.")
            return

        await check_user(ctx.author)
        await check_user(opponent_disc_profile)

        game = ConnectFour(str(ctx.author.id), str(opponent_disc_profile.id))
        message = await ctx.send(game.as_string())

        contender_game_profile = UsersCollection.get_user(str(ctx.author.id))
        opponent_game_profile = UsersCollection.get_user(
            str(opponent_disc_profile.id)
        )
        contender_game_profile.pending_command = message.id
        opponent_game_profile.pending_command = message.id

        #while 1:
        while not game.check_if_won():

            user_id_turn = int(game.get_id_of_user_turn())

            view = ConnectFourChoices(user_id_turn)

            print("LMAO")
            await message.edit(game.as_string(), view=view)

            await view.wait()

            if view.response is None:
                return
                # TODO: ADD SOME THINGS HERE

            game.push_move(view.response - 1)

        print("This is out")
        await ctx.send("Feenix won!")





        async def _create_board_embed(
            self,
            game: ConnectFour,
            user1_disc: nextcord.Member,
            user2_disc: nextcord.Member,
        ) -> nextcord.Embed:
            return nextcord.Embed(
                title=f"Ongoing game: {user1_disc.name} vs {user2_disc.name}",
            )


def setup(client):
    client.add_cog(ConnectFourGame(client))
