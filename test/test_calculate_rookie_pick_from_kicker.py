"""Unit tests for the kicker_to_pick module."""

from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

from pathlib import Path

import pytest

from qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker import (
    fetch_data,
    get_auto_draft_id,
    get_league_info,
    resolve_draft_id,
    fetch_draft_data,
    generate_output,
    write_log_file,
    run_kicker_scan,
)


@pytest.fixture
def mock_player_data() -> Dict[str, Any]:
    """Mock player data from Sleeper API."""
    return {
        "1": {"first_name": "Patrick", "last_name": "Mahomes", "position": "QB"},
        "2": {"first_name": "Travis", "last_name": "Kelce", "position": "TE"},
        "3": {"first_name": "Harrison", "last_name": "Butker", "position": "K"},
        "4": {"first_name": "Jake", "last_name": "Elliott", "position": "K"},
    }


@pytest.fixture
def mock_users_data() -> List[Dict[str, Any]]:
    """Mock users data from Sleeper API."""
    return [
        {"user_id": "user1", "display_name": "TeamOwner1"},
        {"user_id": "user2", "display_name": "TeamOwner2"},
        {"user_id": "user3", "display_name": "TeamOwner3"},
    ]


@pytest.fixture
def mock_draft_picks() -> List[Dict[str, Any]]:
    """Mock draft picks data from Sleeper API."""
    return [
        {
            "pick_id": "1",
            "picked_by": "user1",
            "player_id": "3",
            "metadata": {"first_name": "Harrison", "last_name": "Butker"},
        },
        {
            "pick_id": "2",
            "picked_by": "user2",
            "player_id": "4",
            "metadata": {"first_name": "Jake", "last_name": "Elliott"},
        },
        {
            "pick_id": "3",
            "picked_by": "user3",
            "player_id": "1",
            "metadata": {"first_name": "Patrick", "last_name": "Mahomes"},
        },
    ]


@pytest.fixture
def mock_league_info() -> Dict[str, Any]:
    """Mock league info data from Sleeper API."""
    return {
        "league_id": "league123",
        "name": "Test Dynasty League",
        "total_rosters": 12,
        "settings": {"best_ball": 0},
    }


@pytest.fixture
def mock_drafts_list() -> List[Dict[str, Any]]:
    """Mock drafts list from Sleeper API."""
    return [
        {
            "draft_id": "draft123",
            "league_id": "league123",
            "created_at": 1673000000,
        }
    ]


class TestFetchData:
    """Test suite for fetch_data function."""

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.requests.get")
    def test_fetch_data_success(self, mock_get: MagicMock, mock_player_data: Dict[str, Any]) -> None:
        """Test successful data fetch."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_player_data
        mock_get.return_value = mock_response

        result = fetch_data("https://api.sleeper.app/v1/players/nfl")

        assert result == mock_player_data
        mock_get.assert_called_once_with("https://api.sleeper.app/v1/players/nfl")

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.requests.get")
    def test_fetch_data_http_error(self, mock_get: MagicMock) -> None:
        """Test fetch_data with HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = fetch_data("https://api.sleeper.app/v1/invalid")

        assert result is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.requests.get")
    def test_fetch_data_network_exception(self, mock_get: MagicMock) -> None:
        """Test fetch_data with network exception."""
        mock_get.side_effect = Exception("Network error")

        result = fetch_data("https://api.sleeper.app/v1/players/nfl")

        assert result is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.requests.get")
    def test_fetch_data_list_response(self, mock_get: MagicMock) -> None:
        """Test fetch_data with list response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "1"}, {"id": "2"}]
        mock_get.return_value = mock_response

        result = fetch_data("https://api.sleeper.app/v1/league/123/users")

        assert isinstance(result, list)
        assert len(result) == 2


class TestGetAutoAutoDraftId:
    """Test suite for get_auto_draft_id function."""

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_get_auto_draft_id_success(self, mock_fetch: MagicMock, mock_drafts_list: List[Dict[str, Any]]) -> None:
        """Test successful draft ID retrieval."""
        mock_fetch.return_value = mock_drafts_list

        result = get_auto_draft_id("league123")

        assert result == "draft123"
        mock_fetch.assert_called_once_with("https://api.sleeper.app/v1/league/league123/drafts")

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_get_auto_draft_id_empty_list(self, mock_fetch: MagicMock) -> None:
        """Test get_auto_draft_id with empty drafts list."""
        mock_fetch.return_value = []

        result = get_auto_draft_id("league123")

        assert result is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_get_auto_draft_id_not_list(self, mock_fetch: MagicMock) -> None:
        """Test get_auto_draft_id when response is not a list."""
        mock_fetch.return_value = {"error": "not a list"}

        result = get_auto_draft_id("league123")

        assert result is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_get_auto_draft_id_non_string_draft_id(self, mock_fetch: MagicMock) -> None:
        """Test get_auto_draft_id when draft_id is not a string."""
        mock_fetch.return_value = [{"draft_id": 12345}]

        result = get_auto_draft_id("league123")

        assert result is None


class TestGetLeagueInfo:
    """Test suite for get_league_info function."""

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_get_league_info_success(self, mock_fetch: MagicMock, mock_league_info: Dict[str, Any]) -> None:
        """Test successful league info retrieval."""
        mock_fetch.return_value = mock_league_info

        result = get_league_info("league123")

        assert result == mock_league_info
        mock_fetch.assert_called_once_with("https://api.sleeper.app/v1/league/league123")

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_get_league_info_not_dict(self, mock_fetch: MagicMock) -> None:
        """Test get_league_info when response is not a dict."""
        mock_fetch.return_value = [{"league_id": "league123"}]

        result = get_league_info("league123")

        assert result is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_get_league_info_none(self, mock_fetch: MagicMock) -> None:
        """Test get_league_info when fetch returns None."""
        mock_fetch.return_value = None

        result = get_league_info("league123")

        assert result is None


class TestResolveDraftId:
    """Test suite for resolve_draft_id function."""

    def test_resolve_draft_id_provided(self) -> None:
        """Test resolve_draft_id when draft_id is already provided."""
        result = resolve_draft_id("league123", "draft456")

        assert result == "draft456"

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_auto_draft_id")
    def test_resolve_draft_id_fetch_latest(self, mock_auto_draft: MagicMock) -> None:
        """Test resolve_draft_id fetches latest when not provided."""
        mock_auto_draft.return_value = "draft789"

        result = resolve_draft_id("league123", None)

        assert result == "draft789"
        mock_auto_draft.assert_called_once_with("league123")

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_auto_draft_id")
    def test_resolve_draft_id_not_found(self, mock_auto_draft: MagicMock) -> None:
        """Test resolve_draft_id when no draft found."""
        mock_auto_draft.return_value = None

        result = resolve_draft_id("league123", None)

        assert result is None


class TestFetchDraftData:
    """Test suite for fetch_draft_data function."""

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_fetch_draft_data_success(
        self, mock_fetch: MagicMock, mock_users_data: List[Dict[str, Any]], mock_draft_picks: List[Dict[str, Any]]
    ) -> None:
        """Test successful draft data fetch."""
        mock_fetch.side_effect = [mock_users_data, mock_draft_picks]

        users, picks = fetch_draft_data("league123", "draft456")

        assert users == mock_users_data
        assert picks == mock_draft_picks
        assert mock_fetch.call_count == 2

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_fetch_draft_data_partial_failure(
        self, mock_fetch: MagicMock,
        mock_users_data: List[Dict[str, Any]]
        ) -> None:
        """Test draft data fetch with one request failing."""
        mock_fetch.side_effect = [mock_users_data, None]

        users, picks = fetch_draft_data("league123", "draft456")

        assert users == mock_users_data
        assert picks is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_data")
    def test_fetch_draft_data_both_none(self, mock_fetch: MagicMock) -> None:
        """Test draft data fetch when both requests fail."""
        mock_fetch.side_effect = [None, None]

        users, picks = fetch_draft_data("league123", "draft456")

        assert users is None
        assert picks is None


class TestGenerateOutput:
    """Test suite for generate_output function."""

    def test_generate_output_basic(
        self, mock_player_data: Dict[str, Any], mock_draft_picks: List[Dict[str, Any]]
    ) -> None:
        """Test basic output generation."""
        user_map = {"user1": "TeamOwner1", "user2": "TeamOwner2", "user3": "TeamOwner3"}

        output = generate_output(mock_player_data, mock_draft_picks, user_map, teams=3, final_name="Test League")

        assert "Test League" in output
        assert "TeamOwner1" in output
        assert "TeamOwner2" in output
        assert "Harrison Butker" in output
        assert "Pick 1.01" in output

    def test_generate_output_with_empty_picks(self, mock_player_data: Dict[str, Any]) -> None:
        """Test output generation with no picks."""
        user_map: Dict[str, str] = {}

        output = generate_output(mock_player_data, [], user_map, teams=12, final_name="Empty League")

        assert "Empty League" in output
        # No picks yet, so remaining message is not shown for > threshold picks

    def test_generate_output_near_completion(self, mock_player_data: Dict[str, Any]) -> None:
        """Test output generation when nearly complete."""
        draft_picks = [{"picked_by": f"user{i}", "metadata": {}} for i in range(44)]
        user_map = {f"user{i}": f"Team{i}" for i in range(44)}

        output = generate_output(mock_player_data, draft_picks, user_map, teams=12, final_name="Test League")

        assert "Only 4 rookie picks remaining" in output

    def test_generate_output_all_complete(self, mock_player_data: Dict[str, Any]) -> None:
        """Test output generation when all picks assigned."""
        draft_picks = [{"picked_by": f"user{i}", "metadata": {}} for i in range(48)]
        user_map = {f"user{i}": f"Team{i}" for i in range(48)}

        output = generate_output(mock_player_data, draft_picks, user_map, teams=12, final_name="Test League")

        assert "Rookie draft picking complete" in output

    def test_generate_output_exceeds_48_picks(self, mock_player_data: Dict[str, Any]) -> None:
        """Test that output only includes first 48 picks."""
        draft_picks = [{"picked_by": f"user{i}", "metadata": {}} for i in range(60)]
        user_map = {f"user{i}": f"Team{i}" for i in range(60)}

        output = generate_output(mock_player_data, draft_picks, user_map, teams=12, final_name="Test League")

        lines = output.split("\n")
        pick_lines = [line for line in lines if line.startswith("Pick ")]
        assert len(pick_lines) == 48

    def test_generate_output_pick_numbering(self, mock_player_data: Dict[str, Any]) -> None:
        """Test correct pick numbering in output."""
        draft_picks = [{"picked_by": f"user{i}", "metadata": {}} for i in range(6)]
        user_map = {f"user{i}": f"Team{i}" for i in range(6)}

        output = generate_output(mock_player_data, draft_picks, user_map, teams=3, final_name="Test")

        assert "Pick 1.01" in output
        assert "Pick 1.02" in output
        assert "Pick 1.03" in output
        assert "Pick 2.01" in output
        assert "Pick 2.02" in output
        assert "Pick 2.03" in output

    def test_generate_output_unknown_user(self, mock_player_data: Dict[str, Any]) -> None:
        """Test output with unknown user."""
        draft_picks = [{"picked_by": "unknown_user", "metadata": {}}]
        user_map: Dict[str, str] = {}

        output = generate_output(mock_player_data, draft_picks, user_map, teams=12, final_name="Test")

        assert "Unknown" in output

    def test_generate_output_missing_metadata(self, mock_player_data: Dict[str, Any]) -> None:
        """Test output when pick metadata is missing."""
        draft_picks = [{"picked_by": "user1"}]
        user_map = {"user1": "Team1"}

        output = generate_output(mock_player_data, draft_picks, user_map, teams=12, final_name="Test")

        assert "Pick 1.01" in output
        assert "Team1" in output

    def test_generate_output_has_timestamp(self, mock_player_data: Dict[str, Any]) -> None:
        """Test that output includes timestamp."""
        output = generate_output(mock_player_data, [], {}, teams=12, final_name="Test")

        assert "Last Updated:" in output
        # Check for datetime format
        assert any(char.isdigit() for char in output)


class TestWriteLogFile:
    """Test suite for write_log_file function."""

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.ROOT_PATH")
    def test_write_log_file_success(self, mock_root: MagicMock, tmp_path: Path) -> None:
        """Test successful log file write."""
        mock_root.__truediv__ = lambda self, x: tmp_path / x

        write_log_file("test_league", "Test output content")

        log_file = tmp_path / "logs" / "test_league_log.txt"
        assert log_file.exists()
        assert "Test output content" in log_file.read_text()

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.ROOT_PATH")
    def test_write_log_file_append(self, mock_root: MagicMock, tmp_path: Path) -> None:
        """Test that log file appends rather than overwrites."""
        mock_root.__truediv__ = lambda self, x: tmp_path / x

        write_log_file("test_league", "First line")
        write_log_file("test_league", "Second line")

        log_file = tmp_path / "logs" / "test_league_log.txt"
        content = log_file.read_text()
        assert "First line" in content
        assert "Second line" in content

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.ROOT_PATH")
    def test_write_log_file_creates_directory(self, mock_root: MagicMock, tmp_path: Path) -> None:
        """Test that write_log_file creates directory if it doesn't exist."""
        mock_root.__truediv__ = lambda self, x: tmp_path / x

        write_log_file("test_league", "Test content")

        assert (tmp_path / "logs").exists()


class TestRunKickerScan:
    """Test suite for run_kicker_scan function."""

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_draft_data")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_players")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.resolve_draft_id")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_league_info")
    def test_run_kicker_scan_success(
        self,
        mock_get_league_info: MagicMock,
        mock_resolve_draft: MagicMock,
        mock_get_players: MagicMock,
        mock_fetch_draft: MagicMock,
        mock_player_data: Dict[str, Any],
        mock_users_data: List[Dict[str, Any]],
        mock_draft_picks: List[Dict[str, Any]],
        mock_league_info: Dict[str, Any],
    ) -> None:
        """Test successful kicker scan."""
        mock_get_league_info.return_value = mock_league_info
        mock_resolve_draft.return_value = "draft123"
        mock_get_players.return_value = mock_player_data
        mock_fetch_draft.return_value = (mock_users_data, mock_draft_picks)

        result = run_kicker_scan("league123", None, "Default Name", 12)

        assert result is not None
        assert "Test Dynasty League" in result

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_league_info")
    def test_run_kicker_scan_invalid_league(self, mock_league_info: MagicMock) -> None:
        """Test kicker scan with invalid league."""
        mock_league_info.return_value = None

        result = run_kicker_scan("invalid_league", None, "Default Name", 12)

        assert result is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_draft_data")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_players")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.resolve_draft_id")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_league_info")
    def test_run_kicker_scan_missing_draft_id(
        self,
        mock_get_league_info: MagicMock,
        mock_resolve_draft: MagicMock,
        mock_get_players: MagicMock,
        mock_fetch_draft: MagicMock,
        mock_league_info: Dict[str, Any],
    ) -> None:
        """Test kicker scan when draft ID resolution fails."""
        mock_get_league_info.return_value = mock_league_info
        mock_resolve_draft.return_value = None

        result = run_kicker_scan("league123", None, "Default Name", 12)

        assert result is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.write_log_file")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_draft_data")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_players")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.resolve_draft_id")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_league_info")
    def test_run_kicker_scan_failed_data_fetch(
        self,
        mock_get_league_info: MagicMock,
        mock_resolve_draft: MagicMock,
        mock_get_players: MagicMock,
        mock_fetch_draft: MagicMock,
        mock_write_log: MagicMock,
        mock_league_info: Dict[str, Any],
        mock_player_data: Dict[str, Any],
    ) -> None:
        """Test kicker scan when draft data fetch fails."""
        mock_get_league_info.return_value = mock_league_info
        mock_resolve_draft.return_value = "draft123"
        mock_get_players.return_value = mock_player_data
        mock_fetch_draft.return_value = (None, None)

        result = run_kicker_scan("league123", None, "Default Name", 12)

        assert result is None

    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.fetch_draft_data")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_players")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.resolve_draft_id")
    @patch("qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker.get_league_info")
    def test_run_kicker_scan_custom_name(
        self,
        mock_get_league_info: MagicMock,
        mock_resolve_draft: MagicMock,
        mock_get_players: MagicMock,
        mock_fetch_draft: MagicMock,
        mock_player_data: Dict[str, Any],
        mock_users_data: List[Dict[str, Any]],
        mock_draft_picks: List[Dict[str, Any]],
    ) -> None:
        """Test kicker scan uses custom name when league name missing."""
        mock_league_data = {"league_id": "league123"}  # Missing 'name' key
        mock_get_league_info.return_value = mock_league_data
        mock_resolve_draft.return_value = "draft123"
        mock_get_players.return_value = mock_player_data
        mock_fetch_draft.return_value = (mock_users_data, mock_draft_picks)

        result = run_kicker_scan("league123", None, "Custom League Name", 12)

        assert result is not None
        assert "Custom League Name" in result
