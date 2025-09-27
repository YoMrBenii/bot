import discord
from discord.ext import commands
from creds import find_user_clan, setuserclan, createclan, clanexists, getuservar, setuservar

class clansys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joinclan(self, ctx, clan: str = None):
        if clan is None:
            await ctx.send("Must name the clan you want to join.")
            return
        user = ctx.author
        result = find_user_clan(ctx.author.id)
        if not clanexists(clan):
            await ctx.send("The clan doesnt exist")
            return
        if isinstance(result, str):
            await ctx.send(f"Your already in a clan called {result}")
            return
        else:
            setuserclan(clan, ctx.author.id)
            await ctx.send(f"You were added to {clan}.")

    @commands.command()
    async def createclan(self, ctx, clan: str = None):
        if clan is None:
            await ctx.send("Must mention what the clan name is.")
        if 2 > len(clan) > 7:
            ctx.send("The clans name must be between 2 and 6 letters.")
            return
        b, c = createclan(clan, ctx.author.id)
        if b is False:
            await ctx.send(c)
            return
        else:
            await ctx.send(c)


async def setup(bot):
    await bot.add_cog(clansys(bot))