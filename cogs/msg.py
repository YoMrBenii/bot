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
        changeuservar("username", message.author.id, message.author.name)

    @commands.command()
    async def messages(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        a = getuservar("messages", member.id)
        b = getlbspot("messages", member.id)
        embed = discord.Embed(description=f"<@{member.id}> has {a} messages since last saturday.\nYour top {b}")
        await ctx.send(embed=embed)

    @commands.command()
    async def top(self, ctx):
        try:
            a = lb("messages", 20)
        except Exception as e:
            await ctx.send(e)
        embed = discord.Embed(description=a)
        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(messages(bot))