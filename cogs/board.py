import logging
import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Board(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bmem = ['beni', 'ish', 'wixy']        
                  
    @commands.command()
    async def getboard(self, ctx):
        bmems = "\n".join(self.bmem)
        embed = discord.Embed(
        title="Board", description=f"board members: \n{bmems}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Board(bot))