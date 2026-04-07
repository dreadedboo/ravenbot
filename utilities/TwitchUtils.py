from twitchio import User
from twitchio.ext import commands
from utilities.CoreUtils import logger

LOGGER = logger("TwitchUtils")


# function for any command that needs to change the current game
async def change_game(bot, ctx: commands.Context, game_name: str) -> None:
    channel_info = await ctx.channel.fetch_channel_info()
    game = await bot.fetch_game(name=game_name)
    if game is not None:
        if channel_info.game_name != game_name:
            await ctx.channel.modify_channel(game_id=game.id)
            await ctx.send(f"Game successfully changed to: {game.name}")
            return
    else:
        await ctx.send(f"Could not find: {game_name} please try again")
    await ctx.send(f"Current game is: {channel_info.game_name}")


# function for any command that needs to change the current title
async def change_title(ctx: commands.Context, title: str) -> None:
    channel_info = await ctx.channel.fetch_channel_info()
    if title != channel_info.title:
        await ctx.channel.modify_channel(title=title)
        await ctx.send(f"Title successfully changed to: {title}")
        return
    await ctx.send(f"Current title is: {channel_info.title}")


# function to check if a user is moderator or the broadcaster for commands that do different things for mods like game and title
async def check_mod(ctx: commands.Context) -> bool:
    moderators = ctx.channel.fetch_moderators()
    async for m in moderators:
        if ctx.author.id == m.id or ctx.broadcaster.id:
            return True
    return False


# function to check if a user is vip
async def check_vip(ctx: commands.Context, user: User) -> bool:
    vips = ctx.channel.fetch_vips()
    async for v in vips:
        if user.id == v.id:
            return True
    return False
