import twitchio
from twitchio.ext import commands

from utilities.FileUtils import openfile, parse_commands


class CustomCommands(commands.Component):

    def __init__(self, bot) -> None:
        self.list_of_cmds = []
        self.bot = bot
        self.custom_commands = openfile("resources/commands.json")
        for c in self.custom_commands:
            self.list_of_cmds.append(c["Name"])
            for a in c["Aliases"]:
                self.list_of_cmds.append(a)

    # will add create_command, edit_command, delete_command,
    # and other functions to this file, for now need to add to json manually

    @commands.command(name="commands", invoke_fallback=True)
    async def custom_cmds(self, ctx: commands.Context) -> None:
        reply: str = "Available commands: " + str(self.list_of_cmds)
        await ctx.send(reply)

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        for a in self.list_of_cmds:
            if payload.text == '!'+a:
                await self.bot.get_context(payload).send(str(parse_commands(a, self.custom_commands)))