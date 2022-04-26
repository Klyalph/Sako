import nextcord


def parse_user(instance, ctx, contender: str) -> nextcord.Member:
    if user := (ctx.message.mentions or [None])[0]:
        # Checks if the user is a bot
        if user.bot:
            return None
        return user

    members = []
    for member in ctx.message.author.guild.members:
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
    # TODO: add priority to those who have chatted in the guild last 24 hours.
