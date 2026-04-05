import twitchio
from twitchio.ext import commands

from utilities.CoreUtils import openfile, parse_commands, concat_string_from_args, append_file


class CustomCommands(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.list_of_cmds = []
        self.update_commands()

    def update_commands(self) -> None:
        self.list_of_cmds.clear()
        for c in openfile("resources/commands.json"):
            self.list_of_cmds.append(c["Name"])
            for a in c["Aliases"]:
                self.list_of_cmds.append(a)

    @commands.command(name="commands", invoke_fallback=True)
    async def custom_cmds(self, ctx: commands.Context, func: str = None, command_name: str = None, *result: str) -> None:
        user = ctx.author
        channel = ctx.channel
        reply: str = "Available commands: " + str(self.list_of_cmds)
        if func:
            if user.moderator or user.broadcaster:
                match func:
                    case func if func == "add":
                        if command_name:
                            if result:
                                response: str = concat_string_from_args(result)
                                new_command: dict = {
                                    "Name": command_name,
                                    "Response": response,
                                    "Aliases": []
                                }
                                append_file("resources/commands.json", new_command)
                                self.update_commands()
                                await ctx.send(f"Command '{command_name}' added successfully")
                            else:
                                await ctx.send(f"No response for '{command_name}' provided. Failed to add command")
                        else:
                            await ctx.send(f"No command name provided. Syntax for adding commands is !commands add <command_name> <response>")
                    case func if func == 'help':
                        await ctx.send(f"Available options for this command: add, edit, del, alias, cooldown, help")
                    # case func if func == 'edit':
                    #     return
                    # case func if func == 'del':
                    #     return
                    # case func if func == 'alias':
                    #     return
                    # case func if func == 'cooldown' or 'cdown':
                    #     return
                    case _:
                        await ctx.send(f"correct syntax: !commands <add/edit/del/alias/cooldown> <command_name> <response>")
            else:
                await ctx.send(reply)
        else:
            await ctx.send(reply)

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        for a in self.list_of_cmds:
            if payload.text == '!'+a:
                await self.bot.get_context(payload).send(str(parse_commands(a, openfile("resources/commands.json"))))