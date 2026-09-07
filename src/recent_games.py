"""
Fetch recent completed games from ESPN public schedule APIs.

Mirrors src/upcoming_schedule.py: live ESPN first, then a committed
snapshot under src/data/recent_games.json when Vercel cannot reach ESPN.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

import requests

from src.espn_client import build_session, espn_get_json

try:
    from dateutil import parser as date_parser
except ImportError:  # pragma: no cover
    date_parser = None


ESPN_TEAMS = [
    {
        "name": "Dallas Cowboys",
        "sport": "NFL",
        "path": "football/nfl",
        "team_id": "6",
        "allow_prior_season": True,
    },
    {
        "name": "Dallas Mavericks",
        "sport": "NBA",
        "path": "basketball/nba",
        "team_id": "6",
        "allow_prior_season": True,
    },
    {
        "name": "Golden State Warriors",
        "sport": "NBA",
        "path": "basketball/nba",
        "team_id": "9",
        "allow_prior_season": True,
    },
    {
        "name": "Texas Rangers",
        "sport": "MLB",
        "path": "baseball/mlb",
        "team_id": "13",
        "allow_prior_season": True,
    },
    {
        "name": "North Carolina Tar Heels",
        "sport": "NCAA Basketball",
        "path": "basketball/mens-college-basketball",
        "team_id": "153",
        "allow_prior_season": True,
    },
    {
        "name": "North Carolina Tar Heels",
        "sport": "NCAA Football",
        "path": "football/college-football",
        "team_id": "153",
        "allow_prior_season": False,
    },
]


def _session() -> requests.Session:
    return build_session()


def _score_value(score_obj) -> Optional[float]:
    if score_obj is None:
        return None
    if isinstance(score_obj, dict):
        value = score_obj.get("value")
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
    try:
        return float(score_obj)
    except (TypeError, ValueError):
        return None


def _parse_completed_event(event: dict, team: dict) -> Optional[dict]:
    competitions = event.get("competitions") or []
    if not competitions:
        return None

    comp = competitions[0]
    status_type = (comp.get("status") or {}).get("type") or {}
    status_name = (
        status_type.get("name", "").upper()
        if isinstance(status_type, dict)
        else str(status_type).upper()
    )

    competitors = comp.get("competitors") or []
    if len(competitors) < 2:
        return None

    team_row = next(
        (
            c
            for c in competitors
            if str((c.get("team") or {}).get("id") or "") == str(team["team_id"])
        ),
        None,
    )
    if not team_row:
        return None

    other = next(
        (
            c
            for c in competitors
            if str((c.get("team") or {}).get("id") or "") != str(team["team_id"])
        ),
        None,
    )
    if not other:
        return None

    team_score = _score_value(team_row.get("score"))
    other_score = _score_value(other.get("score"))
    completed = bool(status_type.get("completed") or status_type.get("state") == "post")
    if not completed and (team_score is None or other_score is None):
        return None
    if team_score is None or other_score is None:
        return None

    team_winner = team_row.get("winner")
    other_winner = other.get("winner")
    if team_score == other_score and team_score > 0 and not team_winner and not other_winner:
        result = "T"
    elif team_winner is True:
        result = "W"
    elif team_winner is False:
        result = "L"
    elif team_score > other_score:
        result = "W"
    elif team_score < other_score:
        result = "L"
    else:
        result = "T"

    opponent = ((other.get("team") or {}).get("displayName") or "").strip()
    if not opponent:
        return None

    date_str = event.get("date") or ""
    if not date_str:
        return None

    return {
        "result": result,
        "date": date_str,
        "datetime": date_str,
        "opponent": opponent,
        "team_score": int(team_score),
        "opponent_score": int(other_score),
        "score_margin": abs(int(team_score) - int(other_score)),
        "is_home": str(team_row.get("homeAway") or "").lower() == "home",
        "is_overtime": "OT" in status_name or "OVERTIME" in status_name,
        "team": team["name"],
        "sport": team["sport"],
        "type": "game",
    }


def _fetch_schedule_events(
    session: requests.Session, team: dict, season: Optional[int] = None
) -> List[dict]:
    path = f"/apis/site/v2/sports/{team['path']}/teams/{team['team_id']}/schedule"
    params = {"season": season} if season is not None else None
    payload = espn_get_json(path, session=session, params=params, timeout=10)
    if not payload:
        print(
            f"Recent schedule empty/failed for {team['name']}"
            f"{f' season={season}' if season else ''}: {path}"
        )
        return []

    events = payload.get("events") or []
    parsed: List[dict] = []
    for event in events:
        item = _parse_completed_event(event, team)
        if item:
            parsed.append(item)
    return parsed


def _season_candidates(team: dict) -> List[Optional[int]]:
    """Try current schedule, then current/prior year season params."""
    year = datetime.now().year
    candidates: List[Optional[int]] = [None, year]
    if team.get("allow_prior_season", True):
        candidates.append(year - 1)
    # Deduplicate while preserving order
    seen = set()
    ordered: List[Optional[int]] = []
    for item in candidates:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def _fetch_team_recent(
    session: requests.Session, team: dict, num_games: int
) -> List[dict]:
    for season in _season_candidates(team):
        try:
            games = _fetch_schedule_events(session, team, season=season)
        except Exception as exc:  # noqa: BLE001
            print(f"Error fetching recent for {team['name']} season={season}: {exc}")
            continue
        if games:
            games.sort(key=lambda g: g.get("date") or "", reverse=True)
            return games[:num_games]
    return []


def _load_rivals_map() -> Dict[Tuple[str, str], List[str]]:
    """Map (team name, sport) -> rival names from teams_config.json."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "teams_config.json")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except Exception as exc:  # noqa: BLE001
        print(f"Could not load rivals from teams_config.json: {exc}")
        return {}

    rivals: Dict[Tuple[str, str], List[str]] = {}
    for team in payload.get("teams") or []:
        name = team.get("name")
        sport = team.get("sport")
        if name and sport:
            rivals[(name, sport)] = list(team.get("rivals") or [])
    return rivals


def _relative_ago_label(event_dt: datetime, now: datetime) -> Optional[str]:
    days_ago = (now.date() - event_dt.date()).days
    if days_ago < 0:
        return None
    if days_ago == 0:
        return "Today"
    if days_ago == 1:
        return "Yesterday"
    return f"{days_ago} days ago"


def _format_games(raw_games: List[dict], limit: int) -> List[dict]:
    rivals_map = _load_rivals_map()
    if date_parser is None:
        formatted = []
        for game in raw_games[:limit]:
            iso = game.get("datetime") or game.get("date") or ""
            opponent = (game.get("opponent") or "").strip()
            team_rivals = rivals_map.get((game.get("team"), game.get("sport")), [])
            formatted.append(
                {
                    "date": iso,
                    "datetime": iso,
                    "team": game["team"],
                    "sport": game["sport"],
                    "result": game.get("result", "?"),
                    "type": "game",
                    "opponent": opponent,
                    "team_score": game.get("team_score", 0),
                    "opponent_score": game.get("opponent_score", 0),
                    "score_margin": game.get("score_margin", 0),
                    "is_home": game.get("is_home", False),
                    "is_overtime": game.get("is_overtime", False),
                    "is_rivalry": opponent.lower() in [r.lower() for r in team_rivals],
                }
            )
        return formatted

    now = datetime.now(timezone.utc)
    formatted: List[dict] = []
    for game in raw_games:
        try:
            iso = game.get("datetime") or game.get("date") or ""
            opponent = (game.get("opponent") or "").strip()
            if not opponent or opponent.lower() == "unknown" or not iso:
                continue
            event_dt = date_parser.parse(iso)
            if event_dt.tzinfo is None:
                event_dt = event_dt.replace(tzinfo=timezone.utc)
            now_cmp = now.astimezone(event_dt.tzinfo)
            label = _relative_ago_label(event_dt, now_cmp)
            if label is None:
                continue
            team_rivals = rivals_map.get((game.get("team"), game.get("sport")), [])
            formatted.append(
                {
                    "date": label,
                    "datetime": iso,
                    "team": game["team"],
                    "sport": game["sport"],
                    "result": game.get("result", "?"),
                    "type": "game",
                    "opponent": opponent,
                    "team_score": game.get("team_score", 0),
                    "opponent_score": game.get("opponent_score", 0),
                    "score_margin": game.get("score_margin", 0),
                    "is_home": game.get("is_home", False),
                    "is_overtime": game.get("is_overtime", False),
                    "is_rivalry": opponent.lower() in [r.lower() for r in team_rivals],
                }
            )
        except Exception as exc:  # noqa: BLE001
            print(f"Error formatting recent date: {exc}")

        if len(formatted) >= limit:
            break
    return formatted


_SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "data", "recent_games.json")


def load_recent_snapshot(limit: int = 20) -> List[dict]:
    """Load committed snapshot (for Vercel when ESPN is unreachable)."""
    try:
        with open(_SNAPSHOT_PATH, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        print(f"Recent snapshot missing: {_SNAPSHOT_PATH}")
        return []
    except Exception as exc:  # noqa: BLE001
        print(f"Error reading recent snapshot: {exc}")
        return []

    games = payload.get("games") or []
    raw = []
    for game in games:
        iso = game.get("datetime") or game.get("date")
        opponent = (game.get("opponent") or "").strip()
        if not iso or not opponent or opponent.lower() == "unknown":
            continue
        raw.append(
            {
                "date": iso,
                "datetime": iso,
                "team": game.get("team"),
                "sport": game.get("sport"),
                "result": game.get("result", "?"),
                "type": "game",
                "opponent": opponent,
                "team_score": game.get("team_score", 0),
                "opponent_score": game.get("opponent_score", 0),
                "score_margin": game.get("score_margin", 0),
                "is_home": game.get("is_home", False),
                "is_overtime": game.get("is_overtime", False),
            }
        )
    raw.sort(key=lambda item: item.get("datetime") or "", reverse=True)
    return _format_games(raw, limit)


def save_recent_snapshot(games: List[dict], source: str = "espn") -> str:
    """Persist recent games for serverless fallback."""
    os.makedirs(os.path.dirname(_SNAPSHOT_PATH), exist_ok=True)
    # Store ISO datetime rows so labels stay fresh on read.
    stored = []
    for game in games:
        iso = game.get("datetime") or game.get("date")
        if not iso:
            continue
        stored.append(
            {
                "datetime": iso,
                "team": game.get("team"),
                "sport": game.get("sport"),
                "result": game.get("result", "?"),
                "type": "game",
                "opponent": game.get("opponent"),
                "team_score": game.get("team_score", 0),
                "opponent_score": game.get("opponent_score", 0),
                "score_margin": game.get("score_margin", 0),
                "is_home": game.get("is_home", False),
                "is_overtime": game.get("is_overtime", False),
            }
        )
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "games": stored,
    }
    with open(_SNAPSHOT_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return _SNAPSHOT_PATH


def fetch_recent_games(
    limit: int = 20, per_team: int = 5, *, allow_snapshot: bool = True
) -> List[dict]:
    """
    Return recent completed games across tracked teams.

    Prefer live ESPN (with prior-season fallback when the current schedule has
    no completed games). If ESPN fails/empty (common on Vercel), fall back to
    the committed snapshot under src/data/recent_games.json.
    """
    session = _session()
    collected: List[dict] = []
    errors: List[str] = []

    for team in ESPN_TEAMS:
        try:
            collected.extend(_fetch_team_recent(session, team, per_team))
        except Exception as exc:  # noqa: BLE001
            msg = f"{team['name']} ({team['sport']}): {exc}"
            errors.append(msg)
            print(f"Error fetching recent for {msg}")

    collected.sort(key=lambda item: item.get("date") or "", reverse=True)
    formatted = _format_games(collected, limit)

    if formatted:
        return formatted

    if errors:
        print(f"Recent games empty after errors: {errors}")

    if allow_snapshot:
        snapshot = load_recent_snapshot(limit=limit)
        if snapshot:
            print(f"Using recent snapshot ({len(snapshot)} games)")
            return snapshot

    return []
