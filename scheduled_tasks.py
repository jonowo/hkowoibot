import random
from datetime import time

from discord.ext import commands, tasks

from constants import CONTEST_NOTIF_ID, CONTEST_NOTIF_ROLE_ID, CONTEST_CNT
from utils import sleep_until


class ScheduledTasks(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.contest_notif.start()

    @tasks.loop(hours=24)
    async def contest_notif(self) -> None:
        await self.bot.get_channel(CONTEST_NOTIF_ID).send(
            f"<@&{CONTEST_NOTIF_ROLE_ID}> There {random.choice(CONTEST_CNT)} contests today."
        )

    @contest_notif.before_loop
    async def before_contest_notif(self) -> None:
        target = time(hour=8)
        await sleep_until(target)
