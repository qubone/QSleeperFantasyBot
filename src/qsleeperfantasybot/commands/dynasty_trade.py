# src/qsleeperfantasybot/commands/dynasty_trade.py
from discord import Interaction, app_commands
from discord.ext import commands
from qsleeperfantasybot.dynasty_compare import dynasty_compare
from qsleeperfantasybot.autocomplete import asset_autocomplete


def setup(bot: commands.Bot) -> None:
    @bot.tree.command(name="dynastytrade", description="Compare dynasty trade value between two sides.")
    @app_commands.describe(
        side_a="Comma-separated list of assets for side A", side_b="Comma-separated list of assets for side B"
    )
    @app_commands.autocomplete(side_a=asset_autocomplete, side_b=asset_autocomplete)
    async def compare_dynasty_trade(interaction: Interaction, side_a: str, side_b: str) -> None:
        """Compare dynasty trade value between two sides using slash command."""
        await interaction.response.defer()
        side_a_list = [s.strip() for s in side_a.split(",")]
        side_b_list = [s.strip() for s in side_b.split(",")]
        result = await dynasty_compare(side_a_list, side_b_list)
        await interaction.followup.send(result, ephemeral=True)
