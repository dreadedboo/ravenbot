from datetime import datetime

from twitchio import User
from twitchio.ext import commands

from utilities.CoreUtils import concat_string_from_args, logger
from utilities.TwitchUtils import change_game, change_title

LOGGER = logger("twitch-bot: CoreComponent")

class CoreComp(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="game", aliases=["setgame"])
    async def game_command(self, ctx: commands.Context, *g: str) -> None:
        channel_info = await ctx.channel.fetch_channel_info()
        # check if a game was provided
        if g:
            if ctx.author.moderator or ctx.author.broadcaster:
                game_name = concat_string_from_args(g)
                await change_game(self.bot, ctx, game_name)
        else:
            await ctx.send(f"Current game is: {channel_info.game_name}")

    @commands.command(name="title", aliases=["settitle"])
    async def title_command(self, ctx: commands.Context, *t: str) -> None:
        channel_info = await ctx.channel.fetch_channel_info()
        # check if a title was provided
        if t:
            if ctx.author.moderator or ctx.author.broadcaster:
                title = concat_string_from_args(t)
                await change_title(self.bot, ctx, title)
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
