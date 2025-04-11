import discord
from discord.ext import commands
import random

class emb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def embed(self, ctx, *, message: str):
        embed = discord.Embed(
        description=message
        )
        await ctx.send(embed=embed)
        
    @commands.command()
    async def history(self, ctx, amount: int):
    	messages = [message async for message in ctx.channel.history(limit=amount)]
    	message_content = "\n".join([f"{message.author}: {message.content}" for message in messages if message.content])
    	a = discord.Embed(message_content)
    	await ctx.send(a)

async def setup(bot):
    await bot.add_cog(emb(bot))