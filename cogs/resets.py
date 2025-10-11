import discord
from discord.ext import commands
from functions import *
from mongo import *
import traceback

class resets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def resetallmsgs(self, ctx):
        if not owneronly(ctx.author):
            await ctx.send("Only for Beni.")
            return

        try:
            # Fetch leaderboard and record data safely
            top_user = top1lb("messages")
            record_holder = getservervar("recordholder") or None
            record_msgs = getservervar("recordmsgs") or 0
            top_value = top1lbvalue("messages") or 0

            # Update record if top_value beats record_msgs
            if top_value > record_msgs:
                changeservervar("recordmsgs", top_value)
                changeservervar("recordholder", top_user)

            # Reset all users
            result = resetallusers("messages")  # should return modified_count ideally

            # If your resetallusers doesn't return anything, remove the f-string part
            await ctx.send(f" All message counts have been reset successfully. ({result or 'unknown'} users affected)")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"Error while resetting messages:\n```{e}```")

    @commands.command()
    async def manualaddrecord(self, ctx, user: discord.Member, record: int):
        if not owneronly(ctx.author):
            await ctx.send("Only for Beni.")
            return

        try:
            changeservervar("recordmsgs", record)
            changeservervar("recordholder", user.id)
            await ctx.send(f"✅ Manually set record to **{record}** for {user.mention}.")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"❌ Error while updating record:\n```{e}```")

async def setup(bot):
    await bot.add_cog(resets(bot))
