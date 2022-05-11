from dataclasses import asdict


from ..objects import GamesCollection, UsersCollection


def save_data(db) -> None:
    """
    Saves data from the collections into MongoDB.
    """
    _save_user_data(db)
    _save_game_data(db)
    _save_game_id(db)


def _save_user_data(db) -> None:
    users = db["users"]
    for user_id, user in UsersCollection.get_users().items():
        u = asdict(user).copy()
        del u["last_board_req"]
        users.update_one({"_id": user_id}, {"$set": u}, upsert=True)


def _save_game_data(db) -> None:
    """
    Saves data from the collections into MongoDB.
    """
    games = db["games"]
    for game_id, game in GamesCollection.get_games().items():
        g = asdict(game)
        g["user1_id"] = game.user1_id.id
        g["user2_id"] = game.user2_id.id
        games.update_one({"_id": game_id}, {"$set": g}, upsert=True)


def _save_game_id(db) -> None:
    data = db["misc"]
    data.update_one(
        {"_id": "game_id"},
        {"$set": {"game_id": GamesCollection._game_id}},
        upsert=True,
    )
