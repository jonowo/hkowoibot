import asyncio
import random
from typing import Optional

from discord.errors import Forbidden
from discord.ext import commands

from constants import bot, BOT_STATUS_ID, SHUTDOWN_MSGS


class Miscellaneous(commands.Cog):
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context) -> None:
        await asyncio.gather(
            ctx.send("Coggers deactivated. Shutting down..."),
            bot.get_channel(BOT_STATUS_ID).send(random.choice(SHUTDOWN_MSGS))
        )
        await bot.logout()

    @commands.command(name="help")
    async def help_command(self, ctx: commands.Context) -> None:
        await ctx.send("You need help? You think a Discord bot can help you?")

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("ping pong ding dong bing bong")

    @commands.command(name="r")
    async def repeat(self, ctx: commands.Context, *, text: Optional[str]) -> None:
        if not text:
            await ctx.send("where text")
            return
        try:
            await asyncio.gather(
                ctx.send(text),
                ctx.message.delete()
            )
        except Forbidden:
            pass
