import discord
from discord.ext import commands
from mongo import *

class daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self, ctx):
        time = getuservar("lastdaily", ctx.author.id)
        await ctx.send(time)