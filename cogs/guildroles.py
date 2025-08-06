import discord
from discord.ext import commands

class ServerRoles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def guildroles(self, ctx):
	   	guildroles = [role.name for role in ctx.guild.roles]
	   	guildroles.reverse()
	   	guildrole = "\n".join(guildroles)
	   	embed = discord.Embed(description=guildrole)
	   	await ctx.send(embed=embed)

		
async def setup(bot):
	await bot.add_cog(ServerRoles(bot))

