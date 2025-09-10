import discord
from discord.ext import commands
from creds import db

class wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wallet(self, ctx):
        id = ctx.author.id
        wall = db.collection("users").document(id)
        data = wall.get()
        ctx.send(data["usd"])
 
async def setup(bot):
    await bot.add_cog(wallet(bot))