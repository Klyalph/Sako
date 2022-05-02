from dataclasses import asdict

from pymongo import MongoClient

from ..objects import GamesCollection, UsersCollection


def save_data(token: str) -> None:
    """
    Saves data from the collections into MongoDB.
    """
    db = MongoClient(token)['sako']
    save_user_data(db)
    save_game_data(db)

def save_user_data(db) -> None:
    """
    Saves data from the collections into MongoDB.
    """
    users = db['users']
    for user_id, user in UsersCollection.get_users().items():
        users.update_one(
            {'_id': user_id},
            {'$set': asdict(user)},
            upsert=True
        )

def save_game_data(db) -> None:
    """
    Saves data from the collections into MongoDB.
    """
    games = db['games']
    for game_id, game in GamesCollection.get_games().items():
        games.update_one(
            {'_id': game_id},
            {'$set': asdict(game)},
            upsert=True
        )
