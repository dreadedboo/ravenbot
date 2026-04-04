import json

from twitchio.ext import commands
import logging

LOGGER: logging.Logger = logging.getLogger("bot")

class CustomCommands(commands.Component):

    def __init__(self, bot: commands.AutoBot) -> None:
        self.bot = bot

    @commands.Component.listener()
    # if a command sent in chat invokes an error, check if that error is "command not found"
    async def event_command_error(self, payload):
        if str(payload.exception).find("not found") != -1:
            # if the error is command not found, check custom commands file for a match
            with open('resources/commands.json', 'r', encoding='utf-8') as f:
                cmds = json.load(f)
            ch = [" "]
            for c in cmds:
                ch[0] = '!' + c["Name"]
                for a in c["Aliases"]:
                    ch.append('!' + a)
                for k in ch:
                    # if match is found, send reply in chat and bypass error
                    if payload.context.message.text == k:
                        await payload.context.send(c["Response"])
                        return None
            # if no match throw error as normal
            LOGGER.info('no matching command in file')
        return await self.bot.event_command_error(payload)