"""
Vercel serverless function for /api/recent-games
"""
from http.server import BaseHTTPRequestHandler
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _utils import get_calculator, json_response, error_response

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request"""
        try:
            calc = get_calculator()
            games = []
            
            # Try to fetch enhanced game data from APIs
            from sports_api import SportsDataFetcher
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
                    except Exception as e:
                        # Fallback to basic data if detailed fetch fails
                        pass
                    
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
            
            response = json_response({
                "success": True,
                "games": games[:20],  # Last 20 events
                "timestamp": datetime.now().isoformat()
            })
            
            self.send_response(response['statusCode'])
            for key, value in response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response['body'].encode())
            
        except Exception as e:
            import traceback
            response = error_response(e, 500, traceback.format_exc())
            self.send_response(response['statusCode'])
            for key, value in response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response['body'].encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()



