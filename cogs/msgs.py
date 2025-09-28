import discord
from discord.ext import commands
from collections import defaultdict
from creds import *
from google.cloud import firestore

class msgcounting(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        author = message.author
        authorid = author.id

        self.bot.msgs[message.author.id] += 1
        if self.bot.msgs[message.author.id] % 100 == 0:
            await message.channel.send(f"{message.author.name} has reached {self.bot.msgs[message.author.id]} messages.")

    def cog_unload(self):
        batch = self.db.batch()
        ref = self.db.collection("users")
        for authorid, count in self.bot.msgs():
            doc_ref = ref.document(str(authorid))
            batch.set(doc_ref, {"messages": firestore.Increment(count)}, merge=True)
        





    @commands.command()
    async def msgs(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        a = self.bot.msgs[member.id] + getuservar("messages", member.id)
        await ctx.send(f"{member.name} has {a} messages.")

    

async def setup(bot, extras):
    await bot.add_cog(msgcounting(bot, extras["db"]))