import discord
from discord.ext import commands
from mongo import *

class donate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def donate(self, ctx, user: discord.Member = None, amount: str = None):
        if not user or not amount:
            await ctx.send("Must ping whoever you want to donate to and name how much.")
            return
        if amount == "all":
            amount = getuservar("usd", ctx.author.id)
        elif amount.isdigit() is True:
            amount = int(amount)
        else:
            await ctx.send("Must provide how much you want to donate or use -donate [user] all to donate everything")
            return
        if amount <= 0:
            await ctx.send("Cant donate less than 1.")
        a = getuservar("usd", ctx.author.id)
        if amount > a:
            await ctx.send("You cant donate more than you have")
        setuservar("usd", user.id, amount)
        embed = discord.Embed(description=f"{ctx.author.name} donated {amount} to <@{user.id}>.", title="Donation", color=0x39f69b)
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(donate(bot))