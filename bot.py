import discord
from discord.ext import commands
from fantasycalc import get_player_value
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="trade")
async def trade(ctx, *, players: str):
    """
    Usage: !trade player1 vs player2
    Example: !trade Tyreek Hill vs Bijan Robinson
    """
    try:
        parts = players.split(" vs ")
        if len(parts) != 2:
            await ctx.send("Use format: `!trade Player A vs Player B`")
            return

        player_a, player_b = parts
        val_a = await get_player_value(player_a.strip())
        val_b = await get_player_value(player_b.strip())

        if not val_a or not val_b:
            await ctx.send("One or both players not found.")
            return
        print (f"Player A: {val_a}, Player B: {val_b}")
        response = (
            f"🔄 **Trade Evaluation**\n"
            f"**{val_a['player']['name']}**: {val_a['value']} pts\n"
            f"**{val_b['player']['name']}**: {val_b['value']} pts\n\n"
            f"{val_a['player']['name']} {'>' if val_a['value'] > val_b['value'] else '<'} {val_b['player']['name']}"
        )

        await ctx.send(response)

    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run(str(TOKEN))
