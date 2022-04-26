import nextcord

from ...objects import User, UsersCollection


async def check_user(user: nextcord.Member) -> None:
    """
    Checks if the user exists in the database.
    If not, then creates a user object and stores it
    in the collection.
    """
    if not UsersCollection.user_exists(str(user.id)):
        User(id=str(user.id), elo=1500)
