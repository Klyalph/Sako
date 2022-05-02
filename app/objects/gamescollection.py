from __future__ import annotations

from .userscollection import UsersCollection

from typing import List


class GamesCollection:
    """A collection of game objects."""

    _games = {}
    _gameid = 9999

    @classmethod
    def add_game(cls, game: Game) -> None:
        game_id = cls._create_game_id()
        game.user1_id.ongoing_games.append(game_id)
        game.user2_id.ongoing_games.append(game_id)
        game.id = game_id
        cls._games[game_id] = game

    @classmethod
    def get_game(cls, game_id) -> Game:
        return cls._games[game_id]

    @classmethod
    def delete_game(cls, game_id) -> None:
        del cls._games[game_id]

    @classmethod
    def _create_game_id(cls) -> str:
        cls._gameid += 1
        return str(cls._gameid)

    @classmethod
    def get_games_by_user_id(cls, user_id: str) -> List[Game]:
        games = []
        for game_id, game in cls._games.items():
            if game.user1_id.id == user_id or game.user2_id.id == user_id:
                games.append(game)
        return games

    @classmethod
    def get_games(cls):
        return cls._games
