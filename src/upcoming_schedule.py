"""
Fetch upcoming games from ESPN public schedule APIs.

Kept dependency-light (requests only) so Vercel serverless can call ESPN
without importing the heavier SportsDataFetcher stack.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

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
    },
    {
        "name": "Dallas Mavericks",
        "sport": "NBA",
        "path": "basketball/nba",
        "team_id": "6",
    },
    {
        "name": "Golden State Warriors",
        "sport": "NBA",
        "path": "basketball/nba",
        "team_id": "9",
    },
    {
        "name": "Texas Rangers",
        "sport": "MLB",
        "path": "baseball/mlb",
        "team_id": "13",
    },
    {
        "name": "North Carolina Tar Heels",
        "sport": "NCAA Football",
        "path": "football/college-football",
        "team_id": "153",
    },
]


def _session() -> requests.Session:
    return build_session()


def _relative_date_label(event_dt: datetime, now: datetime) -> Optional[str]:
    days_until = (event_dt.date() - now.date()).days
    if days_until < 0:
        return None
    if days_until == 0:
        return "Today"
    if days_until == 1:
        return "Tomorrow"
    return f"In {days_until} days"


def _parse_event(event: dict, team_name: str, sport: str, team_id: str) -> Optional[dict]:
    competitions = event.get("competitions") or []
    if not competitions:
        return None

    comp = competitions[0]
    status_type = (comp.get("status") or {}).get("type") or {}
    if status_type.get("completed") or status_type.get("state") == "post":
        return None

    competitors = comp.get("competitors") or []
    if len(competitors) < 2:
        return None

    home = next((c for c in competitors if c.get("homeAway") == "home"), None)
    away = next((c for c in competitors if c.get("homeAway") == "away"), None)
    if not home or not away:
        return None

    home_id = str(((home.get("team") or {}).get("id") or ""))
    away_id = str(((away.get("team") or {}).get("id") or ""))
    home_name = (home.get("team") or {}).get("displayName")
    away_name = (away.get("team") or {}).get("displayName")

    if home_id == str(team_id):
        opponent = away_name
        is_home = True
    elif away_id == str(team_id):
        opponent = home_name
        is_home = False
    else:
        return None

    if not opponent:
        return None

    date_str = event.get("date") or ""
    if not date_str:
        return None

    return {
        "date": date_str,
        "team": team_name,
        "sport": sport,
        "opponent": opponent,
        "type": "game",
        "is_home": is_home,
    }


def _fetch_team_schedule(session: requests.Session, team: dict) -> List[dict]:
    path = f"/apis/site/v2/sports/{team['path']}/teams/{team['team_id']}/schedule"
    payload = espn_get_json(path, session=session, timeout=8)
    if not payload:
        print(f"Upcoming schedule empty/failed for {team['name']}: {path}")
        return []

    events = payload.get("events") or []
    parsed: List[dict] = []
    for event in events:
        item = _parse_event(event, team["name"], team["sport"], team["team_id"])
        if item:
            parsed.append(item)
    return parsed


# Bundled with Vercel via includeFiles src/** — used when live ESPN is blocked.
_SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "data", "upcoming_events.json")


def _format_events(raw_events: List[dict], limit: int) -> List[dict]:
    """Turn raw ISO-dated events into API rows with relative labels."""
    if date_parser is None:
        formatted = []
        for event in raw_events[:limit]:
            iso = event.get("datetime") or event.get("date") or ""
            formatted.append(
                {
                    "date": iso,
                    "datetime": iso,
                    "team": event["team"],
                    "sport": event["sport"],
                    "opponent": event["opponent"],
                    "type": event.get("type", "game"),
                    "is_home": event["is_home"],
                }
            )
        return formatted

    now = datetime.now(timezone.utc)
    formatted: List[dict] = []
    for event in raw_events:
        try:
            iso = event.get("datetime") or event.get("date") or ""
            event_dt = date_parser.parse(iso)
            if event_dt.tzinfo is None:
                event_dt = event_dt.replace(tzinfo=timezone.utc)
            now_cmp = now.astimezone(event_dt.tzinfo)
            label = _relative_date_label(event_dt, now_cmp)
            if label is None:
                continue
            formatted.append(
                {
                    "date": label,
                    "datetime": iso,
                    "team": event["team"],
                    "sport": event["sport"],
                    "opponent": event["opponent"],
                    "type": event.get("type", "game"),
                    "is_home": event["is_home"],
                }
            )
        except Exception as exc:  # noqa: BLE001
            print(f"Error formatting upcoming date: {exc}")

        if len(formatted) >= limit:
            break
    return formatted


def load_upcoming_snapshot(limit: int = 10) -> List[dict]:
    """Load committed snapshot (for Vercel when ESPN is unreachable)."""
    try:
        with open(_SNAPSHOT_PATH, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        print(f"Upcoming snapshot missing: {_SNAPSHOT_PATH}")
        return []
    except Exception as exc:  # noqa: BLE001
        print(f"Error reading upcoming snapshot: {exc}")
        return []

    events = payload.get("events") or []
    # Snapshot may already be formatted; normalize to ISO-first rows then re-label.
    raw = []
    for event in events:
        iso = event.get("datetime") or event.get("date")
        if not iso:
            continue
        raw.append(
            {
                "date": iso,
                "datetime": iso,
                "team": event.get("team"),
                "sport": event.get("sport"),
                "opponent": event.get("opponent"),
                "type": event.get("type", "game"),
                "is_home": event.get("is_home", False),
            }
        )
    raw.sort(key=lambda item: item.get("datetime") or "")
    return _format_events(raw, limit)


def save_upcoming_snapshot(events: List[dict], source: str = "espn") -> str:
    """Persist upcoming events for serverless fallback."""
    os.makedirs(os.path.dirname(_SNAPSHOT_PATH), exist_ok=True)
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "events": events,
    }
    with open(_SNAPSHOT_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    return _SNAPSHOT_PATH


def fetch_upcoming_events(limit: int = 10, *, allow_snapshot: bool = True) -> List[dict]:
    """
    Return the next upcoming games across tracked teams.

    Prefer live ESPN. If ESPN fails/empty (common on Vercel), fall back to the
    committed snapshot under src/data/upcoming_events.json.
    """
    session = _session()
    upcoming: List[dict] = []
    errors: List[str] = []

    for team in ESPN_TEAMS:
        try:
            upcoming.extend(_fetch_team_schedule(session, team))
        except Exception as exc:  # noqa: BLE001 - keep endpoint resilient
            msg = f"{team['name']}: {exc}"
            errors.append(msg)
            print(f"Error fetching upcoming for {msg}")

    upcoming.sort(key=lambda item: item.get("date") or "")
    # Raw schedule rows use ISO in "date"; normalize for formatter.
    raw = [
        {
            "date": event["date"],
            "datetime": event["date"],
            "team": event["team"],
            "sport": event["sport"],
            "opponent": event["opponent"],
            "type": event.get("type", "game"),
            "is_home": event["is_home"],
        }
        for event in upcoming
    ]
    formatted = _format_events(raw, limit)

    if formatted:
        return formatted

    if errors:
        print(f"Upcoming events empty after errors: {errors}")

    if allow_snapshot:
        snapshot = load_upcoming_snapshot(limit=limit)
        if snapshot:
            print(f"Using upcoming snapshot ({len(snapshot)} events)")
            return snapshot

    return []
