import discord
from discord.ext import commands
from mongo import *
from functions import *

class clansys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joinclan(self, ctx, clan: str = None):
        if not owneronly:
            return
        if clan is None:
            await ctx.send("Must name the clan you want to join.")
            return
        user = ctx.author
        result = userinclan(ctx.author.id)
        if not clanexists(clan):
            await ctx.send("The clan doesnt exist")
            return
        if isinstance(result, str):
            await ctx.send(f"Your already in a clan called {result}")
            return
        else:
            a = setuserclan(clan, ctx.author.id)
            await ctx.send(a)

    @commands.command()
    async def createclan(self, ctx, clan: str = None):
        if not owneronly:
            return
        if clan is None:
            await ctx.send("Must mention what the clan name is.")
            return
        if 2 > len(clan) or len(clan) > 7:
            await ctx.send("The clans name must be between 2 and 6 letters.")
            return
        b = ccreateclan(clan, ctx.author.id)
        print("e")
        await ctx.send(b)


async def setup(bot):
    await bot.add_cog(clansys(bot))