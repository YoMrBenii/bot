import discord
from discord.ext import commands
from utils.dt import isUser

class database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @isUser(1118218807694065684)
    async def banlist(self, ctx):
        MAX_CHARS = 4000
        bans = [ban async for ban in ctx.guild.bans()]
        banlist = "\n".join([f"{bn.user}" for bn in bans])
        chunks = [banlist[i:i + MAX_CHARS] for i in range(0, len(banlist), MAX_CHARS)]
        for chunk in chunks:
        	embed = discord.Embed(description=chunk)
        	await ctx.send(embed=embed)
        banamount = len(bans)
        await ctx.send(banamount)
        
    @banlist.error
    async def banlist_error(self, ctx, error):
        await ctx.send("Only for beni.")

async def setup(bot):
    await bot.add_cog(database(bot))
