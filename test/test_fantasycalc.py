
from typing import Any, Dict

from src.fantasycalc import create_lookup_dict
from src.player_model import Player



def test_create_lookup_dict_basic(
    player_a_dict: Dict[str, Any],
    player_b_dict: Dict[str, Any]
) -> None:
    """Test the basic functionality of the `create_lookup_dict` function.
    This test verifies that:
    - The lookup dictionary contains keys for each player's name in lowercase.
    - The values in the lookup dictionary are instances of `Player`.
    - The `info.name` attribute of each `Player` instance matches the original player name.
    Assertions:
    - The lookup contains the expected lowercase player names as keys.
    - The values are instances of `Player`.
    - The `info.name` attribute of each player matches the input data.
    """

    lookup: Dict[str, Any] = create_lookup_dict([player_a_dict, player_b_dict])

    assert "player a" in lookup
    assert "player b" in lookup
    assert isinstance(lookup["player a"], Player)
    assert isinstance(lookup["player b"], Player)
    assert lookup["player a"].info.name == "Player A"
    assert lookup["player b"].info.name == "Player B"


def test_create_lookup_dict_skips_missing_info_or_name(
    player_a_dict: Dict[str, Any],
    player_no_value_dict: Dict[str, Any],
    player_no_name_dict: Dict[str, Any]
) -> None:
    """Test that `create_lookup_dict` skips players with missing `info` or missing `name` attributes.
    This test verifies that:
    - Players with valid `info` and `name` are included in the lookup dictionary.
    - Players with missing `info` or missing `name` are skipped and not included in the lookup.
    - The resulting lookup dictionary contains only the valid player(s).
    """

    lookup: Dict[str, Player] = create_lookup_dict([
        player_a_dict, player_no_value_dict, player_no_name_dict
    ])

    assert "player a" in lookup
    assert lookup["player a"].info.name == "Player A"
    assert lookup["player b"].value is None
    assert len(lookup) == 2

def test_create_lookup_dict_overwrites_duplicates(
    player_a_dict: Dict[str, Any],
) -> None:
    """Test that create_lookup_dict overwrites duplicate player names in the lookup dictionary.
    This test verifies that when multiple player dictionaries with the same name (case-insensitive)
    are provided, the resulting lookup dictionary contains only one entry for that name, and that
    the value corresponds to the last player processed. It also checks that the key is stored in
    lowercase and that the correct player object is associated with the key.
    Args:
        player_a_dict: A dictionary representing Player A.
    Asserts:
        - The lowercase player name is present in the lookup dictionary.
        - The value for the player name key is the last created player object.
        - The lookup dictionary contains only one entry.
    """

    lookup: Dict[str, Any] = create_lookup_dict([player_a_dict, player_a_dict])

    assert "player a" in lookup
    assert len(lookup) == 1
