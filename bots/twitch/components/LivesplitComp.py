from twitchio.ext import commands

from utilities.LivesplitUtils import ping_livesplit_server, send_receive
from utilities.CoreUtils import logger
from utilities.TwitchUtils import change_game, change_title

LOGGER = logger("twitch-bot: Livesplit")

# a lot of the possible commands for livesplit just return a time
# any commands that return a time in this component will just call this function
async def get_time_from_livesplit(ctx: commands.Context, command: str, message: str):
    if ping_livesplit_server():
        time = send_receive(command)
        if time:
            await ctx.send(f"{message}{time[:11]}")
    else:
        await ctx.send("Could not connect to livesplit")


class Livesplit(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot
        ping_livesplit_server()

    @commands.group(name="livesplit", aliases=["lsplit"])
    async def livesplit(self, ctx: commands.Context, func: str = None) -> None:
        if ping_livesplit_server():
            await ctx.send("Currently connected to livesplit. Available commands: !pb !bpt !sob")
        else:
            await ctx.send("Could not connect to livesplit")
            LOGGER.info("Could not connect to livesplit")

    @commands.is_moderator()
    @livesplit.command(name="game")
    async def set_game_from_splits(self, ctx: commands.Context) -> None:
        game_name = send_receive("getgamename")
        if game_name is not False:
            await change_game(self.bot, ctx, game_name[:-1])
        else:
            await ctx.send("Failed to receive data from Livesplit")
            LOGGER.error("Failed to receive data from Livesplit")

    @commands.is_moderator()
    @livesplit.command(name="title")
    async def set_title_from_category(self, ctx: commands.Context) -> None:
        game_name = send_receive("getgamename")
        category = send_receive("getcategoryname")
        if game_name is not False and category is not False:
            title: str = f"{game_name[:-1]} - {category[:-1]}"
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
        await get_time_from_livesplit(ctx, "getfinaltime Personal Best","Current splits PB: ")
        # this command will also get leaderboard PB from SRC once livesplit server can return game name to have command also search SRC runs

    @commands.command(name="bpt")
    async def get_bpt(self, ctx: commands.Context) -> None:
        await get_time_from_livesplit(ctx, "getbestpossibletime", "Best Possible Time: ")

    @commands.command(name="sob")
    async def get_sob(self, ctx: commands.Context) -> None:
        await get_time_from_livesplit(ctx, "getfinaltime Best Segments", "Sum of Best: ")

