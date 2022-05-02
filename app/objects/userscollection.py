from __future__ import annotations

from typing import List


class UsersCollection:

    _users = {}

    @classmethod
    def add_user(cls, user: User):
        cls._users[user.id] = user

    @classmethod
    def user_exists(cls, user_id: str) -> bool:
        return user_id in cls._users

    @classmethod
    def get_user(cls, user_id: str) -> User:
        return cls._users[str(user_id)]

    @classmethod
    def get_users(cls):
        return cls._users

