import discord
from discord.ext import commands
from creds import db, getuservar, setuservar
from functions import hasrole

class addm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gm(self, ctx, member: discord.Member = None, amount: int = 0):
        if member is None:
            member = ctx.author
        if hasrole(member, 1191804053362061312) == False:
            await ctx.send("No perms")
            return
        if amount == 0:
            await ctx.send("give a value")
            return
        setuservar("usd", member.id, amount)
        await ctx.send(f"gave <@{member.id}> {amount} usd.")
        money = getuservar("usd", member.id)
        await ctx.send(f"Added {amount} usd to <@{member.id}>. New balance: {money} usd.")
    

async def setup(bot):
    await bot.add_cog(addm(bot))