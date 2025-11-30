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
        calc = get_calculator()
        games = []
        
        # Try to fetch enhanced game data from APIs
        from src.sports_api import SportsDataFetcher
        fetcher = SportsDataFetcher()
        
        # Process team games with enhanced data
        for team in calc.teams:
            if team.recent_streak:
                # Try to get detailed game data
                detailed_games = []
                try:
                    if team.sport == 'NFL':
                        detailed_games = fetcher.nfl.get_recent_games_detailed(team.name, 5)
                    elif team.sport == 'NBA':
                        detailed_games = fetcher.nba.get_recent_games_detailed(team.name, 5)
                    elif team.sport == 'NCAA Basketball':
                        detailed_games = fetcher.college_bball.get_recent_games_detailed(team.name, 5)
                    elif team.sport == 'NCAA Football':
                        detailed_games = fetcher.college_football.get_recent_games_detailed(team.name, 5)
                except Exception as e:
                    # Fallback to basic data if detailed fetch fails
                    print(f"Warning: Failed to fetch detailed games for {team.name} ({team.sport}): {e}")
                    import traceback
                    traceback.print_exc()
                
                # Use detailed data if available, otherwise use basic
                if detailed_games:
                    for game in detailed_games:
                        # Check if this is a rivalry game
                        is_rivalry = game.get('opponent', '').lower() in [r.lower() for r in team.rivals]
                        
                        # Format date
                        game_date = game.get('date', '')
                        if game_date:
                            try:
                                from dateutil import parser as date_parser
                                parsed_date = date_parser.parse(game_date)
                                now = datetime.now(parsed_date.tzinfo) if parsed_date.tzinfo else datetime.now()
                                days_ago = (now.date() - parsed_date.date()).days
                                if days_ago == 0:
                                    date_str = "Today"
                                elif days_ago == 1:
                                    date_str = "Yesterday"
                                else:
                                    date_str = f"{days_ago} days ago"
                            except:
                                date_str = game_date
                        else:
                            date_str = "Unknown date"
                        
                        games.append({
                            "date": date_str,
                            "datetime": game_date,
                            "team": team.name,
                            "sport": team.sport,
                            "result": game.get('result', '?'),
                            "type": "game",
                            "opponent": game.get('opponent', 'Unknown'),
                            "team_score": game.get('team_score', 0),
                            "opponent_score": game.get('opponent_score', 0),
                            "score_margin": game.get('score_margin', 0),
                            "is_home": game.get('is_home', False),
                            "is_overtime": game.get('is_overtime', False),
                            "is_rivalry": is_rivalry
                        })
                else:
                    # Fallback to basic data
                    for i, result in enumerate(team.recent_streak[:5]):
                        games.append({
                            "date": f"{len(team.recent_streak) - i} days ago",
                            "datetime": "",
                            "team": team.name,
                            "sport": team.sport,
                            "result": result,
                            "type": "game",
                            "opponent": "Unknown",
                            "team_score": 0,
                            "opponent_score": 0,
                            "score_margin": 0,
                            "is_home": False,
                            "is_overtime": False,
                            "is_rivalry": False
                        })
        
        # Process F1 races
        if calc.f1_driver and calc.f1_driver.recent_races:
            for i, result in enumerate(calc.f1_driver.recent_races[:5]):
                games.append({
                    "date": f"{len(calc.f1_driver.recent_races) - i} races ago",
                    "datetime": "",
                    "team": calc.f1_driver.name,
                    "sport": "F1",
                    "result": result,
                    "type": "race",
                    "opponent": "",
                    "team_score": 0,
                    "opponent_score": 0,
                    "score_margin": 0,
                    "is_home": False,
                    "is_overtime": False,
                    "is_rivalry": False
                })
        
        # Process fantasy games
        if calc.fantasy_team and calc.fantasy_team.recent_streak:
            for i, result in enumerate(calc.fantasy_team.recent_streak[:5]):
                games.append({
                    "date": f"Week {len(calc.fantasy_team.recent_streak) - i}",
                    "datetime": "",
                    "team": calc.fantasy_team.name,
                    "sport": "Fantasy",
                    "result": result,
                    "type": "fantasy",
                    "opponent": "",
                    "team_score": 0,
                    "opponent_score": 0,
                    "score_margin": 0,
                    "is_home": False,
                    "is_overtime": False,
                    "is_rivalry": False
                })
        
        # Sort by datetime if available, otherwise by date string
        def sort_key(game):
            dt = game.get('datetime', '')
            if dt:
                try:
                    from dateutil import parser as date_parser
                    return date_parser.parse(dt)
                except:
                    pass
            return datetime.min
        
        games.sort(key=sort_key, reverse=True)
        
        return jsonify({
            "success": True,
            "games": games[:20],  # Last 20 events
            "timestamp": datetime.now().isoformat()
        })
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
        from src.sports_api import SportsDataFetcher
        fetcher = SportsDataFetcher()
        upcoming_events = []
        
        # Get upcoming NFL games (Cowboys)
        try:
            team_id = 6  # Cowboys
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
            response = fetcher.nfl.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                for event in events:
                    competitions = event.get('competitions', [])
                    if competitions:
                        comp = competitions[0]
                        status = comp.get('status', {})
                        status_type = status.get('type', {})
                        completed = status_type.get('completed', False)
                        
                        if not completed:  # Upcoming game
                            date_str = event.get('date', '')
                            competitors = comp.get('competitors', [])
                            if len(competitors) == 2:
                                away = next((c for c in competitors if not c.get('homeAway') == 'home'), None)
                                home = next((c for c in competitors if c.get('homeAway') == 'home'), None)
                                opponent = away.get('team', {}).get('displayName') if home and home.get('team', {}).get('id') == str(team_id) else home.get('team', {}).get('displayName') if away and away.get('team', {}).get('id') == str(team_id) else None
                                
                                if opponent:
                                    upcoming_events.append({
                                        "date": date_str,
                                        "team": "Dallas Cowboys",
                                        "sport": "NFL",
                                        "opponent": opponent,
                                        "type": "game",
                                        "is_home": home and home.get('team', {}).get('id') == str(team_id) if home else False
                                    })
        except Exception as e:
            print(f"Error fetching upcoming NFL games: {e}")
        
        # Get upcoming NBA games (Mavericks)
        try:
            team_id = 6  # Mavericks
            url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule"
            response = fetcher.nba.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                for event in events:
                    competitions = event.get('competitions', [])
                    if competitions:
                        comp = competitions[0]
                        status = comp.get('status', {})
                        status_type = status.get('type', {})
                        completed = status_type.get('completed', False)
                        
                        if not completed:
                            date_str = event.get('date', '')
                            competitors = comp.get('competitors', [])
                            if len(competitors) == 2:
                                away = next((c for c in competitors if c.get('homeAway') == 'away'), None)
                                home = next((c for c in competitors if c.get('homeAway') == 'home'), None)
                                opponent = away.get('team', {}).get('displayName') if home and home.get('team', {}).get('id') == str(team_id) else home.get('team', {}).get('displayName') if away and away.get('team', {}).get('id') == str(team_id) else None
                                
                                if opponent:
                                    upcoming_events.append({
                                        "date": date_str,
                                        "team": "Dallas Mavericks",
                                        "sport": "NBA",
                                        "opponent": opponent,
                                        "type": "game",
                                        "is_home": home and home.get('team', {}).get('id') == str(team_id) if home else False
                                    })
        except Exception as e:
            print(f"Error fetching upcoming NBA games: {e}")
        
        # Get upcoming NBA games (Warriors)
        try:
            team_id = 9  # Warriors
            url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule"
            response = fetcher.nba.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                for event in events:
                    competitions = event.get('competitions', [])
                    if competitions:
                        comp = competitions[0]
                        status = comp.get('status', {})
                        status_type = status.get('type', {})
                        completed = status_type.get('completed', False)
                        
                        if not completed:
                            date_str = event.get('date', '')
                            competitors = comp.get('competitors', [])
                            if len(competitors) == 2:
                                away = next((c for c in competitors if c.get('homeAway') == 'away'), None)
                                home = next((c for c in competitors if c.get('homeAway') == 'home'), None)
                                opponent = away.get('team', {}).get('displayName') if home and home.get('team', {}).get('id') == str(team_id) else home.get('team', {}).get('displayName') if away and away.get('team', {}).get('id') == str(team_id) else None
                                
                                if opponent:
                                    upcoming_events.append({
                                        "date": date_str,
                                        "team": "Golden State Warriors",
                                        "sport": "NBA",
                                        "opponent": opponent,
                                        "type": "game",
                                        "is_home": home and home.get('team', {}).get('id') == str(team_id) if home else False
                                    })
        except Exception as e:
            print(f"Error fetching upcoming Warriors games: {e}")
        
        # Sort by date (upcoming first)
        upcoming_events.sort(key=lambda x: x.get("date", ""))
        
        # Format dates and limit to next 10 events
        formatted_events = []
        for event in upcoming_events[:10]:
            try:
                event_date = date_parser.parse(event["date"])
                now = datetime.now(event_date.tzinfo) if event_date.tzinfo else datetime.now()
                days_until = (event_date.date() - now.date()).days
                
                if days_until >= 0:
                    if days_until == 0:
                        date_str = "Today"
                    elif days_until == 1:
                        date_str = "Tomorrow"
                    else:
                        date_str = f"In {days_until} days"
                    
                    formatted_events.append({
                        "date": date_str,
                        "datetime": event["date"],
                        "team": event["team"],
                        "sport": event["sport"],
                        "opponent": event.get("opponent", "TBD"),
                        "type": event["type"],
                        "is_home": event.get("is_home", False)
                    })
            except Exception as e:
                print(f"Error formatting date: {e}")
        
        return jsonify({
            "success": True,
            "events": formatted_events,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
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

