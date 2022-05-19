from ..objects import (
    Game,
    User,
    UsersCollection,
    GamesCollection,
    PreviousGame,
)


def load_data(db) -> None:
    """
    Loads data from MongoDB into the collections.
    """
    _load_user_data(db)
    _load_game_data(db)
    _load_game_id(db)


def _load_user_data(db) -> None:
    users = db["users"]
    for user in users.find():
        u = user.copy()
        del u["_id"]
        del u["ongoing_games"]
        u["previous_games"] = [
            PreviousGame(**pg) for pg in u["previous_games"]
        ]
        User(**u)


def _load_game_data(db) -> None:
    games = db["games"]
    for game in games.find():
        g = game.copy()
        del g["_id"]
        g["user1_id"] = UsersCollection.get_user(g["user1_id"])
        g["user2_id"] = UsersCollection.get_user(g["user2_id"])
        Game(**g)


def _load_game_id(db) -> None:
    data = db["misc"]
    number = data.find_one({"_id": "game_id"})["game_id"]
    GamesCollection._game_id = number
