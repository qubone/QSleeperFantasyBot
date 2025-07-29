"""This module defines data models for representing fantasy football players and their associated metadata.
Classes:
    Info: Data class representing detailed player information, including IDs from various platforms, personal details, and team information.
    Player: Data class representing a fantasy football player, including their Info, value metrics, rankings, trends, and other fantasy-related attributes.
Functions:
    create_player_from_dict(data: dict) -> Player:
        Creates a Player instance from a dictionary, parsing nested player information and mapping dictionary fields to dataclass attributes.
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Info:
    """
    Data class representing player information.

    Attributes:
        id (int): Unique identifier for the player.
        name (str): Name of the player.
        mflId (Optional[str]): MyFantasyLeague player ID, if available.
        sleeperId (Optional[str]): Sleeper platform player ID, if available.
        position (str): Player's position (e.g., QB, RB, WR).
        maybeBirthday (Optional[str]): Player's birthday, if known.
        maybeHeight (Optional[str]): Player's height, if known.
        maybeWeight (Optional[int]): Player's weight, if known.
        maybeCollege (Optional[str]): College the player attended, if known.
        maybeTeam (Optional[str]): Current or last known team, if known.
        maybeAge (Optional[float]): Player's age, if known.
        maybeYoe (Optional[int]): Years of experience, if known.
        espnId (Optional[str]): ESPN player ID, if available.
        fleaflickerId (Optional[str]): Fleaflicker platform player ID, if available.
    """
    id: int
    name: str
    mflId: Optional[str]
    sleeperId: Optional[str]
    position: str
    maybeBirthday: Optional[str]
    maybeHeight: Optional[str]
    maybeWeight: Optional[int]
    maybeCollege: Optional[str]
    maybeTeam: Optional[str]
    maybeAge: Optional[float]
    maybeYoe: Optional[int]
    espnId: Optional[str]
    fleaflickerId: Optional[str]

@dataclass
class Player:
    """
    Represents a fantasy football player with associated metadata and statistics.

    Attributes:
        info (Info): The player's basic information.
        value (int): The player's current value.
        overallRank (int): The player's overall rank.
        positionRank (int): The player's rank within their position.
        trend30Day (int): The player's 30-day trend value.
        redraftDynastyValueDifference (int): Difference between redraft and dynasty values.
        redraftDynastyValuePercDifference (int): Percentage difference between redraft and dynasty values.
        redraftValue (int): The player's redraft value.
        combinedValue (int): The player's combined value metric.
        maybeMovingStandardDeviation (int): Standard deviation for movement metrics.
        maybeMovingStandardDeviationPerc (int): Percentage standard deviation for movement metrics.
        maybeMovingStandardDeviationAdjusted (int): Adjusted standard deviation for movement metrics.
        displayTrend (bool): Whether to display the player's trend.
        maybeOwner (Optional[str]): The possible owner of the player, if any.
        starter (bool): Whether the player is a starter.
        maybeTier (Optional[int]): The player's tier, if available.
        maybeAdp (Optional[int]): The player's average draft position, if available.
        maybeTradeFrequency (Optional[int]): The player's trade frequency, if available.
    """
    info: Info
    value: int
    overallRank: int
    positionRank: int
    trend30Day: int
    redraftDynastyValueDifference: int
    redraftDynastyValuePercDifference: int
    redraftValue: int
    combinedValue: int
    maybeMovingStandardDeviation: int
    maybeMovingStandardDeviationPerc: int
    maybeMovingStandardDeviationAdjusted: int
    displayTrend: bool
    maybeOwner: Optional[str]
    starter: bool
    maybeTier: Optional[int]
    maybeAdp: Optional[int]
    maybeTradeFrequency: Optional[int]

def create_player_from_dict(data: Dict[str, Any]) -> Player:
    """
    Create a Player instance from a dictionary.

    Args:
        data (dict): A dictionary with a "player" key containing Info fields, and other keys matching Player fields.

    Returns:
        Player: An instance of the Player dataclass.

    Raises:
        KeyError: If the "player" key is missing in the input dictionary.
        TypeError: If the dictionary fields do not match the expected dataclass fields.
    """
    player_info = Info(**data["player"])
    player_fields = {field for field in Player.__dataclass_fields__ if field != "player"}
    player_kwargs = {k: v for k, v in data.items() if k in player_fields}
    return Player(info=player_info, **player_kwargs)