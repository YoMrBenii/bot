import os
import discord
from discord.ext import commands
import google.generativeai as genai
import sys

def is_in_channel(channel_id, user_id):
    def predicate(ctx):
        if ctx.author.id == user_id:
            return True
        return ctx.channel.id == channel_id
    return commands.check(predicate)

print(f"Cog Python executable: {sys.executable}")  # Prints the Python executable path
print(f"Cog PYTHONPATH: {os.environ.get('PYTHONPATH')}")  # Prints the PYTHONPATH environment variable


class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Configure Gemini
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    @commands.command(name="ai")
    @is_in_channel(channel_id=1108669778383613952, user_id=1118218807694065684)
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