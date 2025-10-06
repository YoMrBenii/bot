import discord
from discord.ext import commands
from functions import *
from mongo import *

class resets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def resetallmsgs(self, ctx):
        if not owneronly(ctx.author):
            await ctx.send("Only for beni")
            return
        a = top1lb("messages")
        b = getservervar("recordholder")
        c = getservervar("recordmsgs")
        d = top1lbvalue("messages")
        if c <= d:
            changeservervar("recordmsgs", d)
            changeservervar("recordholder", a)
        resetallusers("messages")

    @commands.command()
    async def manualaddrecord(self, ctx, user: discord.Member, record: int):
        if not owneronly(ctx.author):
            await ctx.send("Only for beni.")
            return
        changeservervar("recordmsgs", record)
        changeservervar("recordholder", user.id)

