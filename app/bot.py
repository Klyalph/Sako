import datetime

import nextcord
from nextcord.ext import commands

INITIAL_EXTENSIONS = [
    "app.cogs.profile",
    "app.cogs.createchallenge",
    "app.cogs.makemove",
    "app.cogs.currentgames",
    "app.cogs.onready",
]


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = nextcord.Intents.all()
        super().__init__(
            command_prefix="?", intents=intents, help_command=None
        )
        for extension in INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f"Error loading extension {extension}")

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        print(f"Current time: {datetime.datetime.now()}"[:-7])
        print(f"{self.user.id}")
        print("------")
