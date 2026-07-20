import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")  # unused now that commands are slash commands

# Optional: a guild (server) ID to sync slash commands to instantly during
# development. Without it, commands sync globally, which can take up to an
# hour to show up everywhere.
GUILD_ID = int(os.getenv("GUILD_ID")) if os.getenv("GUILD_ID") else None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
DEVICES_FILE = os.path.join(DATA_DIR, "devices.json")
FILTERS_FILE = os.path.join(DATA_DIR, "filters.json")
LANGUAGES_FILE = os.path.join(DATA_DIR, "languages.json")

PID_POLL_INTERVAL_SECONDS = int(os.getenv("PID_POLL_INTERVAL_SECONDS", "5"))
# Per-operation timeout (TCP connect, SSH banner/auth, and gaps between reads on an open channel).
SSH_TIMEOUT_SECONDS = int(os.getenv("SSH_TIMEOUT_SECONDS", "10"))
# Hard wall-clock cap for one whole SSH call (connect + exec + read to completion),
# so a slow/stuck remote command can't leave a Discord interaction hanging forever.
SSH_TOTAL_TIMEOUT_SECONDS = int(os.getenv("SSH_TOTAL_TIMEOUT_SECONDS", "30"))
