import discord
from discord.ext import commands
import time
from mongo import *
from functions import *

class messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_timestamps = {}
        self.hourly_timestamps = {} 

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
            setuservar("remainingmsgs", user_id, 1)
            return
        timestamps.append(now)
        self.user_timestamps[user_id] = timestamps
        hour_timestamps = self.hourly_timestamps.get(user_id, [])
        hour_timestamps = [t for t in hour_timestamps if now - t < 3600]
        hour_timestamps.append(now)
        self.hourly_timestamps[user_id] = hour_timestamps
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

    @commands.command()
    async def rmsgs(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        a = getuservar("remainingmsgs", member.id)
        embed = discord.Embed(
            description=f"<@{member.id}> has {a} remaining messages since last saturday.",
            title="Messages",
            color=0xa3a2ff
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def pace(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        now = time.time()
        timestamps = self.hourly_timestamps.get(member.id, [])
        timestamps = [t for t in timestamps if now - t < 3600]
        self.hourly_timestamps[member.id] = timestamps

        message_count = len(timestamps)
        if message_count == 0:
            description = f"<@{member.id}> has not sent any trackable messages in the last hour."
        else:
            elapsed_seconds = max(now - timestamps[0], 1)
            projected_per_hour = message_count / elapsed_seconds * 3600
            description = (
                f"<@{member.id}> has sent {message_count} messages in the last hour.\n"
                f"Estimated hourly pace: {projected_per_hour:.1f} messages/hour."
            )

        embed = discord.Embed(
            description=description,
            title="Message Pace",
            color=0xa3a2ff
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(messages(bot))
