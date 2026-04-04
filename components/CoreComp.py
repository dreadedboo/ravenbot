import twitchio
from twitchio.ext import commands

class MainComponent(commands.Component):

    def __init__(self, bot: commands.AutoBot) -> None:
        self.bot = bot

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")