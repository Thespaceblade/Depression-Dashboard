#!/usr/bin/env python3
"""
Flask API for Depression Dashboard
Serves depression calculator data to the frontend
"""

import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
from dateutil import parser as date_parser

# Add parent directory to path to import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.depression_calculator import DepressionCalculator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Global calculator instance
calculator = None

def get_calculator(force_reload=False):
    """Get or create calculator instance"""
    global calculator
    # Always reload from config file to ensure fresh data
    # Get path to config file in parent directory
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "teams_config.json")
    
    if force_reload or calculator is None:
        calculator = None  # Clear cache first
        calculator = DepressionCalculator(config_path, use_espn_api=True)
        # Log fantasy team status
        if calculator.fantasy_team:
            print(f"✅ Calculator loaded. Fantasy team: {calculator.fantasy_team.name} ({calculator.fantasy_team.wins}-{calculator.fantasy_team.losses})")
        else:
            print("⚠️  Calculator loaded but no fantasy team found")
    return calculator

@app.route('/api/depression', methods=['GET'])
def get_depression():
    """Get current depression score and breakdown"""
    try:
        calc = get_calculator()
        result = calc.calculate_total_depression()
        # Use total_score (0-100) for level calculation
        emoji, level = calc.get_depression_level(result["total_score"])
        
        return jsonify({
            "success": True,
            "score": round(result["total_score"], 1),  # Scaled score (0-100)
            "level": level,
            "emoji": emoji,
            "breakdown": result["breakdown"],
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in get_depression: {error_details}")
        return jsonify({
            "success": False,
            "error": str(e),
            "details": error_details
        }), 500

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all team data"""
    try:
        calc = get_calculator()
        teams_data = []
        
        # Get team data
        for team in calc.teams:
            team_result = team.calculate_depression()
            total_games = team.wins + team.losses + getattr(team, 'ties', 0)
            win_percentage = round((team.wins / total_games * 100), 1) if total_games > 0 else 0
            teams_data.append({
                "name": team.name,
                "sport": team.sport,
                "wins": team.wins,
                "losses": team.losses,
                "ties": getattr(team, 'ties', 0),
                "record": f"{team.wins}-{team.losses}" + (f"-{team.ties}" if hasattr(team, 'ties') and team.ties > 0 else ""),
                "win_percentage": win_percentage,
                "recent_streak": team.recent_streak,
                "depression_points": round(team_result["score"], 1),
                "breakdown": team_result["breakdown"],
                "expected_performance": team.expected_performance,
                "jasons_expectations": team.jasons_expectations,
                "rivals": team.rivals,
                "recent_rivalry_losses": team.recent_rivalry_losses,
                "interest_level": team.interest_level,
                "notes": team.notes
            })
        
        # Get F1 driver data
        if calc.f1_driver:
            f1_result = calc.f1_driver.calculate_depression()
            teams_data.append({
                "name": calc.f1_driver.name,
                "sport": "F1",
                "wins": calc.f1_driver.recent_races.count("W"),
                "losses": len([r for r in calc.f1_driver.recent_races if r not in ["W", "P2", "P3"]]),
                "record": f"P{calc.f1_driver.championship_position}",
                "win_percentage": (calc.f1_driver.recent_races.count("W") / len(calc.f1_driver.recent_races) * 100) if calc.f1_driver.recent_races else 0,
                "recent_streak": calc.f1_driver.recent_races,
                "depression_points": round(f1_result["score"], 1),
                "breakdown": f1_result["breakdown"],
                "championship_position": calc.f1_driver.championship_position,
                "recent_dnfs": calc.f1_driver.recent_dnfs,
                "expected_performance": calc.f1_driver.expected_performance,
                "jasons_expectations": calc.f1_driver.jasons_expectations,
                "notes": calc.f1_driver.notes
            })
        
        # Get fantasy team data
        if calc.fantasy_team:
            fantasy_result = calc.fantasy_team.calculate_depression()
            teams_data.append({
                "name": calc.fantasy_team.name,
                "sport": "Fantasy",
                "wins": calc.fantasy_team.wins,
                "losses": calc.fantasy_team.losses,
                "record": f"{calc.fantasy_team.wins}-{calc.fantasy_team.losses}",
                "win_percentage": round((calc.fantasy_team.wins / (calc.fantasy_team.wins + calc.fantasy_team.losses) * 100), 1) if (calc.fantasy_team.wins + calc.fantasy_team.losses) > 0 else 0,
                "recent_streak": calc.fantasy_team.recent_streak,
                "depression_points": round(fantasy_result["score"], 1),
                "breakdown": fantasy_result["breakdown"],
                "expected_performance": calc.fantasy_team.expected_performance,
                "jasons_expectations": calc.fantasy_team.jasons_expectations
            })
        else:
            # Debug: log why fantasy team is missing
            print("⚠️  Fantasy team is None in /api/teams endpoint")
            import json
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "teams_config.json")
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    fantasy_config = config.get('fantasy_team', {})
                    print(f"   Config has fantasy_team: {bool(fantasy_config)}")
                    print(f"   Config fantasy_team keys: {list(fantasy_config.keys())}")
                    espn_config = fantasy_config.get('espn', {})
                    print(f"   ESPN config present: {bool(espn_config)}")
                    if espn_config:
                        print(f"   ESPN league_id: {espn_config.get('league_id')}")
                        print(f"   ESPN year: {espn_config.get('year')}")
            except Exception as e:
                print(f"   Error reading config: {e}")
        
        return jsonify({
            "success": True,
            "teams": teams_data,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recent-games', methods=['GET'])
def get_recent_games():
    """Get recent games timeline with enhanced data"""
    try:
        from src.recent_games import fetch_recent_games_result

        result = fetch_recent_games_result(limit=20, per_team=5, allow_snapshot=True)
        payload = {
            "success": bool(result.get("success", True)),
            "games": result.get("games") or [],
            "count": len(result.get("games") or []),
            "source": result.get("source") or "none",
            "partial": bool(result.get("partial")),
            "timestamp": datetime.now().isoformat(),
        }
        if result.get("warning"):
            payload["warning"] = result["warning"]
        if result.get("errors"):
            payload["errors"] = result["errors"]
        return jsonify(payload)
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/upcoming-events', methods=['GET'])
def get_upcoming_events():
    """Get upcoming games, races, and events"""
    try:
        from src.upcoming_schedule import fetch_upcoming_events_result

        result = fetch_upcoming_events_result(limit=10, allow_snapshot=True)
        payload = {
            "success": bool(result.get("success", True)),
            "events": result.get("events") or [],
            "count": len(result.get("events") or []),
            "source": result.get("source") or "none",
            "partial": bool(result.get("partial")),
            "timestamp": datetime.now().isoformat(),
        }
        if result.get("warning"):
            payload["warning"] = result["warning"]
        if result.get("errors"):
            payload["errors"] = result["errors"]
        return jsonify(payload)
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Trigger data refresh from all APIs (sports + fantasy)"""
    global calculator  # Declare once at function start
    try:
        import subprocess
        import sys
        
        # Use the comprehensive fetch_all_data.py script
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "fetch_all_data.py")
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "teams_config.json")
        
        # Run the fetch script
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(script_path),
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        if result.returncode == 0:
            # Reload calculator to get fresh data
            calculator = None
            calc = get_calculator()
            
            return jsonify({
                "success": True,
                "refreshed": True,
                "mode": "live",
                "message": "Data refreshed successfully from all sources",
                "timestamp": datetime.now().isoformat(),
                "output": result.stdout[-500:] if result.stdout else ""  # Last 500 chars
            })
        else:
            # Script failed, but try to continue with existing data
            error_msg = result.stderr[-500:] if result.stderr else "Unknown error"
            return jsonify({
                "success": False,
                "error": f"Refresh script failed: {error_msg}",
                "timestamp": datetime.now().isoformat()
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": "Refresh timed out after 2 minutes"
        }), 500
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in refresh_data: {error_details}")
        
        # Fallback: try basic refresh without fantasy
        try:
            from src.sports_api import SportsDataFetcher
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "teams_config.json")
            fetcher = SportsDataFetcher()
            fetcher.update_config_file(config_path)
            
            calculator = None
            calc = get_calculator()
            
            return jsonify({
                "success": True,
                "refreshed": True,
                "mode": "live",
                "message": "Data refreshed (basic refresh, fantasy skipped)",
                "timestamp": datetime.now().isoformat(),
                "warning": str(e)
            })
        except Exception as e2:
            return jsonify({
                "success": False,
                "error": f"Refresh failed: {str(e)}"
        }), 500

@app.route('/api/reload', methods=['POST'])
def reload_calculator():
    """Force reload the calculator from config file (doesn't fetch from APIs)"""
    global calculator
    try:
        calculator = None  # Clear cache
        calc = get_calculator(force_reload=True)
        
        fantasy_info = "None"
        if calc.fantasy_team:
            fantasy_info = f"{calc.fantasy_team.name} ({calc.fantasy_team.wins}-{calc.fantasy_team.losses})"
        
        return jsonify({
            "success": True,
            "message": "Calculator reloaded from config file",
            "fantasy_team": fantasy_info,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in reload_calculator: {error_details}")
        return jsonify({
            "success": False,
            "error": str(e),
            "details": error_details
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - lists available API endpoints"""
    return jsonify({
        "message": "Depression Dashboard API",
        "version": "1.0",
        "endpoints": {
            "health": "/api/health",
            "depression": "/api/depression",
            "teams": "/api/teams",
            "recent_games": "/api/recent-games",
            "upcoming_events": "/api/upcoming-events",
            "refresh": "/api/refresh (POST)"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Get port from environment variable (for production) or use default
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, port=port, host='0.0.0.0')

