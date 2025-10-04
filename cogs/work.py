import discord
from discord.ext import commands

class work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def work(self, ctx):
        pass

    @commands.command()
    async def apply(self, ctx, job: str = None):
        jobs = ["cleaner", "teacher"]
        if job is None or job not in jobs:
            await ctx.send("""Must choose a job from the following:
                           ``cleaner
                           teacher
                           software dev``""")
        values = {"cleaner": 100, "teacher": 200, "software dev": 300}
        pass

async def setup(bot):
    await bot.add_cog(work(bot))
