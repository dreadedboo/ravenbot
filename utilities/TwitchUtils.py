from twitchio.ext import commands
from utilities.CoreUtils import logger

LOGGER = logger("TwitchUtils")

# function for any command that needs to change the current game
async def change_game(bot, ctx: commands.Context, game_name: str) -> None:
    channel = ctx.channel
    channel_info = await channel.fetch_channel_info()
    if ctx.author.moderator or ctx.author.broadcaster:
        game = await bot.fetch_game(name=game_name)
        if game is not None:
            await channel.modify_channel(game_id=game.id)
            await ctx.send(f"Game successfully changed to: {game.name}")
        else:
            await ctx.send(f"Could not find: {game_name} please try again")
            await ctx.send(f"Current game is: {channel_info.game_name}")
    else:
        await ctx.send(f"Current game is: {channel_info.game_name}")

# function for any command that needs to change the current title
async def change_title(bot, ctx: commands.Context, title: str) -> None:
    channel = ctx.channel
    channel_info = await channel.fetch_channel_info()
    if ctx.author.moderator or ctx.author.broadcaster:
        await channel.modify_channel(title=title)
        await ctx.send(f"Title successfully changed to: {title}")
    else:
        await ctx.send(f"Current title is: {channel_info.title}")