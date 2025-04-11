import discord
from discord.ext import commands
import random

class el(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pps(self, ctx):
        # Use ctx.author for the user who invoked the command
        await ctx.send(f"Hi {ctx.author.id}")  # Send the author's ID

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(el(bot))
