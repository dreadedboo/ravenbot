from twitchio.ext import commands
from utilities.Logger import new_logger

LOGGER = new_logger("TwitchUtils")

async def change_game(bot, ctx: commands.Context, game_name: str) -> None:
    channel = ctx.channel
    channel_info = await channel.fetch_channel_info()
    game = await bot.fetch_game(name=game_name)
    if game is not None:
        await channel.modify_channel(game_id=game.id)
        await ctx.send(f"Game successfully changed to: {game.name}")
    else:
        await ctx.send(f"Could not find: {game_name} please try again")
        await ctx.send(f"Current game is: {channel_info.game_name}")