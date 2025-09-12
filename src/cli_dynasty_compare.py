"""This module is used for comparing dynasty trades between two sides locally using launch.json in VS Code."""

import argparse
import asyncio

from typing import List

from qsleeperfantasybot.dynasty_compare import dynasty_compare
from qsleeperfantasybot.logger import logger


async def main(side_a: List[str], side_b: List[str], ppr: float, super_flex: bool, number_of_teams: int) -> None:
    result = await dynasty_compare(
        side_a=side_a,
        side_b=side_b,
        ppr=ppr,
        is_super_flex=super_flex,
        number_of_teams=number_of_teams,
    )
    logger.info("Trade comparison complete. \n %s", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynasty trade comparison")
    parser.add_argument("--side-a", nargs="+", required=True, help="Assets for Side A (players or picks)")
    parser.add_argument("--side-b", nargs="+", required=True, help="Assets for Side B (players or picks)")
    parser.add_argument("--ppr", type=float, default=1.0, help="PPR setting (e.g., 0, 0.5, 1). Default is 1.")
    (
        parser.add_argument(
            "--super-flex", type=bool, default=True, help="Is this a super flex league? (True/False). Default is True."
        ),
    )
    parser.add_argument(
        "--number-of-teams", type=int, default=12, help="Number of teams in the league. Default is 12."
    )
    args = parser.parse_args()

    asyncio.run(main(args.side_a, args.side_b, args.ppr, args.super_flex, args.number_of_teams))
