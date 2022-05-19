class PreviousGamesCollection:
    _previous_games = {}

    @classmethod
    def add_previous_game(cls, user_id, previous_game):
        if user_id not in cls._previous_games:
            cls._previous_games[user_id] = []
        cls._previous_games[user_id].append(previous_game)

    @classmethod
    def get_previous_games(cls, user_id):
        return cls._previous_games[user_id]
