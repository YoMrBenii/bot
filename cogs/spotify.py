import discord
from discord.ext import commands

class SpotifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fm(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        
        spotify_activity = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
        
        if spotify_activity:
            embed = discord.Embed(
                title=f"{user.display_name}'s Now Playing",
                color=spotify_activity.color
            )
            embed.set_thumbnail(url=spotify_activity.album_cover_url)
            embed.add_field(name="Song", value=spotify_activity.title, inline=False)
            embed.add_field(name="Artist", value=spotify_activity.artist, inline=False)
            embed.add_field(name="Album", value=spotify_activity.album, inline=False)
            embed.add_field(name="Listen on Spotify", value=f"[Click here]({spotify_activity.track_url})", inline=False)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{user.display_name} is not currently listening to Spotify.")

async def setup(bot):
    await bot.add_cog(SpotifyCog(bot))