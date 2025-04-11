import discord
from discord.ext import commands

class gg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reforms(self, ctx, role: discord.Role):
        role_members = [member for member in role.members]
        
        sorted_members = sorted(role_members, key=lambda m: m.top_role.position, reverse=True)
        
        if not sorted_members:
            await ctx.send(f"No members have the {role.name} role.")
        else:
            member_list = "\n".join([member.name for member in sorted_members])
            await ctx.send(f"**Members with the {role.name} role (ranked):**\n{member_list}")

async def setup(bot):
    await bot.add_cog(gg(bot))
