import aiohttp
import time
from typing import Dict, Any, List
from player_model import create_player_from_dict, Player
from logger import logger

BASE_URL = "https://api.fantasycalc.com/values/current"


def create_lookup_dict(players: List[Dict[str, Any]]) -> Dict[str, Player]:
    """
    Creates a lookup dictionary from a list of player dictionaries.
    The keys are normalized player names (lowercase) and the values are Player objects.
    """
    logger.debug("Building player lookup dictionary")
    start_time = time.perf_counter()
    player_lookup: Dict[str, Player] = {}
    for player_dict in players:
        player = create_player_from_dict(player_dict)
        if player.info and player.info.name:
            normalized_name = player.info.name.lower()
            player_lookup[normalized_name] = player
    elapsed = time.perf_counter() - start_time
    logger.debug(f"Player lookup dictionary built with {len(player_lookup)} entries in {elapsed:.6f} seconds")
    return player_lookup

async def get_player_value(
    player_name: str,
    is_dynasty: bool = False,
    num_qbs: int = 1,
    num_teams: int = 12,
    ppr: int = 1,
) -> Player | None:
    """
    Fetches and returns a player object with value information from the FantasyCalc API based on the provided player name and league settings.
    Args:
        player_name (str): The name of the player to search for.
        is_dynasty (bool, optional): Whether the league is a dynasty league. Defaults to False.
        num_qbs (int, optional): Number of starting quarterbacks in the league. Defaults to 1.
        num_teams (int, optional): Number of teams in the league. Defaults to 12.
        ppr (int, optional): Points per reception setting (0 for standard, 1 for full PPR, etc.). Defaults to 1.
    Returns:
        Player or None: The player object if found (exact or substring match), otherwise None.
    Raises:
        Exception: If the FantasyCalc API returns a non-200 status code.
    """
    params = {
        "isDynasty": __import__('json').dumps(is_dynasty),
        "numQbs": str(num_qbs),
        "numTeams": str(num_teams),
        "ppr": str(ppr),
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"FantasyCalc API error {resp.status}: {text}")
            response = await resp.json()
    # '2027 Round 1'
    # '2025 Pick 1.01'
    player_lookup = create_lookup_dict(response)
    # Try exact match first
    normalized_query = player_name.lower()
    logger.debug(f"Searching for player: {player_name}")

    if normalized_query in player_lookup:
        return player_lookup[normalized_query]

    # Fallback to substring match
    for name, player in player_lookup.items():
        if normalized_query in name:
            return player
    return None
