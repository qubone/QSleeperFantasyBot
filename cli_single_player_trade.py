import asyncio
import argparse
from fantasycalc import get_player_value  # Adjust the import if needed

async def main(player_name: str):
    player = await get_player_value(player_name)
    if player:
        print(f"✅ Found: {player.info.name} - Value: {player.value}")
    else:
        print("❌ Player not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch fantasy value of a player.")
    parser.add_argument("player", help="Name of the player to search for")

    args = parser.parse_args()
    asyncio.run(main(args.player))