""" This module provides utility functions for constructing formatted trade evaluation messages
for Discord, specifically for fantasy sports scenarios. It includes functions to generate
messages comparing two players or two sides of a dynasty trade, displaying their values
and indicating which side has the advantage.
Functions:
    construct_trade_message(player_a: Player, player_b: Player) -> str:
        Constructs a formatted message comparing two players' values.
    format_side(details: List[Tuple[str, int]]) -> str:
        Formats a list of (name, value) tuples for display in a trade message.
    construct_dynasty_trade_message(
        Constructs a formatted message comparing two sides of a dynasty trade,
        including detailed breakdowns and indicating which side has the advantage.
"""
from player_model import Player
from typing import List, Tuple
def construct_trade_message(player_a: Player, player_b: Player) -> str:
    """
    Constructs a trade evaluation message for Discord.

    Args:
        player_a (Player): Model of Player A.
        player_b (Player): Model of Player B.

    Returns:
        str: Formatted trade evaluation message.
    """
    return (
        f"🔄 **Trade Evaluation**\n"
        f"**{player_a.info.name}**: {player_a.value} pts\n"
        f"**{player_b.info.name}**: {player_b.value} pts\n\n"
        f"{player_a.info.name} {'>' if player_a.value > player_b.value else '<'} {player_b.info.name}"
    )

def format_side(details):
        """
        Formats a list of (name, value) pairs into a multi-line string.

        Each pair is formatted as "  - name: value" on its own line.

        Args:
            details (Iterable[Tuple[str, Any]]): An iterable of (name, value) pairs to format.

        Returns:
            str: A string with each pair on a separate line, formatted for display.
        """
        return "\n".join([f"  - {name}: {val}" for name, val in details])

def construct_dynasty_trade_message(
    total_a: int,
    details_a: List[Tuple[str, int]],
    total_b: int,
    details_b: List[Tuple[str, int]]
) -> str:
    """Constructs a formatted message comparing two sides of a dynasty trade.

    Args:
        total_a (int): The total value for Side A.
        details_a (List[Tuple[str, int]]): A list of tuples containing player/item names and their values for Side A.
        total_b (int): The total value for Side B.
        details_b (List[Tuple[str, int]]): A list of tuples containing player/item names and their values for Side B.

    Returns:
        str: A formatted string summarizing the trade comparison, including totals, details for each side, and which side has the advantage.
    """
    advantage = "Side A" if total_a > total_b else "Side B"
    diff = abs(total_a - total_b)
    return (
        f"🔁 Dynasty Trade Comparison\n\n"
        f"🅰️ Side A Total: {total_a}\n{format_side(details_a)}\n\n"
        f"🅱️ Side B Total: {total_b}\n{format_side(details_b)}\n\n"
        f"➡️ **Advantage:** {advantage} by {diff} points"
    )