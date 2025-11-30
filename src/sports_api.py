#!/usr/bin/env python3
"""
Sports API Integration Module
Fetches scores and data from various sports APIs
"""

import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import json


class SportsAPI:
    """Base class for sports API integrations"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_team_record(self, team_name: str, sport: str) -> Optional[Dict]:
        """Get current record for a team"""
        raise NotImplementedError


class NFLAPI(SportsAPI):
    """NFL API using ESPN's public API"""
    
    def __init__(self):
        super().__init__()
        # ESPN team IDs: Dallas Cowboys = 6 (NOT 2!)
        self.team_ids = {
            'dallas cowboys': 6,
            'cowboys': 6
        }
    
    def get_team_record(self, team_name: str) -> Optional[Dict]:
        """Get Cowboys record from ESPN API"""
        try:
            # Use ESPN's public API
            team_id = self.team_ids.get(team_name.lower(), None)
            if not team_id:
                # Try to find by name
                if 'dallas' in team_name.lower() and 'cowboys' in team_name.lower():
                    team_id = 6  # Correct ID for Dallas Cowboys
                else:
                    return None
            
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                team = data.get('team', {})
                record = team.get('record', {})
                items = record.get('items', [])
                
                if items:
                    # Find the "total" record (overall record, not home/away)
                    total_record = next((item for item in items if item.get('type') == 'total'), items[0])
                    stats = total_record.get('stats', [])
                    wins = next((int(s['value']) for s in stats if s['name'] == 'wins'), 0)
                    losses = next((int(s['value']) for s in stats if s['name'] == 'losses'), 0)
                    ties = next((int(s['value']) for s in stats if s['name'] == 'ties'), 0)
                    
                    return {
                        'wins': wins,
                        'losses': losses,
                        'ties': ties,
                        'win_percentage': wins / (wins + losses + ties) if (wins + losses + ties) > 0 else 0
                    }
        except Exception as e:
            print(f"Error fetching NFL data: {e}")
            return None
        return None
    
    def get_recent_games(self, team_name: str, num_games: int = 5) -> List[str]:
        """Get recent game results (W/L/T) from ESPN"""
        game_data = self.get_recent_games_detailed(team_name, num_games)
        return [game['result'] for game in game_data]
    
    def get_recent_games_detailed(self, team_name: str, num_games: int = 5) -> List[Dict]:
        """Get recent game results with detailed data (dates, scores, opponents, home/away)"""
        try:
            team_id = self.team_ids.get(team_name.lower(), 6)  # Default to Cowboys (ID 6)
            
            # Use schedule endpoint instead of events
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                results = []
                
                # Process all events, filter completed ones
                for event in events:
                    # Check if game is completed - check competition status
                    competitions = event.get('competitions', [])
                    if not competitions:
                        continue
                    
                    comp = competitions[0]
                    comp_status = comp.get('status', {}).get('type', {})
                    status_name = comp_status.get('name', '').upper() if isinstance(comp_status, dict) else str(comp_status).upper()
                    
                    # Game is completed if it has scores and status indicates completion
                    competitors = comp.get('competitors', [])
                    if len(competitors) != 2:
                        continue
                    
                    # Check if both teams have scores (game has been played)
                    team1_score_obj = competitors[0].get('score')
                    team2_score_obj = competitors[1].get('score')
                    
                    # Extract score value (can be dict with 'value' key or direct number)
                    def get_score_value(score_obj):
                        if score_obj is None:
                            return None
                        if isinstance(score_obj, dict):
                            return score_obj.get('value')
                        return score_obj
                    
                    team1_score = get_score_value(team1_score_obj)
                    team2_score = get_score_value(team2_score_obj)
                    
                    # If no scores, game hasn't been played yet
                    if team1_score is None or team2_score is None:
                        continue
                    
                    # Find our team
                    team = next((c for c in competitors if c.get('team', {}).get('id') == str(team_id)), None)
                    if not team:
                        continue
                    
                    # Get opponent
                    other_team = next((c for c in competitors if c.get('team', {}).get('id') != str(team_id)), None)
                    
                    # Extract game data
                    team_score = get_score_value(team.get('score')) or 0
                    other_score = get_score_value(other_team.get('score')) if other_team else 0
                    team_winner = team.get('winner', False)
                    other_winner = other_team.get('winner', False) if other_team else False
                    
                    # Determine result
                    if team_score == other_score and team_score > 0 and not team_winner and not other_winner:
                        result = 'T'
                    elif team_winner:
                        result = 'W'
                    else:
                        result = 'L'
                    
                    # Extract date
                    event_date = event.get('date', '')
                    
                    # Determine home/away
                    is_home = team.get('homeAway', '').lower() == 'home'
                    
                    # Get opponent name
                    opponent_name = other_team.get('team', {}).get('displayName', 'Unknown') if other_team else 'Unknown'
                    
                    # Calculate score margin
                    score_margin = abs(team_score - other_score)
                    
                    # Check for overtime (if status indicates it)
                    is_overtime = 'OT' in status_name or 'OVERTIME' in status_name
                    
                    results.append({
                        'result': result,
                        'date': event_date,
                        'opponent': opponent_name,
                        'team_score': team_score,
                        'opponent_score': other_score,
                        'score_margin': score_margin,
                        'is_home': is_home,
                        'is_overtime': is_overtime
                    })
                
                # Sort by date (most recent first) and return top N
                def sort_key(game):
                    try:
                        from dateutil import parser as date_parser
                        return date_parser.parse(game['date'])
                    except:
                        return datetime.min
                
                results.sort(key=sort_key, reverse=True)
                return results[:num_games]  # Return most recent N games
        except Exception as e:
            print(f"Error fetching NFL schedule: {e}")
            return []
        return []


class NBAAPI(SportsAPI):
    """NBA API using nba_api"""
    
    def __init__(self):
        super().__init__()
        try:
            from nba_api.stats.endpoints import teamgamelog, scoreboard
            from nba_api.stats.static import teams
            self.teamgamelog = teamgamelog
            self.scoreboard = scoreboard
            self.teams = teams
        except ImportError:
            print("Warning: nba_api not installed. Install with: pip install nba_api")
            self.teamgamelog = None
    
    def get_team_id(self, team_name: str) -> Optional[int]:
        """Get team ID from name"""
        if not self.teams:
            return None
        
        try:
            nba_teams = self.teams.get_teams()
            for team in nba_teams:
                if team_name.lower() in team['full_name'].lower():
                    return team['id']
        except Exception as e:
            print(f"Error finding NBA team: {e}")
        return None
    
    def get_team_record(self, team_name: str) -> Optional[Dict]:
        """Get team record (Mavericks or Warriors) - uses ESPN API for current standings"""
        try:
            # Use ESPN API for current standings (more reliable)
            # ESPN team IDs: Mavericks = 6, Warriors = 9
            espn_team_ids = {
                'dallas mavericks': 6,
                'mavericks': 6,
                'golden state warriors': 9,
                'warriors': 9
            }
            
            espn_id = espn_team_ids.get(team_name.lower())
            if not espn_id:
                return None
            
            url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{espn_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                team = data.get('team', {})
                record = team.get('record', {})
                items = record.get('items', [])
                
                if items:
                    # Find the "total" record (overall record, not home/away)
                    total_record = next((item for item in items if item.get('type') == 'total'), items[0])
                    stats = total_record.get('stats', [])
                    wins = next((int(s['value']) for s in stats if s['name'] == 'wins'), 0)
                    losses = next((int(s['value']) for s in stats if s['name'] == 'losses'), 0)
                    
                    return {
                        'wins': wins,
                        'losses': losses,
                        'win_percentage': wins / (wins + losses) if (wins + losses) > 0 else 0
                    }
        except Exception as e:
            print(f"Error fetching NBA data for {team_name} from ESPN: {e}")
            # Fallback to nba_api game log method (but filter to only completed games)
            if self.teamgamelog:
                try:
                    team_id = self.get_team_id(team_name)
                    if team_id:
                        current_season = datetime.now().year
                        if datetime.now().month < 10:
                            current_season -= 1
                        
                        game_log = self.teamgamelog.TeamGameLog(
                            team_id=team_id,
                            season=f"{current_season}-{str(current_season+1)[-2:]}"
                        )
                        
                        df = game_log.get_data_frames()[0]
                        # Only count games that have been played (have a result)
                        completed = df[df['WL'].notna()]
                        wins = len(completed[completed['WL'] == 'W'])
                        losses = len(completed[completed['WL'] == 'L'])
                        
                        return {
                            'wins': wins,
                            'losses': losses,
                            'win_percentage': wins / (wins + losses) if (wins + losses) > 0 else 0
                        }
                except Exception as e2:
                    print(f"Fallback method also failed: {e2}")
        return None
    
    def get_recent_games(self, team_name: str, num_games: int = 5) -> List[str]:
        """Get recent game results from ESPN API - uses schedule endpoint like NFL"""
        game_data = self.get_recent_games_detailed(team_name, num_games)
        return [game['result'] for game in game_data]
    
    def get_recent_games_detailed(self, team_name: str, num_games: int = 5) -> List[Dict]:
        """Get recent game results with detailed data (dates, scores, opponents, home/away)"""
        try:
            # ESPN team IDs: Mavericks = 6, Warriors = 9
            espn_team_ids = {
                'dallas mavericks': 6,
                'mavericks': 6,
                'golden state warriors': 9,
                'warriors': 9
            }
            
            espn_id = espn_team_ids.get(team_name.lower())
            if not espn_id:
                return []
            
            # Use schedule endpoint instead of events (more reliable)
            url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{espn_id}/schedule"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                results = []
                
                # Process all events, filter completed ones
                for event in events:
                    # Check if game is completed - check competition status
                    competitions = event.get('competitions', [])
                    if not competitions:
                        continue
                    
                    comp = competitions[0]
                    comp_status = comp.get('status', {}).get('type', {})
                    status_name = comp_status.get('name', '').upper() if isinstance(comp_status, dict) else str(comp_status).upper()
                    
                    # Game is completed if it has scores and status indicates completion
                    competitors = comp.get('competitors', [])
                    if len(competitors) != 2:
                        continue
                    
                    # Check if both teams have scores (game has been played)
                    team1_score_obj = competitors[0].get('score')
                    team2_score_obj = competitors[1].get('score')
                    
                    # Extract score value (can be dict with 'value' key or direct number)
                    def get_score_value(score_obj):
                        if score_obj is None:
                            return None
                        if isinstance(score_obj, dict):
                            return score_obj.get('value')
                        return score_obj
                    
                    team1_score = get_score_value(team1_score_obj)
                    team2_score = get_score_value(team2_score_obj)
                    
                    # If no scores, game hasn't been played yet
                    if team1_score is None or team2_score is None:
                        continue
                    
                    # Find our team
                    team = next((c for c in competitors if c.get('team', {}).get('id') == str(espn_id)), None)
                    if not team:
                        continue
                    
                    # Get opponent
                    other_team = next((c for c in competitors if c.get('team', {}).get('id') != str(espn_id)), None)
                    
                    # Extract game data
                    team_score = get_score_value(team.get('score')) or 0
                    other_score = get_score_value(other_team.get('score')) if other_team else 0
                    team_winner = team.get('winner', False)
                    
                    # Determine result
                    result = 'W' if team_winner else 'L'
                    
                    # Extract date
                    event_date = event.get('date', '')
                    
                    # Determine home/away
                    is_home = team.get('homeAway', '').lower() == 'home'
                    
                    # Get opponent name
                    opponent_name = other_team.get('team', {}).get('displayName', 'Unknown') if other_team else 'Unknown'
                    
                    # Calculate score margin
                    score_margin = abs(team_score - other_score)
                    
                    # Check for overtime (if status indicates it)
                    is_overtime = 'OT' in status_name or 'OVERTIME' in status_name
                    
                    results.append({
                        'result': result,
                        'date': event_date,
                        'opponent': opponent_name,
                        'team_score': team_score,
                        'opponent_score': other_score,
                        'score_margin': score_margin,
                        'is_home': is_home,
                        'is_overtime': is_overtime
                    })
                
                # Sort by date (most recent first) and return top N
                def sort_key(game):
                    try:
                        from dateutil import parser as date_parser
                        return date_parser.parse(game['date'])
                    except:
                        return datetime.min
                
                results.sort(key=sort_key, reverse=True)
                return results[:num_games]  # Return most recent N games
        except Exception as e:
            print(f"Error fetching NBA schedule from ESPN: {e}")
            # Fallback to nba_api (returns simple list)
            if self.teamgamelog:
                try:
                    team_id = self.get_team_id(team_name)
                    if team_id:
                        current_season = datetime.now().year
                        if datetime.now().month < 10:
                            current_season -= 1
                        
                        game_log = self.teamgamelog.TeamGameLog(
                            team_id=team_id,
                            season=f"{current_season}-{str(current_season+1)[-2:]}"
                        )
                        
                        df = game_log.get_data_frames()[0]
                        # Only get completed games
                        completed = df[df['WL'].notna()].head(num_games)
                        simple_results = completed['WL'].tolist()
                        # Convert to detailed format (limited data from nba_api)
                        results = []
                        for i, r in enumerate(simple_results):
                            results.append({
                                'result': r if r in ['W', 'L'] else 'L',
                                'date': '',  # nba_api doesn't provide dates easily
                                'opponent': 'Unknown',
                                'team_score': 0,
                                'opponent_score': 0,
                                'score_margin': 0,
                                'is_home': False,
                                'is_overtime': False
                            })
                        return results
                except Exception as e2:
                    print(f"Fallback method also failed: {e2}")
        return []


class MLBAPI(SportsAPI):
    """MLB API using sportsipy"""
    
    def __init__(self):
        super().__init__()
        try:
            from sportsipy.mlb.teams import Teams
            from sportsipy.mlb.schedule import Schedule
            self.Teams = Teams
            self.Schedule = Schedule
        except ImportError:
            print("Warning: sportsipy not installed. Install with: pip install sportsipy")
            self.Teams = None
    
    def get_team_record(self, team_name: str) -> Optional[Dict]:
        """Get Rangers record from ESPN API"""
        try:
            # ESPN team ID for Texas Rangers is 13
            url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/13"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                team = data.get('team', {})
                record = team.get('record', {})
                items = record.get('items', [])
                
                if items:
                    # Find the "total" record (overall record, not home/away)
                    total_record = next((item for item in items if item.get('type') == 'total'), items[0])
                    stats = total_record.get('stats', [])
                    wins = next((int(s['value']) for s in stats if s['name'] == 'wins'), 0)
                    losses = next((int(s['value']) for s in stats if s['name'] == 'losses'), 0)
                    
                    return {
                        'wins': wins,
                        'losses': losses,
                        'win_percentage': wins / (wins + losses) if (wins + losses) > 0 else 0
                    }
        except Exception as e:
            print(f"Error fetching MLB data: {e}")
            # Fallback to sportsipy if available
            if self.Teams:
                try:
                    teams = self.Teams()
                    for team in teams:
                        if 'texas' in team.name.lower() and 'rangers' in team.name.lower():
                            return {
                                'wins': team.wins,
                                'losses': team.losses,
                                'win_percentage': team.win_percentage
                            }
                except Exception as e2:
                    print(f"Fallback method also failed: {e2}")
        return None


class F1API(SportsAPI):
    """F1 API using OpenF1 REST API (simplified, no dependencies)"""
    
    def __init__(self):
        super().__init__()
        self.openf1_base = "https://api.openf1.org/v1"
        # Verstappen's driver number is 1
        self.driver_number = 1
    
    def get_driver_standings(self, driver_name: str = "Verstappen") -> Optional[Dict]:
        """Get Max Verstappen's championship position using OpenF1 API"""
        current_year = datetime.now().year
        # F1 season typically runs March-November
        if datetime.now().month < 3:
            current_year -= 1
        
        try:
            # Use OpenF1's simple standings endpoint if available, otherwise calculate from sessions
            # Try to get standings directly first
            standings_url = f"{self.openf1_base}/standings?year={current_year}"
            try:
                response = self.session.get(standings_url, timeout=10)
                if response.status_code == 200:
                    standings = response.json()
                    if standings:
                        # Find Verstappen in standings (driver_number = 1)
                        for entry in standings:
                            if entry.get('driver_number') == self.driver_number:
                                return {
                                    'position': entry.get('position', 1),
                                    'points': entry.get('points', 0),
                                    'wins': entry.get('wins', 0)
                                }
            except Exception:
                # Standings endpoint might not exist, continue to session-based method
                pass
            
            # Fallback: Calculate from race sessions (simpler approach)
            url = f"{self.openf1_base}/sessions?year={current_year}&session_type=Race"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                sessions = response.json()
                if sessions and len(sessions) > 0:
                    # Sort sessions by date to process chronologically
                    sessions.sort(key=lambda x: x.get('date_start', ''))
                    
                    driver_points = {}
                    driver_wins = {}
                    
                    # Process only completed races (limit to last 10 for speed)
                    completed_sessions = [s for s in sessions if s.get('date_end')][-10:]
                    
                    for session in completed_sessions:
                        session_key = session.get('session_key')
                        if not session_key:
                            continue
                        
                        try:
                            # Get results for this race
                            results_url = f"{self.openf1_base}/results?session_key={session_key}"
                            results_response = self.session.get(results_url, timeout=5)
                            
                            if results_response.status_code == 200:
                                results = results_response.json()
                                if results:
                                    for result in results:
                                        driver_num = result.get('driver_number')
                                        points = result.get('points', 0) or 0
                                        position = result.get('position')
                                        
                                        if driver_num:
                                            if driver_num not in driver_points:
                                                driver_points[driver_num] = 0
                                                driver_wins[driver_num] = 0
                                            driver_points[driver_num] += float(points or 0)
                                            if position == 1:
                                                driver_wins[driver_num] += 1
                        except Exception:
                            # Skip this race if it fails, continue with others
                            continue
                    
                    # Find Verstappen (driver number 1) and calculate position
                    if self.driver_number in driver_points:
                        # Calculate position by sorting all drivers
                        sorted_drivers = sorted(driver_points.items(), key=lambda x: x[1], reverse=True)
                        position = next((i+1 for i, (num, pts) in enumerate(sorted_drivers) if num == self.driver_number), 1)
                        
                        return {
                            'position': position,
                            'points': driver_points[self.driver_number],
                            'wins': driver_wins.get(self.driver_number, 0)
                        }
        except requests.exceptions.RequestException as e:
            print(f"OpenF1 API connection error: {e}")
        except Exception as e:
            print(f"OpenF1 API error: {e}")
        
        # Graceful fallback - return None so manual input can be used
        print(f"Warning: Could not fetch F1 standings for {driver_name}. Using manual data from config.")
        return None
    
    def get_recent_race_results(self, driver_name: str = "Verstappen", num_races: int = 5) -> List[str]:
        """Get recent race results for Max using OpenF1 API"""
        current_year = datetime.now().year
        if datetime.now().month < 3:
            current_year -= 1
        
        try:
            url = f"{self.openf1_base}/sessions?year={current_year}&session_type=Race"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                sessions = response.json()
                if sessions and len(sessions) > 0:
                    # Sort by date and get completed races only
                    completed_sessions = [s for s in sessions if s.get('date_end')]
                    completed_sessions.sort(key=lambda x: x.get('date_start', ''))
                    
                    results = []
                    # Get last N completed races (most recent first)
                    for session in reversed(completed_sessions[-num_races:]):
                        session_key = session.get('session_key')
                        if not session_key:
                            continue
                        
                        try:
                            results_url = f"{self.openf1_base}/results?session_key={session_key}"
                            results_response = self.session.get(results_url, timeout=5)
                            
                            if results_response.status_code == 200:
                                race_results = results_response.json()
                                if race_results:
                                    # Find Verstappen (driver number 1)
                                    for result in race_results:
                                        if result.get('driver_number') == self.driver_number:
                                            position = result.get('position')
                                            status = result.get('status', '') or ''
                                            
                                            # Check for DNF
                                            if not position or status.upper() in ['DNF', 'DSQ', 'DNS']:
                                                results.append('DNF')
                                            elif position == 1:
                                                results.append('W')
                                            elif position in [2, 3]:
                                                results.append(f'P{position}')
                                            elif position:
                                                results.append(f'P{position}')
                                            else:
                                                results.append('DNF')
                                            break
                        except Exception:
                            # Skip this race if it fails, continue with others
                            continue
                    
                    if results:
                        return results
        except requests.exceptions.RequestException as e:
            print(f"OpenF1 race results connection error: {e}")
        except Exception as e:
            print(f"OpenF1 race results error: {e}")
        
        # Graceful fallback - return empty list so manual data can be used
        print(f"Warning: Could not fetch recent F1 race results for {driver_name}. Using manual data from config.")
        return []


class CollegeBasketballAPI(SportsAPI):
    """College Basketball API using espn-api"""
    
    def __init__(self):
        super().__init__()
        try:
            from espn_api.basketball import League
            # For college, we'll use ESPN's API directly
            self.League = League
        except ImportError:
            print("Warning: espn-api not installed. Install with: pip install espn-api")
            self.League = None
    
    def get_team_record(self, team_name: str) -> Optional[Dict]:
        """Get UNC Tar Heels basketball record"""
        # ESPN API for college basketball is tricky
        # We'll use a web scraping approach or ESPN API
        try:
            # Try using ESPN's API endpoint
            url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/153"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                team = data.get('team', {})
                record = team.get('record', {})
                items = record.get('items', [])
                if items:
                    stats = items[0].get('stats', [])
                    wins_raw = next((s['value'] for s in stats if s['name'] == 'wins'), 0)
                    losses_raw = next((s['value'] for s in stats if s['name'] == 'losses'), 0)
                    # Convert to int (ESPN API returns floats like 6.0, 1.0)
                    # Use float() first to handle both int and float, then int() to ensure integer
                    wins = int(float(wins_raw)) if wins_raw is not None else 0
                    losses = int(float(losses_raw)) if losses_raw is not None else 0
                    return {
                        'wins': wins,
                        'losses': losses,
                        'win_percentage': wins / (wins + losses) if (wins + losses) > 0 else 0
                    }
        except Exception as e:
            print(f"Error fetching college basketball data: {e}")
        return None
    
    def get_recent_games(self, team_name: str, num_games: int = 5) -> List[str]:
        """Get recent game results (W/L) from ESPN"""
        game_data = self.get_recent_games_detailed(team_name, num_games)
        return [game['result'] for game in game_data]
    
    def get_recent_games_detailed(self, team_name: str, num_games: int = 5) -> List[Dict]:
        """Get recent game results with detailed data (dates, scores, opponents, home/away)"""
        try:
            # UNC's ESPN team ID is 153
            team_id = 153
            
            # Use schedule endpoint instead of events (more reliable)
            url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team_id}/schedule"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                results = []
                
                # Process all events, filter completed ones
                for event in events:
                    competitions = event.get('competitions', [])
                    if not competitions:
                        continue
                    
                    comp = competitions[0]
                    competitors = comp.get('competitors', [])
                    if len(competitors) != 2:
                        continue
                    
                    # Check if both teams have scores (game has been played)
                    team1_score_obj = competitors[0].get('score')
                    team2_score_obj = competitors[1].get('score')
                    
                    # Extract score value
                    def get_score_value(score_obj):
                        if score_obj is None:
                            return None
                        if isinstance(score_obj, dict):
                            return score_obj.get('value')
                        return score_obj
                    
                    team1_score = get_score_value(team1_score_obj)
                    team2_score = get_score_value(team2_score_obj)
                    
                    # If no scores, game hasn't been played yet
                    if team1_score is None or team2_score is None:
                        continue
                    
                    # Find UNC
                    team = next((c for c in competitors if c.get('team', {}).get('id') == str(team_id)), None)
                    if not team:
                        continue
                    
                    # Get opponent
                    other_team = next((c for c in competitors if c.get('team', {}).get('id') != str(team_id)), None)
                    
                    # Extract game data
                    team_score = get_score_value(team.get('score')) or 0
                    other_score = get_score_value(other_team.get('score')) if other_team else 0
                    team_winner = team.get('winner', False)
                    
                    # Determine result
                    result = 'W' if team_winner else 'L'
                    
                    # Extract date
                    event_date = event.get('date', '')
                    
                    # Determine home/away
                    is_home = team.get('homeAway', '').lower() == 'home'
                    
                    # Get opponent name
                    opponent_name = other_team.get('team', {}).get('displayName', 'Unknown') if other_team else 'Unknown'
                    
                    # Calculate score margin
                    score_margin = abs(team_score - other_score)
                    
                    # Check for overtime
                    comp_status = comp.get('status', {}).get('type', {})
                    status_name = comp_status.get('name', '').upper() if isinstance(comp_status, dict) else str(comp_status).upper()
                    is_overtime = 'OT' in status_name or 'OVERTIME' in status_name
                    
                    results.append({
                        'result': result,
                        'date': event_date,
                        'opponent': opponent_name,
                        'team_score': team_score,
                        'opponent_score': other_score,
                        'score_margin': score_margin,
                        'is_home': is_home,
                        'is_overtime': is_overtime
                    })
                
                # Sort by date (most recent first) and return top N
                def sort_key(game):
                    try:
                        from dateutil import parser as date_parser
                        return date_parser.parse(game['date'])
                    except:
                        return datetime.min
                
                results.sort(key=sort_key, reverse=True)
                return results[:num_games]  # Return most recent N games
        except Exception as e:
            print(f"Error fetching college basketball schedule: {e}")
            import traceback
            traceback.print_exc()
        return []


class CollegeFootballAPI(SportsAPI):
    """College Football API using espn-api"""
    
    def __init__(self):
        super().__init__()
        try:
            from espn_api.football import League
            self.League = League
        except ImportError:
            print("Warning: espn-api not installed. Install with: pip install espn-api")
            self.League = None
    
    def get_team_record(self, team_name: str) -> Optional[Dict]:
        """Get UNC Tar Heels football record"""
        try:
            # UNC's ESPN team ID is 153
            url = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/153"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                team = data.get('team', {})
                record = team.get('record', {})
                items = record.get('items', [])
                if items:
                    stats = items[0].get('stats', [])
                    wins_raw = next((s['value'] for s in stats if s['name'] == 'wins'), 0)
                    losses_raw = next((s['value'] for s in stats if s['name'] == 'losses'), 0)
                    # Convert to int (ESPN API returns floats like 6.0, 1.0)
                    # Use float() first to handle both int and float, then int() to ensure integer
                    wins = int(float(wins_raw)) if wins_raw is not None else 0
                    losses = int(float(losses_raw)) if losses_raw is not None else 0
                    return {
                        'wins': wins,
                        'losses': losses,
                        'win_percentage': wins / (wins + losses) if (wins + losses) > 0 else 0
                    }
        except Exception as e:
            print(f"Error fetching college football data: {e}")
        return None
    
    def get_recent_games(self, team_name: str, num_games: int = 5) -> List[str]:
        """Get recent game results (W/L/T) from ESPN"""
        game_data = self.get_recent_games_detailed(team_name, num_games)
        return [game['result'] for game in game_data]
    
    def get_recent_games_detailed(self, team_name: str, num_games: int = 5) -> List[Dict]:
        """Get recent game results with detailed data (dates, scores, opponents, home/away)"""
        try:
            # UNC's ESPN team ID is 153
            team_id = 153
            
            # Use schedule endpoint instead of events (more reliable)
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/{team_id}/schedule"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                results = []
                
                # Process all events, filter completed ones
                for event in events:
                    competitions = event.get('competitions', [])
                    if not competitions:
                        continue
                    
                    comp = competitions[0]
                    competitors = comp.get('competitors', [])
                    if len(competitors) != 2:
                        continue
                    
                    # Check if both teams have scores (game has been played)
                    team1_score_obj = competitors[0].get('score')
                    team2_score_obj = competitors[1].get('score')
                    
                    # Extract score value
                    def get_score_value(score_obj):
                        if score_obj is None:
                            return None
                        if isinstance(score_obj, dict):
                            return score_obj.get('value')
                        return score_obj
                    
                    team1_score = get_score_value(team1_score_obj)
                    team2_score = get_score_value(team2_score_obj)
                    
                    # If no scores, game hasn't been played yet
                    if team1_score is None or team2_score is None:
                        continue
                    
                    # Find UNC
                    team = next((c for c in competitors if c.get('team', {}).get('id') == str(team_id)), None)
                    if not team:
                        continue
                    
                    # Get opponent
                    other_team = next((c for c in competitors if c.get('team', {}).get('id') != str(team_id)), None)
                    
                    # Extract game data
                    team_score = get_score_value(team.get('score')) or 0
                    other_score = get_score_value(other_team.get('score')) if other_team else 0
                    team_winner = team.get('winner', False)
                    other_winner = other_team.get('winner', False) if other_team else False
                    
                    # Determine result (college football can have ties)
                    if team_score == other_score and team_score > 0 and not team_winner and not other_winner:
                        result = 'T'
                    elif team_winner:
                        result = 'W'
                    else:
                        result = 'L'
                    
                    # Extract date
                    event_date = event.get('date', '')
                    
                    # Determine home/away
                    is_home = team.get('homeAway', '').lower() == 'home'
                    
                    # Get opponent name
                    opponent_name = other_team.get('team', {}).get('displayName', 'Unknown') if other_team else 'Unknown'
                    
                    # Calculate score margin
                    score_margin = abs(team_score - other_score)
                    
                    # Check for overtime
                    comp_status = comp.get('status', {}).get('type', {})
                    status_name = comp_status.get('name', '').upper() if isinstance(comp_status, dict) else str(comp_status).upper()
                    is_overtime = 'OT' in status_name or 'OVERTIME' in status_name
                    
                    results.append({
                        'result': result,
                        'date': event_date,
                        'opponent': opponent_name,
                        'team_score': team_score,
                        'opponent_score': other_score,
                        'score_margin': score_margin,
                        'is_home': is_home,
                        'is_overtime': is_overtime
                    })
                
                # Sort by date (most recent first) and return top N
                def sort_key(game):
                    try:
                        from dateutil import parser as date_parser
                        return date_parser.parse(game['date'])
                    except:
                        return datetime.min
                
                results.sort(key=sort_key, reverse=True)
                return results[:num_games]  # Return most recent N games
        except Exception as e:
            print(f"Error fetching college football schedule: {e}")
            import traceback
            traceback.print_exc()
        return []


class SportsDataFetcher:
    """Main class to fetch all sports data"""
    
    def __init__(self):
        self.nfl = NFLAPI()
        self.nba = NBAAPI()
        self.mlb = MLBAPI()
        self.f1 = F1API()
        self.college_bball = CollegeBasketballAPI()
        self.college_football = CollegeFootballAPI()
    
    def fetch_fantasy_data(self, espn_config: dict) -> Optional[Dict]:
        """Fetch fantasy team data from ESPN API"""
        try:
            # Try relative import first (when used as module)
            try:
                from .espn_fantasy import ESPNFantasyClient
            except ImportError:
                # Fall back to absolute import (when used as script)
                from src.espn_fantasy import ESPNFantasyClient
        except ImportError:
            print("Warning: ESPN Fantasy integration not available. Install espn-api library.")
            return None
        
        try:
            league_id = espn_config.get("league_id")
            year = espn_config.get("year")
            if not league_id or not year:
                return None
            
            team_id = espn_config.get("team_id")
            team_name = espn_config.get("team_name")
            espn_s2 = espn_config.get("espn_s2")
            swid = espn_config.get("swid")
            
            # Initialize ESPN client
            client = ESPNFantasyClient(
                league_id=league_id,
                year=year,
                team_id=team_id,
                espn_s2=espn_s2,
                swid=swid
            )
            
            # Fetch team data
            team_data = client.get_my_team(team_name)
            return team_data
        except Exception as e:
            print(f"Error fetching fantasy data from ESPN: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_opponent_record(self, opponent_name: str, sport: str) -> Optional[Dict]:
        """Get record for an opponent team (used for context)"""
        try:
            if sport == 'NFL':
                return self.nfl.get_team_record(opponent_name)
            elif sport == 'NBA':
                return self.nba.get_team_record(opponent_name)
            elif sport == 'MLB':
                return self.mlb.get_team_record(opponent_name)
            elif sport == 'NCAA Basketball':
                return self.college_bball.get_team_record(opponent_name)
            elif sport == 'NCAA Football':
                return self.college_football.get_team_record(opponent_name)
        except Exception as e:
            print(f"Error fetching opponent record for {opponent_name} ({sport}): {e}")
        return None
    
    def fetch_all_data(self) -> Dict:
        """Fetch data for all of Jason's teams"""
        data = {
            'cowboys': self.nfl.get_team_record('Dallas Cowboys'),
            'mavericks': self.nba.get_team_record('Dallas Mavericks'),
            'warriors': self.nba.get_team_record('Golden State Warriors'),
            'rangers': self.mlb.get_team_record('Texas Rangers'),
            'verstappen': self.f1.get_driver_standings('Verstappen'),
            'unc_basketball': self.college_bball.get_team_record('North Carolina Tar Heels'),
            'unc_football': self.college_football.get_team_record('North Carolina Tar Heels')
        }
        
        # Add recent games
        if data['cowboys']:
            data['cowboys']['recent_games'] = self.nfl.get_recent_games('Dallas Cowboys')
        if data['mavericks']:
            data['mavericks']['recent_games'] = self.nba.get_recent_games('Dallas Mavericks')
        if data['warriors']:
            data['warriors']['recent_games'] = self.nba.get_recent_games('Golden State Warriors')
        if data['verstappen']:
            data['verstappen']['recent_races'] = self.f1.get_recent_race_results('Verstappen')
        if data['unc_basketball']:
            data['unc_basketball']['recent_games'] = self.college_bball.get_recent_games('North Carolina Tar Heels')
        if data['unc_football']:
            data['unc_football']['recent_games'] = self.college_football.get_recent_games('North Carolina Tar Heels')
        
        return data
    
    def update_config_file(self, config_path: str = "teams_config.json"):
        """Update the config file with fresh data"""
        data = self.fetch_all_data()
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_path} not found")
            return
        except json.JSONDecodeError as e:
            print(f"Error: Config file {config_path} is not valid JSON: {e}")
            print("Cannot update - please fix the config file first")
            return
        except Exception as e:
            print(f"Error reading config file: {e}")
            return
        
        # Ensure config structure is valid
        if not isinstance(config, dict):
            print("Error: Config file is not a valid JSON object")
            return
        
        if "teams" not in config:
            config["teams"] = []
        
        # Update Cowboys
        if data['cowboys']:
            for team in config['teams']:
                if 'cowboys' in team['name'].lower():
                    # Ensure record structure exists
                    if 'record' not in team:
                        team['record'] = {}
                    team['record']['wins'] = int(data['cowboys'].get('wins', team['record'].get('wins', 0)))
                    team['record']['losses'] = int(data['cowboys'].get('losses', team['record'].get('losses', 0)))
                    # Preserve ties if not in API data
                    if 'ties' in data['cowboys']:
                        team['record']['ties'] = int(data['cowboys']['ties'])
                    elif 'ties' not in team['record']:
                        team['record']['ties'] = 0
                    if 'recent_games' in data['cowboys']:
                        team['recent_streak'] = data['cowboys']['recent_games']
        
        # Update Mavericks
        if data['mavericks']:
            for team in config['teams']:
                if 'mavericks' in team.get('name', '').lower():
                    if 'record' not in team:
                        team['record'] = {}
                    if 'wins' in data['mavericks']:
                        team['record']['wins'] = int(data['mavericks']['wins'])
                    if 'losses' in data['mavericks']:
                        team['record']['losses'] = int(data['mavericks']['losses'])
                    if 'recent_games' in data['mavericks'] and data['mavericks']['recent_games']:
                        team['recent_streak'] = data['mavericks']['recent_games']
        
        # Update Warriors
        if data['warriors']:
            for team in config['teams']:
                if 'warriors' in team.get('name', '').lower():
                    if 'record' not in team:
                        team['record'] = {}
                    if 'wins' in data['warriors']:
                        team['record']['wins'] = int(data['warriors']['wins'])
                    if 'losses' in data['warriors']:
                        team['record']['losses'] = int(data['warriors']['losses'])
                    if 'recent_games' in data['warriors'] and data['warriors']['recent_games']:
                        team['recent_streak'] = data['warriors']['recent_games']
        
        # Update Rangers
        if data['rangers']:
            for team in config['teams']:
                if 'rangers' in team.get('name', '').lower() and team.get('sport') == 'MLB':
                    if 'record' not in team:
                        team['record'] = {}
                    if 'wins' in data['rangers']:
                        team['record']['wins'] = int(data['rangers']['wins'])
                    if 'losses' in data['rangers']:
                        team['record']['losses'] = int(data['rangers']['losses'])
        
        # Update UNC Basketball
        if data['unc_basketball']:
            for team in config['teams']:
                if 'tar heels' in team.get('name', '').lower() and team.get('sport') == 'NCAA Basketball':
                    if 'record' not in team:
                        team['record'] = {}
                    if 'wins' in data['unc_basketball']:
                        team['record']['wins'] = int(data['unc_basketball']['wins'])
                    if 'losses' in data['unc_basketball']:
                        team['record']['losses'] = int(data['unc_basketball']['losses'])
                    if 'recent_games' in data['unc_basketball'] and data['unc_basketball']['recent_games']:
                        team['recent_streak'] = data['unc_basketball']['recent_games']
        
        # Update UNC Football
        if data['unc_football']:
            for team in config['teams']:
                if 'tar heels' in team.get('name', '').lower() and team.get('sport') == 'NCAA Football':
                    if 'record' not in team:
                        team['record'] = {}
                    if 'wins' in data['unc_football']:
                        team['record']['wins'] = int(data['unc_football']['wins'])
                    if 'losses' in data['unc_football']:
                        team['record']['losses'] = int(data['unc_football']['losses'])
                    if 'recent_games' in data['unc_football'] and data['unc_football']['recent_games']:
                        team['recent_streak'] = data['unc_football']['recent_games']
        
        # Update Verstappen
        if data['verstappen']:
            if 'f1_driver' in config:
                config['f1_driver']['championship_position'] = data['verstappen']['position']
                if 'recent_races' in data['verstappen']:
                    config['f1_driver']['recent_races'] = data['verstappen']['recent_races']
                
                # Count DNFs
                dnf_count = sum(1 for r in data['verstappen'].get('recent_races', []) if r == 'DNF')
                config['f1_driver']['recent_dnfs'] = dnf_count
        
        # Update Fantasy Team (if ESPN credentials are configured)
        if 'fantasy_team' in config:
            fantasy_data = config.get('fantasy_team', {})
            espn_config = fantasy_data.get('espn', {})
            
            if espn_config.get('league_id') and espn_config.get('year'):
                print("Fetching fantasy data from ESPN API...")
                fantasy_api_data = self.fetch_fantasy_data(espn_config)
                
                if fantasy_api_data:
                    # Ensure fantasy_team section exists
                    if 'fantasy_team' not in config:
                        config['fantasy_team'] = {}
                    
                    # Update record
                    if 'record' not in config['fantasy_team']:
                        config['fantasy_team']['record'] = {}
                    
                    config['fantasy_team']['record']['wins'] = int(fantasy_api_data.get('wins', config['fantasy_team']['record'].get('wins', 0)))
                    config['fantasy_team']['record']['losses'] = int(fantasy_api_data.get('losses', config['fantasy_team']['record'].get('losses', 0)))
                    
                    # Update recent streak
                    if 'recent_streak' in fantasy_api_data:
                        config['fantasy_team']['recent_streak'] = fantasy_api_data['recent_streak']
                    
                    # Update name if it changed
                    if 'name' in fantasy_api_data:
                        config['fantasy_team']['name'] = fantasy_api_data['name']
                    
                    print(f"✅ Updated fantasy team '{fantasy_api_data.get('name', 'Fantasy Team')}' from ESPN")
                    print(f"   Record: {fantasy_api_data.get('wins', 0)}-{fantasy_api_data.get('losses', 0)}")
                else:
                    print("⚠️  Could not fetch fantasy data from ESPN. Check your credentials or network connection.")
            else:
                print("ℹ️  Fantasy team ESPN credentials not configured. Skipping fantasy update.")
                print("   To enable automatic fantasy updates, add an 'espn' section to fantasy_team in config.")
        
        # Save updated config with error handling
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Updated {config_path} with fresh data!")
        except Exception as e:
            print(f"❌ Error saving config file: {e}")
            print("Config file was not updated to prevent data loss")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Test the API fetcher
    fetcher = SportsDataFetcher()
    data = fetcher.fetch_all_data()
    print(json.dumps(data, indent=2))
    
    # Update config file
    fetcher.update_config_file()

