from twitchio.ext import commands
from utilities.EmoteUtils import SevenTVConnection

class EmotesComp(commands.Component):
    def __init__(self, bot):
        self.bot = bot
        self.token = bot.tokens[bot.bot_id]["token"]
        self.seven_tv = SevenTVConnection(self.token)
