import pymongo

from ..objects import Game, User, UsersCollection

# Make it a bit more efficient as it is storing redundant data 
# In the games collection of the database

def load_data(token: str) -> None:
    """
    Loads data from MongoDB into the collections.
    """
    db = pymongo.MongoClient(token)['sako']
    load_user_data(db)
    load_game_data(db)
    print("DATA LOADED")

def load_user_data(db) -> None:
    users = db['users']
    for user in users.find():
        u = user.copy()
        del u['_id']
        # Check if this works
        del u['ongoing_games']
        User(**u)

def load_game_data(db) -> None:
    games = db['games']
    for game in games.find():
        g = game.copy()
        del g['_id']
        g['user1_id'] = UsersCollection.get_user(g['user1_id']['id'])
        g['user2_id'] = UsersCollection.get_user(g['user2_id']['id'])
        Game(**g)
