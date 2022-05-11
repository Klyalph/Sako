import nextcord

from ...objects import User, UsersCollection


async def check_user(user: nextcord.Member) -> None:
    """
    Sheesh"""
    if not UsersCollection.user_exists(str(user.id)):
        User(id=str(user.id), elo=1500)
