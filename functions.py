import discord

def hasrole(member: discord.Member, roleid: list[int]) -> bool:
    if not isinstance(roleid, list):
        roleid = [roleid]
    for role in member.roles:
        if role.id in roleid:
            return True
    return False 

def owneronly(member: discord.Member) -> bool:
    if member.id == 1118218807694065684:
        return True
    return False
