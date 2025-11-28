#!/usr/bin/env python3
"""
ESPN Fantasy Football API Integration
Fetches fantasy team data from ESPN Fantasy Football
"""

from typing import Dict, Optional, List
from espn_api.football import League
from datetime import datetime


class ESPNFantasyClient:
    """Client for fetching ESPN Fantasy Football data"""
    
    def __init__(self, league_id: int, year: int, team_id: Optional[int] = None, 
                 espn_s2: Optional[str] = None, swid: Optional[str] = None):
        """
        Initialize ESPN Fantasy client
        
        Args:
            league_id: Your ESPN league ID (found in the URL)
            year: Season year (e.g., 2024, 2025)
            team_id: Your team ID (optional, will find by team name if not provided)
            espn_s2: ESPN authentication cookie (required for private leagues)
            swid: ESPN SWID cookie (required for private leagues)
        """
        self.league_id = league_id
        self.year = year
        self.team_id = team_id
        self.espn_s2 = espn_s2
        self.swid = swid
        self.league = None
        self._connect()
    
    def _connect(self):
        """Connect to ESPN Fantasy League"""
        try:
            if self.espn_s2 and self.swid:
                # Private league - requires authentication
                self.league = League(
                    league_id=self.league_id,
                    year=self.year,
                    espn_s2=self.espn_s2,
                    swid=self.swid
                )
            else:
                # Public league - no authentication needed
                self.league = League(
                    league_id=self.league_id,
                    year=self.year
                )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to ESPN Fantasy League: {e}")
    
    def get_team_by_id(self, team_id: int):
        """Get team by team ID"""
        for team in self.league.teams:
            if team.team_id == team_id:
                return team
        raise ValueError(f"Team ID {team_id} not found in league")
    
    def get_team_by_name(self, team_name: str):
        """Get team by team name (case-insensitive partial match)"""
        team_name_lower = team_name.lower()
        for team in self.league.teams:
            if team_name_lower in team.team_name.lower() or team.team_name.lower() in team_name_lower:
                return team
        raise ValueError(f"Team '{team_name}' not found in league")
    
    def get_my_team(self, team_name: Optional[str] = None) -> Dict:
        """
        Get your fantasy team data
        
        Args:
            team_name: Your team name (optional, uses team_id if provided in init)
        
        Returns:
            Dictionary with team data including:
            - name: Team name
            - wins: Number of wins
            - losses: Number of losses
            - ties: Number of ties
            - record: Formatted record string
            - recent_streak: List of recent results (W/L/T)
            - current_week: Current week number
            - matchup: Current week matchup info
        """
        try:
            # Get team
            if self.team_id:
                team = self.get_team_by_id(self.team_id)
            elif team_name:
                team = self.get_team_by_name(team_name)
            else:
                # Default to first team (usually yours if you're logged in)
                team = self.league.teams[0]
            
            # Get recent streak (last 5 weeks)
            recent_streak = []
            current_week = self.league.current_week
            
            # Get matchups from recent weeks
            for week in range(max(1, current_week - 5), current_week):
                try:
                    matchup = team.schedule[week - 1] if week <= len(team.schedule) else None
                    if matchup:
                        if matchup.home_team == team:
                            my_score = matchup.home_score
                            opp_score = matchup.away_score
                        else:
                            my_score = matchup.away_score
                            opp_score = matchup.home_score
                        
                        if my_score > opp_score:
                            recent_streak.append("W")
                        elif my_score < opp_score:
                            recent_streak.append("L")
                        else:
                            recent_streak.append("T")
                except (IndexError, AttributeError):
                    # Week hasn't happened yet or data unavailable
                    pass
            
            # Get current week matchup
            current_matchup = None
            try:
                if current_week <= len(team.schedule):
                    matchup = team.schedule[current_week - 1]
                    if matchup:
                        if matchup.home_team == team:
                            opponent = matchup.away_team.team_name
                            my_score = matchup.home_score
                            opp_score = matchup.away_score
                        else:
                            opponent = matchup.home_team.team_name
                            my_score = matchup.away_score
                            opp_score = matchup.home_score
                        
                        current_matchup = {
                            "opponent": opponent,
                            "my_score": my_score,
                            "opponent_score": opp_score,
                            "week": current_week
                        }
            except (IndexError, AttributeError):
                pass
            
            return {
                "name": team.team_name,
                "wins": team.wins,
                "losses": team.losses,
                "ties": team.ties,
                "record": f"{team.wins}-{team.losses}-{team.ties}",
                "recent_streak": recent_streak,
                "current_week": current_week,
                "matchup": current_matchup,
                "team_id": team.team_id,
                "points_for": getattr(team, 'points_for', 0),
                "points_against": getattr(team, 'points_against', 0)
            }
        except Exception as e:
            raise ValueError(f"Failed to get team data: {e}")
    
    def get_league_info(self) -> Dict:
        """Get general league information"""
        return {
            "league_name": self.league.settings.name,
            "current_week": self.league.current_week,
            "total_teams": len(self.league.teams),
            "season_year": self.year
        }


def get_espn_credentials_instructions() -> str:
    """Return instructions for getting ESPN credentials"""
    return """
    HOW TO GET YOUR ESPN FANTASY CREDENTIALS:
    
    1. LEAGUE ID:
       - Go to your ESPN Fantasy Football league page
       - Look at the URL: https://fantasy.espn.com/football/league?leagueId=123456
       - The number after "leagueId=" is your league ID
    
    2. TEAM ID (Optional):
       - Go to your team page in the league
       - Look at the URL or inspect the page source
       - Or just use your team name (we'll find it automatically)
    
    3. FOR PRIVATE LEAGUES (if needed):
       - Open your browser's Developer Tools (F12)
       - Go to Application/Storage > Cookies > https://fantasy.espn.com
       - Find these cookies:
         * espn_s2: Long string value
         * SWID: Usually starts with { and contains a GUID
       - Copy both values
    
    4. YEAR:
       - Use the current season year (e.g., 2024, 2025)
    
    NOTE: If your league is PUBLIC, you don't need espn_s2 or SWID cookies.
    """

