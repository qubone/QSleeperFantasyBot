"""Get linked Sleeper leagues command."""

from discord import Interaction
from discord.ext.commands import Bot
from qsleeperfantasybot.logger import logger
from qsleeperfantasybot.sleeper.api.parser import sleeper_api_parser
from qsleeperfantasybot.commands.store_sleeper_user import sleeper_user_handler
from qsleeperfantasybot.sleeper.model.user import User
from qsleeperfantasybot.sleeper.model.league import League, create_league_from_dict
from typing import List


def setup(bot: Bot) -> None:
    """Setup the get_leagues command for the bot."""

    @bot.tree.command(name="getleagues", description="Get your linked Sleeper leagues")
    async def getleagues(interaction: Interaction) -> None:
        """Get your linked Sleeper leagues using slash command."""

        sleeper_username = sleeper_user_handler.get_username(interaction.user.id)
        if not sleeper_username:
            await interaction.response.send_message(
                "❌ No linked Sleeper username found. Please set your username using `/setusername`.",
                ephemeral=True,
            )
            return
        user_data = sleeper_api_parser.get_user(user_name=sleeper_username)
        logger.info(f"Retrieved user data: {user_data}")
        if not user_data:
            await interaction.response.send_message(
                f"❌ Could not retrieve user data for username `{sleeper_username}`.",
                ephemeral=True,
            )
            return
        if isinstance(user_data, dict):
            user = User.from_dict(user_data)
            user_leagues = sleeper_api_parser.get_all_leagues_for_user(user.id)
            logger.info(f"Retrieved leagues for user {sleeper_username}: {user_leagues}")
            if not user_leagues:
                await interaction.response.send_message(
                    f"❌ No leagues found for Sleeper username `{sleeper_username}`.",
                    ephemeral=True,
                )
                return

        league_list = ""
        if isinstance(user_leagues, list):
            leagues: List[League] = []
            for league_data in user_leagues:
                league = create_league_from_dict(league_data)
                leagues.append(league)
            sorted_leagues = sorted(leagues, key=lambda x: x.name)
            league_list = "\n".join(
                (
                    f"• {league.name} "
                    f"(ID: {league.league_id}, "
                    f"Season: {league.season}), "
                    f"Type: {league.settings.type.name}"
                )
                for league in sorted_leagues
            )

        await interaction.response.send_message(
            f"✅ Leagues linked to Sleeper username `{sleeper_username}`:\n{league_list}",
            ephemeral=True,
        )
