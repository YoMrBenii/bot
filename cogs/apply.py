import discord
import logging
import random
import string
from discord.ext import commands
from discord.ui import Modal, TextInput, Button, View

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Feedback modal for users to apply for staff
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

    # Persistent button with the callback to open modal
    class StaffButtonView(View):
        def __init__(self):
            super().__init__(timeout=None)  # Timeout None makes the view persistent
            self.add_item(Button(label="Apply", style=discord.ButtonStyle.primary, custom_id=self.generate_custom_id()))

        @discord.ui.button(label="Apply", style=discord.ButtonStyle.primary)
        async def apply_callback(self, interaction: discord.Interaction, button: Button):
            modal = ModalCog.FeedbackModal()
            await interaction.response.send_modal(modal)
            logger.info('Modal sent')

        def generate_custom_id(self):
            """Generate a unique custom ID for each button."""
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            return f"persistent_button_{random_str}"  # Example custom ID: persistent_button_<random_string>

    # Command to display the button
    @commands.command()
    async def staff(self, ctx):
        view = ModalCog.StaffButtonView()
        await ctx.send("Click the button to apply for staff:", view=view)
        logger.info('Sent message with apply button')

    # Error handling for the staff command
    @staff.error
    async def app_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            logger.error(f"{ctx.author} is missing the required role(s). Error: {error}")
            await ctx.send("You need to be staff or former staff to run this command.")
        else:
            logger.error(f"Unexpected error occurred in app command: {error}")
            await ctx.send("An unexpected error occurred.")

# Register the cog and the persistent view
async def setup(bot):
    await bot.add_cog(ModalCog(bot))
    bot.add_view(ModalCog.StaffButtonView())  # Registering the view with the persistent button
    logger.info('ModalCog loaded and persistent view registered')
