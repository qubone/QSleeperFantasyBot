"""Data models for Sleeper league information."""

from dataclasses import dataclass
from typing import Any, Optional, Dict, Self
from enum import Enum


@dataclass
class ScoringSettings:
    """Handling of scoring settings from Sleeper API."""

    rec_yd: float
    fum: float
    rush_yd: float
    pass_td: float
    rec_td_50p: float
    pass_yd: float
    rush_2pt: float
    pass_td_50p: float
    fum_lost: float
    rec: float
    rec_2pt: float
    rush_td: float
    rec_td: float
    pass_2pt: float


class LeagueType(Enum):
    """Handling of league type from Sleeper API."""

    REDRAFT = 0
    KEEPER = 1
    DYNASTY = 2


@dataclass
class Settings:
    """Handling of league settings from Sleeper API."""

    type: LeagueType
    num_teams: int
    best_ball: int

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> Self:
        """
        Creates a Settings instance from a dictionary.

        Args:
            data (Dict[str, int]): A dictionary containing the settings data with keys
            "type", "num_teams", and "best_ball".

        Returns:
            Settings: An instance of the Settings class initialized with the provided data.

        Raises:
            KeyError: If any of the required keys are missing in the data dictionary.
            ValueError: If the value for "type" cannot be converted to a LeagueType.
        """
        return cls(
            type=LeagueType(data["type"]),
            num_teams=data["num_teams"],
            best_ball=data["best_ball"],
        )


@dataclass
class League:
    """
    Represents a fantasy football league with associated metadata and settings.

    Attributes:
        total_rosters (int): Total number of rosters in the league.
        loser_bracket_id (int): ID of the loser bracket, if applicable.
        roster_positions (List[str]): List of roster positions in the league.
        bracket_id (int): ID of the bracket, if applicable.
        previous_league_id (Optional[Any]): Previous league ID, if applicable.
        league_id (str): Unique identifier for the league.
        draft_id (str): Unique identifier for the draft associated with the league.
        season_type (str): Type of season (e.g., "regular").
        season (str): Season year as a string.
        status (str): Current status of the league (e.g., "complete").
        name (str): Name of the league.
    """

    total_rosters: int
    loser_bracket_id: int
    roster_positions: list[str]
    bracket_id: int
    previous_league_id: Optional[Any]
    league_id: str
    draft_id: str
    season_type: str
    season: str
    settings: Settings
    status: str
    name: str


def create_league_from_dict(data: Dict[str, Any]) -> League:
    """
    Creates a League instance from a dictionary, parsing nested league information and mapping dictionary fields to
    dataclass attributes.

    Args:
        data (Dict[str, Any]): A dictionary containing league data.
    Returns:
        League: An instance of the League dataclass populated with data from the input dictionary.
    """
    league_settings = Settings.from_dict(data["settings"])
    league_fields = {field for field in League.__dataclass_fields__ if field != "settings"}
    league_kwargs = {k: v for k, v in data.items() if k in league_fields}
    return League(settings=league_settings, **league_kwargs)
