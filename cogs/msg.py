import discord
from discord.ext import commands
from mongo import *

class messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        setuservar("messages", message.author.id, 1)

    @commands.command()
    async def messages(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        a = getuservar("messages", member.id)
        embed = discord.Embed(description=f"{ctx.author.id} has {a} messages since last saturday")
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(messages(bot))