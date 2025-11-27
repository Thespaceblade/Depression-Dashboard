#!/usr/bin/env python3
"""
Jason's Depression Calculator
Calculates depression level based on favorite teams' performance
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Team:
    """Represents a sports team"""
    name: str
    sport: str
    wins: int
    losses: int
    expected_performance: int  # 1-10 scale
    jasons_expectations: int  # 1-10 scale
    rivals: List[str]
    recent_rivalry_losses: List[str]
    recent_streak: List[str]  # "W", "L", "T"
    interest_level: float = 1.0  # Multiplier for teams Jason cares less about
    notes: str = ""
    
    def calculate_depression(self) -> Dict[str, float]:
        """Calculate depression contribution from this team"""
        score = 0.0
        breakdown = {}
        
        total_games = self.wins + self.losses
        if total_games == 0:
            return {"score": 0, "breakdown": {}}
        
        win_pct = self.wins / total_games
        
        # Base loss penalty (scaled by interest level)
        base_loss_points = 5.0 * self.interest_level
        loss_points = self.losses * base_loss_points
        score += loss_points
        if loss_points > 0:
            breakdown["Losses"] = loss_points
        
        # Expectation gap penalty
        expected_win_pct = self.expected_performance / 10.0
        actual_win_pct = win_pct
        gap = expected_win_pct - actual_win_pct
        
        if gap > 0:  # Underperforming
            if self.expected_performance >= 8:
                gap_penalty = gap * 30 * self.interest_level
            elif self.expected_performance >= 5:
                gap_penalty = gap * 20 * self.interest_level
            else:
                gap_penalty = gap * 10 * self.interest_level
            
            # Multiply by expectations multiplier
            expectations_mult = self.jasons_expectations / 10.0
            gap_penalty *= expectations_mult
            
            score += gap_penalty
            if gap_penalty > 0:
                breakdown["Expectation Gap"] = gap_penalty
        
        # Rivalry loss multiplier
        if self.recent_rivalry_losses:
            rivalry_multiplier = 2.5 * self.interest_level
            rivalry_penalty = len(self.recent_rivalry_losses) * base_loss_points * (rivalry_multiplier - 1)
            score += rivalry_penalty
            if rivalry_penalty > 0:
                breakdown["Rivalry Losses"] = rivalry_penalty
        
        # Consecutive losses
        if self.recent_streak:
            consecutive_losses = 0
            max_streak = 0
            for result in reversed(self.recent_streak):
                if result == "L":
                    consecutive_losses += 1
                    max_streak = max(max_streak, consecutive_losses)
                else:
                    break
            
            if consecutive_losses > 1:
                streak_penalty = (consecutive_losses - 1) * 3 * self.interest_level
                score += streak_penalty
                if streak_penalty > 0:
                    breakdown[f"Losing Streak ({consecutive_losses} games)"] = streak_penalty
        
        return {
            "score": score,
            "breakdown": breakdown,
            "win_pct": win_pct,
            "expected_win_pct": expected_win_pct
        }


@dataclass
class F1Driver:
    """Represents an F1 driver"""
    name: str
    championship_position: int
    expected_performance: int  # 1-10 scale
    jasons_expectations: int  # 1-10 scale
    recent_races: List[str]  # "W", "P2", "P3", "DNF", etc.
    recent_dnfs: int
    rivals: List[str]
    notes: str = ""
    
    def calculate_depression(self) -> Dict[str, float]:
        """Calculate depression contribution from F1 performance"""
        score = 0.0
        breakdown = {}
        
        # Position penalty (lower is better, so position 1 = 0, position 10 = 9 points)
        if self.championship_position > 1:
            position_penalty = (self.championship_position - 1) * 3
            score += position_penalty
            breakdown["Championship Position"] = position_penalty
        
        # Expectation gap (Max should be #1, huge expectations)
        if self.expected_performance >= 9 and self.championship_position > 1:
            gap_penalty = (self.championship_position - 1) * 8
            expectations_mult = self.jasons_expectations / 10.0
            gap_penalty *= expectations_mult
            score += gap_penalty
            if gap_penalty > 0:
                breakdown["Expectation Gap (Should be #1)"] = gap_penalty
        
        # DNF penalty (huge for Max fans)
        if self.recent_dnfs > 0:
            dnf_penalty = self.recent_dnfs * 12
            score += dnf_penalty
            breakdown["DNFs"] = dnf_penalty
        
        # Recent race performance
        if self.recent_races:
            recent_losses = sum(1 for r in self.recent_races if r not in ["W", "P2", "P3"])
            if recent_losses > 0:
                race_penalty = recent_losses * 5
                score += race_penalty
                breakdown["Recent Poor Results"] = race_penalty
        
        return {
            "score": score,
            "breakdown": breakdown
        }


@dataclass
class FantasyTeam:
    """Represents fantasy team"""
    name: str
    wins: int
    losses: int
    expected_performance: int
    jasons_expectations: int
    recent_streak: List[str]
    
    def calculate_depression(self) -> Dict[str, float]:
        """Calculate depression contribution from fantasy team"""
        score = 0.0
        breakdown = {}
        
        total_games = self.wins + self.losses
        if total_games == 0:
            return {"score": 0, "breakdown": {}}
        
        # Fantasy losses hurt more emotionally
        loss_points = self.losses * 8
        score += loss_points
        if loss_points > 0:
            breakdown["Fantasy Losses"] = loss_points
        
        # Expectation gap
        win_pct = self.wins / total_games
        expected_win_pct = self.expected_performance / 10.0
        gap = expected_win_pct - win_pct
        
        if gap > 0:
            gap_penalty = gap * 25
            expectations_mult = self.jasons_expectations / 10.0
            gap_penalty *= expectations_mult
            score += gap_penalty
            if gap_penalty > 0:
                breakdown["Fantasy Expectation Gap"] = gap_penalty
        
        # Consecutive losses
        if self.recent_streak:
            consecutive_losses = sum(1 for r in reversed(self.recent_streak) if r == "L")
            if consecutive_losses > 1:
                streak_penalty = (consecutive_losses - 1) * 5
                score += streak_penalty
                if streak_penalty > 0:
                    breakdown[f"Fantasy Losing Streak ({consecutive_losses})"] = streak_penalty
        
        return {
            "score": score,
            "breakdown": breakdown
        }


class DepressionCalculator:
    """Main calculator class"""
    
    def __init__(self, config_path: str = "teams_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.teams = []
        self.f1_driver = None
        self.fantasy_team = None
        self.load_data()
    
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {self.config_path} not found. Using defaults.")
            return {"teams": [], "fantasy_team": {}, "f1_driver": {}}
    
    def save_config(self):
        """Save current state to config file"""
        config = {
            "teams": [],
            "fantasy_team": {},
            "f1_driver": {}
        }
        
        for team in self.teams:
            config["teams"].append({
                "name": team.name,
                "sport": team.sport,
                "record": {"wins": team.wins, "losses": team.losses},
                "expected_performance": team.expected_performance,
                "jasons_expectations": team.jasons_expectations,
                "rivals": team.rivals,
                "recent_rivalry_losses": team.recent_rivalry_losses,
                "recent_streak": team.recent_streak,
                "interest_level": team.interest_level,
                "notes": team.notes
            })
        
        if self.f1_driver:
            config["f1_driver"] = {
                "name": self.f1_driver.name,
                "championship_position": self.f1_driver.championship_position,
                "expected_performance": self.f1_driver.expected_performance,
                "jasons_expectations": self.f1_driver.jasons_expectations,
                "recent_races": self.f1_driver.recent_races,
                "recent_dnfs": self.f1_driver.recent_dnfs,
                "rivals": self.f1_driver.rivals,
                "notes": self.f1_driver.notes
            }
        
        if self.fantasy_team:
            config["fantasy_team"] = {
                "name": self.fantasy_team.name,
                "record": {"wins": self.fantasy_team.wins, "losses": self.fantasy_team.losses},
                "expected_performance": self.fantasy_team.expected_performance,
                "jasons_expectations": self.fantasy_team.jasons_expectations,
                "recent_streak": self.fantasy_team.recent_streak
            }
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_data(self):
        """Load teams and data from config"""
        # Load teams
        for team_data in self.config.get("teams", []):
            record = team_data.get("record", {"wins": 0, "losses": 0})
            team = Team(
                name=team_data["name"],
                sport=team_data["sport"],
                wins=record.get("wins", 0),
                losses=record.get("losses", 0),
                expected_performance=team_data.get("expected_performance", 5),
                jasons_expectations=team_data.get("jasons_expectations", 5),
                rivals=team_data.get("rivals", []),
                recent_rivalry_losses=team_data.get("recent_rivalry_losses", []),
                recent_streak=team_data.get("recent_streak", []),
                interest_level=team_data.get("interest_level", 1.0),
                notes=team_data.get("notes", "")
            )
            self.teams.append(team)
        
        # Load F1 driver
        f1_data = self.config.get("f1_driver", {})
        if f1_data:
            self.f1_driver = F1Driver(
                name=f1_data.get("name", ""),
                championship_position=f1_data.get("championship_position", 1),
                expected_performance=f1_data.get("expected_performance", 10),
                jasons_expectations=f1_data.get("jasons_expectations", 10),
                recent_races=f1_data.get("recent_races", []),
                recent_dnfs=f1_data.get("recent_dnfs", 0),
                rivals=f1_data.get("rivals", []),
                notes=f1_data.get("notes", "")
            )
        
        # Load fantasy team
        fantasy_data = self.config.get("fantasy_team", {})
        if fantasy_data:
            record = fantasy_data.get("record", {"wins": 0, "losses": 0})
            self.fantasy_team = FantasyTeam(
                name=fantasy_data.get("name", "Fantasy Team"),
                wins=record.get("wins", 0),
                losses=record.get("losses", 0),
                expected_performance=fantasy_data.get("expected_performance", 5),
                jasons_expectations=fantasy_data.get("jasons_expectations", 5),
                recent_streak=fantasy_data.get("recent_streak", [])
            )
    
    def calculate_total_depression(self) -> Dict:
        """Calculate total depression score and breakdown"""
        total_score = 0.0
        breakdown = {}
        
        # Team contributions
        for team in self.teams:
            result = team.calculate_depression()
            team_score = result["score"]
            total_score += team_score
            if team_score > 0:
                breakdown[team.name] = {
                    "score": team_score,
                    "details": result["breakdown"],
                    "record": f"{team.wins}-{team.losses}"
                }
        
        # F1 contribution
        if self.f1_driver:
            result = self.f1_driver.calculate_depression()
            f1_score = result["score"]
            total_score += f1_score
            if f1_score > 0:
                breakdown[self.f1_driver.name] = {
                    "score": f1_score,
                    "details": result["breakdown"],
                    "position": f"P{self.f1_driver.championship_position}"
                }
        
        # Fantasy contribution
        if self.fantasy_team:
            result = self.fantasy_team.calculate_depression()
            fantasy_score = result["score"]
            total_score += fantasy_score
            if fantasy_score > 0:
                breakdown[self.fantasy_team.name] = {
                    "score": fantasy_score,
                    "details": result["breakdown"],
                    "record": f"{self.fantasy_team.wins}-{self.fantasy_team.losses}"
                }
        
        return {
            "total_score": max(0, total_score),  # Can't go negative
            "breakdown": breakdown
        }
    
    def get_depression_level(self, score: float) -> tuple:
        """Get emoji and description for depression level"""
        if score <= 10:
            return ("😊", "Feeling Great!")
        elif score <= 25:
            return ("😐", "Mildly Disappointed")
        elif score <= 50:
            return ("😔", "Pretty Depressed")
        elif score <= 75:
            return ("😢", "Very Depressed")
        elif score <= 100:
            return ("😭", "Rock Bottom")
        else:
            return ("💀", "Call for Help")
    
    def generate_report(self) -> str:
        """Generate a formatted report"""
        result = self.calculate_total_depression()
        score = result["total_score"]
        breakdown = result["breakdown"]
        
        emoji, level = self.get_depression_level(score)
        
        report = []
        report.append("=" * 60)
        report.append(f"  JASON'S DEPRESSION CALCULATOR")
        report.append("=" * 60)
        report.append("")
        report.append(f"  Depression Score: {score:.1f}")
        report.append(f"  Level: {emoji} {level}")
        report.append("")
        
        if breakdown:
            report.append("  BREAKDOWN BY SOURCE:")
            report.append("-" * 60)
            
            # Sort by score (highest first)
            sorted_breakdown = sorted(breakdown.items(), key=lambda x: x[1]["score"], reverse=True)
            
            for source, data in sorted_breakdown:
                report.append(f"  {source}: {data['score']:.1f} points")
                if "record" in data:
                    report.append(f"    Record: {data['record']}")
                if "position" in data:
                    report.append(f"    Position: {data['position']}")
                
                if data.get("details"):
                    for detail, points in data["details"].items():
                        report.append(f"    - {detail}: +{points:.1f}")
                report.append("")
        else:
            report.append("  No depression sources found. You're doing great! 😊")
            report.append("")
        
        report.append("=" * 60)
        report.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Calculate Jason's depression level")
    parser.add_argument("--config", default="teams_config.json", help="Path to config file")
    parser.add_argument("--update-team", help="Team name to update")
    parser.add_argument("--wins", type=int, help="Number of wins")
    parser.add_argument("--losses", type=int, help="Number of losses")
    parser.add_argument("--rivalry-loss", help="Add a rivalry loss (team name)")
    parser.add_argument("--f1-position", type=int, help="Update F1 championship position")
    parser.add_argument("--f1-dnf", type=int, help="Number of recent DNFs")
    parser.add_argument("--fantasy-wins", type=int, help="Fantasy team wins")
    parser.add_argument("--fantasy-losses", type=int, help="Fantasy team losses")
    
    args = parser.parse_args()
    
    calc = DepressionCalculator(args.config)
    
    # Handle updates
    if args.update_team:
        for team in calc.teams:
            if args.update_team.lower() in team.name.lower():
                if args.wins is not None:
                    team.wins = args.wins
                if args.losses is not None:
                    team.losses = args.losses
                if args.rivalry_loss:
                    if args.rivalry_loss not in team.recent_rivalry_losses:
                        team.recent_rivalry_losses.append(args.rivalry_loss)
                calc.save_config()
                break
    
    if args.f1_position is not None and calc.f1_driver:
        calc.f1_driver.championship_position = args.f1_position
        calc.save_config()
    
    if args.f1_dnf is not None and calc.f1_driver:
        calc.f1_driver.recent_dnfs = args.f1_dnf
        calc.save_config()
    
    if args.fantasy_wins is not None and calc.fantasy_team:
        calc.fantasy_team.wins = args.fantasy_wins
        calc.save_config()
    
    if args.fantasy_losses is not None and calc.fantasy_team:
        calc.fantasy_team.losses = args.fantasy_losses
        calc.save_config()
    
    # Generate and print report
    report = calc.generate_report()
    print(report)


if __name__ == "__main__":
    main()

