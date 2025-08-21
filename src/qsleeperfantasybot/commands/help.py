"""This file is part of QSleeperFantasyBot, a Discord bot for fantasy football.
It provides commands for comparing dynasty trades and fetching help information."""
from discord import Interaction
from discord.ext.commands import Bot

from qsleeperfantasybot.version import __version__

def setup(bot: Bot) -> None:
    """Setup the help command for the bot.
    """
    @bot.tree.command(name="help", description="Show help for all bot commands.")
    async def help_command(interaction: Interaction) -> None:
        """Display help information for the bot commands and features.
        """
        help_text = (
            "**Available Commands:**\n"
            "• `/dynastytrade` — Compare dynasty trade value between two sides.\n"
            "   - Example: `side_a = Tyreek Hill`, `side_b = Bijan Robinson`\n"
            "• `/help` — Show this message.\n\n"
            "For autocomplete, just start typing a name — it will suggest matching players or assets."
        )
        await interaction.response.send_message(help_text, ephemeral=True)

    @bot.tree.command(name="version", description="Show bot version.")
    async def version(interaction: Interaction) -> None:
        """Display the current version of the bot.
        """
        await interaction.response.send_message(f"**QSleeperFantasyBot v{__version__}**", ephemeral=True)
