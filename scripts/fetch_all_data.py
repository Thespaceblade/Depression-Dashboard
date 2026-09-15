#!/usr/bin/env python3
"""
Automated data fetching script
Runs on schedule to update teams_config.json with latest sports data
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from src.sports_api import SportsDataFetcher
from src.upcoming_schedule import fetch_upcoming_events, save_upcoming_snapshot
from src.recent_games import fetch_recent_games, save_recent_snapshot


def main():
    """Fetch all sports data and update config file"""
    config_path = os.path.join(parent_dir, "teams_config.json")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting data fetch...")

    try:
        fetcher = SportsDataFetcher()
        fetcher.update_config_file(config_path)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Data fetch complete!")

        # Belt-and-suspenders: Vercel reads src/data/teams_config.json (includeFiles src/**).
        mirror_path = os.path.join(parent_dir, "src", "data", "teams_config.json")
        try:
            import shutil

            os.makedirs(os.path.dirname(mirror_path), exist_ok=True)
            shutil.copy2(config_path, mirror_path)
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"✅ Synced Vercel mirror -> {mirror_path}"
            )
        except Exception as mirror_err:  # noqa: BLE001
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"⚠️  Failed to sync teams_config mirror: {mirror_err}"
            )

        # Refresh upcoming snapshot for Vercel (live ESPN often blocked there).
        try:
            events = fetch_upcoming_events(limit=15, allow_snapshot=False)
            if events:
                path = save_upcoming_snapshot(events, source="espn")
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"✅ Upcoming snapshot ({len(events)} events) -> {path}"
                )
            else:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    "⚠️  Live upcoming fetch empty; leaving existing snapshot unchanged"
                )
        except Exception as upcoming_err:  # noqa: BLE001
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"⚠️  Upcoming snapshot refresh failed: {upcoming_err}"
            )

        # Refresh recent-games snapshot for Vercel (same ESPN IP-block problem).
        try:
            games = fetch_recent_games(limit=20, per_team=5, allow_snapshot=False)
            if games:
                path = save_recent_snapshot(games, source="espn")
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"✅ Recent snapshot ({len(games)} games) -> {path}"
                )
            else:
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    "⚠️  Live recent fetch empty; leaving existing snapshot unchanged"
                )
        except Exception as recent_err:  # noqa: BLE001
            print(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"⚠️  Recent snapshot refresh failed: {recent_err}"
            )

        return 0
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error fetching data: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
