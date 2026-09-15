"""
Vercel serverless function for /api/teams
"""
from http.server import BaseHTTPRequestHandler
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _utils import get_calculator, json_response, error_response, _team_payload


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request"""
        try:
            calc = get_calculator()
            teams_data = []

            for team in calc.teams:
                team_result = team.calculate_depression()
                teams_data.append(_team_payload(team, team_result))

            if calc.f1_driver:
                f1_result = calc.f1_driver.calculate_depression()
                MIN_RAW, MAX_RAW = -50.0, 100.0
                raw = float(f1_result.get("score") or 0)
                scaled = max(0.0, min(100.0, ((raw - MIN_RAW) / (MAX_RAW - MIN_RAW)) * 100.0))
                mood_impact = abs(scaled - 50.0)
                teams_data.append({
                    "name": calc.f1_driver.name,
                    "sport": "F1",
                    "wins": calc.f1_driver.recent_races.count("W"),
                    "losses": len([r for r in calc.f1_driver.recent_races if r not in ["W", "P2", "P3"]]),
                    "record": f"P{calc.f1_driver.championship_position}",
                    "win_percentage": (
                        calc.f1_driver.recent_races.count("W") / len(calc.f1_driver.recent_races) * 100
                        if calc.f1_driver.recent_races else 0
                    ),
                    "recent_streak": calc.f1_driver.recent_races,
                    "depression_points": round(raw, 1),
                    "scaled_score": round(scaled, 1),
                    "mood_impact": round(mood_impact, 2),
                    "recency_factor": 1.0,
                    "from_prior_season": None,
                    "is_offseason": False,
                    "breakdown": f1_result.get("breakdown", {}),
                    "championship_position": calc.f1_driver.championship_position,
                    "recent_dnfs": calc.f1_driver.recent_dnfs,
                    "expected_performance": calc.f1_driver.expected_performance,
                    "jasons_expectations": calc.f1_driver.jasons_expectations,
                    "notes": calc.f1_driver.notes,
                })

            if calc.fantasy_team:
                fantasy_result = calc.fantasy_team.calculate_depression()
                MIN_RAW, MAX_RAW = -50.0, 100.0
                raw = float(fantasy_result.get("score") or 0)
                scaled = max(0.0, min(100.0, ((raw - MIN_RAW) / (MAX_RAW - MIN_RAW)) * 100.0))
                mood_impact = abs(scaled - 50.0)
                teams_data.append({
                    "name": calc.fantasy_team.name,
                    "sport": "Fantasy",
                    "wins": calc.fantasy_team.wins,
                    "losses": calc.fantasy_team.losses,
                    "record": f"{calc.fantasy_team.wins}-{calc.fantasy_team.losses}",
                    "win_percentage": round(
                        (calc.fantasy_team.wins / (calc.fantasy_team.wins + calc.fantasy_team.losses) * 100), 1
                    ) if (calc.fantasy_team.wins + calc.fantasy_team.losses) else 0,
                    "recent_streak": calc.fantasy_team.recent_streak,
                    "depression_points": round(raw, 1),
                    "scaled_score": round(scaled, 1),
                    "mood_impact": round(mood_impact, 2),
                    "recency_factor": 1.0,
                    "from_prior_season": None,
                    "is_offseason": False,
                    "breakdown": fantasy_result.get("breakdown", {}),
                    "expected_performance": calc.fantasy_team.expected_performance,
                    "jasons_expectations": calc.fantasy_team.jasons_expectations,
                })

            # Highest mood impact first — what is actually moving Jason's state
            teams_data.sort(key=lambda t: t.get("mood_impact") or 0, reverse=True)

            response = json_response({
                "success": True,
                "teams": teams_data,
                "timestamp": datetime.now().isoformat(),
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
