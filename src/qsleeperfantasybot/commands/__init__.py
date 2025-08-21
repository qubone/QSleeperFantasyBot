"""This module initializes the command setup for the QSleeper Fantasy Bot.
It imports and sets up all command modules, allowing the bot to handle various commands
like dynasty trade comparisons and help requests."""

from discord.ext.commands import Bot
__all__ = ["dynasty_trade", "help"]


def setup_commands(bot: Bot) -> None:
    """Setup all commands for the bot.
    Args:
        bot (commands.Bot): The Discord bot instance.
    """
    from . import dynasty_trade, help  # Add future command modules here

    dynasty_trade.setup(bot)
    help.setup(bot)
