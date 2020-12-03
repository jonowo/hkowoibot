import asyncio
import logging
import os
import traceback
from typing import Optional

import discord.utils
from discord.errors import Forbidden
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")

CONTEST_NOTIF = bot.get_channel(782946468289576990)
SPAM = bot.get_channel(772437968538435594)


@bot.event
async def on_ready():
    print(f"Coggers initiated. {bot.user} starting...")


@bot.command()
async def ping(ctx):
    await ctx.send("ping pong ding dong bing bong")


def sep_emojis(emoji, cnt):
    """Bypass Discord message limit by separating emoijs into muliple messges."""
    emoji = str(emoji)
    per_msg = 2000 // len(emoji)
    try:
        cnt = int(cnt)
    except:
        cnt = 1
    cnt = max(cnt, 1)    # Min: 1
    cnt = min(cnt, 420)  # Max: 420
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
    sep_msgs = sep_emojis(emoji, cnt)
    # Note: Asynchronously sent message arrive in arbitrary order
    # We send the messages ASAP while keeping the message with the least emojis the last to arrive for A E S T H E T I C S
    if sep_msgs[0] == sep_msgs[-1]:
        await asyncio.gather(*[ctx.send(msg) for msg in sep_msgs])
    else:
        await asyncio.gather(*[ctx.send(msg) for msg in sep_msgs[:-1]])
        await ctx.send(sep_msgs[-1])


@bot.command()
async def ick(ctx, cnt: Optional[int]):
    await send_emojis(ctx, "ick", cnt)


@bot.command()
async def ito(ctx, cnt: Optional[int]):
    await send_emojis(ctx, "ito", cnt)


@bot.command(name="r")
async def repeat(ctx, *, text: Optional[str]):
    if ctx.message.author == bot.user:  # No recursion
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
