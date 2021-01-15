import asyncio
import logging
import random
import time
from typing import Optional

import discord.utils
from discord import Game, Message
from discord.ext import commands

from constants import bot, TOKEN, HKOI_SERVER_ID, BOT_STATUS_ID, OWNER_ROLE_ID, STARTUP_MSGS
from emojis import Emoji
from misc import Miscellaneous
from scheduled_tasks import ScheduledTasks

random.seed(time.time())
logging.basicConfig(level=logging.WARNING)


@bot.event
async def on_ready() -> None:
    print(f"Coggers activated. {bot.user} starting...")
    await asyncio.gather(
        bot.change_presence(activity=Game(name="your mom")),
        bot.get_channel(BOT_STATUS_ID).send(random.choice(STARTUP_MSGS))
    )


@bot.listen('on_message')  # Don't use @bot.event since it overrides the default message processing
async def on_message(msg: Message) -> None:
    if msg.guild.id != HKOI_SERVER_ID or msg.author == bot.user:
        return
    for role in msg.role_mentions:
        if role.id == OWNER_ROLE_ID:
            asyncio.create_task(msg.channel.send(discord.utils.get(msg.guild.emojis, name="ito")))
            break
    if msg.content.lower().startswith("imagine "):
        asyncio.create_task(msg.channel.send("couldn't be me"))


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception) -> None:
    if isinstance(error, (commands.CommandNotFound, commands.NotOwner)):
        return
    if isinstance(error, commands.CommandInvokeError) and "NotFound" in str(error):
        return
    try:
        await ctx.send(f"An error occurred.\n```{error.__class__.__name__}: {error}```")
    except:  # Can't log the error if any exception is raised
        pass
    raise error from None


def main():
    bot.add_cog(Miscellaneous(bot))
    bot.add_cog(Emoji(bot))
    bot.add_cog(ScheduledTasks(bot))
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
