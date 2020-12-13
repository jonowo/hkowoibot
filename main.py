import asyncio
import logging
import random

from discord import Game, ActivityType
from discord.errors import NotFound
from discord.ext import commands

from constants import bot, TOKEN, BOT_STATUS_ID, STARTUP_MSGS
from emojis import Emoji
from misc import Miscellaneous
from scheduled_tasks import ScheduledTasks

logging.basicConfig(level=logging.WARNING)


@bot.event
async def on_ready() -> None:
    print(f"Coggers activated. {bot.user} starting...")
    await asyncio.gather(
        bot.change_presence(activity=Game(name="your mom")),
        bot.get_channel(BOT_STATUS_ID).send(random.choice(STARTUP_MSGS))
    )


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception) -> None:
    if isinstance(error, (commands.CommandNotFound, commands.NotOwner)):
        return
    if isinstance(error, commands.CommandInvokeError) and "NotFound" in str(error):
        return
    raise error from None


def main():
    bot.add_cog(Miscellaneous())
    bot.add_cog(Emoji())
    bot.add_cog(ScheduledTasks())
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
