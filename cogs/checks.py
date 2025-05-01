from discord.ext import commands

def is_in_channel(channel_id):
    def predicate(ctx):
        return ctx.channel.id == channel_id
    return commands.check(predicate)
