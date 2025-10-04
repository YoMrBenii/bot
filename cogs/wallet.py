import discord
from discord.ext import commands
from mongo import *
from functions import owneronly


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command()
    async def wallet(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        memberid = str(member.id)
        memname = member.name
        money = getuservar("usd", memberid)
        if money is None:
            money = 0
        permlvl = getuservar("permlvl", memberid)
        lbspot = "\nRank: " + str(getlbspot("usd", memberid))
        rep = "\nRep: " + str(getuservar("rep", memberid))
        permtext = f"\nPermlvl: {permlvl}" if permlvl > 0 else ""
        embed = discord.Embed(description=f"<@{memberid}> has {round(money):,} dollars.{lbspot}{rep}{permtext}",
                              title=f"{memname}s wallet",
                              colour=0x000000)
        await ctx.send(embed=embed)

    @commands.command()
    async def em(self, ctx):
        if owneronly(ctx.author) is False:
            return await ctx.send("Owner only")
        userid = str(ctx.author.id)
        setuservar("usd", userid, 5)
        await ctx.send("Added 5 USD to your wallet.")

    
async def setup(bot):
    await bot.add_cog(Wallet(bot))