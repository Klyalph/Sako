import pymongo
import datetime

import nextcord
from nextcord.ext import commands

COGS = [
    "app.cogs.profile",
    "app.cogs.createchallenge",
    "app.cogs.makemove",
    "app.cogs.currentgames",
    "app.cogs.onready",
    "app.cogs.help",
    "app.cogs.gamelist",
]


class Bot(commands.Bot):
    def __init__(self, mongodb_token: str = "", **kwargs):
        intents = nextcord.Intents.all()
        super().__init__(
            command_prefix="?", intents=intents, help_command=None
        )
        for extension in COGS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(e)
                print(f"Error loading extension {extension}")

        if mongodb_token:
            self.mongo_client = pymongo.MongoClient(mongodb_token)["sako"]

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        print(f"Current time: {datetime.datetime.now()}"[:-7])
        print(f"{self.user.id}")
        print("------")
