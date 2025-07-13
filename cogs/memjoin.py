import discord
from discord.ext import commands

class joins(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel = member.guild.get_channel(1250240937913749618)
		guild = member.guild
		mems = guild.member_count
		mem = member.id
		await channel.send(f"Hello, <@{mem}>, welcome to PVP clans. You are the {mems}th member to join.")
				
		
async def setup(bot):
	await bot.add_cog(joins(bot))