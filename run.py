import os

from dotenv import load_dotenv

from app import Bot

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TOKEN")
    bot = Bot()
    bot.run(token)
