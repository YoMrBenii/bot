import discord
from discord.ext import commands
from mongo import *
from functions import hasrole
import time

class hire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hire(self, ctx, member: discord.Member = None):
        a = getuservar("permlvl", ctx.author.id)
        if a < 1:
            await ctx.send("Must have perm level 1.")
            return
        if not member:
            await ctx.send("Must ping whoever you want to hire")
            return
        if hasrole(member.id, 1032679589648011325):
            await ctx.send("User is already staff")
            return
        
        role = ctx.guild.get_role(1037089161104076921)
        role2 = ctx.guild.get_role(1032679589648011325)
        await member.add_roles(role, role2)
        changeuservar("hiredate", member.id, int(time.time()))
        changeuservar("hirer", member.id, ctx.author.id)
        embed1 = discord.Embed(title="Hired user", description=f"<@{ctx.author.id}> hired <@{member.id}> at <t:{time.time()}:f>")
        channel = self.bot.fetch_channel(1292146574205521970)
        embed = discord.Embed(description=f"hired {member.id}")
        await ctx.send(embed=embed)
        await channel.send(embed=embed1)
    
async def setup(bot):
    await bot.add_cog(hire(bot))