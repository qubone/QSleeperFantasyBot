"""Tests for the store_sleeper_user command."""

import pytest
from unittest.mock import AsyncMock, patch
from discord.ext import commands
from discord import app_commands, Interaction, Intents
from typing import cast, Callable, Awaitable

from qsleeperfantasybot.commands import store_sleeper_user


@pytest.fixture
def bot() -> commands.Bot:
    """Shared bot instance for tests."""
    bot = commands.Bot(command_prefix="!", intents=Intents.default())
    store_sleeper_user.setup(bot)
    return bot


@pytest.fixture
def interaction() -> AsyncMock:
    """Shared mock interaction for tests."""
    interaction = AsyncMock(spec=Interaction)
    interaction.user.id = 42
    interaction.response = AsyncMock()
    return interaction


set_username_type = Callable[[Interaction, str], Awaitable[None]]


@pytest.mark.asyncio
async def test_setusername_command(bot: commands.Bot, interaction: AsyncMock) -> None:
    """Test the /setusername command."""
    with patch.object(store_sleeper_user.sleeper_user_handler, "set_username") as mock_set:
        cmd = bot.tree.get_command("setusername")
        assert isinstance(cmd, app_commands.Command)
        callback = cast(set_username_type, cmd.callback)
        await callback(interaction, "testuser")
        mock_set.assert_called_once_with(42, "testuser")
        interaction.response.send_message.assert_called_once_with(
            "✅ Sleeper username `testuser` linked to QSleeperFantasyBot",
            ephemeral=True,
        )


get_username_type = Callable[[Interaction], Awaitable[None]]


@pytest.mark.asyncio
async def test_getusername_command_found(
    bot: commands.Bot,
    interaction: AsyncMock,
) -> None:
    """Test the /getusername command when username is found."""
    with patch.object(store_sleeper_user.sleeper_user_handler, "get_username", return_value="testuser"):
        cmd = bot.tree.get_command("getusername")
        assert isinstance(cmd, app_commands.Command)
        callback = cast(get_username_type, cmd.callback)
        await callback(interaction)
        interaction.response.send_message.assert_called_once_with(
            "Your linked Sleeper username is `testuser`",
            ephemeral=True,
        )


@pytest.mark.asyncio
async def test_getusername_command_not_found(
    bot: commands.Bot,
    interaction: AsyncMock,
) -> None:
    """Test the /getusername command when username is not found."""
    with patch.object(store_sleeper_user.sleeper_user_handler, "get_username", return_value=None):
        cmd = bot.tree.get_command("getusername")
        assert isinstance(cmd, app_commands.Command)
        callback = cast(get_username_type, cmd.callback)
        await callback(interaction)
        interaction.response.send_message.assert_called_once_with(
            "You have not set your Sleeper username yet. Use `/setusername` to set it.",
            ephemeral=True,
        )
