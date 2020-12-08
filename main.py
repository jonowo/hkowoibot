import logging
from random import choice

from discord.errors import NotFound
from discord.ext import commands

from constants import bot, TOKEN, BOT_STATUS_ID, STARTUP_MSGS
from emojis import Emoji
from misc import Miscellaneous

logging.basicConfig(level=logging.WARNING)


@bot.event
async def on_ready():
    print(f"Coggers activated. {bot.user} starting...")
    await bot.get_channel(BOT_STATUS_ID).send(choice(STARTUP_MSGS))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.CommandNotFound, commands.NotOwner, NotFound)):
        return
    raise error from None


def main():
    bot.add_cog(Miscellaneous(bot))
    bot.add_cog(Emoji(bot))
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
