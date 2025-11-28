#!/usr/bin/env python3
"""
Automated data fetching script
Runs on schedule to update teams_config.json with latest sports data
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sports_api import SportsDataFetcher

def main():
    """Fetch all sports data and update config file"""
    config_path = os.path.join(os.path.dirname(__file__), "teams_config.json")
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting data fetch...")
    
    try:
        fetcher = SportsDataFetcher()
        fetcher.update_config_file(config_path)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Data fetch complete!")
        return 0
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
