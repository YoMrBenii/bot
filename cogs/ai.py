import os
import discord
from discord.ext import commands
import google.generativeai as genai
import time

# Adjustable Parameters
API_KEY = os.getenv("GOOGLE_API_KEY", "your-api-key-here")
MODEL_NAME = "gemini-1.5-pro-latest"
EMBED_COLOR = discord.Color.blue()
DEFAULT_PROMPT = "Hello, how can I assist you today?"

# Generation Parameters (Less Restrictive)
TEMPERATURE = 1.0
TOP_P = 1.0
MAX_OUTPUT_TOKENS = 500
STOP_SEQUENCES = []
CANDIDATES = 1
CONTEXT = ""
EXAMPLES = []

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not API_KEY or API_KEY == "your-api-key-here":
            raise ValueError("GOOGLE_API_KEY is missing or not set properly")
        genai.configure(api_key=API_KEY)

    @commands.command(name="ai")
    async def ai_command(self, ctx, *, prompt: str = None):
        if not prompt:
            prompt = DEFAULT_PROMPT

        try:
            # Corrected method call
            response = genai.generate_content(
                model=MODEL_NAME,
                input_text=prompt,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )

            generated_text = response.candidates[0]["output"] if response.candidates else "No response generated."

            embed = discord.Embed(
                title="AI Response",
                description=generated_text,
                color=EMBED_COLOR
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(AICog(bot))