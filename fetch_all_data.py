#!/usr/bin/env python3
"""
Daily Data Fetching Script
Fetches all sports data and updates the config file
Designed to run daily via cron or scheduled task
"""

import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sports_api import SportsDataFetcher
from depression_calculator import DepressionCalculator

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"data_fetch_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def fetch_fantasy_data(config_path: str):
    """Fetch fantasy team data from ESPN API"""
    try:
        from espn_fantasy import ESPNFantasyClient
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        fantasy_data = config.get("fantasy_team", {})
        espn_config = fantasy_data.get("espn", {})
        
        if espn_config.get("league_id") and espn_config.get("year"):
            logger.info("Fetching fantasy data from ESPN...")
            client = ESPNFantasyClient(
                league_id=espn_config["league_id"],
                year=espn_config["year"],
                team_id=espn_config.get("team_id"),
                team_name=espn_config.get("team_name") or fantasy_data.get("name"),
                espn_s2=espn_config.get("espn_s2"),
                swid=espn_config.get("swid")
            )
            
            team_data = client.get_my_team()
            
            # Update config
            fantasy_data["name"] = team_data["name"]
            fantasy_data["record"] = {
                "wins": team_data["wins"],
                "losses": team_data["losses"],
                "ties": team_data.get("ties", 0)
            }
            fantasy_data["recent_streak"] = team_data.get("recent_streak", [])
            
            logger.info(f"✓ Fantasy team '{team_data['name']}': {team_data['record']}")
            return True
    except ImportError:
        logger.warning("ESPN Fantasy API not available")
    except Exception as e:
        logger.error(f"Error fetching fantasy data: {e}")
    return False


def fetch_all_sports_data(config_path: str = "teams_config.json"):
    """
    Fetch all sports data and update config file
    Returns: (success: bool, summary: dict)
    """
    logger.info("=" * 60)
    logger.info("Starting daily data fetch")
    logger.info("=" * 60)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "successful": [],
        "failed": [],
        "skipped": []
    }
    
    try:
        # Load current config
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Fetch from sports APIs
        logger.info("\n--- Fetching Sports Data ---")
        fetcher = SportsDataFetcher()
        data = fetcher.fetch_all_data()
        
        # Update Cowboys
        if data.get('cowboys'):
            try:
                for team in config['teams']:
                    if 'cowboys' in team['name'].lower() and team['sport'] == 'NFL':
                        team['record']['wins'] = data['cowboys']['wins']
                        team['record']['losses'] = data['cowboys']['losses']
                        team['record']['ties'] = data['cowboys'].get('ties', 0)
                        if 'recent_games' in data['cowboys']:
                            team['recent_streak'] = data['cowboys']['recent_games']
                        summary["successful"].append("Cowboys (NFL)")
                        logger.info(f"✓ Cowboys: {data['cowboys']['wins']}-{data['cowboys']['losses']}-{data['cowboys'].get('ties', 0)}")
            except Exception as e:
                summary["failed"].append(f"Cowboys: {e}")
                logger.error(f"✗ Cowboys: {e}")
        
        # Update Mavericks
        if data.get('mavericks'):
            try:
                for team in config['teams']:
                    if 'mavericks' in team['name'].lower() and team['sport'] == 'NBA':
                        team['record']['wins'] = data['mavericks']['wins']
                        team['record']['losses'] = data['mavericks']['losses']
                        if 'recent_games' in data['mavericks']:
                            team['recent_streak'] = data['mavericks']['recent_games']
                        summary["successful"].append("Mavericks (NBA)")
                        logger.info(f"✓ Mavericks: {data['mavericks']['wins']}-{data['mavericks']['losses']}")
            except Exception as e:
                summary["failed"].append(f"Mavericks: {e}")
                logger.error(f"✗ Mavericks: {e}")
        
        # Update Warriors
        if data.get('warriors'):
            try:
                for team in config['teams']:
                    if 'warriors' in team['name'].lower() and team['sport'] == 'NBA':
                        team['record']['wins'] = data['warriors']['wins']
                        team['record']['losses'] = data['warriors']['losses']
                        if 'recent_games' in data['warriors']:
                            team['recent_streak'] = data['warriors']['recent_games']
                        summary["successful"].append("Warriors (NBA)")
                        logger.info(f"✓ Warriors: {data['warriors']['wins']}-{data['warriors']['losses']}")
            except Exception as e:
                summary["failed"].append(f"Warriors: {e}")
                logger.error(f"✗ Warriors: {e}")
        
        # Update Rangers
        if data.get('rangers'):
            try:
                for team in config['teams']:
                    if 'rangers' in team['name'].lower() and team['sport'] == 'MLB':
                        team['record']['wins'] = data['rangers']['wins']
                        team['record']['losses'] = data['rangers']['losses']
                        summary["successful"].append("Rangers (MLB)")
                        logger.info(f"✓ Rangers: {data['rangers']['wins']}-{data['rangers']['losses']}")
            except Exception as e:
                summary["failed"].append(f"Rangers: {e}")
                logger.error(f"✗ Rangers: {e}")
        
        # Update UNC Basketball
        if data.get('unc_basketball'):
            try:
                for team in config['teams']:
                    if 'tar heels' in team['name'].lower() and team['sport'] == 'NCAA Basketball':
                        team['record']['wins'] = int(data['unc_basketball']['wins'])
                        team['record']['losses'] = int(data['unc_basketball']['losses'])
                        if 'recent_games' in data['unc_basketball']:
                            team['recent_streak'] = data['unc_basketball']['recent_games']
                        summary["successful"].append("UNC Basketball")
                        logger.info(f"✓ UNC Basketball: {data['unc_basketball']['wins']}-{data['unc_basketball']['losses']}")
            except Exception as e:
                summary["failed"].append(f"UNC Basketball: {e}")
                logger.error(f"✗ UNC Basketball: {e}")
        
        # Update UNC Football
        if data.get('unc_football'):
            try:
                for team in config['teams']:
                    if 'tar heels' in team['name'].lower() and team['sport'] == 'NCAA Football':
                        team['record']['wins'] = int(data['unc_football']['wins'])
                        team['record']['losses'] = int(data['unc_football']['losses'])
                        if 'recent_games' in data['unc_football']:
                            team['recent_streak'] = data['unc_football']['recent_games']
                        summary["successful"].append("UNC Football")
                        logger.info(f"✓ UNC Football: {data['unc_football']['wins']}-{data['unc_football']['losses']}")
            except Exception as e:
                summary["failed"].append(f"UNC Football: {e}")
                logger.error(f"✗ UNC Football: {e}")
        
        # Update F1 (Verstappen)
        if data.get('verstappen'):
            try:
                if 'f1_driver' in config:
                    config['f1_driver']['championship_position'] = data['verstappen']['position']
                    if 'recent_races' in data['verstappen']:
                        config['f1_driver']['recent_races'] = data['verstappen']['recent_races']
                    dnf_count = sum(1 for r in data['verstappen'].get('recent_races', []) if r == 'DNF')
                    config['f1_driver']['recent_dnfs'] = dnf_count
                    summary["successful"].append("F1 (Verstappen)")
                    logger.info(f"✓ Verstappen: Position {data['verstappen']['position']}")
            except Exception as e:
                summary["failed"].append(f"F1: {e}")
                logger.error(f"✗ F1: {e}")
        else:
            summary["skipped"].append("F1 (API unavailable)")
            logger.warning("⚠ F1 data not available (API down)")
        
        # Fetch Fantasy data
        logger.info("\n--- Fetching Fantasy Data ---")
        if fetch_fantasy_data(config_path):
            summary["successful"].append("Fantasy Team")
        else:
            summary["skipped"].append("Fantasy Team (using cached data)")
        
        # Save updated config
        logger.info("\n--- Saving Config ---")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"✓ Config saved to {config_path}")
        
        # Calculate and log depression score
        logger.info("\n--- Calculating Depression Score ---")
        calc = DepressionCalculator(config_path)
        result = calc.calculate_total_depression()
        emoji, level = calc.get_depression_level(result["total_score"])
        logger.info(f"Depression Score: {result['total_score']:.1f}")
        logger.info(f"Level: {emoji} {level}")
        
        summary["depression_score"] = round(result["total_score"], 1)
        summary["depression_level"] = level
        summary["depression_emoji"] = emoji
        
        logger.info("\n" + "=" * 60)
        logger.info("Data fetch completed successfully!")
        logger.info("=" * 60)
        
        return True, summary
        
    except Exception as e:
        logger.error(f"Fatal error during data fetch: {e}", exc_info=True)
        summary["error"] = str(e)
        return False, summary


def main():
    """Main entry point"""
    config_path = os.environ.get("CONFIG_PATH", "teams_config.json")
    
    success, summary = fetch_all_sports_data(config_path)
    
    # Save summary to file
    summary_file = log_dir / f"fetch_summary_{datetime.now().strftime('%Y%m%d')}.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Exit with appropriate code for cron
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

