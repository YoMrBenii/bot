import discord
from discord.ext import commands
from mongo import getuservar, setuservar
from functions import owneronly


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command()
    async def wallet(self, ctx, member: discord.Member = None):
        if member is None:
            member = str(ctx.author.id)
            memname = str(ctx.author.name)
        else:
            member = str(member.id)
            memname = str(member.name)
        money = getuservar("usd", member)
        permlvl = getuservar("permlvl", member)
        lbspot = "\nRank: " + str(lbspot("usd", member))
        rep = "\nRep: " + str(getuservar("rep", member))
        permtext = f"\nPermlvl: {permlvl}" if permlvl > 0 else ""
        embed = discord.Embed(description=f"<@{member}> has {round(money):,} dollars.{lbspot}{rep}{permtext}",
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