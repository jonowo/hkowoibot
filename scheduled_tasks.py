from datetime import time

import discord.utils
from discord.ext import commands, tasks

from constants import bot, CONTEST_NOTIF_ID, CONTEST_NOTIF_ROLE_ID
from utils import sleep_until


class ScheduledTasks(commands.Cog):
    def __init__(self):
        self.contest_notif.start()

    @tasks.loop(hours=24)
    async def contest_notif(self):
        await bot.get_channel(CONTEST_NOTIF_ID).send(
            f"<@&{CONTEST_NOTIF_ROLE_ID}> There is a non-negative number of contests today."
        )

    @contest_notif.before_loop
    async def before_contest_notif(self):
        print("Sleeping until 8 AM for Contest Notif task.")
        target = time(hour=8)
        await sleep_until(target)
