def create_move_check(ctx, available_moves):
    def check(m):
        return (
            m.author.id == ctx.author.id
            and m.channel == ctx.channel
            and (
                m.content in available_moves
                or m.content == "resign"
                or m.content == "draw"
            )
        )
    return check
