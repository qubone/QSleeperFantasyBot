"""Convert Sleeper kicker picks to rookie picks via league ID.

This registers a slash command `/kickertopick` that accepts a `league_id` and
optional `draft_id`, `teams`, and `name`. It uses the Sleeper API to fetch
players, users, and draft picks and returns a formatted summary of kicker
picks converted to rookie picks.
"""

from __future__ import annotations

from typing import Optional

from discord import Interaction
from discord.ext.commands import Bot
from discord import app_commands


from qsleeperfantasybot.kicker_to_pick.calculate_rookie_pick_from_kicker import run_kicker_scan



#BASE_URL = "https://api.sleeper.app/v1"
#TOTAL_NUM_PICKS = 48
#LOW_REMAINING_THRESHOLD = 5


#def _fetch_json(url: str) -> Optional[Any]:
#    try:
#        r = requests.get(url, timeout=10)
#        r.raise_for_status()
#        return r.json()
#    except Exception as e:
#        logger.exception("HTTP error fetching %s: %s", url, e)
#        return None


#def _resolve_draft_id(league_id: str, draft_id: Optional[str]) -> Optional[str]:
#    if draft_id:
#        return draft_id
#    drafts = sleeper_api_parser.get_all_drafts_for_a_league(league_id)
#    if isinstance(drafts, list) and len(drafts) > 0:
#        first = drafts[0].get("draft_id")
#        return first if isinstance(first, str) else None
#    return None


#def _generate_output(
# players: Dict[str, Any],
#  draft_picks: List[Any],
#  user_map: Dict[str, str],
#  teams: int, final_name: str) -> str:
#    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#    output_lines: List[str] = [
# f"**{datetime.now().year} Rookie Pick Tracker: {final_name}**", f"*Last Updated: {now}*", "---"]
#
#    for i, pick in enumerate(draft_picks):
#        if i >= TOTAL_NUM_PICKS:
#            break
#
#        round_num = (i // teams) + 1
#        pick_num = (i % teams) + 1
#        label = f"{round_num}.{pick_num:02d}"

#        username = user_map.get(pick.get("picked_by"), "Unknown")
#        p_meta = pick.get("metadata", {})
#        player_name = f"{p_meta.get('first_name','')} {p_meta.get('last_name','')}".strip()

#        output_lines.append(f"Pick {label} @{username} (via {player_name})")

#        if (i + 1) % teams == 0:
#            output_lines.append("---")

#    output_lines.append("\n")

#    remaining = TOTAL_NUM_PICKS - len(draft_picks)
#    if 0 < remaining <= LOW_REMAINING_THRESHOLD:
#        output_lines.append(f"**Only {remaining} rookie picks remaining.**")
#    elif remaining <= 0:
#        output_lines.append("**Rookie draft picking complete: All 4 rounds assigned.**")

#    return "\n".join(output_lines)


#def _compute_kicker_text(league_id: str, draft_id: Optional[str], teams: int, name: Optional[str]) -> str:
    # Fetch league info
    #league = _fetch_json(f"{BASE_URL}/league/{league_id}")
    #league = sleeper_api_parser.get_specific_league(league_id)
    #if not league or not isinstance(league, dict):
    #    return f"Error: Could not find league with ID {league_id}."

    #final_name = league.get("name", name or "Sleeper League")

    #draft_id = _resolve_draft_id(league_id, draft_id)
    #if not draft_id:
    #    return "Error: No drafts found for this league."

    # Fetch players mapping (use Sleeper players endpoint)
    #players = _fetch_json(f"{BASE_URL}/players/nfl") or {}
    #players = sleeper_api_parser.fetch_all_players()

    # Fetch users and draft picks
    #users_data = sleeper_api_parser.get_users_in_a_league(league_id)
    #draft_picks = sleeper_api_parser.get_all_picks_in_draft(draft_id)

    #if not users_data or not draft_picks or not isinstance(draft_picks, list):
    #    return "Error: Failed to retrieve league users or draft picks."

    #user_map = {
    # u.get("user_id"): u.get("display_name") or u.get("username") for u in users_data if isinstance(u, dict)}

    # filter picks to only kickers
    #k_picks = [p for p in draft_picks if players.get(p.get("player_id", ""), {}).get("position") == "K"]

    #final_text = _generate_output(players, k_picks, user_map, teams, final_name)
    #return final_text


def setup(bot: Bot) -> None:
    """Register the kicker_to_pick slash command onto the bot."""

    @bot.tree.command(name="kickertopick", description="Convert kicker picks to rookie picks by league ID")
    @app_commands.describe(
        league_id="Sleeper league ID",
        draft_id="Draft ID (optional)",
        teams="Number of teams (picks per round)",
         name="Custom league name"
    )
    async def kickertopick(
        interaction: Interaction,
        league_id: str,
        draft_id: Optional[str] = None,
        teams: int = 12,
        name: Optional[str] = None
        ) -> None:
        """Slash command handler for kicker->rookie pick conversion."""
        await interaction.response.defer(ephemeral=True)

        #loop = asyncio.get_running_loop()
        #result = await loop.run_in_executor(None, _compute_kicker_text, league_id, draft_id, teams, name)
        result = run_kicker_scan(league_id, draft_id, name or "Sleeper League", teams)
        # Send result as followup (we deferred earlier)
        if result:
            await interaction.followup.send(result, ephemeral=True)
