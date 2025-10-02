import discord
from discord.ext import commands, tasks
from creds import *
from google.cloud import firestore
import asyncio
import signal


class msgcounting(commands.Cog):
    def __init__(self, bot, db2):
        self.bot = bot
        self.db2 = db2

        self.auto_flush.start()

        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(self._handle_exit(s)))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        self.bot.msgs[message.author.id] += 1
        if self.bot.msgs[message.author.id] % 100 == 0:
            await message.channel.send(
                f"{message.author.name} has reached {self.bot.msgs[message.author.id]} messages."
            )

    def cog_unload(self):
        self.flush_to_db_sync()
        self.auto_flush.cancel()

    async def _handle_exit(self, sig):
        await self.flush_to_db()
        await self.bot.close()

    async def flush_to_db(self):
        if not self.bot.msgs:
            return
        batch = self.db.batch()
        ref = self.db.collection("users")
        for authorid, count in self.bot.msgs.items():
            doc_ref = ref.document(str(authorid))
            batch.set(doc_ref, {"messages": firestore.Increment(count)}, merge=True)
        batch.commit()
        self.bot.msgs.clear()

    def flush_to_db_sync(self):
        if not self.bot.msgs:
            return
        batch = self.db.batch()
        ref = self.db.collection("users")
        for authorid, count in self.bot.msgs.items():
            doc_ref = ref.document(str(authorid))
            batch.set(doc_ref, {"messages": firestore.Increment(count)}, merge=True)
        batch.commit()
        self.bot.msgs.clear()

    @tasks.loop(seconds=1200)
    async def auto_flush(self):
        await self.flush_to_db()

    @commands.command()
    async def msgs(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        total = self.bot.msgs[member.id] + getuservar("messages", member.id)
        await ctx.send(f"{member.name} has {total} messages.")


async def setup(bot):
    await bot.add_cog(msgcounting(bot, bot.db2))
