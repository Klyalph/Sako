import os

from dotenv import load_dotenv

from app import Bot

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TOKEN")
    mongodb_token = os.getenv("MONGO_DB_TOKEN")
    bot = Bot(mongodb_token)
    bot.run(token)
