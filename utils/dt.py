from discord.ext import commands
        
def isUser(user_id):
    async def predicate(ctx):
        try:
            if ctx.author.id == user_id:
                return True
            else:
                # You can log or do something here
                print(f"User {ctx.author} tried to run command but is not allowed.")
                return False
        except Exception as e:
            print(f"Error inside isUser check: {e}")
            return False  # Fail safe: block command if error happens

    return commands.check(predicate)


