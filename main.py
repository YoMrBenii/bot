import asyncio
import os
import discord
from discord.ext import commands

TOKEN = os.getenv("a")

allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
intents = discord.Intents.all()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None, allowed_mentions=allowed_mentions)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
	activity = discord.Activity(type=discord.ActivityType.custom, name="I love men")
	await bot.change_presence(activity=activity)
	print("Online")


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
