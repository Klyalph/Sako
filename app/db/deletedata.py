
def delete_game_from_db(db, game_id: str) -> None:
    games = db["games"]
    games.delete_one({"_id": game_id})
