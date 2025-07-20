from discord.ext import commands
from googletrans import Translator

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @commands.command()
    async def trans(self, ctx, lang: str = "en"):
        if ctx.message.reference is None:
            await ctx.send("You need to **reply to a message** to translate it.")
            return

        try:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            text_to_translate = replied_message.content
            result = await self.translator.translate(text_to_translate, dest=lang)

            await ctx.send(f"{result.text}")

        except Exception as e:
            await ctx.send(f"Translation failed: {e}")

async def setup(bot):
    await bot.add_cog(Translate(bot))
