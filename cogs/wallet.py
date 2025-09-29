import discord
from discord.ext import commands
from creds import db, getuservar, setuservar
from functions import owneronly


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def manualwallet(self, ctx):
        user_id = str(ctx.author.id)
        doc_ref = db.collection("users").document(user_id)
        snapshot = doc_ref.get()
        if not snapshot.exists:
            await ctx.send("No wallet found.")
            return
        data = snapshot.to_dict() or {}
        usd = data.get("usd", 0)
        await ctx.send(f"{usd}")
        
    @commands.command()
    async def wallet(self, ctx, member: discord.Member = None):
        if member is None:
            member = str(ctx.author.id)
            memname = str(ctx.author.name)
        else:
            member = str(member.id)
            memname = str(ctx.author.name)
        money = getuservar("usd", member)
        permlvl = getuservar("permlvl", member)
        permtext = f"\nPermlvl: {permlvl}" if permlvl > 0 else ""
        embed = discord.Embed(description=f"<@{member}> has {round(money):,} dollars.{permtext}",
                              title=f"{memname}s wallet",
                              colour=000000)
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