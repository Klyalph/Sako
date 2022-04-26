from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Tuple

import numpy as np

from .userscollection import UsersCollection


@dataclass(slots=True)
class User:
    id: str  # Their discord id
    wins: int = 0
    losses: int = 0
    stalemates: int = 0
    elo: int = 1500
    ongoing_games: List[str] = field(default_factory=list)
    previous_games: List[str] = field(default_factory=list)
    pending_command: str = ""  # Message id of latest command sent

    def __post_init__(self):
        UsersCollection.add_user(self)

    def compute_win_precentage(self) -> float:
        # this might not work
        try:
            rate = self.wins / (self.wins + self.losses + self.stalemates)
            return f"{round(rate, 2) * 100:.2f}"
        except Exception:
            return "0.00"

    # https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
    def _expected(self, opponent: User) -> float:
        return 1 / (1 + 10 ** ((opponent.elo - self.elo) / 400))

    def _new_elo(self, opponent: User, score: int, k: int = 32) -> int:
        return int(self.elo + k * (score - self._expected(opponent)))

    def format_elo(self, opponent: User) -> str:
        results = [self._new_elo(opponent, i) for i in [1, 0.5, 0]]
        return "{} / {} / {}".format(*map(lambda x: x - self.elo, results))

    def won_game(self, game_id: str) -> None:
        self.wins += 1
        self.elo = self._new_elo(UsersCollection.get_user(self.id), 1)
        self.ongoing_games.remove(game_id)

    def lost_game(self, game_id: str) -> None:
        self.losses += 1
        self.elo = self._new_elo(UsersCollection.get_user(self.id), 0)
        self.ongoing_games.remove(game_id)

    def draw_game(self, game_id: str) -> None:
        self.stalemates += 1
        self.elo = self._new_elo(UsersCollection.get_user(self.id), 0.5)
        self.ongoing_games.remove(game_id)
