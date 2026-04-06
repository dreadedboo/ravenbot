from twitchio.ext import commands

from utilities.LivesplitUtils import LivesplitConnection
from utilities.CoreUtils import logger
from utilities.TwitchUtils import change_game, change_title

LOGGER = logger("twitch-bot: Livesplit")

class Livesplit(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.sckt = LivesplitConnection()

    @commands.group(name="livesplit", aliases=["lsplit"])
    async def livesplit(self, ctx: commands.Context, func: str = None) -> None:
        if self.sckt.get_string("ping") == "pong":
            await ctx.send("Currently connected to livesplit. Available commands: !pb !bpt !sob")
        else:
            await ctx.send("Could not connect to livesplit")
            LOGGER.info("Could not connect to livesplit")

    @commands.is_moderator()
    @livesplit.command(name="game")
    async def set_game_from_splits(self, ctx: commands.Context) -> None:
        game_name = self.sckt.get_string("getgamename")
        if game_name is not False:
            await change_game(self.bot, ctx, str(game_name))
        else:
            await ctx.send("Failed to receive data from Livesplit")
            LOGGER.error("Failed to receive data from Livesplit")

    @commands.is_moderator()
    @livesplit.command(name="title")
    async def set_title_from_category(self, ctx: commands.Context) -> None:
        game_name = self.sckt.get_string("getgamename")
        category = self.sckt.get_string("getcategoryname")
        if game_name is not False and category is not False:
            title: str = f"{game_name} - {category}"
            await change_title(self.bot, ctx, title)
        else:
            await ctx.send("Failed to receive data from Livesplit")
            LOGGER.error("Failed to receive data from Livesplit")

    @commands.is_moderator()
    @livesplit.command(name="setup")
    async def set_game_and_title(self, ctx: commands.Context):
        await self.set_game_from_splits(ctx)
        await self.set_title_from_category(ctx)

    @commands.command(name="pb")
    async def get_personal_best(self, ctx: commands.Context) -> None:
        reply = self.sckt.get_time("getfinaltime Personal Best")
        # this command will also get leaderboard PB from SRC
        await ctx.send(f"Splits PB: {reply}")

    @commands.command(name="bpt")
    async def get_bpt(self, ctx: commands.Context) -> None:
        reply = self.sckt.get_time("getbestpossibletime")
        await ctx.send(f"Best Possible Time: {reply}")

    @commands.command(name="sob")
    async def get_sob(self, ctx: commands.Context) -> None:
        reply = self.sckt.get_time("getfinaltime Best Segments")
        await ctx.send(f"Sum of Best: {reply}")

