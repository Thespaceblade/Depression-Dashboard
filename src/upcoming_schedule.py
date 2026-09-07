"""
Fetch upcoming games from ESPN public schedule APIs.

Kept dependency-light (requests only) so Vercel serverless can call ESPN
without importing the heavier SportsDataFetcher stack.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests

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
    session = requests.Session()
    # Full Chrome UAs get HTTP 403 from ESPN; keep the lightweight bot-style UA.
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (compatible; DepressionDashboard/1.0)",
            "Accept": "application/json",
        }
    )
    return session


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
    url = (
        f"https://site.api.espn.com/apis/site/v2/sports/"
        f"{team['path']}/teams/{team['team_id']}/schedule"
    )
    response = session.get(url, timeout=8)
    if response.status_code != 200:
        print(f"Upcoming schedule HTTP {response.status_code} for {team['name']}: {url}")
        return []

    events = response.json().get("events") or []
    parsed: List[dict] = []
    for event in events:
        item = _parse_event(event, team["name"], team["sport"], team["team_id"])
        if item:
            parsed.append(item)
    return parsed


def fetch_upcoming_events(limit: int = 10) -> List[dict]:
    """Return the next upcoming games across tracked teams."""
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

    if date_parser is None:
        # Without dateutil, return raw ISO dates for the soonest items.
        formatted = []
        for event in upcoming[:limit]:
            formatted.append(
                {
                    "date": event["date"],
                    "datetime": event["date"],
                    "team": event["team"],
                    "sport": event["sport"],
                    "opponent": event["opponent"],
                    "type": event["type"],
                    "is_home": event["is_home"],
                }
            )
        return formatted

    now = datetime.now(timezone.utc)
    formatted = []
    for event in upcoming:
        try:
            event_dt = date_parser.parse(event["date"])
            if event_dt.tzinfo is None:
                event_dt = event_dt.replace(tzinfo=timezone.utc)
            now_cmp = now.astimezone(event_dt.tzinfo)
            label = _relative_date_label(event_dt, now_cmp)
            if label is None:
                continue
            formatted.append(
                {
                    "date": label,
                    "datetime": event["date"],
                    "team": event["team"],
                    "sport": event["sport"],
                    "opponent": event["opponent"],
                    "type": event["type"],
                    "is_home": event["is_home"],
                }
            )
        except Exception as exc:  # noqa: BLE001
            print(f"Error formatting upcoming date: {exc}")

        if len(formatted) >= limit:
            break

    if errors and not formatted:
        print(f"Upcoming events empty after errors: {errors}")

    return formatted
