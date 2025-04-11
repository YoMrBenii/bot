import discord
from discord.ext import commands
import json
import os

DATA_FILE = "black.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump({}, file)

def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def save(self, ctx, sequence: str, *, word: str):
        data = load_data()
        
        # Check if the sequence exists in the data
        if sequence in data:
            # Check if the word already exists in the list for this sequence
            if word not in data[sequence]:
                if isinstance(data[sequence], list):  
                    data[sequence].append(word)
                else:  
                    data[sequence] = [data[sequence], word]
                save_data(data)
                await ctx.send(f"Saved: `{sequence}` -> `{word}`")
            else:
                await ctx.send(f"The word `{word}` already exists in `{sequence}`.")
        else:
            data[sequence] = [word]
            save_data(data)
            await ctx.send(f"Saved: `{sequence}` -> `{word}`")

    @commands.command()
    async def r(self, ctx, sequence: str):
        data = load_data()
        if sequence in data:
            words = ", ".join(f"`{w}`" for w in data[sequence])
            await ctx.send(f"`{sequence}` -> {words}")
        else:
            await ctx.send(f"No words found for `{sequence}`")

    @commands.command()
    async def list(self, ctx):
        data = load_data()
        if data:
            message = "\n".join([f"`{seq}` -> {', '.join(f'`{w}`' for w in words)}"
                                 for seq, words in data.items()])
            await ctx.send(f"Here are all the stored sequences:\n{message}")
        else:
            await ctx.send("No sequences have been saved yet.")

    @commands.command()
    async def test(self, ctx):
        await ctx.send("hi")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
