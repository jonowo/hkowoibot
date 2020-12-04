import asyncio
import logging
import os
import traceback
from random import randint
from typing import Optional

import discord.utils
from discord.errors import Forbidden
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")

HKOI_SERVER_ID = 761629421966065686
CONTEST_NOTIF_ID = 782946468289576990
SPAM_ID = 772437968538435594
BOT_STATUS_ID = 784303031319134229
EMOTE_LOGS_ID = 784254643185909790


@bot.event
async def on_ready():
    print(f"Coggers activated. {bot.user} starting...")
    await bot.get_channel(BOT_STATUS_ID).send("Coggers initiated. Starting...")


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await asyncio.gather(
        ctx.send("Coggers deactivated. Shutting down..."),
        bot.get_channel(BOT_STATUS_ID).send("Coggers deactivated. Shutting down...")
    )
    await ctx.bot.logout()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error from None


@bot.command()
async def ping(ctx):
    await ctx.send("ping pong ding dong bing bong")


def sep_emojis(emoji, cnt):
    """Bypass Discord message limit by separating emoijs into muliple messges."""
    emoji = str(emoji)
    per_msg = 2000 // len(emoji)
    sep_msgs = []
    while True:
        if cnt >= per_msg:
            sep_msgs.append(emoji * per_msg)
            cnt -= per_msg
        else:
            sep_msgs.append(emoji * cnt)
            break
    return sep_msgs


async def send_emojis(ctx, emoji_name, cnt):
    emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name)
    if not emoji:
        await ctx.send("no")
        return

    # Sanitize cnt
    try:
        cnt = int(cnt)
        if cnt <= 0:     # Min: 1
            raise ValueError
    except:
        cnt = randint(1, 420)
    cnt = min(cnt, 420)  # Max: 420

    sep_msgs = sep_emojis(emoji, cnt)
    # Note: Asynchronously sent message arrive in arbitrary order
    # We send the messages ASAP while keeping the message with the least emojis the last to arrive for A E S T H E T I C S
    if sep_msgs[0] == sep_msgs[-1]:
        await asyncio.gather(*[ctx.send(msg) for msg in sep_msgs])
    else:
        await asyncio.gather(*[ctx.send(msg) for msg in sep_msgs[:-1]])
        await ctx.send(sep_msgs[-1])

    # orz ITO asked this to implemented
    if ctx.guild.id == HKOI_SERVER_ID:  # HKOI server only
        await ctx.message.delete()
        await bot.get_channel(EMOTE_LOGS_ID).send(f"**{ctx.author.nick}** requested {emoji}×{cnt} in <#{ctx.channel.id}>")



@bot.command()
async def ick(ctx, cnt: Optional[int]):
    await send_emojis(ctx, "ick", cnt)


@bot.command()
async def ito(ctx, cnt: Optional[int]):
    await send_emojis(ctx, "ito", cnt)


@bot.command()
async def emote_leaderboard(ctx):
    pass  # TODO: Implement


@bot.command(name="r")
async def repeat(ctx, *, text: Optional[str]):
    if ctx.author == bot.user:  # No recursion
        return
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


bot.run(TOKEN)
