"""
Vercel serverless function for /api/teams
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
            teams_data = []
            
            # Get team data
            for team in calc.teams:
                team_result = team.calculate_depression()
                teams_data.append({
                    "name": team.name,
                    "sport": team.sport,
                    "wins": team.wins,
                    "losses": team.losses,
                    "ties": getattr(team, 'ties', 0),
                    "record": f"{team.wins}-{team.losses}" + (f"-{team.ties}" if hasattr(team, 'ties') and team.ties > 0 else ""),
                    "win_percentage": round(team_result.get("win_pct", 0) * 100, 1),
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
            
            response = json_response({
                "success": True,
                "teams": teams_data,
                "timestamp": datetime.now().isoformat()
            })
            
            self.send_response(response['statusCode'])
            for key, value in response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response['body'].encode())
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in get_teams: {error_details}")
            response = error_response(e, 500, error_details)
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





