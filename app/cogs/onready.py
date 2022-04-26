import nextcord
from nextcord.ext import commands
from ..createboard import create_board
import time

class OnReady(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")
        now = time.time()


    @commands.command()
    async def test(self, ctx):
        file_path = create_board(

            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
            f"testy",
        )
        file = nextcord.File(file_path)
        await ctx.reply(file=file)

def setup(client):
    client.add_cog(OnReady(client))


