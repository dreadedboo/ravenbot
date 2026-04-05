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
        for c in openfile("bots/twitch/resources/commands.json"):
            self.list_of_cmds.append(c["Name"])
            for a in c["Aliases"]:
                self.list_of_cmds.append(a)

    @commands.command(name="commands", invoke_fallback=True)
    async def custom_cmds(self, ctx: commands.Context, func: str = None, command_name: str = None, *result: str) -> None:
        self.update_commands()
        user = ctx.author
        reply: str = "Available commands: " + str(self.list_of_cmds)
        if user.moderator or user.broadcaster:
            if func:
                match func:
                    case func if func == "help":
                        await ctx.send(f"Available options for this command are add, edit, del, alias, cooldown")
                    case _:
                        if command_name:
                            if parse_commands(command_name, openfile("bots/twitch/resources/commands.json")) is not None:
                                match func:
                                    case func if func == "del":
                                        print("test")
                                    case func if func == "edit":
                                        print("test")
                                    case func if func == "alias":
                                        print("test")
                                    case func if func == 'cooldown':
                                        print("test")
                                    case _:
                                        if func == "add":
                                            await ctx.send(f"Command '{command_name}' already exists")
                                        else:
                                            await ctx.send(f"Syntax: !commands <add/edit/del/alias/cooldown> <command_name> <response>")
                            else:
                                if func == "add":
                                    if result:
                                        response: str = concat_string_from_args(result)
                                        new_command: dict = {
                                            "Name": command_name,
                                            "Response": response,
                                            "Aliases": []
                                        }
                                        append_file("bots/twitch/resources/commands.json", new_command)
                                        self.update_commands()
                                        await ctx.send(f"Command '{command_name}' added successfully")
                                    else:
                                        await ctx.send(f"No response for '{command_name}' provided. Failed to add command")
                                else:
                                    await ctx.send(f"Syntax: !commands <add/edit/del/alias/cooldown> <command_name> <response>")
                        else:
                            await ctx.send(f"No command name provided. Syntax: !commands <add/edit/del/alias/cooldown> <command_name> <response>")
            else:
                await ctx.send(reply)
        else:
            await ctx.send(reply)

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        for a in self.list_of_cmds:
            if payload.text == '!'+a:
                await self.bot.get_context(payload).send(str(parse_commands(a, openfile("bots/twitch/resources/commands.json"))))