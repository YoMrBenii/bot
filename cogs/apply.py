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
        # ... (keep your existing submission logic) ...

class StaffButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        # Only change: Generate unique custom_id
        custom_id = f"staff_apply_{''.join(random.choices(string.ascii_letters + string.digits, k=10))}"
        self.add_item(Button(
            label="Apply", 
            style=discord.ButtonStyle.primary, 
            custom_id=custom_id
        ))

    async def interaction_check(self, interaction: discord.Interaction):
        # Handle any button with "staff_apply_" prefix
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
