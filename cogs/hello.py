import discord
from discord.ext import commands
import random

class Hi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("hiiii!")

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("heyya babe")
    
    @commands.command()
    async def getid(self, ctx, user: discord.User):
        await ctx.send(f"The ID of {user.name} is {user.id}")
    
    @commands.command()
    async def rolemems(self, ctx, *, role_name: str):
        # Case-insensitive role lookup
        role = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), ctx.guild.roles)

        if role is None:
            await ctx.send(f"Role `{role_name}` not found.")
            return

        # List of member names with the role
        members_with_role = [member.name for member in ctx.guild.members if role in member.roles]

        if members_with_role:
            embed = discord.Embed(
                title=f"Members with role: {role.name}",
                description="\n".join(members_with_role),
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No members found with the role `{role.name}`.")

    @commands.command()
    async def kiss(self, ctx):
    	a = ["You got slapped 💀", "They leaned into the kiss and yall made out.", "You got charged for assault", "They took their clothes off and u had sex", "Yall should make out icl", "i just cummed", "You guys started to have sex and got kids", "THIS IS AMERICA DO WHATEVER THE FUCK YOU WANT 🗣️🗣️🔥🔥🦅🦅"]
    	b = random.choice(a)
    	mentioned_user = ctx.message.mentions[0]
    	await ctx.send(f" {ctx.author.mention} kissed {mentioned_user.mention} \n{b} ")
     
async def setup(bot):
    await bot.add_cog(Hi(bot))
