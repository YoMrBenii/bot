import os
import discord
from discord.ext import commands
import google.generativeai as genai

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Configure Gemini
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Or your preferred model

    @commands.command(name="ai")
    async def ai_command(self, ctx, *, prompt: str):
        """Generates a response from Gemini AI based on the given prompt."""
        try:
            response = self.model.generate_content(prompt)
            embed = discord.Embed(
                title="AI Response",
                description=response.text,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(AICog(bot))