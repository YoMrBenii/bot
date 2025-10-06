import discord
from discord.ext import commands
import time
from mongo import *

class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(description="Latency + DB status")
    async def health(self, ctx: commands.Context):
        t0 = time.perf_counter()
        ws = self.bot.latency
        db_ok = False
        err = None
        try:
            db_ok = ping_db()
        except Exception as e:
            err = str(e)[:200]
        t1 = time.perf_counter()

        embed = discord.Embed(title="Health", colour=0x2b2d31)
        embed.add_field(name="WebSocket", value=f"{ws*1000:.1f} ms", inline=True)
        embed.add_field(name="Handler", value=f"{(t1-t0)*1000:.1f} ms", inline=True)
        embed.add_field(name="MongoDB", value="OK" if db_ok else f"FAIL: {err}", inline=False)
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if ctx.author != 1118218807694065684:
            return
        await ctx.reply(f"Error: `{type(error).__name__}` - {str(error)[:180]}")
        print("COMMAND ERROR:", ctx.command, repr(error))

async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))
