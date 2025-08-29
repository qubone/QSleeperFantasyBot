"""Parser for Sleeper API.

https://docs.sleeper.com/#introduction
"""

from datetime import datetime
from typing import Any, Dict, Optional, Tuple, List
from qsleeperfantasybot.logger import logger

import requests


class SleeperAPIParser:
    """Parses data from Sleeper API with HTTP GET using requests library.

    user_id (str): The numerical ID of the user.
    sport (str): We only support "nfl" right now.
    season (str): Season can be 2017, 2018, etc...
    league_id(str): The ID of the league to retrieve matchups from
    week(str): The week these matchups take place

    """

    def __init__(self) -> None:
        self.base_url = "https://api.sleeper.app/v1"
        self.sport = "nfl"
        self.season = datetime.now().strftime("%Y")

    @staticmethod
    def _http_get_response_data_json(url: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]] | Any]:
        """Returns HTTP GET in JSON format."""
        error_messages = {
            400: "Bad Request -- Your request is invalid..",
            404: "Not Found -- The specified kitten could not be found.",
            429: "Too Many Requests -- You're requesting too many kittens! Slow down!.",
            500: "Internal Server Error -- We had a problem with our server. Try again later.",
            503: "Service Unavailable -- We're temporarily offline for maintenance. Please try again later.",
        }
        try:
            logger.debug(f"Making GET request to URL: {url}")
            response = requests.get(url, timeout=None)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response JSON data: {data}")
            if isinstance(data, dict) or isinstance(data, list):
                return data
            else:
                logger.error("Expected a JSON object (dict or list), but got: %s", type(data))
                return None
        except requests.exceptions.HTTPError as http_err:
            message = error_messages.get(response.status_code, f"An unexpected HTTP error occurred: {http_err}")
            logger.info(message)
        except requests.exceptions.Timeout:
            logger.exception("The request timed out.")
        except requests.exceptions.ConnectionError:
            logger.exception("Network problem or server is unreachable.")
        except requests.exceptions.TooManyRedirects:
            logger.exception("Too many redirects occurred.")
        except requests.exceptions.MissingSchema:
            logger.exception("The URL is missing a scheme (e.g., 'http://').")
        except requests.exceptions.InvalidURL:
            logger.exception("The provided URL is invalid.")
        except requests.exceptions.JSONDecodeError:
            logger.exception("Invalid JSON reponse.")
        except requests.exceptions.RequestException as req_err:
            logger.exception(f"A non-HTTP error occurred: {req_err}")
        return None

    def get_user(
        self, user_id: Optional[str] = None, user_name: Optional[str] = None
    ) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """Via the user resource, you can GET the user object by either providing
        the username or user_id of the user.

        GET https://api.sleeper.app/v1/user/<username>

        GET https://api.sleeper.app/v1/user/<user_id>

        Response data:
        {
            "username": "sleeperuser",
            "user_id": "12345678",
            "display_name": "SleeperUser",
            "avatar": "cc12ec49965eb7856f84d71cf85306af"
        }
        """
        if not user_id and not user_name:
            raise ValueError("Either user_id or user_name must be provided.")
        user = ""
        if user_id and not user_name:
            user = user_id
        elif user_name:
            user = user_name

        return self._http_get_response_data_json(f"{self.base_url}/user/{user}")

    def get_avatars(
        self, avatar_id: str
    ) -> Tuple[Optional[Dict[str, Any] | List[Dict[str, Any]]], Optional[Dict[str, Any]] | List[Dict[str, Any]]]:
        """Users and leagues have avatar images. There are thumbnail and full-size images for each avatar.

        GET https://sleepercdn.com/avatars/<avatar_id>
        """
        sleeper_url = "https://sleepercdn.com/avatars"
        full_size = self._http_get_response_data_json(f"{sleeper_url}/{avatar_id}")
        thumbnail = self._http_get_response_data_json(f"{sleeper_url}/thumbs/{avatar_id}")
        return full_size, thumbnail

    def get_all_leagues_for_user(
        self, user_id: str, season: Optional[str] = None
    ) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all leagues.

        GET https://api.sleeper.app/v1/user/<user_id>/leagues/<sport>/<season>

        [
            {
                "total_rosters": 12,
                "status": "pre_draft", // can also be "drafting", "in_season", or "complete"
                "sport": "nfl",
                "settings": { settings object },
                "season_type": "regular",
                "season": "2018",
                "scoring_settings": { scoring_settings object },
                "roster_positions": [ roster positions array ],
                "previous_league_id": "198946952535085056",
                "name": "Sleeperbot Friends League",
                "league_id": "289646328504385536",
                "draft_id": "289646328508579840",
                "avatar": "efaefa889ae24046a53265a3c71b8b64"
            },
            {
                "total_rosters": 12,
                "status": "in_season",
                "sport": "nfl",
                "settings": { settings object },
                "season_type": "regular",
                "season": "2018",
                "scoring_settings": { scoring_settings object },
                "roster_positions": [ roster positions array ],
                "previous_league_id": "198946952535085056",
                "name": "Sleeperbot Dynasty",
                "league_id": "289646328504385536",
                "draft_id": "289646328508579840",
                "avatar": "efaefa889ae24046a53265a3c71b8b64"
            }
        ]
        """
        if season is None:
            season = self.season
        return self._http_get_response_data_json(f"{self.base_url}/user/{user_id}/leagues/{self.sport}/{season}")

    def get_specific_league(self, league_id: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves a specific league.

        GET https://api.sleeper.app/v1/league/<league_id>

        {
            "total_rosters": 12,
            "status": "in_season",
            "sport": "nfl",
            "settings": { settings object },
            "season_type": "regular",
            "season": "2018",
            "scoring_settings": { scoring_settings object },
            "roster_positions": [ roster positions array ],
            "previous_league_id": "198946952535085056",
            "name": "Sleeperbot Dynasty",
            "league_id": "289646328504385536",
            "draft_id": "289646328508579840",
            "avatar": "efaefa889ae24046a53265a3c71b8b64"
        }
        """
        return self._http_get_response_data_json(f"{self.base_url}/league/{league_id}")

    def get_rosters_in_a_league(self, league_id: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all rosters in a league.

        GET https://api.sleeper.app/v1/league/<league_id>/rosters

        [
            {
                "starters": ["2307", "2257", "4034", "147", "642", "4039", "515", "4149", "DET"],
                "settings": {
                "wins": 5,
                "waiver_position": 7,
                "waiver_budget_used": 0,
                "total_moves": 0,
                "ties": 0,
                "losses": 9,
                "fpts_decimal": 78,
                "fpts_against_decimal": 32,
                "fpts_against": 1670,
                "fpts": 1617
                },
                "roster_id": 1,
                "reserve": [],
                "players": ["1046", "138", "147", "2257", "2307", "2319", "4034",
                "4039", "4040", "4149", "421", "515", "642", "745", "DET"],
                "owner_id": "188815879448829952",
                "league_id": "206827432160788480"
            }
        ]
        """
        return self._http_get_response_data_json(f"{self.base_url}/league/{league_id}/rosters")

    def get_users_in_a_league(self, league_id: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all users in a league.

        This also includes each user's display_name, avatar, and their metadata
        which sometimes includes a nickname they gave their team.

        GET https://api.sleeper.app/v1/league/<league_id>/users

        [
            {
                "user_id": "<user_id>",
                "username": "<username>",
                "display_name": "<display_name>",
                "avatar": "1233456789",
                "metadata": {
                "team_name": "Dezpacito"
                },
                "is_owner": true   // is commissioner (there can be multiple commissioners)
            }
        ]

        """
        return self._http_get_response_data_json(f"{self.base_url}/league/{league_id}/rosters")

    def get_matchups_in_league(self, league_id: str, week: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all matchups in a league for a given week. Each object in
        the list represents one team. The two teams with the same
        matchup_id match up against each other.

        The starters is in an ordered list of player_ids,
        and players is a list of all player_ids in this matchup.

        The bench can be deduced by removing the starters from the players field.

        GET https://api.sleeper.app/v1/league/<league_id>/matchups/<week>

        [
            {
                "starters": ["421", "4035", "3242", "2133", "2449", "4531", "2257", "788", "PHI"],
                "roster_id": 1,
                "players": ["1352", "1387", "2118", "2133", "2182", "223", "2319", "2449", "3208", "4035",
                "421", "4881", "4892", "788", "CLE"],
                "matchup_id": 2,
                "points": 20.0 // total points for team based on league settings
                "custom_points": null // if commissioner overrides points manually
            }
        ]
        """
        return self._http_get_response_data_json(f"{self.base_url}/league/{league_id}/matchups/{week}")

    def get_playoff_bracket(
        self, league_id: str
    ) -> Tuple[Dict[str, Any] | List[Dict[str, Any]], Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves the playoff bracket for a league for 4, 6, and 8 team playoffs.

        Each row represents a matchup between 2 teams.

        GET https://api.sleeper.app/v1/league/<league_id>/winners_bracket

        GET https://api.sleeper.app/v1/league/<league_id>/losers_bracket

        Args:
            league_id (str): The ID of the league to retrieve matchups from
        [
        {r: 1, m: 1,   t1: 3,    t2: 6,     w: null, l: null},
        {r: 1, m: 2,   t1: 4,    t2: 5,     w: null, l: null},

        {r: 2, m: 3,   t1: 1,    t2: null,  t2_from: {w: 1},  w: null, l: null},
        {r: 2, m: 4,   t1: 2,    t2: null,  t2_from: {w: 2},  w: null, l: null},
        {r: 2, m: 5,   t1: null, t2: null,  t1_from: {l: 1},  t2_from: {l: 2},  w: null, l: null, p: 5},

        {r: 3, m: 6,   t1: null, t2: null,  t1_from: {w: 3},  t2_from: {w: 4},  w: null, l: null, p: 1},
        {r: 3, m: 7,   t1: null, t2: null,  t1_from: {l: 3},  t2_from: {l: 4},  w: null, l: null, p: 3}
        ]

        r	int	The round for this matchup, 1st, 2nd, 3rd round, etc.
        m	int	The match id of the matchup, unique for all matchups within a bracket.
        t1	int	The roster_id of a team in this matchup OR {w: 1} which means the winner of match id 1
        t2	int	The roster_id of the other team in this matchup OR {l: 1} which means the loser of match id 1
        w	int	The roster_id of the winning team, if the match has been played.
        l	int	The roster_id of the losing team, if the match has been played.
        t1_from	object	Where t1 comes from, either winner or loser of the match id,
        necessary to show bracket progression.
        t2_from	object	Where t2 comes from, either winner or loser of the match id,
        necessary to show bracket progression.
        """

        winners_bracket = self._http_get_response_data_json(f"{self.base_url}/league/{league_id}/winners_bracket")
        losers_bracket = self._http_get_response_data_json(f"{self.base_url}/league/{league_id}/losers_bracket")
        return winners_bracket or {}, losers_bracket or {}

    def get_transactions(self, league_id: str, round: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all traded picks in a league, including future picks.

        GET https://api.sleeper.app/v1/league/<league_id>/traded_picks

        Args:
            league_id (str): The ID of the league to retrieve traded picks for
            round (str): The week you want to pull from

        [
            {
                "type": "trade",
                "transaction_id": "434852362033561600",
                "status_updated": 1558039402803,
                "status": "complete",
                "settings": null,     // trades do not use this field
                "roster_ids": [2, 1], // roster_ids involved in this transaction
                "metadata": null,
                "leg": 1,         // in football, this is the week
                "drops": null,
                "draft_picks": [  // picks that were traded
                {
                    "season": "2019",// the season this draft pick belongs to
                    "round": 5,      // which round this draft pick is
                    "roster_id": 1,  // original owner's roster_id
                    "previous_owner_id": 1,  // previous owner's roster id (in this trade)
                    "owner_id": 2,   // the new owner of this pick after the trade
                },
                {
                    "season": "2019",
                    "round": 3,
                    "roster_id": 2,
                    "previous_owner_id": 2,
                    "owner_id": 1,
                }
                ],
                "creator": "160000000000000000",  // user id who initiated the transaction
                "created": 1558039391576,
                "consenter_ids": [2, 1], // roster_ids of the people who agreed to this transaction
                "adds": null
                "waiver_budget": [   // roster_id 2 sends 55 FAAB dollars to roster_id 3
                {
                    "sender": 2,
                    "receiver": 3,
                    "amount": 55
                }
                ],
            },
            {
                "type": "free_agent",  // could be waiver or trade as well
                "transaction_id": "434890120798142464",
                "status_updated": 1558048393967,
                "status": "complete",
                "settings": null,   // could be {'waiver_bid': 44} if it's FAAB waivers
                "roster_ids": [1],  // roster_ids involved in this transaction
                "metadata": null,   // can contain notes in waivers like why it didn't go through
                "leg": 1,
                "drops": {
                "1736": 1         // player id 1736 dropped from roster_id 1
                },
                "draft_picks": [],
                "creator": "160000000000000000",
                "created": 1558048393967,
                "consenter_ids": [1], // the roster_ids who agreed to this transaction
                "adds": {
                "2315": 1   // player id 2315 added to roster_id 1
                ...
                },
                "waiver_budget": []  // this used for trades only involving FAAB
            }
        ]
        """
        return self._http_get_response_data_json(f"{self.base_url}/league/{league_id}/transactions/{round}")

    def get_nfl_state(self) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint returns information about the current state for any sport.

        GET https://api.sleeper.app/v1/state/<sport>

        {
            "week": 2, // week
            "season_type": "regular", // pre, post, regular
            "season_start_date": "2020-09-10", // regular season start
            "season": "2020", // current season
            "previous_season": "2019",
            "leg": 2, // week of regular season
            "league_season": "2021", // active season for leagues
            "league_create_season": "2021", // flips in December
            "display_week": 3 // Which week to display in UI, can be different than week
        }
        """
        return self._http_get_response_data_json(f"{self.base_url}/state/{self.sport}")

    def get_all_drafts_for_user(
        self, user_id: str, season: Optional[str] = None
    ) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all drafts by a user.

        Args:
            user_id (str): The numerical ID of the user.
            season (Optional[str], optional): Season can be 2017, 2018, etc.... Defaults to None.

        Returns:
            _type_: _description_

        [
            {
                "type": "snake",
                "status": "complete",
                "start_time": 1515700800000,
                "sport": "nfl",
                "settings": {
                "teams": 6,
                "slots_wr": 2,
                "slots_te": 1,
                "slots_rb": 2,
                "slots_qb": 1,
                "slots_k": 1,
                "slots_flex": 2,
                "slots_def": 1,
                "slots_bn": 5,
                "rounds": 15,
                "pick_timer": 120
                },
                "season_type": "regular",
                "season": "2017",
                "metadata": {
                "scoring_type": "ppr",
                "name": "My Dynasty",
                "description": ""
                },
                "league_id": "257270637750382592",
                "last_picked": 1515700871182,
                "last_message_time": 1515700942674,
                "last_message_id": "257272036450111488",
                "draft_order": null,
                "draft_id": "257270643320426496",
                "creators": null,
                "created": 1515700610526
            }
        ]
        """
        if season is None:
            season = self.season
        return self._http_get_response_data_json(f"{self.base_url}/user/{user_id}/drafts/{self.sport}/{season}")

    def get_all_drafts_for_a_league(self, league_id: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all drafts for a league.
        Keep in mind that a league can have multiple drafts, especially dynasty leagues.

        Drafts are sorted by most recent to earliest.
        Most leagues should only have one draft.

        GET https://api.sleeper.app/v1/league/<league_id>/drafts

        Args:
            league_id (str): The ID of the league for which you are trying to retrieve drafts.

        Returns:
            _type_: _description_

        [
            {
                "type": "snake",
                "status": "complete",
                "start_time": 1515700800000,
                "sport": "nfl",
                "settings": {
                "teams": 6,
                "slots_wr": 2,
                "slots_te": 1,
                "slots_rb": 2,
                "slots_qb": 1,
                "slots_k": 1,
                "slots_flex": 2,
                "slots_def": 1,
                "slots_bn": 5,
                "rounds": 15,
                "pick_timer": 120
                },
                "season_type": "regular",
                "season": "2017",
                "metadata": {
                "scoring_type": "ppr",
                "name": "My Dynasty",
                "description": ""
                },
                "league_id": "257270637750382592",
                "last_picked": 1515700871182,
                "last_message_time": 1515700942674,
                "last_message_id": "257272036450111488",
                "draft_order": null,
                "draft_id": "257270643320426496",
                "creators": null,
                "created": 1515700610526
            }
        ]
        """
        return self._http_get_response_data_json(f"{self.base_url}/league/{league_id}/drafts")

    def get_specific_draft(self, draft_id: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves a specific draft.

        Args:
            draft_id (str): The ID of the draft to retrieve

        Returns:
            _type_: _description_
        """
        return self._http_get_response_data_json(f"{self.base_url}/draft/{draft_id}")

    def get_all_picks_in_draft(self, draft_id: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all picks in a draft.

        Args:
            draft_id (str): The ID of the draft to retrieve picks for

        Returns:
            _type_: _description_
        """
        return self._http_get_response_data_json(f"{self.base_url}/draft/{draft_id}/picks")

    def get_traded_picks_in_draft(self, draft_id: str) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """This endpoint retrieves all traded picks in a draft.

        Args:
            draft_id (str): The ID of the draft to retrieve picks for

        Returns:
            _type_: _description_

        [
            {
                "season": "2019",
                "round": 5,              // which round the pick is
                "roster_id": 1,          // roster_id of ORIGINAL owner
                "previous_owner_id": 1,  // roster_id of the previous owner
                "owner_id": 2,           // roster_id of current owner
            },
            {
                "season": "2019",
                "round": 3,              // which round the pick is
                "roster_id": 2,          // roster_id of original owner
                "previous_owner_id": 2,  // roster_id of previous owner
                "owner_id": 1,           // roster_id of current owner
            }
        ]
        """
        return self._http_get_response_data_json(f"{self.base_url}/draft/{draft_id}/traded_picks")

    def fetch_all_players(self) -> Optional[Dict[str, Dict[str, Any]] | List[Dict[str, Any]]]:
        """Since rosters and draft picks contain Player IDs which look like "1042", "2403", "CAR", etc,
        you will need to know what those IDs map to. The /players call provides you the
        map necessary to look up any player.

        You should save this information on your own servers as this is not intended to
        be called every time you need to look up players due to the filesize being close to 5MB in size.
        You do not need to call this endpoint more than once per day.

        GET https://api.sleeper.app/v1/players/nfl

        Returns:
            _type_: _description_
        """
        url = "https://raw.githubusercontent.com/qubone/sleeper_fetch_players/refs/heads/main/data/sleeper_data_latest.json"
        return self._http_get_response_data_json(url)

    def get_trending_players(
        self, trend_type: str, lookback_hours: Optional[str] = "24", limit: Optional[str] = "25"
    ) -> Optional[Dict[str, Any] | List[Dict[str, Any]]]:
        """You can use this endpoint to get a list of trending players based on adds or drops in the past 24 hours.

        GET https://api.sleeper.app/v1/players/<sport>/trending/<type>?lookback_hours=<hours>&limit=<int>

        Args:
            type (_type_): Either add or drop
            lookback_hours (Optional[str]): Number of hours to look back (default is 24) - optional
            limit (Optional[str]): 	Number of results you want, (default is 25) - optional

            [
                {
                    "player_id": "1111", // the player_id
                    "count": 45         // number or adds
                }
            ]
        """
        return self._http_get_response_data_json(
            f"{self.base_url}/players/{self.sport}/trending/{trend_type}?lookback_hours={lookback_hours}&limit={limit}"
        )


sleeper_api_parser = SleeperAPIParser()
