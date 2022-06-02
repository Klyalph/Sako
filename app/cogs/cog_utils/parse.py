import nextcord
from typing import Optional


def parse_user(instance, ctx, contender: str) -> Optional[nextcord.Member]:
    if user := (ctx.message.mentions or [None])[0]:
        if user.bot:
            return None
        return user

    members = []

    if len(ctx.guild.members) > 200:
        return None

    for member in ctx.guild.members:
        if (
            member.name.lower().startswith(contender.lower())
            and member.id != ctx.author.id
            and member.id != instance.client.user.id
            and not member.bot
        ):
            members.append(member)

    if len(members) == 1:
        return members[0]

    check = [mem.name.lower() == contender.lower() for mem in members]

    if check.count(True) == 1:
        return members[check.index(True)]

    return None
