import os
import discord
from discord.ext import commands
import google.generativeai as genai
import time

def is_in_channel(channel_id):
    def predicate(ctx):
        return ctx.channel.id == channel_id
    return commands.check(predicate)

API_KEY = os.getenv("GOOGLE_API_KEY", "your-api-key-here")
MODEL_NAME = "gemini-1.5-pro-latest"
EMBED_COLOR = discord.Color.blue()
DEFAULT_PROMPT = "Hello, how can I assist you today?"

TEMPERATURE = 1.0
TOP_P = 1.0
MAX_OUTPUT_TOKENS = 500
STOP_SEQUENCES = []
CANDIDATES = 1
SAFETY_SETTINGS = []
CONTEXT = ""
EXAMPLES = []

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not API_KEY or API_KEY == "your-api-key-here":
            raise ValueError("GOOGLE_API_KEY is missing or not set properly")
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)

    @commands.command(name="ai")
    @is_in_channel(1108669778383613952)
    async def ai_command(self, ctx, *, prompt: str = None):
        if not prompt:
            prompt = DEFAULT_PROMPT

        try:
            response = self.model.generate_content(
                prompt=prompt,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                stop_sequences=STOP_SEQUENCES,
                candidate_count=CANDIDATES,
                safety_settings=SAFETY_SETTINGS,
                context=CONTEXT,
                examples=EXAMPLES,
            )

            generated_text = response.candidates[0]["output"] if response.candidates else "No response generated."

            embed = discord.Embed(
                title="AI Response",
                description=generated_text,
                color=EMBED_COLOR
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)

        except genai.exceptions.RateLimitError as e:
            retry_after = getattr(e, "retry_after", None)
            if retry_after:
                await ctx.send(f"Rate limit reached. Please wait {retry_after} seconds before trying again.")
            else:
                await ctx.send("Rate limit reached. Please try again later.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(AICog(bot))