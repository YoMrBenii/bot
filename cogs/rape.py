import discord
from discord.ext import commands
from random import choice

class rap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rape(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        if member is None:
            await ctx.send("ping the user you want to rape by pinging them")
            return
        a = ["ha that was fun", "i love raping men", "Huh, mustve been the wind", "oops accident", ""]
        b = choice(a)
        await ctx.send(f"someone raped {member.mention}\n{b}")
        
async def setup(bot):
    await bot.add_cog(rap(bot))