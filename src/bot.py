"""Discord bot for fantasy football trade analysis.
This module implements a Discord bot that provides fantasy football trade value comparisons and dynasty trade evaluations.
It supports both traditional command and slash command interfaces, including autocomplete for asset names.
Features:
- Fetches and caches player/asset names for autocomplete.
- Provides trade value comparisons between two players.
- Compares dynasty trades between two sides, supporting multiple assets per side.
- Logs bot activity and warnings.
- Loads configuration from environment variables.
Dependencies:
- discord.py (with app_commands and commands extensions)
- dotenv for environment variable management
- Custom modules: fantasycalc, dynasty_compare, messages, logger
Environment Variables:
- DISCORD_TOKEN: Discord bot token
Commands:
- !trade <player1> vs <player2>: Compares two players' trade values.
- !dynastytrade <side A> vs <side B>: Compares dynasty trade value between two sides (comma-separated assets).
- /dynastytrade: Slash command version with autocomplete for asset names.
"""

import os

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from dotenv import load_dotenv

from src.dynasty_compare import dynasty_compare
from src.fantasycalc import (fetch_asset_names, get_cached_asset_names,
                         get_player_value)
from logger import logger
from src.messages import construct_trade_message

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages
bot = commands.Bot(command_prefix="!", intents=intents)


async def asset_autocomplete(interaction: discord.Interaction, current: str):
    """Autocomplete function for asset names.
    Fetches cached asset names and returns matches based on the current input. """
    asset_names = await get_cached_asset_names()
    if not asset_names:
        logger.warning("No asset names available during autocomplete.")
    parts = current.split(",")
    last_part = parts[-1].strip()
    matches = [
        name for name in asset_names
        if last_part.lower() in name.lower()
    ][:25]

    base = ", ".join(p.strip() for p in parts[:-1] if p.strip())

    logger.debug(f"Autocomplete matches for '{current}': {matches}")
    await interaction.response.autocomplete(
        [
            app_commands.Choice(
                name=f"{base}, {match}" if base else match,
                value=f"{base}, {match}" if base else match
            ) 
            for match in matches
        ]
    )

@bot.event
async def on_ready():
    logger.info("Bot starting up...")
    await fetch_asset_names()
    await bot.tree.sync()
    logger.info(f"Logged in as {bot.user}")

@bot.command(name="trade")
async def trade(ctx: commands.Context, *, players_input: str):
    """
    Usage: !trade player1 vs player2
    Example: !trade Tyreek Hill vs Bijan Robinson
    """
    try:
        player_names = players_input.split(" vs ")
        if len(player_names) != 2:
            await ctx.send("Use format: `!trade Player A vs Player B`")
            return

        player_name_a, player_name_b = player_names
        player_a = await get_player_value(player_name=player_name_a.strip())
        player_b = await get_player_value(player_name=player_name_b.strip())

        if not player_a or not player_b:
            await ctx.send("One or both players not found.")
            return
        print (f"Player A: {player_a.info.name}, Player B: {player_b.info.name}")
        response = construct_trade_message(player_a, player_b)

        await ctx.send(response)

    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="dynastytrade")
async def compare_dynasty_trade(ctx: commands.Context, *, trade_assets: str):
    try:
        if "vs" not in trade_assets:
            await ctx.send("Format: `!dynastytrade <side A> vs <side B>`")
            return

        side_a_raw, side_b_raw = trade_assets.split("vs", 1)
        side_a_list = [asset.strip() for asset in side_a_raw.split(",")]
        side_b_list = [asset.strip() for asset in side_b_raw.split(",")]

        if not side_a_list or not side_b_list:
            await ctx.send("Both sides must have at least one asset.")
            return
        result = await dynasty_compare(side_a_list, side_b_list)
        await ctx.send(result)

    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.tree.command(name="dynastytrade", description="Compare dynasty trade value between two sides.")
@app_commands.describe(
    side_a="Comma-separated list of assets for side A",
    side_b="Comma-separated list of assets for side B"
)
@app_commands.autocomplete(
    side_a=asset_autocomplete,
    side_b=asset_autocomplete
)
async def compare_dynasty_trade_slash(interaction: Interaction, side_a: str, side_b: str):
        await interaction.response.defer()  # optional if it takes >3s
        side_a_list = [s.strip() for s in side_a.split(",")]
        side_b_list = [s.strip() for s in side_b.split(",")]
        result = await dynasty_compare(side_a_list, side_b_list)
        await interaction.followup.send(result)

bot.run(str(TOKEN))
