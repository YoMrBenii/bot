import asyncio
import os
import discord
from discord.ext import commands
import sys
from collections import defaultdict
from creds import db

TOKEN = os.getenv("a")

print(f"Cog Python executable: {sys.executable}")
print(f"Cog PYTHONPATH: {os.environ.get('PYTHONPATH')}")


allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
intents = discord.Intents.all()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None, allowed_mentions=allowed_mentions)
bot.msgs = defaultdict(int)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')
            await bot.load_extension("cogs.msgs", extras={"db": db})

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.custom, name="I love men")
    GUILD_ID = 1032670610372968529
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync()
    await bot.change_presence(activity=activity)


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())