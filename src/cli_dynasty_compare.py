"""This module is used for comparing dynasty trades between two sides locally using launch.json in VS Code."""

import argparse
import asyncio

from typing import List

from qsleeperfantasybot.dynasty_compare import dynasty_compare
from qsleeperfantasybot.logger import logger


async def main(side_a: List[str], side_b: List[str]) -> None:
    result = await dynasty_compare(side_a, side_b)
    logger.info("Trade comparison complete. \n %s", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynasty trade comparison")
    parser.add_argument("--side-a", nargs="+", required=True, help="Assets for Side A (players or picks)")
    parser.add_argument("--side-b", nargs="+", required=True, help="Assets for Side B (players or picks)")
    args = parser.parse_args()

    asyncio.run(main(args.side_a, args.side_b))
