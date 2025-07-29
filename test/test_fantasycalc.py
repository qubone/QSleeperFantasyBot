
import pytest
from unittest.mock import patch, MagicMock
from fantasycalc import create_lookup_dict
from typing import Any, Dict, List

class DummyInfo:
    def __init__(self, name: str) -> None:
        self.name: str = name

class DummyPlayer:
    def __init__(self, name: str) -> None:
        self.info: DummyInfo = DummyInfo(name)

@patch("fantasycalc.create_player_from_dict")
@patch("fantasycalc.logger")
def test_create_lookup_dict_basic(
    mock_logger: MagicMock, 
    mock_create_player_from_dict: MagicMock
) -> None:
    """Test the basic functionality of the `create_lookup_dict` function.
    This test verifies that:
    - The lookup dictionary contains keys for each player's name in lowercase.
    - The values in the lookup dictionary are instances of `DummyPlayer`.
    - The `info.name` attribute of each `DummyPlayer` instance matches the original player name.
    Mocks:
    - `mock_logger`: Mocked logger (not directly used in this test).
    - `mock_create_player_from_dict`: Mocked function to create a `DummyPlayer` from a player dictionary, with a side effect to return a `DummyPlayer` using the player's name.
    Assertions:
    - The lookup contains the expected lowercase player names as keys.
    - The values are instances of `DummyPlayer`.
    - The `info.name` attribute of each player matches the input data.
    """
    players_input: List[Dict[str, Any]] = [
        {"id": 1, "name": "Patrick Mahomes"},
        {"id": 2, "name": "Justin Jefferson"},
    ]
    def side_effect(player_dict: Dict[str, Any]) -> DummyPlayer:
        return DummyPlayer(player_dict["name"])
    mock_create_player_from_dict.side_effect = side_effect
    lookup: Dict[str, Any] = create_lookup_dict(players_input)

    assert "patrick mahomes" in lookup
    assert "justin jefferson" in lookup
    assert isinstance(lookup["patrick mahomes"], DummyPlayer)
    assert isinstance(lookup["justin jefferson"], DummyPlayer)
    assert lookup["patrick mahomes"].info.name == "Patrick Mahomes"
    assert lookup["justin jefferson"].info.name == "Justin Jefferson"

@patch("fantasycalc.create_player_from_dict")
@patch("fantasycalc.logger")
def test_create_lookup_dict_skips_missing_info_or_name(
    mock_logger: MagicMock, 
    mock_create_player_from_dict: MagicMock
) -> None:
    """Test that `create_lookup_dict` skips players with missing `info` or missing `name` attributes.
    This test verifies that:
    - Players with valid `info` and `name` are included in the lookup dictionary.
    - Players with missing `info` or missing `name` are skipped and not included in the lookup.
    - The resulting lookup dictionary contains only the valid player(s).
    Mocks:
    - `mock_logger`: Mocked logger (not used directly in this test).
    - `mock_create_player_from_dict`: Mocked function to create player objects from dictionaries, set up to return:
        1. A dummy player with a valid name.
        2. A dummy player with `info` set to `None`.
        3. A dummy player with `info.name` set to `None`.
    """
    player_dicts: List[Dict[str, Any]] = [
        {"id": 1, "name": "Player One"},
        {"id": 2, "name": "Player Two"},
        {"id": 3, "name": "Player Three"},
    ]
    dummy_with_name: DummyPlayer = DummyPlayer("Player One")
    dummy_no_info: MagicMock = MagicMock()
    dummy_no_info.info = None
    dummy_no_name: MagicMock = MagicMock()
    dummy_no_name.info = MagicMock()
    dummy_no_name.info.name = None

    mock_create_player_from_dict.side_effect = [
        dummy_with_name, dummy_no_info, dummy_no_name
    ]

    lookup: Dict[str, Any] = create_lookup_dict(player_dicts)

    assert "player one" in lookup
    assert len(lookup) == 1

@patch("fantasycalc.create_player_from_dict")
@patch("fantasycalc.logger")
def test_create_lookup_dict_overwrites_duplicates(
    mock_logger: MagicMock, 
    mock_create_player_from_dict: MagicMock
) -> None:
    """Test that create_lookup_dict overwrites duplicate player names in the lookup dictionary.
    This test verifies that when multiple player dictionaries with the same name (case-insensitive)
    are provided, the resulting lookup dictionary contains only one entry for that name, and that
    the value corresponds to the last player processed. It also checks that the key is stored in
    lowercase and that the correct player object is associated with the key.
    Args:
        mock_logger (MagicMock): Mocked logger object.
        mock_create_player_from_dict (MagicMock): Mocked function to create player objects from dicts.
    Asserts:
        - The lowercase player name is present in the lookup dictionary.
        - The value for the player name key is the last created player object.
        - The lookup dictionary contains only one entry.
    """
    player_dicts: List[Dict[str, Any]] = [
        {"id": 1, "name": "Player X"},
        {"id": 2, "name": "Player X"},
    ]
    dummy1: DummyPlayer = DummyPlayer("Player X")
    dummy2: DummyPlayer = DummyPlayer("Player X")
    mock_create_player_from_dict.side_effect = [dummy1, dummy2]

    lookup: Dict[str, Any] = create_lookup_dict(player_dicts)

    assert "player x" in lookup
    assert lookup["player x"] is dummy2
    assert len(lookup) == 1
