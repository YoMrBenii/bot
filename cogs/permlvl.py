import discord 
from discord.ext import commands
from creds import *

class perms(commands.Cog):
    async def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def permlvl(self, ctx, member: discord.Member = None, amt: int = None):
        a = getuservar("permlvl", member.id)
        if a < 3:
            await ctx.send("no perms, but have perm level 3.")
            return
        if member is None or amt is None:
            await ctx.send("Must ping a user and specify which perms.")
            return
        changeuservar("permlvl", member.id, amt)
        await ctx.send(f"Gave {member.name} perm level {amt}")

async def setup(bot):
    await bot.add_cog(perms(bot))