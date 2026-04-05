from datetime import datetime

from twitchio import Game, User
from twitchio.ext import commands


def concat_string_from_args(t: tuple) -> str:
    s = ""
    c = 0
    for a in t:
        if c == len(t) - 1:
            s += a
        else:
            c += 1
            s += (a + " ")
    return s


class CoreComp(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="game", aliases=["setgame"])
    async def game_command(self, ctx: commands.Context, *g: str) -> None:
        user = ctx.author
        channel = ctx.channel
        channel_info = await channel.fetch_channel_info()
        # check if a game was provided
        if g:
            # check if user is moderator
            if user.moderator or user.broadcaster:
                game_name = concat_string_from_args(g)
                game: Game = await self.bot.fetch_game(name=game_name)
                if game is not None:
                    await channel.modify_channel(game_id=game.id)
                    await ctx.send(f"Game successfully changed to: {game.name}")
                else:
                    await ctx.send(f"Could not find: {game_name} please try again")
                    await ctx.send(f"Current game is: {channel_info.game_name}")
            else:
                await ctx.send(f"Current game is: {channel_info.game_name}")
        else:
            await ctx.send(f"Current game is: {channel_info.game_name}")

    @commands.command(name="title", aliases=["settitle"])
    async def title_command(self, ctx: commands.Context, *t: str) -> None:
        user = ctx.author
        channel = ctx.channel
        channel_info = await channel.fetch_channel_info()
        # check if a title was provided
        if t:
            # check if user is moderator
            if user.moderator or user.broadcaster:
                title = concat_string_from_args(t)
                await channel.modify_channel(title=title)
                await ctx.send(f"Title successfully changed to: {title}")
            else:
                await ctx.send(f"Current title is: {channel_info.title}")
        else:
            await ctx.send(f"Current title is: {channel_info.title}")

    @commands.command(name="followage")
    async def followage(self, ctx: commands.Context, u: User = None) -> None:
        user = u or ctx.author
        follow_data = await ctx.channel.fetch_followers()
        async for f in follow_data.followers:
            if f.user == user:
                followed = f.followed_at.replace(tzinfo=None)
                delta = datetime.now().replace(tzinfo=None) - followed
                years, days = divmod(delta.days, 365)
                months, days = divmod(days, 30)
                await ctx.send(f"@{user} has been following for {years} years, {months} months, and {days} days!")
                return
        await ctx.send(f"@{user} is not following this channel!")
