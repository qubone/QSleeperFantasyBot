"""Unit tests for the message construction utilities in the fantasy football bot.
This module tests the following functionalities:
- Generating trade evaluation messages between two players.
- Formatting the display of player sides in a trade.
- Constructing dynasty trade comparison messages.
Each test verifies that the output matches the expected format and content, ensuring correct message generation for trade evaluations and comparisons.
"""
from messages import construct_trade_message, format_side, construct_dynasty_trade_message
from player_model import create_player_from_dict


def test_construct_trade_message():
    """
    Tests the construct_trade_message function to ensure it generates the correct trade evaluation message
    given two player objects with their respective values. The test checks that the output message
    matches the expected format and content, comparing the values of Player A and Player B.
    """
    player_a_dict = {
        "player": {
            "id": 5856,
            "name": "Player A",
            "mflId": "15281",
            "sleeperId": "7564",
            "position": "WR",
            "maybeBirthday": "2000-03-01",
            "maybeHeight": "72",
            "maybeWeight": 205,
            "maybeCollege": "LSU",
            "maybeTeam": "CIN",
            "maybeAge": 25.4,
            "maybeYoe": 4,
            "espnId": "4362628",
            "fleaflickerId": "16250"
        },
        "value": 10152,
        "overallRank": 1,
        "positionRank": 1,
        "trend30Day": -35,
        "redraftDynastyValueDifference": 0,
        "redraftDynastyValuePercDifference": 0,
        "redraftValue": 10152,
        "combinedValue": 20304,
        "maybeMovingStandardDeviation": -1,
        "maybeMovingStandardDeviationPerc": 0,
        "maybeMovingStandardDeviationAdjusted": 2,
        "displayTrend": False,
        "maybeOwner": None,
        "starter": False,
        "maybeTier": 1,
        "maybeAdp": None,
        "maybeTradeFrequency": None
    }

    player_b_dict = {
        "player": {
            "id": 5856,
            "name": "Player B",
            "mflId": "15281",
            "sleeperId": "7564",
            "position": "WR",
            "maybeBirthday": "2000-03-01",
            "maybeHeight": "72",
            "maybeWeight": 205,
            "maybeCollege": "LSU",
            "maybeTeam": "CIN",
            "maybeAge": 25.4,
            "maybeYoe": 4,
            "espnId": "4362628",
            "fleaflickerId": "16250"
        },
        "value": 12000,
        "overallRank": 1,
        "positionRank": 1,
        "trend30Day": -35,
        "redraftDynastyValueDifference": 0,
        "redraftDynastyValuePercDifference": 0,
        "redraftValue": 10152,
        "combinedValue": 20304,
        "maybeMovingStandardDeviation": -1,
        "maybeMovingStandardDeviationPerc": 0,
        "maybeMovingStandardDeviationAdjusted": 2,
        "displayTrend": False,
        "maybeOwner": None,
        "starter": False,
        "maybeTier": 1,
        "maybeAdp": None,
        "maybeTradeFrequency": None
    }
    player_A = create_player_from_dict(player_a_dict)
    player_B = create_player_from_dict(player_b_dict)
    expected_message = '🔄 **Trade Evaluation**\n**Player A**: 10152 pts\n**Player B**: 12000 pts\n\nPlayer A < Player B'
    assert construct_trade_message(player_A, player_B) == expected_message

def test_format_side():
    """
    Tests the format_side function to ensure it correctly formats a list of player-score tuples
    into a string where each player and their score are listed on separate lines, prefixed with '  - '.
    """
    side_data = [("Player 1", 100), ("Player 2", 200)]
    expected_format = "  - Player 1: 100\n  - Player 2: 200"
    assert format_side(side_data) == expected_format

def test_construct_dynasty_trade_message():
    """
    Test the construct_dynasty_trade_message function to ensure it correctly formats a dynasty trade comparison message.

    This test verifies that given totals and player details for two sides of a trade, the function returns a formatted string
    that includes:
    - The total value for each side (A and B)
    - A breakdown of each player's contribution to the total
    - An indication of which side has the advantage and by how many points
    """
    total_a = 300
    details_a = [("Player 1", 100), ("Player 2", 200)]
    total_b = 250
    details_b = [("Player 3", 150), ("Player 4", 100)]
    expected_message = '🔁 Dynasty Trade Comparison\n\n🅰️ Side A Total: 300\n  - Player 1: 100\n  - Player 2: 200\n\n🅱️ Side B Total: 250\n  - Player 3: 150\n  - Player 4: 100\n\n➡️ **Advantage:** Side A by 50 points'
    assert construct_dynasty_trade_message(total_a, details_a, total_b, details_b) == expected_message