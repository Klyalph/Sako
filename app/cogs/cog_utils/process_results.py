import chess
import nextcord

from ...objects import Game, GamesCollection, User, UsersCollection
from ...utils.emojis import EMOJI


async def process_resignation(self_, ctx, game: Game, msg, board: chess.Board):
    winner_profile, loser_profile = game.profile_of_winner_and_loser(board)

    winner_profile.won_game(str(game.id))
    loser_profile.lost_game(str(game.id))
    GamesCollection.delete_game(str(game.id))

    embed = _resign_embed(self_, winner_profile, loser_profile)

    await ctx.send(embed=embed)


def _resign_embed(self_, winner_profile, loser_profile):
    winner_disc_profile = self_.client.get_user(int(winner_profile.id))
    loser_disc_profile = self_.client.get_user(int(loser_profile.id))

    return (
        nextcord.Embed(
            title="Game Results",
            description=f"{winner_disc_profile.name} Won Against "
            f"{loser_disc_profile.name} Through Resignation",
            color=nextcord.Color.from_rgb(0, 0, 0),
        )
        .add_field(
            name=f"{EMOJI['trophy']} {winner_disc_profile.name}",
            value=f"{EMOJI['chart']} New Elo: {winner_profile.elo}",
            inline=True,
        )
        .add_field(
            name=f"{EMOJI['anger']} {loser_disc_profile.name}",
            value=f"{EMOJI['down_chart']} New Elo: {loser_profile.elo}",
            inline=True,
        )
    )


async def process_win(self_, ctx, game: Game, msg, board: chess.Board):
    winner_profile, loser_profile = game.profile_of_winner_and_loser(board)

    winner_profile.won_game(str(game.id))
    loser_profile.lost_game(str(game.id))
    GamesCollection.delete_game(str(game.id))

    embed = _win_embed(self_, winner_profile, loser_profile)

    await ctx.send(embed=embed)

    # TODO: add game to list to previous games.


def _win_embed(self_, winner_profile, loser_profile) -> nextcord.Embed:

    winner_disc_profile = self_.client.get_user(int(winner_profile.id))
    loser_disc_profile = self_.client.get_user(int(loser_profile.id))

    return (
        nextcord.Embed(
            title="Game Results",
            description=f"{winner_disc_profile.name} Won Against "
            f"{loser_disc_profile.name}!",
            color=nextcord.Color.from_rgb(0, 0, 0),
        )
        .add_field(
            name=f"{EMOJI['trophy']} {winner_disc_profile.name}",
            value=f"{EMOJI['chart']} New Elo: {winner_profile.elo}",
            inline=True,
        )
        .add_field(
            name=f"{EMOJI['anger']} {loser_disc_profile.name}",
            value=f"{EMOJI['down_chart']} New Elo: {loser_profile.elo}",
            inline=True,
        )
    )


async def process_draw(self_, ctx, game: Game, msg, board: chess.Board):
    profile_one, profile_two = game.profile_of_winner_and_loser(board)

    profile_one.draw_game(str(game.id))
    profile_two.draw_game(str(game.id))
    GamesCollection.delete_game(str(game.id))

    embed = _draw_embed(self_, profile_one, profile_two)
    await ctx.send(embed=embed)


def _draw_embed(self_, profile_one, profile_two) -> nextcord.Embed:

    profile_one_disc = self_.client.get_user(int(profile_one.id))
    profile_two_disc = self_.client.get_user(int(profile_two.id))

    return (
        nextcord.Embed(
            title="Game Results",
            description="Draw Between "
            f"{profile_one_disc.name} And {profile_two_disc.name}",
            color=nextcord.Color.from_rgb(0, 0, 0),
        )
        .add_field(
            name=f"{EMOJI['shake']} {profile_one_disc.name}",
            value=f"New Elo: {profile_one.elo}",
            inline=True,
        )
        .add_field(
            name=f"{EMOJI['shake']} {profile_two_disc.name}",
            value=f"New Elo: {profile_two.elo}",
            inline=True,
        )
    )
