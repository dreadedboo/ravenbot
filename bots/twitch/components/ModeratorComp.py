from twitchio import User
from twitchio.ext import commands

from utilities.CoreUtils import logger
from utilities.TwitchUtils import check_vip

LOGGER = logger("twitch-bot: ModComponent")


class ModComp(commands.Component):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_moderator()
    @commands.group(name="vip", invoke_fallback=True)
    async def vip_command(self, ctx: commands.Context, u: str = None) -> None:
        if u:
            user: User = await self.bot.fetch_user(login=u)
            if await check_vip(ctx, user):
                await ctx.send(f"{u} is already VIP")
            else:
                await ctx.channel.add_vip(user.id)
                await ctx.send(f"{u} has been added as a VIP")
        else:
            await ctx.send("Command syntax: !vip <uname> OR !vip remove <uname>")

    @commands.is_moderator()
    @vip_command.command(name="remove", aliases=["rem"])
    async def vip_remove(self, ctx: commands.Context, u: str = None) -> None:
        if u:
            user: User = await self.bot.fetch_user(login=u)
            if not await check_vip(ctx, user):
                await ctx.send(f"{u} is not VIP")
            else:
                await ctx.channel.remove_vip(user)
                await ctx.send(f"{u} has been removed as a VIP!")
        else:
            await ctx.send("Command syntax: !vip <uname> OR !vip remove <uname>")
