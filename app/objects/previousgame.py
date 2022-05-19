from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List
from .previousgamescollection import PreviousGamesCollection

from enum import Enum, auto
import time


@dataclass(slots=True)
class PreviousGame:
    game_id: int
    result: int
    opponent_id: str  # discord opponent id
    user_id: str
    time: int = field(
        default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )

    def __post_init__(self):
        PreviousGamesCollection.add_previous_game(self.user_id, self)
