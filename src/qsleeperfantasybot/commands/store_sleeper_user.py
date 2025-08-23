"""This file is part of QSleeperFantasyBot, a Discord bot for fantasy football.
It handles the storage and retrieval of Sleeper usernames for Discord users.
It provides commands to set and get the Sleeper name associated with a Discord user.
"""

from discord import Interaction, app_commands
import json
import os
from discord.ext.commands import Bot
from typing import Dict, Optional

TOKEN = "YOUR_DISCORD_BOT_TOKEN"  # replace with your bot token
DATA_FILE = "user_data.json"


# --- Data Handling ---
def load_data() -> Dict[str, str]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return dict(json.load(f))
    return {}


def save_data() -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(user_data, f, indent=4)


def set_sleeper_username(discord_id: int, sleeper_id: str) -> None:
    user_data[str(discord_id)] = sleeper_id
    save_data()


def get_sleeper_username(discord_id: int) -> Optional[str]:
    return user_data.get(str(discord_id))


user_data = load_data()


def setup(bot: Bot) -> None:
    """Setup the help command for the bot."""

    @bot.tree.command(name="setusername", description="Set your Sleeper username")
    @app_commands.describe(sleeper_username="Your Sleeper account user name")
    async def setusername(interaction: Interaction, sleeper_username: str) -> None:
        """Set your Sleeper username using slash command."""
        set_sleeper_username(interaction.user.id, sleeper_username)
        await interaction.response.send_message(
            f"✅ Sleeper username `{sleeper_username}` linked to QSleeperFantasyBot",
            ephemeral=True,
        )

    @bot.tree.command(name="getusername", description="Get your linked Sleeper username")
    async def getusername(interaction: Interaction) -> None:
        """Get your Sleeper username using slash command."""
        sleeper_username = get_sleeper_username(interaction.user.id)
        if sleeper_username:
            await interaction.response.send_message(
                f"Your linked Sleeper username is `{sleeper_username}`", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "You have not set your Sleeper username yet. Use `/setusername` to set it.",
                ephemeral=True,
            )
