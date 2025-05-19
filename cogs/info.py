import discord
from discord.ext import commands
 
class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def info(self, ctx, user: discord.Member):
		await ctx.send(f"```\n{user.mention}\nID: {user.id}\nUser: {user.name}\nCreation date: {user.created_at}\n\nServer Info\n\nServer nickname: {user.nick}\nHighest role: {user.top_role}\n```")
		
	@commands.command()
	async def infoembed(self, ctx, user: discord.Member):
		creation_timestamp = int(user.created_at.timestamp())
		avatar_url = user.avatar.url
		embed = discord.Embed(description=f"\n{user.mention}\nID: {user.id}\nUser: {user.name}\nCreation date: <t:{creation_timestamp}:R>\n\nServer Info\n\nServer nickname: {user.nick}\nHighest role: {user.top_role}\n")
		embed.set_thumbnail(url=avatar_url)
		await ctx.send(embed=embed)
			
	@commands.command()
	async def cmds(self, ctx):
		commands = [f"- {command.name}" for command in self.bot.commands]
		await ctx.send("\n".join(commands))
		
async def setup(bot):
	await bot.add_cog(Info(bot))