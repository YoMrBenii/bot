import discord
from discord.ext import commands
from functions import owneronly
import sys

class OwnerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="owner")
    async def owner(self, ctx: commands.Context):
        app_info = await self.bot.application_info()
        owner = app_info.owner
        await ctx.send(f"The owner of this bot is: **{owner}** (ID: {owner.id})")

    @commands.command()
    async def shutdown(self, ctx):
        if not owneronly(ctx.author):
            await ctx.send("Must be beni.")
        else:
            await ctx.send("Bot shutting down.")
            await self.bot.close()
            sys.exit(0)




async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerCog(bot))
