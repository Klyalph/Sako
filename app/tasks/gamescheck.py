import nextcord

from ..objects import GamesCollection
from .. import db
from ..utils.emojis import EMOJI


async def game_check(client: nextcord.Client):
    games = GamesCollection.get_games().copy().values()
    for game in games:
        if not game.is_time_left():
            winner_profile, loser_profile = game.profile_of_winner_and_loser(
                game.fen_notation
            )
            winner_profile.won_game(game.id)
            loser_profile.lost_game(game.id)
            GamesCollection.delete_game(str(game.id))
            if hasattr(client, "mongo_client"):
                db.delete_game_from_db(client.mongo_client, str(game.id))

            winner_disc_profile = client.get_user(int(winner_profile.id))
            loser_disc_profile = client.get_user(int(loser_profile.id))
            await winner_disc_profile.send(
                embed=_win_embed(client, winner_profile, loser_profile)
            )
            await loser_disc_profile.send(
                embed=_lose_embed(client, winner_profile, loser_profile)
            )


def _lose_embed(
    client: nextcord.Client, winner_profile, loser_profile
) -> nextcord.Embed:
    winner_disc_profile = client.get_user(int(winner_profile.id))
    loser_disc_profile = client.get_user(int(loser_profile.id))

    return nextcord.Embed(
        title="Game Results",
        description=f"You Ran Out Of Time Against {winner_disc_profile.name}",
        color=0x2F3136,
    ).add_field(
        name=f"{EMOJI['anger']} {loser_disc_profile.name}",
        value=f"{EMOJI['down_chart']} New Elo: {loser_profile.elo}",
        inline=True,
    )


def _win_embed(
    client: nextcord.Client, winner_profile, loser_profile
) -> nextcord.Embed:
    winner_disc_profile = client.get_user(int(winner_profile.id))
    loser_disc_profile = client.get_user(int(loser_profile.id))

    return nextcord.Embed(
        title="Game Results",
        description=f"{loser_disc_profile.name} Went Out Of Time, You Won!",
        color=0x2F3136,
    ).add_field(
        name=f"{EMOJI['trophy']} {winner_disc_profile.name}",
        value=f"{EMOJI['chart']} New Elo: {winner_profile.elo}",
        inline=True,
    )
