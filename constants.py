import os

from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

HKOI_SERVER_ID = 761629421966065686
BOT_STATUS_ID = 784303031319134229
EMOTE_LOGS_ID = 784254643185909790
CONTEST_NOTIF_ID = 782946468289576990
SPAM_ID = 772437968538435594

STARTUP_MSGS = [
    "Coggers initiated. Starting..."
]

SHUTDOWN_MSGS = [
    "Coggers deactivated. Shutting down..."
]

USER_TO_EMOJI = {
    481311190539304960: "ick",
    384283816715354112: "ito",
    608649264595206185: "tosi",
    530347323973435392: "yeet",
    628523058742820884: "ic"
}

bot = Bot(command_prefix=("!", "."), help_command=None)
