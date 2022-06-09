import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import time


from .cog_utils.check import check_user
from typing import List
from ..objects import UsersCollection, ConnectFour
from .cog_utils.parse import parse_user


class ConnectFourChoices(nextcord.ui.View):
    # The user is the person who's turn it is
    def __init__(self, user_id: nextcord.Member):
        super().__init__(timeout=45)
        self.response = None
        self.user_id = user_id

    # MUST be a better way
    @nextcord.ui.button(label="1", style=nextcord.ButtonStyle.primary)
    async def button1(self, button, interaction: Interaction):
        if interaction.user.id == self.user_id:
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


    @nextcord.ui.button(label="delete", style=nextcord.ButtonStyle.primary)
    async def delete(self, button, interaction: Interaction):
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

        contender_game_profile = UsersCollection.get_user(str(ctx.author.id))
        opponent_game_profile = UsersCollection.get_user(
            str(opponent_disc_profile.id)
        )
        embed = self._create_board_embed(
            game, ctx.author, opponent_disc_profile
        )
        message = await ctx.send(embed=embed)

        contender_game_profile.pending_command = message.id
        opponent_game_profile.pending_command = message.id

        # TODO: CEHCK if there is no availble moves
        while not game.check_if_won():
            user_id_turn = int(game.get_id_of_user_turn())

            if (
                contender_game_profile.pending_command != message.id
                or opponent_game_profile.pending_command != message.id
            ):
                return

            view = ConnectFourChoices(user_id_turn)

            embed = self._create_board_embed(
                game, ctx.author, opponent_disc_profile
            )
            await message.edit(embed=embed, view=view)

            await view.wait()

            if view.response is None:
                return

            try:
                game.push_move(view.response - 1)
            except ValueError:  # Column is full
                continue

            if game.is_draw():
                await ctx.send(self._create_draw_embed)
                break

        await message.edit(
            embed=self._results_embed(game, ctx.author, opponent_disc_profile),
        )
        time.sleep(2)
        try:
            await message.delete()
        except:
            pass

    @commands.command()
    async def cf(self, ctx, opponent):
        await self.connectfour(ctx, opponent)

    def _create_draw_embed(self) -> nextcord.Embed:
        return nextcord.Embed(
            title="Draw", description="No one won this game."
        )

    def _create_board_embed(
        self,
        game: ConnectFour,
        user1_disc: nextcord.Member,
        user2_disc: nextcord.Member,
    ) -> nextcord.Embed:

        user_turn = (
            user1_disc
            if game.get_id_of_user_turn() == str(user1_disc.id)
            else user2_disc
        )

        return (
            nextcord.Embed(
                title=f"{user1_disc.name} vs {user2_disc.name}",
                description=game.as_string(),
            )
            .add_field(name=f"{user_turn.name}'s turn", value="\u200b")
            .set_footer(
                text=f"Requested by {user1_disc.name}",
                icon_url=user1_disc.display_avatar,
            )
        )


    def _results_embed(self, game: ConnectFour, user1_disc, user2_disc) -> nextcord.Embed:
        winner_id = game.get_winner_id()
        winner_disc_profile = (
            user1_disc if user1_disc.id == int(winner_id) else user2_disc
        )

        return nextcord.Embed(
            title=f"Game over: {user1_disc.name} vs {user2_disc.name}",
            description=game.as_string(),
        ).add_field(
            name=f"{winner_disc_profile.name} Won!",
            value="\u200b",
        )


def setup(client):
    client.add_cog(ConnectFourGame(client))
