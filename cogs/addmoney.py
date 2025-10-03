import discord
from discord.ext import commands
from mongo import getuservar, setuservar, resetuservar
from functions import hasrole

class addm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gm(self, ctx,  amount: int = 0, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if hasrole(ctx.author, 1191804053362061312) == False:
            await ctx.send("No perms")
            return
        if amount == 0:
            await ctx.send("give a value")
            return
        setuservar("usd", member.id, amount)
        await ctx.send(f"gave <@{member.id}> {amount} usd.")
        money = getuservar("usd", member.id)
        await ctx.send(f"Added {amount} usd to <@{member.id}>. New balance: {money} usd.")

    @commands.command()
    async def rst(self, ctx, member: discord.Member = None):
        if hasrole(ctx.author, 1191804053362061312) == False:
            await ctx.send("Only meant for Beni")
            return
        if member is None:
            await ctx.send("Ping a user to reset")
            return
        member = str(member.id)
        resetuservar("usd", member)
        a = getuservar("usd", member)
        await ctx.send(f"<@{member}>s balance has been reset to {a}")
    

async def setup(bot):
    await bot.add_cog(addm(bot))