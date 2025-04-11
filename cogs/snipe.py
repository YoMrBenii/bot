import discord
from discord.ext import commands

class bell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.a = None
        self.b = None
    @commands.command()
    async def type(self, ctx, *, text: str):
        await ctx.send(f"{text}")
        await ctx.message.delete()
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
    	self.a = message.content
    	self.b = message.author
    	
    	
    @commands.command()
    async def snipe(self, ctx):
    	await ctx.send(f"{self.a}\nSent by {self.b}")
    
async def setup(bot):
    await bot.add_cog(bell(bot))