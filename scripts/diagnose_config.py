#!/usr/bin/env python3
"""
Diagnostic script to check config file and identify loading issues
"""

import json
import sys
from pathlib import Path

def diagnose_config(config_path: str = "teams_config.json"):
    """Diagnose config file issues"""
    print("=" * 60)
    print("CONFIG FILE DIAGNOSTIC")
    print("=" * 60)
    print()
    
    # Check if file exists
    if not Path(config_path).exists():
        print(f"❌ Config file not found: {config_path}")
        return False
    
    # Try to load JSON
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("✅ Config file is valid JSON")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        print(f"   Line {e.lineno}, Column {e.colno}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Check structure
    print("\nChecking structure...")
    if not isinstance(config, dict):
        print("❌ Config is not a dictionary")
        return False
    
    # Check required top-level keys
    required_keys = ["teams", "f1_driver", "fantasy_team"]
    for key in required_keys:
        if key not in config:
            print(f"⚠️  Missing top-level key: {key} (will use defaults)")
        else:
            print(f"✅ Found key: {key}")
    
    # Check teams
    print("\nChecking teams...")
    teams = config.get("teams", [])
    if not isinstance(teams, list):
        print("❌ 'teams' is not a list")
        return False
    
    print(f"   Found {len(teams)} teams")
    
    for i, team in enumerate(teams):
        print(f"\n   Team {i+1}: {team.get('name', 'UNNAMED')}")
        
        # Required fields
        required = ["name", "sport", "record"]
        for field in required:
            if field not in team:
                print(f"      ❌ Missing required field: {field}")
            else:
                print(f"      ✅ Has field: {field}")
        
        # Check record structure
        if "record" in team:
            record = team["record"]
            if not isinstance(record, dict):
                print(f"      ❌ 'record' is not a dictionary")
            else:
                for field in ["wins", "losses"]:
                    if field not in record:
                        print(f"      ❌ Record missing: {field}")
                    else:
                        print(f"      ✅ Record has: {field} = {record[field]}")
                
                # Ties is optional but recommended for NFL
                if team.get("sport") == "NFL" and "ties" not in record:
                    print(f"      ⚠️  NFL team missing 'ties' field (will default to 0)")
                elif "ties" in record:
                    print(f"      ✅ Record has: ties = {record['ties']}")
    
    # Check F1 driver
    print("\nChecking F1 driver...")
    f1_data = config.get("f1_driver", {})
    if f1_data:
        required = ["name", "championship_position"]
        for field in required:
            if field not in f1_data:
                print(f"   ⚠️  Missing field: {field}")
            else:
                print(f"   ✅ Has field: {field}")
    else:
        print("   ⚠️  No F1 driver data (optional)")
    
    # Check fantasy team
    print("\nChecking fantasy team...")
    fantasy_data = config.get("fantasy_team", {})
    if fantasy_data:
        if "record" not in fantasy_data:
            print("   ⚠️  Missing 'record' field")
        else:
            record = fantasy_data["record"]
            if "wins" not in record or "losses" not in record:
                print("   ⚠️  Record missing wins/losses")
            else:
                print(f"   ✅ Record: {record.get('wins', 0)}-{record.get('losses', 0)}")
    else:
        print("   ⚠️  No fantasy team data (optional)")
    
    print("\n" + "=" * 60)
    print("✅ Config file structure looks good!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "teams_config.json"
    diagnose_config(config_path)

