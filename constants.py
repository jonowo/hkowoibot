import os

from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

HKOI_SERVER_ID = 761629421966065686
BOT_STATUS_ID = 784303031319134229
EMOTE_LOGS_ID = 784254643185909790
CONTEST_NOTIF_ID = 782946468289576990
CONTEST_NOTIF_ROLE_ID = 782946347594416159

USER_TO_EMOJI = {
    481311190539304960: "ick",
    384283816715354112: "ito",
    608649264595206185: "tosi",
    530347323973435392: "yeet",
    628523058742820884: "ic",
    634946884787634179: "c8k"
}

STARTUP_MSGS = (
    "Coggers initiated. Starting...",
)

SHUTDOWN_MSGS = (
    "Coggers deactivated. Shutting down...",
)

CONTEST_CNT = (
    "is a non-negative number of",
    "is an integral number of",
    "are zero or more",
    "is an even or odd number of",
    "is less than π or more than e",
    "is a real number of",
    "is a complex number of",
    "are 69",
    "are 420",
    "are 69420",
    "is 0/0",
    "are [REDACTED]",
    "could be",
    "may or may not be",
    "is a possiblity that there are"
)

bot = Bot(command_prefix=("!", "."), case_insensitive=True, help_command=None)
