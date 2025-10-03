import discord
from discord.ext import commands

class Bell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages = []

    @commands.command()
    async def type(self, ctx, *, text: str):
        await ctx.send(f"{text}")
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.deleted_messages.insert(0, (message.content, message.author))  
        if len(self.deleted_messages) > 20:
            self.deleted_messages.pop()

    @commands.command()
    async def snipe(self, ctx, count: int = 1):
        if count < 1 or count > 20:
            await ctx.send("Please specify a number between 1 and 20.")
            return
        messages_to_snipe = self.deleted_messages[:count]

        if not messages_to_snipe:
            await ctx.send("There's nothing to snipe!")
            return
        embed = discord.Embed(title="Sniped Messages", color=discord.Color.blue())
        for idx, (content, author) in enumerate(messages_to_snipe, start=1):
            embed.add_field(name=f"Message #{idx}", value=f"**Content:** {content}\n**Author:** {author}", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Bell(bot))