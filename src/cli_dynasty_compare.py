import argparse
import asyncio

from src.dynasty_compare import dynasty_compare


async def main(side_a, side_b):
    result = await dynasty_compare(side_a, side_b)
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynasty trade comparison")
    parser.add_argument("--side-a", nargs="+", required=True, help="Assets for Side A (players or picks)")
    parser.add_argument("--side-b", nargs="+", required=True, help="Assets for Side B (players or picks)")
    args = parser.parse_args()

    asyncio.run(main(args.side_a, args.side_b))
