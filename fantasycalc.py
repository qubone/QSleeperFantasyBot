import aiohttp


BASE_URL = "https://api.fantasycalc.com/values/current"

async def get_player_value(player_name: str, is_dynasty: bool=False, num_qbs: int =1, num_teams:int =12, ppr: int=1):
    params = {
        "isDynasty": str(is_dynasty).lower(),
        "numQbs": str(num_qbs),
        "numTeams": str(num_teams),
        "ppr": str(ppr)
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"FantasyCalc API error {resp.status}: {text}")
            data = await resp.json()
    # Fuzzy match player name
    #matches = [p for p in data if player_name.lower() in p["player"]["name"].lower()]
    for player in data:
        if "player" in player and "name" in player["player"]:
            if player_name.lower() in player["player"]["name"].lower():
                return player
    return None
