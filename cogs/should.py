import discord
from discord.ext import commands
from random import *

class should(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message, ctx: commands.context):
        lowmsg = message.lower()
        if lowmsg != "should":
            return
        texts = ["Yes king;No you nigger", "Hell yes", "Fuck no", "Yes idiot", "Yes idiot", "No idiot", "No idiot", "maybe 😏", "maybe 😏", "Yes dumbo", "Yes dumbo", "No dumbo", "No dumbo", "hmm idk ask urself r u that stupid or what be clever mf you keep skipping school go learn and get bitches", "definetly", "definetly", "Nah dont do that bro;Yeah do that man its a great idea"]
        text = choice(texts)
        await ctx.send(text)


