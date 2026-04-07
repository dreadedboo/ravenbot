import json

from obsws_python.error import OBSSDKError
from twitchio.ext import commands

from utilities.OBSUtils import OBSConnection
from utilities.CoreUtils import logger

LOGGER = logger("OBSComp")


class OBSComp(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.cl = OBSConnection()
        self.retry_count = 0

    @commands.is_moderator()
    @commands.group(name="obs", invoke_fallback=True)
    async def obs_main(self, ctx: commands.Context) -> None:
        try:
            self.cl.get_version()
            await ctx.send("Connected to OBS")
        except (ConnectionError or
                AttributeError or
                OBSSDKError):
            if self.retry_count < 3:
                self.retry_count += 1
                self.cl.reconnect()
                await self.obs_main(ctx)
            else:
                await ctx.send("Failed to connect to OBS")
        self.retry_count = 0
