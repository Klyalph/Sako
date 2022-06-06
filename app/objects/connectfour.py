from dataclasses import dataclass, field
from typing import List
from enum import Enum
import sys
from ..utils.emojis import EMOJI


class TileStatus(Enum):
    EMPTY = 0
    RED = 1
    GREEN = 2


@dataclass(slots=True)
class ConnectFour:
    user1_id: str
    user2_id: str
    turn: TileStatus = TileStatus.RED
    last_move: List = field(default_factory=lambda: [-1, -1])
    board: list = field(
        default_factory=lambda: [
            [TileStatus.EMPTY for _ in range(7)] for _ in range(6)
        ]
    )

    def __post_init__(self):
        pass

    def push_move(self, column: int) -> None:
        if column < 0 or column > 6:
            raise ValueError("Invalid column")
        if self.board[0][column] != TileStatus.EMPTY:
            raise ValueError("Column is full")

        for i in range(5, -1, -1):
            if self.board[i][column] == TileStatus.EMPTY:
                self.board[i][column] = self.turn
                self.last_move = [i, column]
                self.turn = (
                    TileStatus.RED
                    if self.turn == TileStatus.GREEN
                    else TileStatus.GREEN
                )
                break

    def get_id_of_user_turn(self):
        if self.turn == TileStatus.RED:
            return self.user1_id
        else:
            return self.user2_id


    def check_if_won(self) -> bool:
        if self.last_move == [-1, -1]:
            return False

        return (
            self._check_vertically()
            or self._check_horizontally()
            or self._check_diagonally_left()
            or self._check_diagonally_right()
        )

    def _check_vertically(self) -> bool:
        count = 0
        last_color = self.last_move_color

        for i in range(len(self.board) - 1, -1, -1):
            if self.board[i][self.last_move[1]] == last_color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    def _check_horizontally(self) -> bool:
        count = 0
        last_color = self.last_move_color

        for i in range(len(self.board[0])):
            if self.board[self.last_move[0]][i] == last_color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    def _check_diagonally_left(self) -> bool:
        count = 0
        last_color = self.last_move_color
        row = self.last_move[0]
        column = self.last_move[1]

        while row > 0 and column > 0:
            row -= 1
            column -= 1

        while row < len(self.board) and column < len(self.board[0]):
            if self.board[row][column] == last_color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            row += 1
            column += 1

        return False

    def _check_diagonally_right(self) -> bool:
        count = 0
        last_color = self.last_move_color
        row = self.last_move[0]
        column = self.last_move[1]

        while row > 0 and column < len(self.board[0]) - 1:
            row -= 1
            column += 1

        while row < len(self.board) and column > 0:
            if self.board[row][column] == last_color:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            row += 1
            column -= 1

        return False

    @property
    def last_move_color(self) -> int:
        return self.board[self.last_move[0]][self.last_move[1]]

    @last_move_color.setter
    def last_move_color(self, value) -> None:
        raise AttributeError("Cannot set last move color")

    
    def as_string(self):
        colors = []

        for row in self.board:
            string = ""
            for item in row: 
                match item:
                    case TileStatus.EMPTY:
                        string += f"{EMOJI['black_circle']}"
                    case TileStatus.RED:
                        string += f"{EMOJI['red_circle']}"
                    case TileStatus.GREEN:
                        string += f"{EMOJI['green_circle']}"
                string += ""
            colors.append(string)

        return "\n".join(colors)