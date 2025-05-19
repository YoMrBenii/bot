import discord
from discord.ext import commands

class AllRoles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def roles(self, ctx, user: discord.Member = None):
		target = user or ctx.author
		sorted_roles = sorted(target.roles, key=lambda p: p.position, reverse=True)
		rolename = [role.name for role in sorted_roles if role.name != "@everyone"]
		end = "• " + "\n• ".join(rolename)
		embed = discord.Embed(
		description=end, title=f"{target.display_name}s roles")
		await ctx.send(embed=embed)

async def setup(bot):
	await bot.add_cog(AllRoles(bot))
	
	