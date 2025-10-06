import discord
from discord.ext import commands
from random import *
from mongo import *

ALLOWED_CHANNEL_ID = 1108669778383613952
OWNER_ID = 1118218807694065684

BLACK_HEX = 0x000001
RED_HEX = 0xED004C
EMOJI_BLACK = "<a:BlackArrow:1380680364242243616>"
EMOJI_RED = "<a:0_arrowww:1380680635815034940>"

class betting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bet(self, ctx, num: str = None):
        if num is None:
            await ctx.send("Must specify how much you want to bet.")
            return
        if not num.isdigit():
            await ctx.send("Must be a valid number")
            return
        num = int(num)
        if num < 1 or num >= 20000:
            await ctx.send("Cant bet with more than 20,000 or less than 1.")
            return
        a = getuservar("usd", ctx.author.id)
        if num > a:
            await ctx.send(f"You only have {a} usd, you cannot bet with {num}.")
            return
        values = [-0.5, -0.4, -0.3 , -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.5]
        endvalue = choice(values)
        transaction = num * endvalue
        transaction = int(transaction)
        setuservar("usd", ctx.author.id, transaction)
        b = getuservar("usd", ctx.author.id)
        if transaction > 0:
            await ctx.send(f"You won {transaction}!\nYour balance is now {b}.")
        else:
            await ctx.send(f"You lost {transaction}\n Your balance is now {b}")

    @commands.command(name="roulette", aliases=["r"])
    async def roulette(self, ctx, amount: str = None, color: str = None):
        if amount is None or color is None:
            await ctx.send("Format: r {amount} {red/black}")
            return
        if not amount.isdigit():
            await ctx.send("Format: r {amount} {red/black}")
            return
        amt = int(amount)
        if amt <= 1:
            await ctx.send("Must be more than 1$")
            return
        if amt > 20000:
            await ctx.send("Cant bet more than 20k")
            return
        val = color.lower()
        if val not in ("red", "black"):
            await ctx.send("Format: r {amount} {red/black}")
            return
        uid = str(ctx.author.id)
        balance = getuservar("usd", uid) or 0
        if amt > balance:
            await ctx.send("You cant bet with more than you have")
            return
        chance = randint(1, 2)
        if chance == 1:
            landed = val
            win = True
        else:
            landed = "red" if val == "black" else "black"
            win = False
        landed_emoji = EMOJI_BLACK if landed == "black" else EMOJI_RED
        landed_hex = BLACK_HEX if landed == "black" else RED_HEX
        if win:
            desc = (
                f"{landed_emoji} The ball landed on {landed}!\n"
                f"{landed_emoji} YOU WIN ${amt:,}!!"
            )
            setuservar("usd", uid, amt)
        else:
            desc = (
                f"{landed_emoji} The ball landed on {'red' if landed == 'red' else 'black'}!\n"
                f"{landed_emoji} You lost your ${amt:,}"
            )
            setuservar("usd", uid, -amt)
        embed = discord.Embed(title="Roulette", description=desc, colour=landed_hex)
        embed.set_footer(text="You either get the money you betted with or lose it all.")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(betting(bot))