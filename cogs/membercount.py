import discord
from discord.ext import commands

class Membercount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mc(self, ctx):
        mem = len(ctx.guild.members)
        embed = discord.Embed(
            description=f"PVP has {mem} members.", color=0xffffff, title="Membercount"
        )
        embed.set_footer(text="Updates in real time.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Membercount(bot))