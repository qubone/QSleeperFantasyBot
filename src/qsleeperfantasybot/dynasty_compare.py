"""This module provides functionality to compare two sides of a dynasty fantasy football trade.
It calculates the total value of assets on each side using player values from the fantasycalc module,
and returns a formatted message summarizing the trade comparison, including the total values for each side,
a breakdown of individual asset values, and which side holds the advantage.
Functions:
    dynasty_compare(side_a: List[str], side_b: List) -> str
        Asynchronously compares two lists of dynasty assets and returns a formatted trade comparison message.
"""

from typing import List, Tuple

from qsleeperfantasybot.fantasycalc import get_player_value
from qsleeperfantasybot.messages import construct_dynasty_trade_message


async def dynasty_compare(side_a: List[str], side_b: List[str]) -> str:
    """Compare two sides of a dynasty trade and return a formatted message.
    Args:
        side_a (List[str]): List of assets for side A.
        side_b (List[str]): List of assets for side B.
    Returns:
        str: Formatted message with total values and advantage.
    """

    async def total_value(assets: List[str]) -> Tuple[int, List[Tuple[str, int]]]:
        """Calculate the total value of a list of assets and return the total and details.
        Args:
            assets (List[str]): List of asset names.
        Returns:
            Tuple[int, List[Tuple[str, int]]]: Total value and a list of tuples with asset names and their values.
        """
        total = 0
        asset_details: List[Tuple[str, int]] = []
        for name in assets:
            player = await get_player_value(name, is_dynasty=True)
            if player:
                value = player.value
                total += value
                asset_details.append((player.info.name, value))
            else:
                asset_details.append((name, 0))
        return total, asset_details

    total_a, details_a = await total_value(side_a)
    total_b, details_b = await total_value(side_b)

    return construct_dynasty_trade_message(total_a, details_a, total_b, details_b)
