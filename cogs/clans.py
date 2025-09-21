import discord
from discord.ext import commands
from creds import find_user_clan, setuserclan, createclan, clanexists

class clansys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    async def joinclan(self, ctx, clan: str):
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

async def setup(bot):
    await bot.add_cog(clansys(bot))
    