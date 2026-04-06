from twitchio.ext import commands

from utilities.LivesplitUtils import ping_livesplit_server, send_receive
from utilities.CoreUtils import logger

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

    @commands.command(name="livesplit", aliases=["lsplit"])
    async def livesplit(self, ctx: commands.Context, func: str = None) -> None:
        # only pings livesplit for now
        if ping_livesplit_server():
            # this command will eventually include the ability to set stream game to game name from livesplit for moderators
            if func:
                if ctx.author.moderator or ctx.author.broadcaster:
                    match func:
                        case func if func == "game":
                            print(send_receive("getcurrentgamename"))
                        case _:
                            await ctx.send("Currently connected to livesplit. Available commands: !pb !bpt !sob")
                else:
                    await ctx.send("Currently connected to livesplit. Available commands: !pb !bpt !sob")
            else:
                await ctx.send("Currently connected to livesplit. Available commands: !pb !bpt !sob")
        else:
            await ctx.send("Could not connect to livesplit")
            LOGGER.info("Could not connect to livesplit")

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

