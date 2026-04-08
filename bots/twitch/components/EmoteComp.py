# any commands or rewards that interact with FFZ, 7TV, or BTTV will go here

from twitchio.ext import commands
# from utilities.EmoteUtils import SevenTVConnection

class EmotesComp(commands.Component):
    def __init__(self, bot):
        self.bot = bot
        self.token = bot.tokens["42048430"]["token"]
        # self.seven_tv = SevenTVConnection(self.token)
