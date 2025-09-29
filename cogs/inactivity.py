import discord
from discord.ext import commands

class loa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def inactivity(self, ctx, days: int = None):
        if days is None:
            await ctx.send("Name how many days your going to be gone for.")
            days = days * 86400

async def setup(bot):
    await bot.add_cog(loa(bot))