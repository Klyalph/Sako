from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Tuple

import chess

from .gamescollection import GamesCollection
from .user import User

flags = {
    chess.WHITE: "<:flag_white:959942962920439818>",
    chess.BLACK: "<:flag_black:959942962902708737>",
}


@dataclass(slots=True)
class Game:
    user2_id: User
    user1_id: User
    id: int = 0
    user1_color: chess.Color = chess.WHITE
    user2_color: chess.Color = chess.BLACK
    # Add value for turn
    turn: chess.Color = chess.WHITE
    moves: int = 0

    last_move_date: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    fen_notation: str = (
        # "k7/8/2K5/8/8/1Q6/8/8 w - - 0 1"
        # "3Qk3/8/8/8/8/8/8/4K3 w - - 0 1"
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )

    def __post_init__(self):
        GamesCollection.add_game(self)

    def is_game_over(self) -> bool:
        time_since_last_move = datetime.now() - datetime.strptime(
            self.last_move_date, "%Y-%m-%d %H:%M:%S"
        )
        return time_since_last_move.days > 1

    def time_left(self) -> str:
        time_since_last_move = datetime.now() - datetime.strptime(
            self.last_move_date, "%Y-%m-%d %H:%M:%S"
        )
        time = timedelta(hours=24) - time_since_last_move
        return str(time)[:-7]

    def update_time(self) -> None:
        self.last_move_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_epoch_time(self) -> int:
        return int(datetime.now().timestamp()) + 24 * 3600

    def user_flags(self) -> Tuple[str]:
        return flags[self.user1_color], flags[self.user2_color]

    def get_opponent_profile(self, id: str) -> str:
        if self.user1_id.id == id:
            return self.user2_id
        else:
            return self.user1_id

    def is_user_turn(self, id: str) -> bool:
        board = chess.Board(fen=self.fen_notation)
        if self.user1_id.id == id:
            return board.turn is chess.WHITE
        else:
            return board.turn is chess.BLACK

    def get_user_color(self, id: str) -> chess.Color:
        if self.user1_id.id == id:
            return self.user1_color
        else:
            return self.user2_color

    def move(self, fen: str):
        self.fen_notation = fen
        self.moves += 1
        self.update_time()

    def profile_of_winner_and_loser(
        self, board: chess.Board
    ) -> Tuple[User, User]:
        if board.turn is chess.WHITE:
            return self.user2_id, self.user1_id
        else:
            return self.user1_id, self.user2_id
