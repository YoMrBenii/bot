import discord  
from discord.ext import commands
class testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def nigga(self, ctx, arg1: int = None, arg2: int = None):
        if arg2 is None:
            await ctx.send("provide two numbers")
            return
        if arg2 is str or arg1 is str:
            await ctx.send("must be a number")
            return
        arg3 = 0
        arg3 = arg1 * arg2
        await ctx.send(f"{arg3} niggers")
        

async def setup(bot):
    await bot.add_cog(testing(bot))