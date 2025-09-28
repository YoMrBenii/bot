import discord
from discord.ext import commands
from random import *
from creds import *

class betting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bet(self, ctx, num: int = None):
        if num is None:
            await ctx.send("Must specify how much you want to bet.")
            return
        if not isinstance(num, int):
            await ctx.send("Must be a number")
            return
        if num < 1 or num >= 100000:
            await ctx.send("Cant bet with more than 100,000 or less than 1.")
            return
        a = getuservar("usd", ctx.author.id)
        if num > a:
            await ctx.send(f"You only have {a} usd, you cannot bet with {num}.")
            return
        values = [-0.5, -0.4, -0.3 , -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.5]
        endvalue = choice(values)
        transaction = num * endvalue
        setuservar("usd", ctx.author.id, transaction)
        b = getuservar("usd", ctx.author.id)
        if transaction > 0:
            await ctx.send(f"You won {transaction}!\nYour balance is now {b}.")
        else:
            await ctx.send(f"You lost {transaction}\n Your balance is now {b}")




async def setup(bot):
    await bot.add_cog(betting(bot))