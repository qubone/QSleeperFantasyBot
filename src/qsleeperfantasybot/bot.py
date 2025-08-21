"""Discord bot for fantasy football trade analysis.
This module implements a Discord bot that provides fantasy football trade value comparisons
and dynasty trade evaluations.
It supports slash command interface, including autocomplete for asset names.
Features:
- Fetches and caches player/asset names for autocomplete.
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
- /dynastytrade <side A> vs <side B>: Compares dynasty trade value between two sides (comma-separated assets).
  Autocomplete for asset names is available.

This file is the main entry point for the Discord bot.
It initializes the bot, sets up commands, and starts the event loop.
"""

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
GUILD_ID = int(os.getenv("TEST_GUILD_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages

class FantasyBot(commands.Bot):
    """Custom bot class for QSleeper Fantasy Bot."""
    async def setup_hook(self) -> None:
        setup_commands(self)
        await fetch_asset_names()

        # Sync commands (guild = instant, global = slow)
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info("Synced commands to guild %s", GUILD_ID)
        else:
            await self.tree.sync()
            logger.info("Synced commands globally (may take up to 1h)")

    async def on_ready(self) -> None:
        logger.info("Starting QSleeperFantasyBot version %s", __version__)
        logger.info("Logged in as %s", self.user)

if __name__ == "__main__":
    if not TOKEN:
        logger.error("DISCORD_TOKEN environment variable not set.")
        exit(1)
    bot = FantasyBot(command_prefix="!", intents=intents)
    bot.run(TOKEN)
