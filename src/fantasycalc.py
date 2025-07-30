"""This module provides asynchronous utilities for fetching and processing player value data from the FantasyCalc API.
Functions:
    - create_lookup_dict(players): Builds a lookup dictionary of Player objects keyed by normalized player names.
    - get_cached_asset_names(force=False): Retrieves and caches the list of asset (player) names from the FantasyCalc API.
    - fetch_asset_names(): Fetches and caches asset names from the FantasyCalc API if not already loaded.
    - get_player_value(player_name, is_dynasty=False, num_qbs=1, num_teams=12, ppr=1): Fetches a Player object with value information from the FantasyCalc API based on player name and league settings.
Globals:
    - BASE_URL: The FantasyCalc API endpoint for current player values.
    - _cached_asset_names: Cached list of asset names from the API.
    - _asset_names_loaded: Boolean flag indicating whether asset names have been loaded.
Dependencies:
    - aiohttp: For asynchronous HTTP requests.
    - time: For performance measurement.
    - typing: For type annotations.
    - player_model: For Player model and creation utility.
    - logger: For logging debug information.
Typical usage:
    Use the provided asynchronous functions to fetch player values and asset names for fantasy football applications, supporting customizable league settings.
"""
import time
from typing import Any, Dict, List

import aiohttp

from src.logger import logger
from src.player_model import Player, create_player_from_dict

BASE_URL = "https://api.fantasycalc.com/values/current"

_cached_asset_names: List[str] = []
_asset_names_loaded = False

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

async def get_cached_asset_names(force: bool = False) -> List[str]:
    global _cached_asset_names, _asset_names_loaded
    if not _asset_names_loaded or force:
        await fetch_asset_names()
    return _cached_asset_names


async def fetch_asset_names():
    global _cached_asset_names, _asset_names_loaded
    if _asset_names_loaded:
        return  # Already fetched
    params = {
        "isDynasty": __import__('json').dumps(True),
        "numQbs": str(1),
        "numTeams": str(12),
        "ppr": str(1),
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"FantasyCalc API error {resp.status}: {text}")
            response = await resp.json()
            logger.debug(f"Fetched {len(response)} assets from FantasyCalc API")
            _cached_asset_names = [
                item["player"]["name"] for item in response if "player" in item and "name" in item["player"]
            ]
            logger.debug(f"Cached {_cached_asset_names[:10]}... ({len(_cached_asset_names)} total)")
            _asset_names_loaded = True


async def get_player_value(
    player_name: str,
    is_dynasty: bool = False,
    num_qbs: int = 1,
    num_teams: int = 12,
    ppr: int = 1,
) -> Player | None:
    """Fetches and returns a player object with value information from the FantasyCalc API based on the provided player name and league settings.
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
