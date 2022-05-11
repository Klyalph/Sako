import datetime

from nextcord.ext import commands
import nextcord

from .. import db
import asyncio
from .. import tasks


class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.listening, name=f"?help"
            )
        )
        # Make this a function
        if hasattr(self.client, "mongo_client"):
            db.load_data(self.client.mongo_client)
            print("DATA LOADED")
            while 1:
                db.save_data(self.client.mongo_client)
                await tasks.game_check(self.client)
                print(f"Saved {datetime.datetime.now()}")
                await asyncio.sleep(30)


def setup(client):
    client.add_cog(OnReady(client))
