#!/usr/bin/env python3
"""
Depression Dashboard
Calculates depression level based on favorite teams' performance
"""

import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import math

try:
    from .espn_fantasy import ESPNFantasyClient, get_espn_credentials_instructions
    ESPN_AVAILABLE = True
except ImportError:
    ESPN_AVAILABLE = False
    print("Warning: ESPN Fantasy integration not available. Install espn-api library.")


def calculate_time_weight(days_ago: float, hours_ago: float = None, decay_rate: float = 0.5) -> float:
    """
    Calculate time-based weight using exponential decay.
    Recent events have MUCH more impact than older ones.
    
    Args:
        days_ago: Number of days since the event
        hours_ago: Optional hours since event (for very recent events)
        decay_rate: Decay rate (higher = faster decay). Default 0.5 gives:
            - 0 hours (just happened): 1.0 (100%)
            - 6 hours: 0.78 (78%)
            - 12 hours: 0.61 (61%)
            - 1 day: 0.61 (61%)
            - 2 days: 0.37 (37%)
            - 3 days: 0.22 (22%)
            - 4 days: 0.14 (14%)
            - 5+ days: < 0.08 (< 8%)
    
    Returns:
        Weight multiplier (0.0 to 1.0)
    """
    if days_ago < 0:
        days_ago = 0
    
    # If hours_ago is provided and less than 1 day, use more granular calculation
    if hours_ago is not None and hours_ago < 24:
        # Convert to days for calculation, but use more aggressive decay
        effective_days = hours_ago / 24.0
        # More aggressive decay for very recent events
        return math.exp(-effective_days * decay_rate * 1.5)
    
    # Standard exponential decay
    return math.exp(-days_ago * decay_rate)


def get_event_timestamps(events: List[str], days_back: int = 5) -> List[Tuple[str, float]]:
    """
    Convert event list to list of (event, days_ago) tuples.
    Assumes events are in chronological order (oldest first) or reverse (newest first).
    
    Args:
        events: List of events (e.g., ["W", "L", "W"])
        days_back: Number of days to go back (default 5)
    
    Returns:
        List of (event, days_ago) tuples
    """
    if not events:
        return []
    
    # Assume events are most recent first (reverse chronological)
    # If you have 5 events, they're from 0, 1, 2, 3, 4 days ago
    result = []
    for i, event in enumerate(events):
        days_ago = i  # Most recent is 0 days ago
        result.append((event, days_ago))
    return result


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
    ties: int = 0  # For NFL teams
    recent_streak_timestamps: List[str] = field(default_factory=list)  # ISO format dates
    recent_rivalry_loss_timestamps: List[str] = field(default_factory=list)  # ISO format dates
    recent_opponents: List[str] = field(default_factory=list)  # Opponent names for recent games (same order as recent_streak)
    recent_opponent_records: List[Dict] = field(default_factory=list)  # [{"wins": X, "losses": Y}] for opponent quality
    interest_level: float = 1.0  # Multiplier for teams Jason cares less about
    notes: str = ""
    is_offseason: bool = False  # True if team is in offseason
    
    # Game Context Parameters
    recent_game_locations: List[str] = field(default_factory=list)  # "home" or "away" for each recent game
    recent_score_margins: List[int] = field(default_factory=list)  # Point differential (positive = win margin, negative = loss margin)
    recent_overtime_games: List[bool] = field(default_factory=list)  # True if game went to OT
    recent_comeback_wins: List[bool] = field(default_factory=list)  # True if came back from behind to win
    recent_comeback_losses: List[bool] = field(default_factory=list)  # True if blew a lead to lose
    recent_blowout_losses: List[bool] = field(default_factory=list)  # True if lost by 20+ points
    recent_blowout_wins: List[bool] = field(default_factory=list)  # True if won by 20+ points
    
    # Season Context Parameters
    playoff_position: Optional[int] = None  # Current playoff seed (1-8, None if not in playoffs)
    division_standing: Optional[int] = None  # Position in division (1-4)
    conference_standing: Optional[int] = None  # Position in conference
    games_back: Optional[float] = None  # Games back from division/conference leader
    playoff_eliminated: bool = False  # True if eliminated from playoffs
    playoff_clinched: bool = False  # True if clinched playoff spot
    division_leader: bool = False  # True if leading division
    conference_leader: bool = False  # True if leading conference
    season_progress: float = 0.5  # 0.0 = start of season, 1.0 = end of season
    
    # Team-Specific Parameters (API-callable or calculable)
    weather_affected_game: List[bool] = field(default_factory=list)  # True if weather was a factor (can get from weather API)
    
    # Game Context (extracted from dates)
    game_day_of_week: List[str] = field(default_factory=list)  # "Monday", "Sunday", etc. (extracted from date)
    game_time_of_day: List[str] = field(default_factory=list)  # "morning", "afternoon", "evening", "night" (extracted from date)
    
    # Historical Context
    head_to_head_record: Dict[str, Dict] = field(default_factory=dict)  # {"Opponent": {"wins": X, "losses": Y}}
    recent_playoff_performance: int = 0  # 1-10 scale: how well did they do in recent playoffs?
    championship_drought_years: int = 0  # Years since last championship
    franchise_legacy: int = 5  # 1-10 scale: how storied is the franchise?
    
    # Streak Context
    longest_win_streak: int = 0  # Longest winning streak this season
    longest_lose_streak: int = 0  # Longest losing streak this season
    current_win_streak: int = 0  # Current winning streak
    current_lose_streak: int = 0  # Current losing streak
    
    def is_in_offseason(self) -> bool:
        """Check if team is currently in offseason based on sport and date"""
        from datetime import datetime
        current_month = datetime.now().month
        current_date = datetime.now()
        
        if self.sport == "MLB":
            # MLB season: March/April - October
            # Offseason: November - February
            return current_month in [11, 12, 1, 2]
        elif self.sport == "NFL":
            # NFL season: September - February (playoffs)
            # Offseason: March - August
            return current_month in [3, 4, 5, 6, 7, 8]
        elif self.sport == "NBA":
            # NBA season: October - June
            # Offseason: July - September
            return current_month in [7, 8, 9]
        elif self.sport in ["NCAA Basketball", "NCAA Football"]:
            # College basketball: November - April
            # College football: August - January
            if self.sport == "NCAA Basketball":
                return current_month in [5, 6, 7, 8, 9, 10]
            else:  # NCAA Football
                return current_month in [2, 3, 4, 5, 6, 7]
        return False
    
    def calculate_depression(self) -> Dict[str, float]:
        """Calculate depression contribution from this team"""
        score = 0.0
        breakdown = {}
        
        # Check if in offseason
        self.is_offseason = self.is_in_offseason()
        
        # If in offseason, drastically reduce impact (only 1% of normal - hardly any impact)
        offseason_multiplier = 0.01 if self.is_offseason else 1.0
        
        total_games = self.wins + self.losses
        if total_games == 0:
            return {"score": 0, "breakdown": {}}
        
        win_pct = self.wins / total_games
        
        # Context-aware weighting: if team is doing well, losses hurt less
        # If win% > 0.6, losses are 50% less impactful
        # If win% > 0.5, losses are 30% less impactful
        if win_pct > 0.6:
            context_multiplier = 0.5  # Team is doing great, losses don't hurt as much
        elif win_pct > 0.5:
            context_multiplier = 0.7  # Team is doing okay, losses hurt less
        else:
            context_multiplier = 1.0  # Team struggling, losses hurt full
        
        # Base loss penalty (reduced from 5.0 to 3.0, scaled by interest and context)
        base_loss_points = 3.0 * self.interest_level * context_multiplier
        
        # POSITIVE: Recent wins reduce depression
        win_points = 0.0
        loss_points = 0.0
        
        # If we have recent games, weight recent events with opponent context
        if self.recent_streak:
            events_with_time = get_event_timestamps(self.recent_streak)
            
            for i, (event, days_ago) in enumerate(events_with_time):
                weight = calculate_time_weight(days_ago)
                opponent_multiplier = 1.0  # Default multiplier
                game_context_multiplier = 1.0  # Game-specific context
                emotional_multiplier = 1.0  # Emotional context
                
                if event == "W":
                    # Wins reduce depression (recent wins help more)
                    # Beating a good team/rival feels better
                    if i < len(self.recent_opponents):
                        opponent = self.recent_opponents[i]
                        if opponent in self.rivals:
                            # Beating a rival feels extra good!
                            opponent_multiplier = 1.5
                        elif i < len(self.recent_opponent_records):
                            opp_record = self.recent_opponent_records[i]
                            opp_wins = opp_record.get("wins", 0)
                            opp_losses = opp_record.get("losses", 0)
                            if opp_wins + opp_losses > 0:
                                opp_win_pct = opp_wins / (opp_wins + opp_losses)
                                if opp_win_pct > 0.6:
                                    # Beating a good team feels better
                                    opponent_multiplier = 1.3
                    
                    # Game context for wins
                    if i < len(self.recent_comeback_wins) and self.recent_comeback_wins[i]:
                        game_context_multiplier *= 1.4  # Comeback wins feel amazing!
                    if i < len(self.recent_blowout_wins) and self.recent_blowout_wins[i]:
                        game_context_multiplier *= 1.2  # Blowout wins are satisfying
                    if i < len(self.recent_overtime_games) and self.recent_overtime_games[i]:
                        game_context_multiplier *= 1.3  # OT wins are thrilling
                    if i < len(self.recent_game_locations) and self.recent_game_locations[i] == "away":
                        game_context_multiplier *= 1.1  # Road wins feel better
                    
                    # Game importance can be inferred from season context
                    # (late season games, playoff implications, etc.)
                    
                    win_points -= 2.0 * self.interest_level * weight * opponent_multiplier * game_context_multiplier * emotional_multiplier
                    
                elif event == "L":
                    # Losses add depression - context matters!
                    if i < len(self.recent_opponents):
                        opponent = self.recent_opponents[i]
                        is_rival = opponent in self.rivals
                        
                        # Get opponent quality if available
                        opp_win_pct = None
                        if i < len(self.recent_opponent_records):
                            opp_record = self.recent_opponent_records[i]
                            opp_wins = opp_record.get("wins", 0)
                            opp_losses = opp_record.get("losses", 0)
                            if opp_wins + opp_losses > 0:
                                opp_win_pct = opp_wins / (opp_wins + opp_losses)
                        
                        # Rivalry losses are always painful, but quality matters
                        if is_rival:
                            if opp_win_pct is not None:
                                if opp_win_pct < 0.35:
                                    # Losing to a BAD rival is EXTRA embarrassing
                                    opponent_multiplier = 2.2  # "We lost to THEM?!"
                                elif opp_win_pct < 0.45:
                                    # Losing to a below-average rival is very disappointing
                                    opponent_multiplier = 2.0
                                elif opp_win_pct > 0.65:
                                    # Losing to a great rival still hurts, but less
                                    opponent_multiplier = 1.5  # "They're good, but still a rival"
                                else:
                                    # Average/good rival
                                    opponent_multiplier = 1.8  # Standard rivalry pain
                            else:
                                # No opponent record, assume standard rivalry pain
                                opponent_multiplier = 1.8
                        elif opp_win_pct is not None:
                            # Non-rival, check quality
                            if opp_win_pct > 0.65:
                                # Losing to a great team (65%+ win rate) hurts less
                                opponent_multiplier = 0.6  # "They're really good, expected loss"
                            elif opp_win_pct > 0.55:
                                # Losing to a good team (55-65%) hurts a bit less
                                opponent_multiplier = 0.8
                            elif opp_win_pct < 0.35:
                                # Losing to a bad team (<35%) is EMBARRASSING
                                opponent_multiplier = 1.5  # "We should have won!"
                            elif opp_win_pct < 0.45:
                                # Losing to a below-average team (35-45%) is disappointing
                                opponent_multiplier = 1.2
                                # 0.45-0.55 = average team, multiplier stays at 1.0
                    
                    # Game context for losses
                    if i < len(self.recent_comeback_losses) and self.recent_comeback_losses[i]:
                        game_context_multiplier *= 1.6  # Blowing a lead is devastating!
                    if i < len(self.recent_blowout_losses) and self.recent_blowout_losses[i]:
                        game_context_multiplier *= 1.4  # Getting blown out is embarrassing
                    if i < len(self.recent_overtime_games) and i < len(self.recent_streak):
                        if self.recent_overtime_games[i] and self.recent_streak[i] == "L":
                            game_context_multiplier *= 1.3  # OT losses are heartbreaking
                    if i < len(self.recent_score_margins):
                        margin = abs(self.recent_score_margins[i])
                        if margin < 3:
                            game_context_multiplier *= 1.2  # Close losses hurt more
                    if i < len(self.recent_game_locations) and self.recent_game_locations[i] == "home":
                        game_context_multiplier *= 1.1  # Home losses are worse
                    
                    # Game importance inferred from season context
                    # (late season, playoff implications handled in season context section)
                    
                    loss_points += base_loss_points * weight * opponent_multiplier * game_context_multiplier * emotional_multiplier
            
            # Add remaining losses (not in recent streak) with lower weight
            total_recent_losses = sum(1 for e in self.recent_streak if e == "L")
            remaining_losses = max(0, self.losses - total_recent_losses)
            if remaining_losses > 0:
                # Older losses get 20% weight
                loss_points += remaining_losses * base_loss_points * 0.2
        else:
            # No recent streak data, use standard calculation with time decay
            # Assume losses are spread over season, so average age is ~half season
            avg_days_ago = 30  # Rough estimate
            weight = calculate_time_weight(avg_days_ago)
            loss_points = self.losses * base_loss_points * weight
        
        # Season context penalties/bonuses
        season_context_penalty = 0.0
        
        # Playoff implications
        if self.playoff_eliminated:
            season_context_penalty += 10.0 * self.interest_level  # Eliminated = major depression
            breakdown["Playoff Eliminated"] = 10.0 * self.interest_level
        elif self.games_back and self.games_back > 3:
            season_context_penalty += 5.0 * self.interest_level  # Far from playoffs
            breakdown["Far from Playoffs"] = 5.0 * self.interest_level
        elif self.playoff_clinched:
            season_context_penalty -= 8.0 * self.interest_level  # Clinched = reduces depression
            breakdown["Playoff Clinched (reduces depression)"] = -8.0 * self.interest_level
        elif self.division_leader or self.conference_leader:
            season_context_penalty -= 3.0 * self.interest_level  # Leading = good
            breakdown["Division/Conference Leader (reduces depression)"] = -3.0 * self.interest_level
        
        # Late season losses hurt more
        if self.season_progress > 0.75:  # Last quarter of season
            late_season_multiplier = 1.3
        elif self.season_progress > 0.5:  # Second half
            late_season_multiplier = 1.1
        else:
            late_season_multiplier = 1.0
        
        loss_points *= late_season_multiplier
        if late_season_multiplier > 1.0:
            breakdown["Late Season Multiplier"] = (late_season_multiplier - 1.0) * loss_points
        
        # Historical context
        historical_penalty = 0.0
        
        # Championship drought (can be calculated from historical data)
        if self.championship_drought_years > 20:
            historical_penalty += 2.0 * self.interest_level
            breakdown[f"Long Championship Drought ({self.championship_drought_years} years)"] = 2.0 * self.interest_level
        
        # Current losing streak
        if self.current_lose_streak >= 5:
            team_context_penalty += 4.0 * self.interest_level
            breakdown[f"Long Losing Streak ({self.current_lose_streak} games)"] = 4.0 * self.interest_level
        elif self.current_lose_streak >= 3:
            team_context_penalty += 2.0 * self.interest_level
            breakdown[f"Losing Streak ({self.current_lose_streak} games)"] = 2.0 * self.interest_level
        
        score += loss_points
        score += win_points  # Negative value reduces depression
        score += season_context_penalty
        score += historical_penalty
        
        if loss_points > 0:
            breakdown["Losses (time-weighted, context-adjusted)"] = loss_points
        if win_points < 0:
            breakdown["Recent Wins (reduces depression)"] = win_points
        
        # Expectation gap penalty (reduced weights)
        expected_win_pct = self.expected_performance / 10.0
        actual_win_pct = win_pct
        gap = expected_win_pct - actual_win_pct
        
        if gap > 0:  # Underperforming
            # Reduced multipliers: 30->15, 20->10, 10->5
            if self.expected_performance >= 8:
                gap_penalty = gap * 15 * self.interest_level
            elif self.expected_performance >= 5:
                gap_penalty = gap * 10 * self.interest_level
            else:
                gap_penalty = gap * 5 * self.interest_level
            
            # Multiply by expectations multiplier
            expectations_mult = self.jasons_expectations / 10.0
            gap_penalty *= expectations_mult
            
            score += gap_penalty
            if gap_penalty > 0:
                breakdown["Expectation Gap"] = gap_penalty
        elif gap < -0.1:  # Overperforming! (doing better than expected)
            # Positive: reduce depression for overperforming
            overperformance_bonus = abs(gap) * 5 * self.interest_level
            score -= overperformance_bonus  # Negative = reduces depression
            if overperformance_bonus > 0:
                breakdown["Overperforming (reduces depression)"] = -overperformance_bonus
        
        # Rivalry loss multiplier (time-weighted, reduced from 2.5x to 1.8x)
        # Rivalry losses already accounted for in recent_streak with opponent context
        # This is for additional rivalry loss tracking if needed
        if self.recent_rivalry_losses:
            # Reduced multiplier and context-aware
            rivalry_multiplier = 1.8 * self.interest_level * context_multiplier
            rivalry_base = base_loss_points * (rivalry_multiplier - 1)
            
            # Calculate time-weighted penalty
            rivalry_penalty = 0.0
            if self.recent_rivalry_loss_timestamps:
                # Use timestamps if available
                for i, loss in enumerate(self.recent_rivalry_losses):
                    if i < len(self.recent_rivalry_loss_timestamps):
                        try:
                            loss_date = datetime.fromisoformat(self.recent_rivalry_loss_timestamps[i])
                            days_ago = (datetime.now() - loss_date.replace(tzinfo=None)).days
                            weight = calculate_time_weight(days_ago)
                            rivalry_penalty += rivalry_base * weight
                        except (ValueError, TypeError):
                            # Fallback: assume recent (0 days ago)
                            rivalry_penalty += rivalry_base * 1.0
                    else:
                        # No timestamp, assume very recent
                        rivalry_penalty += rivalry_base * 1.0
            else:
                # No timestamps: weight by position (most recent = highest weight)
                for i, loss in enumerate(self.recent_rivalry_losses):
                    weight = calculate_time_weight(i)  # i=0 is most recent
                    rivalry_penalty += rivalry_base * weight
            
            score += rivalry_penalty
            if rivalry_penalty > 0:
                breakdown["Rivalry Losses (time-weighted)"] = rivalry_penalty
        
        # Consecutive losses (time-weighted)
        # Recent losing streaks are way more depressing
        if self.recent_streak:
            # Get events with timestamps
            events_with_time = get_event_timestamps(self.recent_streak)
            
            # Calculate time-weighted losing streak
            streak_penalty = 0.0
            consecutive_losses = 0
            
            # Process from most recent backwards
            for event, days_ago in events_with_time:
                if event == "L":
                    consecutive_losses += 1
                    # Very recent losses in a streak are extra painful
                    weight = calculate_time_weight(days_ago, decay_rate=0.5)
                    if days_ago == 0:  # Just lost
                        weight = 1.0  # Full pain
                    elif days_ago == 1:  # Lost yesterday
                        weight = 0.61  # Still hurts
                    
                    # Recent losses in a streak get extra multiplier (reduced from 1.3x to 1.2x)
                    if consecutive_losses <= 2 and days_ago <= 1:
                        weight *= 1.2  # 20% extra pain for recent streak
                    
                    # Reduced from 3 to 2 points per loss in streak
                    streak_penalty += 2 * self.interest_level * context_multiplier * weight
                else:
                    break  # Streak broken
            
            if consecutive_losses > 1:
                score += streak_penalty
                if streak_penalty > 0:
                    breakdown[f"Losing Streak ({consecutive_losses} games, time-weighted)"] = streak_penalty
        
        # Apply offseason multiplier to final score
        final_score = score * offseason_multiplier
        
        # Update breakdown values if in offseason
        if self.is_offseason and score > 0:
            breakdown["Offseason (reduced impact)"] = final_score - score
        
        return {
            "score": final_score,
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
    recent_race_timestamps: List[str] = field(default_factory=list)  # ISO format dates
    recent_dnf_timestamps: List[str] = field(default_factory=list)  # ISO format dates
    notes: str = ""
    
    def calculate_depression(self) -> Dict[str, float]:
        """Calculate depression contribution from F1 performance"""
        score = 0.0
        breakdown = {}
        
        # Position penalty (reduced, and Max is #1 so this should be 0)
        if self.championship_position > 1:
            position_penalty = (self.championship_position - 1) * 2  # Reduced from 3 to 2
            score += position_penalty
            breakdown["Championship Position"] = position_penalty
        elif self.championship_position == 1:
            # POSITIVE: Being #1 reduces depression!
            score -= 5.0  # Negative = reduces depression
            breakdown["Championship Leader (reduces depression)"] = -5.0
        
        # Expectation gap (reduced weights)
        if self.expected_performance >= 9 and self.championship_position > 1:
            gap_penalty = (self.championship_position - 1) * 5  # Reduced from 8 to 5
            expectations_mult = self.jasons_expectations / 10.0
            gap_penalty *= expectations_mult
            score += gap_penalty
            if gap_penalty > 0:
                breakdown["Expectation Gap (Should be #1)"] = gap_penalty
        
        # POSITIVE: Recent wins reduce depression significantly
        if self.recent_races:
            events_with_time = get_event_timestamps(self.recent_races)
            win_bonus = 0.0
            
            for event, days_ago in events_with_time:
                weight = calculate_time_weight(days_ago)
                if event == "W":
                    # Wins reduce depression (recent wins help more)
                    win_bonus -= 4.0 * weight  # Negative = reduces depression
                elif event == "P2":
                    # Podium finishes also help
                    win_bonus -= 2.0 * weight
                elif event == "P3":
                    win_bonus -= 1.0 * weight
            
            score += win_bonus
            if win_bonus < 0:
                breakdown["Recent Wins/Podiums (reduces depression)"] = win_bonus
        
        # DNF penalty (reduced from 12 to 8, time-weighted)
        # A DNF that JUST happened is devastating, but gets less painful over time
        if self.recent_dnfs > 0:
            dnf_penalty = 0.0
            base_dnf_penalty = 8.0  # Reduced from 12 to 8
            
            if self.recent_dnf_timestamps:
                # Use timestamps if available - check hours for very recent DNFs
                for i in range(min(self.recent_dnfs, len(self.recent_dnf_timestamps))):
                    try:
                        dnf_date = datetime.fromisoformat(self.recent_dnf_timestamps[i])
                        now = datetime.now()
                        if dnf_date.tzinfo:
                            # Remove timezone for comparison
                            dnf_date = dnf_date.replace(tzinfo=None)
                        
                        time_diff = now - dnf_date
                        hours_ago = time_diff.total_seconds() / 3600.0
                        days_ago = time_diff.days
                        
                        # Very recent DNFs (within 24 hours) get extra weight
                        if hours_ago < 24:
                            weight = calculate_time_weight(days_ago, hours_ago=hours_ago, decay_rate=0.6)
                            # Boost for very recent (just happened = devastating)
                            if hours_ago < 6:
                                weight = min(1.0, weight * 1.2)  # 20% boost for very recent
                        else:
                            weight = calculate_time_weight(days_ago, decay_rate=0.5)
                        
                        dnf_penalty += base_dnf_penalty * weight
                    except (ValueError, TypeError):
                        # Fallback: assume very recent (full weight)
                        dnf_penalty += base_dnf_penalty * 1.0
            else:
                # No timestamps: weight by position in recent_races
                # Check if DNF is in recent races and weight accordingly
                dnf_found = 0
                if self.recent_races:
                    events_with_time = get_event_timestamps(self.recent_races)
                    for event, days_ago in events_with_time:
                        if event == "DNF" and dnf_found < self.recent_dnfs:
                            # Very recent DNFs hurt WAY more
                            weight = calculate_time_weight(days_ago, decay_rate=0.6)
                            if days_ago == 0:  # Just happened
                                weight = 1.0  # Full devastation
                            dnf_penalty += base_dnf_penalty * weight
                            dnf_found += 1
                
                # If we still have DNFs not accounted for, assume they're older
                remaining_dnfs = self.recent_dnfs - dnf_found
                if remaining_dnfs > 0:
                    # Older DNFs get less weight (assume 7+ days ago)
                    weight = calculate_time_weight(7, decay_rate=0.5)
                    dnf_penalty += remaining_dnfs * base_dnf_penalty * weight
            
            score += dnf_penalty
            if dnf_penalty > 0:
                breakdown["DNFs (time-weighted)"] = dnf_penalty
        
        # Recent race performance (time-weighted, reduced from 5 to 3)
        # Bad results that just happened hurt way more than old ones
        if self.recent_races:
            events_with_time = get_event_timestamps(self.recent_races)
            race_penalty = 0.0
            
            for event, days_ago in events_with_time:
                if event not in ["W", "P2", "P3"]:  # Poor result
                    # Very recent poor results are devastating
                    weight = calculate_time_weight(days_ago, decay_rate=0.5)
                    if days_ago == 0:  # Just happened
                        weight = 1.0  # Full impact
                    elif days_ago == 1:  # Yesterday
                        weight = 0.61  # Still hurts a lot
                    race_penalty += 3 * weight  # Reduced from 5 to 3
            
            if race_penalty > 0:
                score += race_penalty
                breakdown["Recent Poor Results (time-weighted)"] = race_penalty
        
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
    recent_streak_timestamps: List[str] = field(default_factory=list)  # ISO format dates
    
    def calculate_depression(self) -> Dict[str, float]:
        """Calculate depression contribution from fantasy team"""
        score = 0.0
        breakdown = {}
        
        total_games = self.wins + self.losses
        if total_games == 0:
            return {"score": 0, "breakdown": {}}
        
        win_pct = self.wins / total_games
        
        # Context-aware: if fantasy team is doing well, losses hurt less
        # If win% > 0.6, losses are 60% less impactful
        # If win% > 0.5, losses are 40% less impactful
        if win_pct > 0.6:
            context_multiplier = 0.4  # Team is doing great, losses don't hurt much
        elif win_pct > 0.5:
            context_multiplier = 0.6  # Team is doing okay, losses hurt less
        else:
            context_multiplier = 1.0  # Team struggling, losses hurt full
        
        # Fantasy losses (reduced from 8 to 5, context-aware)
        loss_points = 0.0
        win_points = 0.0
        
        if self.recent_streak:
            events_with_time = get_event_timestamps(self.recent_streak)
            
            for event, days_ago in events_with_time:
                weight = calculate_time_weight(days_ago, decay_rate=0.5)
                if event == "W":
                    # Wins reduce depression (recent wins help more)
                    win_points -= 3.0 * weight  # Negative = reduces depression
                elif event == "L":
                    if days_ago == 0:  # Just lost
                        weight = 1.0  # Full devastation
                    loss_points += 5 * context_multiplier * weight  # Reduced from 8 to 5
            
            # Add remaining losses with lower weight
            total_recent_losses = sum(1 for e in self.recent_streak if e == "L")
            remaining_losses = max(0, self.losses - total_recent_losses)
            if remaining_losses > 0:
                loss_points += remaining_losses * 5 * context_multiplier * 0.2  # Older losses less painful
        else:
            # No recent data, assume average age
            weight = calculate_time_weight(30, decay_rate=0.5)
            loss_points = self.losses * 5 * context_multiplier * weight
        
        score += loss_points
        score += win_points  # Negative value reduces depression
        
        if loss_points > 0:
            breakdown["Fantasy Losses (time-weighted, context-adjusted)"] = loss_points
        if win_points < 0:
            breakdown["Fantasy Wins (reduces depression)"] = win_points
        
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
        
        # Consecutive losses (time-weighted)
        if self.recent_streak:
            events_with_time = get_event_timestamps(self.recent_streak)
            streak_penalty = 0.0
            consecutive_losses = 0
            
            # Process from most recent backwards
            for event, days_ago in events_with_time:
                if event == "L":
                    consecutive_losses += 1
                    weight = calculate_time_weight(days_ago)
                    streak_penalty += 5 * weight
                else:
                    break  # Streak broken
            
            if consecutive_losses > 1:
                score += streak_penalty
                if streak_penalty > 0:
                    breakdown[f"Fantasy Losing Streak ({consecutive_losses}, time-weighted)"] = streak_penalty
        
        return {
            "score": score,
            "breakdown": breakdown
        }


class DepressionCalculator:
    """Main calculator class"""
    
    def __init__(self, config_path: str = "teams_config.json", use_espn_api: bool = True):
        self.config_path = config_path
        self.config = self.load_config()
        self.teams = []
        self.f1_driver = None
        self.fantasy_team = None
        self.use_espn_api = use_espn_api
        self.espn_client = None
        self.load_data()
    
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Validate config structure
            if not isinstance(config, dict):
                print(f"Error: Config file {self.config_path} is not a valid JSON object")
                return {"teams": [], "fantasy_team": {}, "f1_driver": {}}
            
            # Ensure required top-level keys exist
            if "teams" not in config:
                config["teams"] = []
            if "fantasy_team" not in config:
                config["fantasy_team"] = {}
            if "f1_driver" not in config:
                config["f1_driver"] = {}
            
            return config
        except FileNotFoundError:
            print(f"Config file {self.config_path} not found. Using defaults.")
            return {"teams": [], "fantasy_team": {}, "f1_driver": {}}
        except json.JSONDecodeError as e:
            print(f"Error: Config file {self.config_path} is not valid JSON: {e}")
            print("Please check the file for syntax errors.")
            return {"teams": [], "fantasy_team": {}, "f1_driver": {}}
        except Exception as e:
            print(f"Error loading config file {self.config_path}: {e}")
            import traceback
            traceback.print_exc()
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
                "record": {"wins": team.wins, "losses": team.losses, "ties": team.ties},
                "expected_performance": team.expected_performance,
                "jasons_expectations": team.jasons_expectations,
                "rivals": team.rivals,
                "recent_rivalry_losses": team.recent_rivalry_losses,
                "recent_streak": team.recent_streak,
                "recent_opponents": team.recent_opponents,
                "recent_opponent_records": team.recent_opponent_records,
                "recent_game_locations": team.recent_game_locations,
                "recent_score_margins": team.recent_score_margins,
                "recent_overtime_games": team.recent_overtime_games,
                "recent_comeback_wins": team.recent_comeback_wins,
                "recent_comeback_losses": team.recent_comeback_losses,
                "recent_blowout_losses": team.recent_blowout_losses,
                "recent_blowout_wins": team.recent_blowout_wins,
                "playoff_position": team.playoff_position,
                "division_standing": team.division_standing,
                "conference_standing": team.conference_standing,
                "games_back": team.games_back,
                "playoff_eliminated": team.playoff_eliminated,
                "playoff_clinched": team.playoff_clinched,
                "division_leader": team.division_leader,
                "conference_leader": team.conference_leader,
                "season_progress": team.season_progress,
                "weather_affected_game": team.weather_affected_game,
                "game_day_of_week": team.game_day_of_week,
                "game_time_of_day": team.game_time_of_day,
                "head_to_head_record": team.head_to_head_record,
                "recent_playoff_performance": team.recent_playoff_performance,
                "championship_drought_years": team.championship_drought_years,
                "franchise_legacy": team.franchise_legacy,
                "longest_win_streak": team.longest_win_streak,
                "longest_lose_streak": team.longest_lose_streak,
                "current_win_streak": team.current_win_streak,
                "current_lose_streak": team.current_lose_streak,
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
            try:
                # Ensure record structure exists and has all required fields
                if "record" not in team_data:
                    team_data["record"] = {}
                record = team_data["record"]
                if "wins" not in record:
                    record["wins"] = 0
                if "losses" not in record:
                    record["losses"] = 0
                if "ties" not in record:
                    record["ties"] = 0
                
                # Ensure required fields exist
                if "name" not in team_data:
                    print(f"Warning: Team missing name field, skipping")
                    continue
                if "sport" not in team_data:
                    print(f"Warning: Team {team_data.get('name', 'Unknown')} missing sport field, skipping")
                    continue
                
                team = Team(
                name=team_data["name"],
                sport=team_data["sport"],
                wins=record.get("wins", 0),
                losses=record.get("losses", 0),
                ties=record.get("ties", 0),
                expected_performance=team_data.get("expected_performance", 5),
                jasons_expectations=team_data.get("jasons_expectations", 5),
                rivals=team_data.get("rivals", []),
                recent_rivalry_losses=team_data.get("recent_rivalry_losses", []),
                recent_streak=team_data.get("recent_streak", []),
                recent_opponents=team_data.get("recent_opponents", []),
                recent_opponent_records=team_data.get("recent_opponent_records", []),
                recent_game_locations=team_data.get("recent_game_locations", []),
                recent_score_margins=team_data.get("recent_score_margins", []),
                recent_overtime_games=team_data.get("recent_overtime_games", []),
                recent_comeback_wins=team_data.get("recent_comeback_wins", []),
                recent_comeback_losses=team_data.get("recent_comeback_losses", []),
                recent_blowout_losses=team_data.get("recent_blowout_losses", []),
                recent_blowout_wins=team_data.get("recent_blowout_wins", []),
                playoff_position=team_data.get("playoff_position"),
                division_standing=team_data.get("division_standing"),
                conference_standing=team_data.get("conference_standing"),
                games_back=team_data.get("games_back"),
                playoff_eliminated=team_data.get("playoff_eliminated", False),
                playoff_clinched=team_data.get("playoff_clinched", False),
                division_leader=team_data.get("division_leader", False),
                conference_leader=team_data.get("conference_leader", False),
                season_progress=team_data.get("season_progress", 0.5),
                weather_affected_game=team_data.get("weather_affected_game", []),
                game_day_of_week=team_data.get("game_day_of_week", []),
                game_time_of_day=team_data.get("game_time_of_day", []),
                head_to_head_record=team_data.get("head_to_head_record", {}),
                recent_playoff_performance=team_data.get("recent_playoff_performance", 0),
                championship_drought_years=team_data.get("championship_drought_years", 0),
                franchise_legacy=team_data.get("franchise_legacy", 5),
                longest_win_streak=team_data.get("longest_win_streak", 0),
                longest_lose_streak=team_data.get("longest_lose_streak", 0),
                current_win_streak=team_data.get("current_win_streak", 0),
                current_lose_streak=team_data.get("current_lose_streak", 0),
                interest_level=team_data.get("interest_level", 1.0),
                notes=team_data.get("notes", "")
                )
                self.teams.append(team)
            except KeyError as e:
                print(f"Error loading team {team_data.get('name', 'Unknown')}: Missing required field {e}")
                continue
            except Exception as e:
                print(f"Error loading team {team_data.get('name', 'Unknown')}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # Load F1 driver
        f1_data = self.config.get("f1_driver", {})
        if f1_data:
            try:
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
            except Exception as e:
                print(f"Error loading F1 driver: {e}")
                import traceback
                traceback.print_exc()
        
        # Load fantasy team
        fantasy_data = self.config.get("fantasy_team", {})
        if fantasy_data:
            # Try to fetch from ESPN API if configured
            if self.use_espn_api and ESPN_AVAILABLE:
                espn_config = fantasy_data.get("espn", {})
                if espn_config.get("league_id") and espn_config.get("year"):
                    try:
                        self._load_fantasy_from_espn(espn_config, fantasy_data)
                        return  # Successfully loaded from API
                    except Exception as e:
                        print(f"Warning: Failed to load fantasy data from ESPN API: {e}")
                        print("Falling back to manual config data...")
            
            # Fall back to manual config
            try:
                record = fantasy_data.get("record", {"wins": 0, "losses": 0})
                # Ensure record has required fields
                if "wins" not in record:
                    record["wins"] = 0
                if "losses" not in record:
                    record["losses"] = 0
                
                self.fantasy_team = FantasyTeam(
                    name=fantasy_data.get("name", "Fantasy Team"),
                    wins=record.get("wins", 0),
                    losses=record.get("losses", 0),
                    expected_performance=fantasy_data.get("expected_performance", 5),
                    jasons_expectations=fantasy_data.get("jasons_expectations", 5),
                    recent_streak=fantasy_data.get("recent_streak", [])
                )
            except Exception as e:
                print(f"Error loading fantasy team: {e}")
                import traceback
                traceback.print_exc()
    
    def _load_fantasy_from_espn(self, espn_config: Dict, fantasy_data: Dict):
        """Load fantasy team data from ESPN API"""
        league_id = espn_config["league_id"]
        year = espn_config["year"]
        team_id = espn_config.get("team_id")
        team_name = espn_config.get("team_name") or fantasy_data.get("name")
        espn_s2 = espn_config.get("espn_s2")
        swid = espn_config.get("swid")
        
        # Initialize ESPN client
        self.espn_client = ESPNFantasyClient(
            league_id=league_id,
            year=year,
            team_id=team_id,
            espn_s2=espn_s2,
            swid=swid
        )
        
        # Fetch team data
        team_data = self.espn_client.get_my_team(team_name)
        
        # Create FantasyTeam from API data
        self.fantasy_team = FantasyTeam(
            name=team_data["name"],
            wins=team_data["wins"],
            losses=team_data["losses"],
            expected_performance=fantasy_data.get("expected_performance", 5),
            jasons_expectations=fantasy_data.get("jasons_expectations", 5),
            recent_streak=team_data.get("recent_streak", [])
        )
        
        print(f"✓ Loaded fantasy team '{team_data['name']}' from ESPN API")
        print(f"  Record: {team_data['record']}")
        if team_data.get("matchup"):
            matchup = team_data["matchup"]
            print(f"  Current Week {matchup['week']} Matchup: vs {matchup['opponent']}")
    
    def refresh_fantasy_data(self):
        """Refresh fantasy team data from ESPN API"""
        if not self.espn_client:
            fantasy_data = self.config.get("fantasy_team", {})
            espn_config = fantasy_data.get("espn", {})
            if espn_config.get("league_id") and espn_config.get("year"):
                self._load_fantasy_from_espn(espn_config, fantasy_data)
            else:
                print("ESPN API not configured. Add 'espn' section to fantasy_team in config.")
        else:
            fantasy_data = self.config.get("fantasy_team", {})
            espn_config = fantasy_data.get("espn", {})
            self._load_fantasy_from_espn(espn_config, fantasy_data)
    
    def calculate_total_depression(self) -> Dict:
        """Calculate total depression score and breakdown"""
        total_score = 0.0
        breakdown = {}
        
        # Team contributions
        for team in self.teams:
            result = team.calculate_depression()
            team_score = result["score"]
            total_score += team_score
            # Show all teams, even if reducing depression
            if team_score != 0:
                breakdown[team.name] = {
                    "score": team_score,
                    "details": result["breakdown"],
                    "record": f"{team.wins}-{team.losses}" + (f"-{team.ties}" if hasattr(team, 'ties') and team.ties > 0 else "")
                }
        
        # F1 contribution
        if self.f1_driver:
            result = self.f1_driver.calculate_depression()
            f1_score = result["score"]
            total_score += f1_score
            # Show F1 even if negative (reducing depression is good!)
            if f1_score != 0:
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
            # Show fantasy even if negative (reducing depression is good!)
            if fantasy_score != 0:
                breakdown[self.fantasy_team.name] = {
                    "score": fantasy_score,
                    "details": result["breakdown"],
                    "record": f"{self.fantasy_team.wins}-{self.fantasy_team.losses}"
                }
        
        return {
            "total_score": max(0, total_score),  # Can't go negative
            "breakdown": breakdown,
            "raw_score": total_score  # Keep raw score for reference
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
        report.append(f"  DEPRESSION DASHBOARD")
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
                score_val = data['score']
                if score_val < 0:
                    report.append(f"  {source}: {score_val:.1f} points (reducing depression! 😊)")
                else:
                    report.append(f"  {source}: {score_val:.1f} points")
                if "record" in data:
                    report.append(f"    Record: {data['record']}")
                if "position" in data:
                    report.append(f"    Position: {data['position']}")
                
                if data.get("details"):
                    for detail, points in data["details"].items():
                        if points < 0:
                            report.append(f"    - {detail}: {points:.1f} (reduces depression)")
                        else:
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
    parser = argparse.ArgumentParser(description="Calculate depression level")
    parser.add_argument("--config", default="teams_config.json", help="Path to config file")
    parser.add_argument("--fetch", action="store_true", help="Fetch latest data from APIs before calculating")
    parser.add_argument("--update-team", help="Team name to update")
    parser.add_argument("--wins", type=int, help="Number of wins")
    parser.add_argument("--losses", type=int, help="Number of losses")
    parser.add_argument("--rivalry-loss", help="Add a rivalry loss (team name)")
    parser.add_argument("--f1-position", type=int, help="Update F1 championship position")
    parser.add_argument("--f1-dnf", type=int, help="Number of recent DNFs")
    parser.add_argument("--fantasy-wins", type=int, help="Fantasy team wins")
    parser.add_argument("--fantasy-losses", type=int, help="Fantasy team losses")
    parser.add_argument("--no-espn", action="store_true", help="Disable ESPN API and use manual config only")
    parser.add_argument("--refresh-fantasy", action="store_true", help="Refresh fantasy data from ESPN API")
    parser.add_argument("--espn-help", action="store_true", help="Show instructions for ESPN API setup")
    
    args = parser.parse_args()
    
    # Show ESPN help if requested
    if args.espn_help:
        if ESPN_AVAILABLE:
            print(get_espn_credentials_instructions())
        else:
            print("ESPN Fantasy integration not available. Install espn-api library:")
            print("  pip install espn-api")
        return
    
    # Fetch data from APIs if requested
    if args.fetch:
        try:
            from .sports_api import SportsDataFetcher
            print("Fetching latest data from APIs...")
            fetcher = SportsDataFetcher()
            fetcher.update_config_file(args.config)
            print("Data updated successfully!\n")
        except ImportError:
            print("Warning: sports_api module not available. Install dependencies: pip install -r requirements.txt")
        except Exception as e:
            print(f"Warning: Could not fetch data from APIs: {e}")
            print("Continuing with existing config data...\n")
    
    calc = DepressionCalculator(args.config, use_espn_api=not args.no_espn)
    
    # Refresh fantasy data if requested
    if args.refresh_fantasy:
        calc.refresh_fantasy_data()
        calc.save_config()
    
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

