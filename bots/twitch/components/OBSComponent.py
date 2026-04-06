from twitchio.ext import commands

from utilities.OBSUtils import connect_to_obs
from utilities.CoreUtils import logger

LOGGER = logger("OBSComp")


class OBSComp(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.cl = connect_to_obs()

    @commands.is_moderator()
    @commands.group(name="obs")
    async def obs_main(self, ctx: commands.Context) -> None:
        try:
            self.cl.get_version()
            await ctx.send("Connected to OBS")
        except:
            x = 0
            while self.cl is False and x < 3:
                self.cl = connect_to_obs()
                x += 1
            if self.cl is False:
                await ctx.send("Failed to connect to OBS")
            else:
                await self.obs_main(ctx)
