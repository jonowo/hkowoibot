import asyncio
import random
from typing import Optional, List  # List instead of list for Python 3.8 compatibility

import discord
from discord.ext import commands

from constants import bot, HKOI_SERVER_ID, EMOTE_LOGS_ID, USER_TO_EMOJI


def sep_emojis(emoji: str, cnt: int) -> List[str]:
    """Bypass Discord message limit by separating emoijs into muliple messges."""
    emoji = str(emoji)
    per_msg = 2000 // len(emoji)
    sep_msgs = []
    while True:
        if cnt >= per_msg:
            sep_msgs.append(emoji * per_msg)
            cnt -= per_msg
            if cnt == 0:
                break
        else:
            sep_msgs.append(emoji * cnt)
            break
    return sep_msgs


async def send_emojis(ctx: commands.Context, emoji_name: str, cnt: int) -> None:
    emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name)
    if not emoji:
        await ctx.send("no u")
        return

    # Sanitize cnt
    try:
        cnt = int(cnt)
    except:
        cnt = random.randint(1, 69)  # One message at max, prevent spam
    cnt = max(cnt, 0)  # Min: 0
    cnt = min(cnt, 420)  # Max: 420

    if cnt:
        sep_msgs = sep_emojis(emoji, cnt)
        # Note: Asynchronously sent message arrive in arbitrary order
        # We send the messages ASAP while keeping the message with the least emojis the last to arrive
        # for A E S T H E T I C S
        if sep_msgs[0] == sep_msgs[-1]:
            for msg in sep_msgs:
                asyncio.create_task(ctx.send(msg))
        else:
            async def f():
                await asyncio.gather(*[ctx.send(msg) for msg in sep_msgs[:-1]])
                await ctx.send(sep_msgs[-1])

            asyncio.create_task(f())
    else:  # cnt == 0, empty message time
        asyncio.create_task(ctx.send("\u200e"))

    # orz ITO asked this to implemented
    if ctx.guild.id == HKOI_SERVER_ID:  # HKOI server only
        asyncio.create_task(ctx.message.delete())
        asyncio.create_task(
            bot.get_channel(EMOTE_LOGS_ID).send(
                f"**{ctx.author.nick or ctx.author}** requested {emoji}×{cnt} in <#{ctx.channel.id}>"
            )
        )
        if not cnt:
            return
        # TODO: Save emoji use data in database


class Emoji(commands.Cog):
    @commands.command()
    async def ick(self, ctx: commands.Context, count: Optional[int]) -> None:
        await send_emojis(ctx, "ick", count)

    @commands.command()
    async def ito(self, ctx: commands.Context, count: Optional[int]) -> None:
        await send_emojis(ctx, "ito", count)

    @commands.command()
    async def tosi(self, ctx: commands.Context, count: Optional[int]) -> None:
        await send_emojis(ctx, "tosi", count)

    @commands.command()
    async def yeet(self, ctx: commands.Context, count: Optional[int]) -> None:
        await send_emojis(ctx, "yeet", count)

    @commands.command()
    async def ic(self, ctx: commands.Context, count: Optional[int]) -> None:
        await send_emojis(ctx, "ic", count)

    @commands.command()
    async def me(self, ctx: commands.Context, count: Optional[int]) -> None:
        if ctx.author.id in USER_TO_EMOJI:
            await send_emojis(ctx, USER_TO_EMOJI[ctx.author.id], count)
        else:
            await ctx.send("no u")

    @commands.command()
    async def leaderboard(self, ctx: commands.Context) -> None:  # for use of emojis commands in HKOI server
        pass  # TODO: Implement
