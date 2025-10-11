import discord
from discord.ext import commands
import time
from mongo import *

class messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_timestamps = {} 

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        notallowedchannels = {1198228961000423486}
        if message.author.bot:
            return
        if message.channel.id in notallowedchannels:
            return
        user_id = message.author.id
        now = time.time()
        timestamps = self.user_timestamps.get(user_id, [])
        timestamps = [t for t in timestamps if now - t < 60]
        if len(timestamps) >= 15:
            self.user_timestamps[user_id] = timestamps
            return
        timestamps.append(now)
        self.user_timestamps[user_id] = timestamps
        setuservar("messages", user_id, 1)
        changeuservar("username", user_id, message.author.name)

    @commands.command()
    async def msgs(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        a = getuservar("messages", member.id)
        b = getlbspot("messages", member.id)
        embed = discord.Embed(
            description=f"<@{member.id}> has {a} messages since last saturday.\nYour top {b}",
            title="Messages",
            color=0xa3a2ff
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def top(self, ctx):
        a = mlb("messages", 20)
        b = f"**Record: <@{getservervar('recordholder')}> - {getservervar('recordmsgs')}**\n\n"
        embed = discord.Embed(description=b + a, title="Top messages", colour=0xa3a2ff)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(messages(bot))
