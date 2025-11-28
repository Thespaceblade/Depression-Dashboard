#!/usr/bin/env python3
"""
Automatic Daily Update Script
Fetches latest scores and calculates depression level
Run this every evening via cron/scheduled task
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add current directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

def main():
    """Main update function"""
    print("=" * 60)
    print(f"  AUTOMATIC DEPRESSION UPDATE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    try:
        # Import modules
        from sports_api import SportsDataFetcher
        from depression_calculator import DepressionCalculator
        
        # Change to script directory
        os.chdir(script_dir)
        
        config_path = "teams_config.json"
        
        # Fetch latest data
        print("Fetching latest scores from APIs...")
        fetcher = SportsDataFetcher()
        fetcher.update_config_file(config_path)
        print()
        
        # Calculate depression
        print("Calculating depression level...")
        calc = DepressionCalculator(config_path)
        report = calc.generate_report()
        print(report)
        
        # Save report to file
        report_file = script_dir / "depression_reports" / f"depression_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\nReport saved to: {report_file}")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

