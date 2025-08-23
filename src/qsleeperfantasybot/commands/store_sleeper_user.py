"""This file is part of QSleeperFantasyBot, a Discord bot for fantasy football.
It handles the storage and retrieval of Sleeper usernames for Discord users.
It provides commands to set and get the Sleeper name associated with a Discord user.
"""

from discord import Interaction, app_commands
import json
from discord.ext.commands import Bot
from typing import Dict, Optional
from pathlib import Path
from qsleeperfantasybot.logger import logger


class SleeperUserStore:
    """Handles storing and retrieving Sleeper usernames for Discord users."""

    def __init__(self, path: Path = Path("sleeper_data/user_data_local.json")) -> None:
        """Initialize the store with the given file path."""
        self.path = path
        self._data: Dict[str, str] = self._load()

    def _load(self) -> Dict[str, str]:
        """Load the user data from the JSON file."""
        if self.path.exists():
            with self.path.open("r") as f:
                return dict(json.load(f))
        logger.info("No existing user data file found. Starting fresh.")
        return {}

    def _save(self) -> None:
        """Save the user data to the JSON file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w") as f:
            json.dump(self._data, f, indent=4)

    def set_username(self, discord_id: int, sleeper_username: str) -> None:
        """Set the Sleeper username for a given Discord ID."""
        self._data[str(discord_id)] = sleeper_username
        self._save()

    def get_username(self, discord_id: int) -> Optional[str]:
        """Get the Sleeper username for a given Discord ID."""
        return self._data.get(str(discord_id))


sleeper_user_handler = SleeperUserStore()


def setup(bot: Bot) -> None:
    """Setup the help command for the bot."""

    @bot.tree.command(name="setusername", description="Set your Sleeper username")
    @app_commands.describe(sleeper_username="Your Sleeper account user name")
    async def setusername(interaction: Interaction, sleeper_username: str) -> None:
        """Set your Sleeper username using slash command."""
        sleeper_user_handler.set_username(interaction.user.id, sleeper_username)
        await interaction.response.send_message(
            f"✅ Sleeper username `{sleeper_username}` linked to QSleeperFantasyBot",
            ephemeral=True,
        )

    @bot.tree.command(name="getusername", description="Get your linked Sleeper username")
    async def getusername(interaction: Interaction) -> None:
        """Get your Sleeper username using slash command."""
        sleeper_username = sleeper_user_handler.get_username(interaction.user.id)
        if sleeper_username:
            await interaction.response.send_message(
                f"Your linked Sleeper username is `{sleeper_username}`", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "You have not set your Sleeper username yet. Use `/setusername` to set it.",
                ephemeral=True,
            )
