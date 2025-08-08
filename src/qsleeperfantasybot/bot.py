"""Discord bot for fantasy football trade analysis.
This module implements a Discord bot that provides fantasy football trade value comparisons
and dynasty trade evaluations.
It supports both traditional command and slash command interfaces, including autocomplete for asset names.
Features:
- Fetches and caches player/asset names for autocomplete.
- Provides trade value comparisons between two players.
- Compares dynasty trades between two sides, supporting multiple assets per side.
- Logs bot activity and warnings.
- Loads configuration from environment variables.
Dependencies:
- discord.py (with app_commands and commands extensions)
- dotenv for environment variable management
- Custom modules: fantasycalc, dynasty_compare, messages, logger
Environment Variables:
- DISCORD_TOKEN: Discord bot token
Commands:
- !trade <player1> vs <player2>: Compares two players' trade values.
- !dynastytrade <side A> vs <side B>: Compares dynasty trade value between two sides (comma-separated assets).
- /dynastytrade: Slash command version with autocomplete for asset names.
"""

# This is the entry point, can be renamed to discord_client.py

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from qsleeperfantasybot.fantasycalc import fetch_asset_names
from qsleeperfantasybot.logger import logger
from qsleeperfantasybot.commands import setup_commands
from qsleeperfantasybot import __version__

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    logger.info(f"Starting QSleeperFantasyBot version {__version__}")
    setup_commands(bot)
    await fetch_asset_names()
    await bot.tree.sync()
    logger.info(f"Logged in as {bot.user}")


if __name__ == "__main__":
    if not TOKEN:
        logger.error("DISCORD_TOKEN environment variable not set.")
        exit(1)
    bot.run(TOKEN)
# bot.run(str(TOKEN))
