import os
import discord
from discord.ext import commands
import google.generativeai as genai
import time  # For handling rate-limiting retries
from .check.utils import is_in_channel

def is_in_channel(channel_id):
    def predicate(ctx):
        return ctx.channel.id == channel_id
    return commands.check(predicate)

# Adjustable Parameters
API_KEY = os.getenv("GOOGLE_API_KEY", "your-api-key-here")  # Replace or ensure it's set as an environment variable
MODEL_NAME = "gemini-1.5-pro-latest"  # Change this to the model you want to use
EMBED_COLOR = discord.Color.blue()  # Customize the embed color
DEFAULT_PROMPT = "Hello, how can I assist you today?"  # Default fallback prompt

# Generation Parameters (Less Restrictive)
TEMPERATURE = 1.0  # Max randomness for highly creative responses
TOP_P = 1.0  # Max nucleus sampling for diverse responses
MAX_OUTPUT_TOKENS = 500  # Allow longer responses
STOP_SEQUENCES = []  # No stop sequences to allow full freedom
CANDIDATES = 1  # Number of response candidates to generate
SAFETY_SETTINGS = []  # Remove safety settings for unrestricted responses
CONTEXT = ""  # Provide additional context for the model to consider
EXAMPLES = []  # List of example input-output pairs for fine-tuning responses

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Configure Generative AI
        if not API_KEY or API_KEY == "your-api-key-here":
            raise ValueError("GOOGLE_API_KEY is missing or not set properly")
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)

    @commands.command(name="ai")
    @is_in_channel(123456789012345678)
    async def ai_command(self, ctx, *, prompt: str = None):
        """Generates a response from Generative AI based on the given prompt."""
        if not prompt:
            prompt = DEFAULT_PROMPT  # Use the default if no prompt is provided

        try:
            # Generate response using the AI model with advanced parameters
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

            # Fetch the generated text from the response
            generated_text = response.candidates[0]["output"] if response.candidates else "No response generated."

            # Create and send the embed
            embed = discord.Embed(
                title="AI Response",
                description=generated_text,
                color=EMBED_COLOR
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)

        except genai.exceptions.RateLimitError as e:
            # Extract retry information from the exception
            retry_after = getattr(e, "retry_after", None)  # Check if Retry-After is available
            if retry_after:
                await ctx.send(f"Rate limit reached. Please wait {retry_after} seconds before trying again.")
            else:
                await ctx.send("Rate limit reached. Please try again later.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(AICog(bot))