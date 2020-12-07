import asyncio
import logging
from random import choice
from typing import Optional

from discord.errors import Forbidden, NotFound
from discord.ext import commands

import emojis
from constants import bot, TOKEN, BOT_STATUS_ID, STARTUP_MSGS, SHUTDOWN_MSGS

logging.basicConfig(level=logging.WARNING)


@bot.event
async def on_ready():
    print(f"Coggers activated. {bot.user} starting...")
    await bot.get_channel(BOT_STATUS_ID).send(choice(STARTUP_MSGS))


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await asyncio.gather(
        ctx.send("Coggers deactivated. Shutting down..."),
        bot.get_channel(BOT_STATUS_ID).send(choice(SHUTDOWN_MSGS))
    )
    await bot.logout()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.CommandNotFound, NotFound)):
        return
    raise error from None


@bot.command()
async def ping(ctx):
    await ctx.send("ping pong ding dong bing bong")


@bot.command(name="r")
async def repeat(ctx, *, text: Optional[str]):
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


if __name__ == "__main__":
    bot.run(TOKEN)
