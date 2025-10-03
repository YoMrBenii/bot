import discord 
from discord.ext import commands
from creds import *

class perms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def permlvl(self, ctx, member: discord.Member = None, amt: int = None):
        if member is None or amt is None:
            await ctx.send("Must ping a user and specify which perms.")
            return
        await ctx.send("3")
        try:
            a = getuservar("permlvl", ctx.author.id)
        except Exception as e:
        await ctx.send(e)
        await ctx.send(a)
        await ctx.send("1")
        if a <= 3:
            await ctx.send("no perms, must have perm level 3.")
            return
        await ctx.send("2")
        changeuservar("permlvl", member.id, amt)
        await ctx.send(f"Gave {member.name} perm level {amt}")

async def setup(bot):
    await bot.add_cog(perms(bot))