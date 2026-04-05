import twitchio
import socket

from twitchio.ext import commands


class Livesplit(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.livesplit_server = None

    @commands.command(name="livesplit")
    async def connect_to_livesplit_server(self, ctx: commands.Context) -> None:
        if ctx.author.moderator or ctx.author.broadcaster:
            try:
                # Create socket and connect to LiveSplit Server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(("localhost", 16834))
                    self.livesplit_server = s
                    await ctx.send("Connected to livesplit. Available commands: !setup <game/title/all>")
            except ConnectionRefusedError:
                await ctx.send("Livesplit connection failed, server not started")
