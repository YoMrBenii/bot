from sys import exception
import discord
from discord.ext import commands
from mongo import *
from functions import hasrole
import time
import traceback

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
            await ctx.send("Must ping whoever you want to hire.")
            return
        if hasrole(member, 1032679589648011325):
            await ctx.send("User is already staff.")
            return
        if member.id == ctx.author.id:
            await ctx.send("Cannot hire yourself")
            return
        role = ctx.guild.get_role(1037089161104076921)
        role2 = ctx.guild.get_role(1032679589648011325)
        await member.add_roles(role, role2)
        changeuservar("hiredate", member.id, int(time.time()))
        changeuservar("hirer", member.id, ctx.author.id)
        embed1 = discord.Embed(
            title=f"Hired {member.name}",
            description=f"<@{ctx.author.id}> hired <@{member.id}> at <t:{int(time.time())}:f>", color=0x369876)
        channel = await self.bot.fetch_channel(1292146574205521970)
        embed = discord.Embed(description=f"Hired <@{member.id}>.")
        await ctx.send(embed=embed)
        await channel.send(embed=embed1)


    @commands.command()
    async def fire(self, ctx, member: discord.Member = None):
        a = getuservar("permlvl", ctx.author.id)
        helperrole = ctx.guild.get_role(1037089161104076921)
        try:
            if a < 2 or (a == 2 and helperrole.position <= member.top_role.position):
                await ctx.send("Must have perm level 2 or 3. Permlvl 2 can only fire helpers.")
                return
        except Exception as e:
            await ctx.send(e)
        if not member:
            await ctx.send("Must ping whoever you want to fire.")
            return
        if not hasrole(member, 1032679589648011325):
            await ctx.send("User is not staff.")
            return
        if member.id == ctx.author.id:
            await ctx.send("Cannot fire yourself")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("Cant fire a higher rank.")
            return
        embed1 = discord.Embed(
            title=f"Fired {member.name}",
            description=f"<@{ctx.author.id}> fired <@{member.id}> at <t:{int(time.time())}:f>", color=0xff4865)
        channel = await self.bot.fetch_channel(1292146574205521970)
        embed = discord.Embed(description=f"Fired <@{member.id}>.")
        await ctx.send(embed=embed)
        await channel.send(embed=embed1)
        roles = [1032679589648011325, 1037089161104076921, 1033011680935944332, 1033003792288972871, 1033003598784770208, 1086352084653314110, 1190333493574639636, 1157030550587068466, 1226612154460016761, 1076315417510952960]
        role = [ctx.guild.get_role(rid) for rid in roles]
        await member.remove_roles(*role)
        former = ctx.guild.get_role(1035219870083727471)
        await member.add_roles(former)
        changeuservar("hiredate", member.id, None)
        changeuservar("hirer", member.id, None)
        

    @commands.command(name="pass")
    async def _pass(self, ctx, member: discord.Member = None):
        if not member:
            await ctx.send("Must ping a user.")
            return
        if not hasrole(member, 1032679589648011325):
            await ctx.send("User must be a staff member.")
            return
        if not hasrole(member, 1037089161104076921):
            await ctx.send("User is not a helper.")
            return
        changeuservar("passdate", member.id, int(time.time()))
        embed1 = discord.Embed(
            title=f"Passed {member.name}",
            description=f"<@{ctx.author.id}> passed <@{member.id}> at <t:{int(time.time())}:f>",
            color=0x28498b)
        channel = await self.bot.fetch_channel(1292146574205521970)
        await channel.send(embed=embed1)
        embed = discord.Embed(description=f"Passed <@{member.id}>.")
        await ctx.send(embed=embed)
        helper = ctx.guild.get_role(1037089161104076921)
        mod = ctx.guild.get_role(1033011680935944332)
        await member.add_roles(mod)
        await member.remove_roles(helper)
        
                               
        




async def setup(bot):
    await bot.add_cog(hire(bot))


