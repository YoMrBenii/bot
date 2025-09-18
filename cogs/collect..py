import discord
from discord.ext import commands
from creds import db, getuservar, setuservar

class collect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def collect(self, ctx):
        member = ctx.author
        roles = [x.name for x in member.roles]
        amount = str(len(roles))
        await ctx.send(f"user has {amount} roles")

async def setup(bot):
    await bot.add_cog(collect(bot))