from __future__ import annotations
import random
import re
from typing import Optional, Set
import discord
from discord import app_commands
from discord.ext import commands


_DURATION_RE = re.compile(r"(?P<value>\d+)(?P<unit>[smhd])", re.I)
_UNIT_SECONDS = {"s": 1, "m": 60, "h": 3_600, "d": 86_400}


def parse_duration(raw: str) -> Optional[int]:
    total = 0
    for match in _DURATION_RE.finditer(raw.lower()):
        total += int(match["value"]) * _UNIT_SECONDS[match["unit"]]
    return total or None


class GiveawayView(discord.ui.View):

    def __init__(
        self,
        *,
        prize: str,
        timeout: float,
        winners: int,
        required_role: Optional[discord.Role],
    ):
        super().__init__(timeout=timeout)
        self.prize: str = prize
        self.participants: Set[discord.Member] = set()
        self.message: discord.Message | None = None
        self.required_role: Optional[discord.Role] = required_role
        self.winners: int = winners

    @discord.ui.button(label="Join 🎉", style=discord.ButtonStyle.primary)
    async def join_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        member = interaction.user
        
        if self.required_role and self.required_role not in member.roles:
            await interaction.response.send_message(
                f"You need the {self.required_role.mention} role to join this giveaway.",
                ephemeral=True,
            )
            return

        if member in self.participants:
            await interaction.response.send_message(
                "You’re already in the draw.", ephemeral=True
            )
            return

        self.participants.add(member)

        embed = self.message.embeds[0]
        embed.set_field_at(
            0, name="People joined:", value=str(len(self.participants)), inline=False
        )
        await self.message.edit(embed=embed, view=self)

        await interaction.response.send_message(
            "Entered, good luck! ", ephemeral=True
        )

    async def on_timeout(self) -> None:
        "
        for item in self.children:
            item.disabled = True

        embed = self.message.embeds[0]

        if self.participants:
            num_winners = min(self.winners, len(self.participants))
            chosen = random.sample(tuple(self.participants), k=num_winners)

            if num_winners == 1:
                winner = chosen[0]
                result = f"**Winner:** {winner.mention}!"
                win_embed = discord.Embed(
                    title="🎉 Giveaway Ended 🎉",
                    description=f"Congratulations {winner.mention}!\nYou won **{self.prize}**",
                    colour=discord.Colour.green(),
                )
                await self.message.channel.send(content=winner.mention, embed=win_embed)

            else:
                mentions = ", ".join(m.mention for m in chosen)
                result = f" **Winners ({num_winners}):** {mentions}!"
                win_embed = discord.Embed(
                    title="🎉 Giveaway Ended 🎉",
                    description=f"Congratulations {mentions}!\nYou won **{self.prize}**",
                    colour=discord.Colour.green(),
                )
                await self.message.channel.send(content=mentions, embed=win_embed)

        else:
            result = "No one joined. Giveaway cancelled."

        embed.add_field(name="Result", value=result, inline=False)
        await self.message.edit(embed=embed, view=self)
        self.stop()


class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @app_commands.command(description="Start a giveaway.")
    @app_commands.describe(
        prize="What you are giving away",
        duration="When it ends (e.g. 30m, 2h, 1d12h)",
        winners="Number of winners (default = 1)",
        required_role="Optional: Role required to join",
    )
    async def giveaway(
        self,
        interaction: discord.Interaction,
        prize: str,
        duration: str,
        winners: int = 1,
        required_role: Optional[discord.Role] = None,
    ):
        seconds = parse_duration(duration)
        if seconds is None:
            await interaction.response.send_message(
                "Invalid duration. Examples: 90s, 30m, 2h, 1d", ephemeral=True
            )
            return

        if winners < 1:
            await interaction.response.send_message(
                "Number of winners must be at least 1.", ephemeral=True
            )
            return

        end_time = int(discord.utils.utcnow().timestamp()) + seconds

        description = f"**Prize:** {prize}\n**Winners:** {winners}\n**Ends:** <t:{end_time}:R>"
        if required_role:
            description += f"\n**Required Role:** {required_role.mention}"

        embed = discord.Embed(
            title="Giveaway!",
            description=description,
            colour=discord.Colour.blue(),
        )
        embed.add_field(name="People joined:", value="0", inline=False)

        view = GiveawayView(
            prize=prize, timeout=seconds, winners=winners, required_role=required_role
        )
        await interaction.response.send_message(embed=embed, view=view)

        view.message = await interaction.original_response()

async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))
