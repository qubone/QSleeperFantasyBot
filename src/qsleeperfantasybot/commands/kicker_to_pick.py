"""Convert Sleeper kicker picks to rookie picks via league ID.

This registers a slash command `/kickertopick` that accepts a `league_id` and
optional `draft_id`, `teams`, and `name`. It uses the Sleeper API to fetch
players, users, and draft picks and returns a formatted summary of kicker
picks converted to rookie picks.
"""

from __future__ import annotations

from typing import Optional

from discord import Interaction
from discord.ext.commands import Bot
from discord import app_commands


from qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker import run_kicker_scan

def setup(bot: Bot) -> None:
    """Register the kicker_to_pick slash command onto the bot."""

    @bot.tree.command(name="kickertopick", description="Convert kicker picks to rookie picks by league ID")
    @app_commands.describe(
        league_id="Sleeper league ID",
        draft_id="Draft ID (optional)",
        teams="Number of teams (picks per round)",
         name="Custom league name"
    )
    async def kickertopick(
        interaction: Interaction,
        league_id: str,
        draft_id: Optional[str] = None,
        teams: int = 12,
        name: Optional[str] = None
        ) -> None:
        """Slash command handler for kicker->rookie pick conversion."""
        await interaction.response.defer(ephemeral=True)

        result = run_kicker_scan(league_id, draft_id, name or "Sleeper League", teams)
        # Send result as followup (we deferred earlier)
        if result:
            await interaction.followup.send(result, ephemeral=True)
