"""This file is part of QSleeperFantasyBot, a Discord bot for fantasy football.
It provides commands for comparing dynasty trades and fetching help information.
It implements a slash command for comparing dynasty trades between two sides,
with autocomplete support for asset names.
"""

from discord import Interaction, app_commands
from discord.ext.commands import Bot
from qsleeperfantasybot.dynasty_compare import dynasty_compare
from qsleeperfantasybot.autocomplete import asset_autocomplete


def setup(bot: Bot) -> None:
    """Setup the help command for the bot."""

    @bot.tree.command(
        name="dynastytrade",
        description="Compare dynasty trade value between two sides.",
    )
    @app_commands.describe(
        side_a="Comma-separated list of assets for side A",
        side_b="Comma-separated list of assets for side B",
        ppr="PPR setting (e.g., 0, 0.5, 1). Default is 1.",
        super_flex="Whether the league is super flex. Default is True.",
        number_of_teams="Number of teams in the league. Default is 12.",
    )
    @app_commands.autocomplete(side_a=asset_autocomplete, side_b=asset_autocomplete)
    @app_commands.choices(
        ppr=[
            app_commands.Choice(name="Standard (0 PPR)", value=0.0),
            app_commands.Choice(name="Half PPR (0.5)", value=0.5),
            app_commands.Choice(name="Full PPR (1.0)", value=1.0),
        ]
    )
    async def compare_dynasty_trade(
        interaction: Interaction,
        side_a: str,
        side_b: str,
        ppr: float = 1.0,
        super_flex: bool = True,
        number_of_teams: int = 12,
    ) -> None:
        """Compare dynasty trade value between two sides using slash command."""
        await interaction.response.defer(ephemeral=True)
        side_a_list = [s.strip() for s in side_a.split(",")]
        side_b_list = [s.strip() for s in side_b.split(",")]
        result = await dynasty_compare(
            side_a_list,
            side_b_list,
            ppr,
            is_super_flex=super_flex,
            number_of_teams=number_of_teams,
        )
        await interaction.followup.send(result, ephemeral=True)
