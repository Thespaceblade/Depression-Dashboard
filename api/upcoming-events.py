"""
Vercel serverless function for /api/upcoming-events
"""
from http.server import BaseHTTPRequestHandler
import sys
import os
from datetime import datetime
from dateutil import parser as date_parser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _utils import json_response, error_response

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request"""
        try:
            from sports_api import SportsDataFetcher
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
            
            response = json_response({
                "success": True,
                "events": formatted_events,
                "timestamp": datetime.now().isoformat()
            })
            
            self.send_response(response['statusCode'])
            for key, value in response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response['body'].encode())
            
        except Exception as e:
            response = error_response(e, 500)
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

