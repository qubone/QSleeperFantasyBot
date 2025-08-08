"""This module provides an autocomplete function for asset names in a fantasy football bot.
It fetches cached asset names and returns matches based on user input.
The autocomplete function is designed to work with Discord's application commands.
"""

from discord import app_commands, Interaction
from qsleeperfantasybot.fantasycalc import get_cached_asset_names
from qsleeperfantasybot.logger import logger
from typing import List


async def asset_autocomplete(interaction: Interaction, current: str) -> List[app_commands.Choice[str]]:
    """Autocomplete function for asset names.
    Fetches cached asset names and returns matches based on the current input."""
    asset_names = await get_cached_asset_names()
    if not asset_names:
        logger.warning("No asset names available during autocomplete.")
    parts = current.split(",")
    last_part = parts[-1].strip()
    matches = [name for name in asset_names if last_part.lower() in name.lower()][:25]

    base = ", ".join(p.strip() for p in parts[:-1] if p.strip())

    logger.debug(f"Autocomplete matches for '{current}': {matches}")
    # await interaction.response.autocomplete(
    return [
        app_commands.Choice(name=f"{base}, {match}" if base else match, value=f"{base}, {match}" if base else match)
        for match in matches
    ]  # [:25]  # Limit to 25 choices as per Discord's limit
    # )
