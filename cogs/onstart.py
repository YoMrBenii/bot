import discord
from discord.ext import commands

class onStart(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
		a = self.bot.get_channel(1147929783968223233)
		await a.send("Bot online")
		
async def setup(bot):
	await bot.add_cog(onStart(bot))
	       
 