from ...objects import User


def create_move_check(ctx, user: User, available_moves):
    def check(m):
        return (
            user.id == str(m.author.id)
            and m.channel == ctx.channel
            and (m.content in available_moves or m.content == "resign")
        )

    return check
