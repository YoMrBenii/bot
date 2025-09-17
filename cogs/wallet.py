import discord
from discord.ext import commands
from creds import db, getuservar, setuservar


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def wallet(self, ctx):
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
    async def gm(self, ctx):
        user_id = str(ctx.author.id)
        money = getuservar("usd", user_id)
        await ctx.send(money)

    @commands.command()
    async def em(self, ctx):
        userid = str(ctx.author.id)
        setuservar("usd", userid, 5)
        await ctx.send("Added 5 USD to your wallet.")

    
async def setup(bot):
    await bot.add_cog(Wallet(bot))