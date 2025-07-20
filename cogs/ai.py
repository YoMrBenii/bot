from discord.ext import commands
from deep_translator import GoogleTranslator
import asyncio

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trans(self, ctx, lang: str = "en"):
        if ctx.message.reference is None:
            await ctx.send("You need to **reply to a message** to translate it.")
            return

        try:
            replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            text_to_translate = replied_message.content

            # Run the translation in an executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: GoogleTranslator(source="auto", target=lang).translate(text_to_translate)
            )

            await ctx.send(result)

        except Exception as e:
            await ctx.send(f"Translation failed: {e}")

async def setup(bot):
    await bot.add_cog(Translate(bot))
