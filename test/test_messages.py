"""Unit tests for the message construction utilities in the fantasy football bot.
This module tests the following functionalities:
- Generating trade evaluation messages between two players.
- Formatting the display of player sides in a trade.
- Constructing dynasty trade comparison messages.
Each test verifies that the output matches the expected format and content, ensuring correct message generation for
trade evaluations and comparisons.
"""

from qsleeperfantasybot.messages import construct_dynasty_trade_message, format_side


def test_format_side() -> None:
    """Tests the format_side function to ensure it correctly formats a list of player-score tuples
    into a string where each player and their score are listed on separate lines, prefixed with '  - '.
    """
    side_data = [("Player 1", 100), ("Player 2", 200)]
    expected_format = " - Player 1: 100\n - Player 2: 200"
    assert format_side(side_data) == expected_format


def test_construct_dynasty_trade_message() -> None:
    """Test the construct_dynasty_trade_message function to ensure it correctly
    formats a dynasty trade comparison message.

    This test verifies that given totals and player details for two sides of a trade, the function returns a formatted
    string
    that includes:uvlue for each side (A and B)
    - A breakdown of each player's contribution to the total
    - An indication of which side has the advantage and by how many points
    """
    total_a = 300
    details_a = [("Player 1", 100), ("Player 2", 200)]
    total_b = 250
    details_b = [("Player 3", 150), ("Player 4", 100)]
    expected_message = (
        "🔁 Dynasty Trade Comparison\n\n🅰️ Side A Total: 300\n - Player 1: 100\n - Player 2: 200\n\n🅱️ "
        "Side B Total: 250\n - Player 3: 150\n - Player 4: 100\n\n➡️ **Advantage:** Side A by 50 points"
    )
    assert construct_dynasty_trade_message(total_a, details_a, total_b, details_b) == expected_message
