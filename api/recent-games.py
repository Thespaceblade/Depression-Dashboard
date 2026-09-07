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
            
            # Try to fetch enhanced game data from APIs (optional - may not be available)
            fetcher = None
            try:
                from src.sports_api import SportsDataFetcher
                fetcher = SportsDataFetcher()
            except Exception as import_error:
                # Sports API unavailable — return only real detailed games (none in this case)
                print(f"⚠️ Sports API not available: {import_error}")
                fetcher = None
            
            # Process team games with real detailed data only
            for team in calc.teams:
                detailed_games = []
                if fetcher:
                    try:
                        if team.sport == 'NFL':
                            detailed_games = fetcher.nfl.get_recent_games_detailed(team.name, 5)
                        elif team.sport == 'NBA':
                            detailed_games = fetcher.nba.get_recent_games_detailed(team.name, 5)
                        elif team.sport == 'NCAA Basketball':
                            detailed_games = fetcher.college_bball.get_recent_games_detailed(team.name, 5)
                        elif team.sport == 'NCAA Football':
                            detailed_games = fetcher.college_football.get_recent_games_detailed(team.name, 5)
                        elif team.sport == 'MLB':
                            # MLB detailed helper may not exist on all versions
                            mlb = getattr(fetcher, 'mlb', None)
                            getter = getattr(mlb, 'get_recent_games_detailed', None) if mlb else None
                            if getter:
                                detailed_games = getter(team.name, 5)
                    except Exception as e:
                        print(f"⚠️ Failed to fetch detailed games for {team.name} ({team.sport}): {e}")
                        detailed_games = []

                # Only include real detailed games. Do not invent dates/opponents
                # from recent_streak — that produced misleading synthetic timeline rows.
                if not detailed_games:
                    continue

                for game in detailed_games:
                    opponent = (game.get('opponent') or '').strip()
                    game_date = game.get('date', '')
                    # Skip incomplete rows that would look like placeholder data
                    if not opponent or opponent.lower() == 'unknown' or not game_date:
                        continue

                    is_rivalry = opponent.lower() in [r.lower() for r in team.rivals]

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
                    except Exception:
                        date_str = game_date

                    games.append({
                        "date": date_str,
                        "datetime": game_date,
                        "team": team.name,
                        "sport": team.sport,
                        "result": game.get('result', '?'),
                        "type": "game",
                        "opponent": opponent,
                        "team_score": game.get('team_score', 0),
                        "opponent_score": game.get('opponent_score', 0),
                        "score_margin": game.get('score_margin', 0),
                        "is_home": game.get('is_home', False),
                        "is_overtime": game.get('is_overtime', False),
                        "is_rivalry": is_rivalry
                    })

            # Sort by datetime when available
            def sort_key(game):
                dt = game.get('datetime', '')
                if dt:
                    try:
                        from dateutil import parser as date_parser
                        return date_parser.parse(dt)
                    except Exception:
                        pass
                return datetime.min

            games.sort(key=sort_key, reverse=True)

            response = json_response({
                "success": True,
                "games": games[:20],  # Last 20 real events
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





