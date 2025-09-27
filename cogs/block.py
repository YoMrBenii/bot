from discord.ext import commands

ALLOWED_USER_ID = 1118218807694065684
ALLOWED_CHANNEL_ID = 1147929783968223233

class AccessGate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_check(self._gate_prefix)

    async def _gate_prefix(self, ctx: commands.Context) -> bool:
        if ctx.author.id == ALLOWED_USER_ID:
            return True
        if ctx.channel and ctx.channel.id == ALLOWED_CHANNEL_ID:
            return True
        return False

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, (commands.CheckFailure, commands.CommandNotFound)):
            return

async def setup(bot: commands.Bot):
    await bot.add_cog(AccessGate(bot))
