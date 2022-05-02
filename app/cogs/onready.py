import datetime
import time

import nextcord
from nextcord.ext import commands

from ..createboard import create_board
from ..db import load_data, save_data


class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # Make this a function
        if self.client.mongodb_token:
            load_data(self.client.mongodb_token)
            while True:
                save_data(self.client.mongodb_token)
                print(f"Saved {datetime.datetime.now()}") 
                time.sleep(30)

    @commands.command()
    async def test(self, ctx):
        # file_path = create_board(
        #     "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        #     f"testyblack",
        # )
        # file_path_two = create_board(
        #     "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        #     f"testywhite",
        # )
        # file = nextcord.File(file_path)
        # file2 = nextcord.File(file_path_two)
        # await ctx.reply(file=file)
        # await ctx.reply(file=file2)
        pass


def setup(client):
    client.add_cog(OnReady(client))
