import discord
from discord.ext import commands
from mongo import getuservar, setuservar

class collect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def collect(self, ctx):
        
        member = ctx.author
        roles = [x.name for x in member.roles]
        amount = len(roles)
        mamount = amount*50
        setuservar("usd", member.id, mamount)
        embed = discord.Embed(description=f"<@{member.id}> collected {mamount} from their {amount} roles.",
                              title="Role Collection",
                              colour=000000)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(collect(bot))