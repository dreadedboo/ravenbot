import twitchio
from twitchio.ext import commands

from utilities.CoreUtils import (
    openfile,
    parse_commands,
    concat_string_from_args,
    append_file,
    remove_from_file,
    logger)

LOGGER = logger("twitch-bot: CustomCommands")

class CustomCommands(commands.Component):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.list_of_cmds = []
        self.file = "resources/twitch_cmds.json"
        self.update_commands()

    def update_commands(self) -> None:
        self.list_of_cmds.clear()
        for c in openfile(self.file):
            self.list_of_cmds.append(c["Name"])
            for a in c["Aliases"]:
                self.list_of_cmds.append(a)
        LOGGER.info(f"Loaded commands from {self.file}: {self.list_of_cmds}")

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
                            c = parse_commands(command_name, openfile(self.file))
                            if c is not None:
                                data = openfile(self.file)
                                match func:
                                    case func if func == "del":
                                        for a in data:
                                            if a["Name"] == c["Name"]:
                                                remove_from_file(self.file, a)
                                                self.update_commands()
                                                await ctx.send(f"Successfully deleted command: {command_name}")
                                                LOGGER.info(f"Deleted {command_name} from {self.file}")
                                                return
                                        await ctx.send(f"Failed to delete {command_name}, try again")
                                        LOGGER.warning(f"Failed to delete {command_name} from {self.file}")
                                    case func if func == "edit":
                                        if result:
                                            response: str = concat_string_from_args(result)
                                            c["Response"] = response
                                            for a in data:
                                                if a["Name"] == c["Name"]:
                                                    remove_from_file(self.file, a)
                                                    append_file(self.file, c)
                                                    self.update_commands()
                                                    await ctx.send(f"Successfully edited command: {command_name}")
                                                    LOGGER.info(f"Edited in {command_name} in {self.file}")
                                                    return
                                            await ctx.send(f"Failed to edit {command_name}, try again")
                                            LOGGER.warning(f"Failed to edit {command_name} in {self.file}")
                                        else:
                                            await ctx.send(f"No response for '{command_name}' provided. Failed to edit command")
                                            LOGGER.warning(f"Failed to edit {command_name} in {self.file}")
                                    case func if func == "alias":
                                        if result:
                                            if result[0] == "add":
                                                print("test")
                                            elif result[0] == "del":
                                                print("test")
                                            else:
                                                await ctx.send(f"Syntax: !commands alias <command_name> <add/del> <alias_name>")
                                    case func if func == 'cooldown':
                                        print("test")
                                    case _:
                                        if func == "add":
                                            await ctx.send(f"Command '{command_name}' already exists")
                                            LOGGER.warning(f"{command_name} already exists in {self.file}")
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
                                        append_file(self.file, new_command)
                                        self.update_commands()
                                        await ctx.send(f"Command '{command_name}' added successfully")
                                    else:
                                        await ctx.send(f"No response for '{command_name}' provided. Failed to add command")
                                        LOGGER.warning(f"Failed to add {command_name} to {self.file}")
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
                c = parse_commands(a, openfile(self.file))
                if c is not None:
                    await self.bot.get_context(payload).send(c["Response"])