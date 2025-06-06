import discord
import random
import string
from discord.ext import commands
from discord.ui import Modal, TextInput, Button, View

class FeedbackModal(Modal, title='Become staff'):
    feedback = TextInput(
        label='Introduce yourself',
        style=discord.TextStyle.long,
        placeholder='Enter answer',
        required=True,
        max_length=200,
    )

    feedback1 = TextInput(
        label='For how long do you plan on staying?',
        style=discord.TextStyle.long,
        required=True,
        placeholder="Enter answer",
        max_length=100,
    )

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        real_username = user.id
        try:
            answer = self.children[0].value
            answer1 = self.children[1].value
            embed = discord.Embed(
                description=f"**Name:** <@{real_username}>\n**Introduction:** {answer}\n**How long:** {answer1}"
            )

            channel = interaction.client.get_channel(1233923949436342412)  # Replace with your channel ID
            await channel.send(embed=embed)
            await interaction.response.send_message(f"Thanks for your response, <@{real_username}>!", ephemeral=True)
        except Exception as e:
            if not interaction.response.is_done():
                await interaction.response.send_message(f"Something went wrong: {e}", ephemeral=True)

class StaffButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        custom_id = f"staff_apply_{''.join(random.choices(string.ascii_letters + string.digits, k=10))}"
        self.add_item(Button(
            label="Apply", 
            style=discord.ButtonStyle.primary, 
            custom_id=custom_id
        ))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.data['custom_id'].startswith("staff_apply_"):
            await interaction.response.send_modal(FeedbackModal())
            return True
        return False

class ModalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def staff(self, ctx):
        view = StaffButtonView()
        await ctx.send("Click the button to apply for staff:", view=view)

async def setup(bot):
    await bot.add_cog(ModalCog(bot))
