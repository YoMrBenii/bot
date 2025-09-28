import discord
from discord.ext import commands
from collections import defaultdict

class msgcounting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        author = message.author

        self.bot.msgs[message.author.id] += 1

    @commands.command()
    async def msgs(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        a = self.bot.msgs[member.id]
        await ctx.send(f"{member.name} has {a} messages.")

    

async def setup(bot):
    await bot.add_cog(msgcounting(bot))