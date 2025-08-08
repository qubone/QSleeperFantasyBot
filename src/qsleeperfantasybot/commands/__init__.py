"""This module initializes the command setup for the QSleeper Fantasy Bot."""

from discord.ext import commands

__all__ = ["dynasty_trade", "help"]


def setup_commands(bot: commands.Bot) -> None:
    """Setup all commands for the bot.
    Args:
        bot (commands.Bot): The Discord bot instance.
    """
    from . import dynasty_trade, help  # Add future command modules here

    dynasty_trade.setup(bot)
    help.setup(bot)
