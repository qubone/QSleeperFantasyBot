import discord
from discord.ext import commands
from fantasycalc import get_player_value
from dynasty_compare import dynasty_compare
from dotenv import load_dotenv
from messages import construct_trade_message
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages
bot = commands.Bot(command_prefix="!", intents=intents)





@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

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
@discord.app_commands.describe(
    side_a="Comma-separated list of assets for side A",
    side_b="Comma-separated list of assets for side B"
)
async def compare_dynasty_trade_slash(interaction: discord.Interaction, side_a: str, side_b: str):
        await interaction.response.defer()  # optional if it takes >3s
        side_a_list = [s.strip() for s in side_a.split(",")]
        side_b_list = [s.strip() for s in side_b.split(",")]
        result = await dynasty_compare(side_a_list, side_b_list)
        await interaction.followup.send(result)



bot.run(str(TOKEN))
