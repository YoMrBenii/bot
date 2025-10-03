import discord
from discord.ext import commands
from mongo import *
class leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def lb(self, ctx):
        if ctx.invoked_subcommand is None:
            a = lb("usd", 20)
            embed = discord.Embed(description=a, title="Money Leaderboard", colour=0xa3a2ff)
            await ctx.send(embed=embed)

    @lb.command()
    async def rep(self, ctx):
        a = lb("rep", 20)
        embed = discord.Embed(description=a, title="Rep Leaderboard", colour=0xa3a2ff)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(leaderboards(bot))