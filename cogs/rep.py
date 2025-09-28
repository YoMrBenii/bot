import discord
from discord.ext import commands
from creds import *
class reps(commands.Cog):
    async def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rep(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Must ping somebody")
            return
        if member.id == ctx.author.id:
            await ctx.send("Cant rep yourself")
            return
        setuservar("rep", member, 1)
        a = getuservar("permlvl", member.id)
        embed = discord.Embed(description=f"<@{member.id}> now has {a} rep!",
                              colour=000000)
        await ctx.send(embed=embed)

async def setup(bot):
    pass
    await bot.add_cog(reps(bot))