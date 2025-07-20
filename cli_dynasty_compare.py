import asyncio
import argparse
from fantasycalc import get_player_value  # Adjust import if needed
from dynasty_compare import compare_dynasty_trade  # Assuming this is where the function is defined
async def main(side_a, side_b):
    result = await compare_dynasty_trade(side_a, side_b, get_player_value)
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynasty trade comparison")
    parser.add_argument("--side-a", nargs="+", required=True, help="Assets for Side A (players or picks)")
    parser.add_argument("--side-b", nargs="+", required=True, help="Assets for Side B (players or picks)")
    args = parser.parse_args()

    asyncio.run(main(args.side_a, args.side_b))
