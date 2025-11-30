#!/usr/bin/env python3
"""
Fetch all sports data and update teams_config.json
This script is used by:
- GitHub Actions (runs every 6 hours, commits updates to repo)
- Render cron jobs (runs every 6 hours)
- Backend /api/refresh endpoint (manual trigger)
- Local cron jobs (manual setup)
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.sports_api import SportsDataFetcher

def main():
    """Fetch data and update config"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "teams_config.json"
    )
    
    print(f"Fetching sports data and updating {config_path}...")
    
    try:
        fetcher = SportsDataFetcher()
        fetcher.update_config_file(config_path)
        print("✓ Data fetched and config updated successfully!")
        return 0
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

