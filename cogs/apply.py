import discord
import logging
import random
import string
from discord.ext import commands
from discord.ui import Modal, TextInput, Button, View

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackModal(Modal, title='Become staff'):
    feedback = TextInput(
        label='Introduce yourself',
        style=discord.TextStyle.long,
        placeholder='Enter answer',
        required=True,
        max_length=200,
        min_length=20,
    )

    feedback1 = TextInput(
        label='For how long do you plan on staying?',
        style=discord.TextStyle.long,
        required=True,
        placeholder="Enter answer",
        max_length=100,
        min_length=5,
    )

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user
        real_username = user.name
        try:
            answer = self.children[0].value
            answer1 = self.children[1].value
            logger.info(f'Received feedback from {real_username}: {answer}')
            embed = discord.Embed(
                description=f"**Name:** {real_username}\n**Reason:** {answer}\n**Why:** {answer1}")

            bot = interaction.client
            channel = bot.get_channel(1233923949436342412)  # Replace with your channel ID

            await channel.send(embed=embed)
            await interaction.response.send_message(f"Thanks for your response, {real_username}!", ephemeral=True)

        except Exception as e:
            logger.error(f"Error in on_submit: {e}")

            if not interaction.response.is_done():
                await interaction.response.send_message(f"Something went wrong: {e}", ephemeral=True)

class StaffButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Apply", style=discord.ButtonStyle.primary, custom_id="staff_apply_button"))

    @discord.ui.button(label="Apply", style=discord.ButtonStyle.primary, custom_id="staff_apply_button")
    async def apply_callback(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(FeedbackModal())
        logger.info('Modal sent')

class ModalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def staff(self, ctx):
        view = StaffButtonView()
        await ctx.send("Click the button to apply for staff:", view=view)
        logger.info('Sent message with apply button')

    @staff.error
    async def app_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            logger.error(f"{ctx.author} is missing the required role(s). Error: {error}")
            await ctx.send("You need to be staff or former staff to run this command.")
        else:
            logger.error(f"Unexpected error occurred in app command: {error}")
            await ctx.send("An unexpected error occurred.")

async def setup(bot):
    await bot.add_cog(ModalCog(bot))
    bot.add_view(StaffButtonView())  # This makes the view persistent
    logger.info('ModalCog loaded and persistent view registered')
