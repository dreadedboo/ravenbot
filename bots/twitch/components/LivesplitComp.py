from twitchio.ext import commands

from utilities.LivesplitUtils import LivesplitConnection
from utilities.CoreUtils import logger
from utilities.SRCUtils import get_pb
from utilities.TwitchUtils import change_game, change_title, get_game

LOGGER = logger("twitch-bot: Livesplit")


class Livesplit(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.livesplit = LivesplitConnection()
        self.retry_count = 0

    @commands.group(name="livesplit", aliases=["lsplit"], invoke_fallback=True)
    async def lsplit(self, ctx: commands.Context) -> None:
        if self.livesplit.get_string("ping") == "pong":
            await ctx.send("Currently connected to livesplit. Available commands: !pb !bpt !sob")
        else:
            if self.retry_count < 3:
                self.livesplit.close()
                self.retry_count += 1
                self.livesplit = LivesplitConnection()
                await self.lsplit(ctx)
            else:
                await ctx.send("Could not connect to livesplit")
                self.livesplit.close()
                LOGGER.info("Could not connect to livesplit")
                self.retry_count = 0

    @commands.is_moderator()
    @lsplit.command(name="game")
    async def set_game_from_splits(self, ctx: commands.Context) -> None:
        game_name = self.livesplit.get_string("getgamename")
        if game_name != "":
            await change_game(self.bot, ctx, str(game_name))
        else:
            await ctx.send("Failed to receive data from Livesplit")
            LOGGER.error("Failed to receive data from Livesplit")

    @commands.is_moderator()
    @lsplit.command(name="title")
    async def set_title_from_category(self, ctx: commands.Context) -> None:
        game_name = self.livesplit.get_string("getgamename")
        category = self.livesplit.get_string("getcategoryname")
        if game_name != "" and category != "":
            title: str = f"{game_name} - {category}"
            await change_title(self.bot, ctx, title)
        else:
            await ctx.send("Failed to receive data from Livesplit")
            LOGGER.error("Failed to receive data from Livesplit")

    @commands.is_moderator()
    @lsplit.command(name="setup")
    async def set_game_and_title(self, ctx: commands.Context):
        await self.set_game_from_splits(ctx)
        await self.set_title_from_category(ctx)

    @commands.command(name="pb")
    async def get_personal_best(self, ctx: commands.Context) -> None:
        reply = self.livesplit.get_string("getfinaltime Personal Best")
        # SRC PB check
        # game_name = self.livesplit.get_string("getgamename")
        # category = self.livesplit.get_string("getcategoryname")
        #
        # if game_name != "" and category != "":
        #     get_pb(game_name, ctx.broadcaster.name, category)
        # else:
        #     LOGGER.error("Failed to receive data from Livesplit")
        #     game_name = await get_game(ctx)
        #     get_pb(game_name, ctx.broadcaster.name)

        if reply != "":
            await ctx.send(f"Splits PB: {reply[:-8]}")
        else:
            await ctx.send("Failed to receive data from Livesplit")
            LOGGER.error("Failed to receive data from Livesplit")


    @commands.command(name="bpt")
    async def get_bpt(self, ctx: commands.Context) -> None:
        reply = self.livesplit.get_string("getbestpossibletime")
        if reply != "":
            await ctx.send(f"Best Possible Time: {reply[:-8]}")
        else:
            await ctx.send("Failed to receive data from Livesplit")
            LOGGER.error("Failed to receive data from Livesplit")

    @commands.command(name="sob")
    async def get_sob(self, ctx: commands.Context) -> None:
        reply = self.livesplit.get_string("getfinaltime Best Segments")
        if reply != "":
            await ctx.send(f"Sum of Best: {reply[:-8]}")
        else:
            await ctx.send("Failed to receive data from Livesplit")
            LOGGER.error("Failed to receive data from Livesplit")
