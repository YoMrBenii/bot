import discord
from discord.ext import commands
from mongo import *
from functions import owneronly
import traceback

class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wallet(self, ctx, member: discord.Member = None):
        try:
            if member is None:
                member = ctx.author

            memberid = str(member.id)
            memname = member.name

            money = getuservar("usd", memberid)
            if money is None or isinstance(money, str):
                money = 0

            permlvl = getuservar("permlvl", memberid) or 0
            rep_val = getuservar("rep", memberid) or 0

            lb_val = getlbspot("usd", memberid)
            lbspot = f"\nRank: {lb_val}" if lb_val not in (None, "") else ""

            permtext = f"\nPermlvl: {permlvl}" if permlvl > 0 else ""
            reptext = f"\nRep: {rep_val}"

            embed = discord.Embed(
                description=f"<@{memberid}> has {round(float(money)):,} dollars.{lbspot}{reptext}{permtext}",
                title=f"{memname}'s wallet",
                colour=0x000000
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ {type(e).__name__}: `{e}`")
            print(traceback.format_exc())

    @commands.command()
    async def em(self, ctx):
        if owneronly(ctx.author) is False:
            return await ctx.send("Owner only")
        userid = str(ctx.author.id)
        setuservar("usd", userid, 5)  # ensure this uses upsert=True internally
        await ctx.send("Added 5 USD to your wallet.")

async def setup(bot):
    await bot.add_cog(Wallet(bot))

