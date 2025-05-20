import discord
from discord.ext import commands
import random

class emb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def embed(self, ctx, *, message: str):
        embed = discord.Embed(
        description=message
        )
        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(emb(bot))