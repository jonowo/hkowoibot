import asyncio
from datetime import datetime, time, timedelta


async def sleep_until(required_time: time):
    now = datetime.now()
    target = datetime(now.year, now.month, now.day, required_time.hour, required_time.minute, required_time.second)
    if target < now:  # past required time already
        target.day += timedelta(days=1)
    seconds = (target - now).total_seconds()
    await asyncio.sleep(seconds)
