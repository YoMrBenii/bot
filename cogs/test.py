import discord  
from discord.ext import commands
class testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def nigga(self, ctx, arg1: int, arg2: int):
        if arg2 == None:
            await ctx.send("provide two numbers")
            return
        if arg2 or arg1 != int:
            await ctx.send("must be a number")
            return
        arg3 = 0
        arg3 = arg1 * arg2
        await ctx.send(f"{arg3} niggers")
        

async def setup(bot):
    await bot.add_cog(testing(bot))