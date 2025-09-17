import discord

def hasrole(member: discord.Member, roleid: list[int]) -> bool:
    roleid = [str(r), for r in roleid]
    for role in member.roles:
        if role.id in roleid:
            return True
        return False 
    
