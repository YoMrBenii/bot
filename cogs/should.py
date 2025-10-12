import discord
from discord.ext import commands
from random import choice

class ShouldResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        lowmsg = message.content.lower().split()
        if not lowmsg or lowmsg[0] != "should":
            return

        texts = [
            "Yes king", "No you nigger", "Hell yes", "Fuck no", "Yes idiot",
            "No idiot", "maybe 😏", "Yes dumbo", "No dumbo",
            "hmm idk ask urself r u that stupid or what be clever mf you keep skipping school go learn and get bitches",
            "definitely", "Nah dont do that bro", "Yeah do that man its a great idea"
        ]

        text = choice(texts)
        await message.channel.send(text)

async def setup(bot):
    await bot.add_cog(ShouldResponder(bot))