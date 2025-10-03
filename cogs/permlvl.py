import discord 
from discord.ext import commands
from mongo import *

class perms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def permlvl(self, ctx, member: discord.Member = None, amt: int = None):
        if member is None or amt is None:
            await ctx.send("Must ping a user and specify which perms.")
            return
        a = getuservar("permlvl", ctx.author.id)
        if amt > 3 or amt < 0:
            await ctx.send("Cant give out a level higher than 3 or lower than 0.")
        if a < 3:
            await ctx.send("no perms, must have perm level 3.")
            return
        changeuservar("permlvl", member.id, amt)
        await ctx.send(f"Gave {member.name} perm level {amt}")

async def setup(bot):
    await bot.add_cog(perms(bot))