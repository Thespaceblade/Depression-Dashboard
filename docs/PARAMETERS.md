# Complete Parameter Reference

The depression calculator now supports **56 parameters** for ultra-granular depression calculation!

## Game Context Parameters (7)

### `recent_game_locations`
- **Type**: `List[str]`
- **Values**: `"home"` or `"away"`
- **Impact**: Home losses hurt 10% more; away wins feel 10% better

### `recent_score_margins`
- **Type**: `List[int]`
- **Values**: Point differential (positive = win margin, negative = loss margin)
- **Impact**: Close losses (<3 points) hurt 20% more

### `recent_overtime_games`
- **Type**: `List[bool]`
- **Impact**: OT wins feel 30% better; OT losses hurt 30% more

### `recent_comeback_wins`
- **Type**: `List[bool]`
- **Impact**: Comeback wins feel 40% better (amazing!)

### `recent_comeback_losses`
- **Type**: `List[bool]`
- **Impact**: Blowing a lead hurts 60% more (devastating!)

### `recent_blowout_losses`
- **Type**: `List[bool]`
- **Impact**: Getting blown out hurts 40% more (embarrassing)

### `recent_blowout_wins`
- **Type**: `List[bool]`
- **Impact**: Blowout wins feel 20% better (satisfying)

## Season Context Parameters (10)

### `playoff_position`
- **Type**: `Optional[int]`
- **Values**: 1-8 (seed), `None` if not in playoffs
- **Impact**: Lower seed = more pressure

### `division_standing`
- **Type**: `Optional[int]`
- **Values**: 1-4 (position in division)
- **Impact**: Lower standing = more depression

### `conference_standing`
- **Type**: `Optional[int]`
- **Impact**: Lower standing = more depression

### `games_back`
- **Type**: `Optional[float]`
- **Impact**: >3 games back = +5 points depression

### `playoff_eliminated`
- **Type**: `bool`
- **Impact**: +10 points (major depression!)

### `playoff_clinched`
- **Type**: `bool`
- **Impact**: -8 points (reduces depression)

### `division_leader`
- **Type**: `bool`
- **Impact**: -3 points (reduces depression)

### `conference_leader`
- **Type**: `bool`
- **Impact**: -3 points (reduces depression)

### `season_progress`
- **Type**: `float`
- **Values**: 0.0 (start) to 1.0 (end)
- **Impact**: Late season (>75%) losses hurt 30% more

### `recent_playoff_performance`
- **Type**: `int`
- **Values**: 1-10 scale
- **Impact**: Recent playoff success/failure affects expectations

## Emotional Context Parameters (9)

### `jason_watched_game`
- **Type**: `List[bool]`
- **Impact**: Watching a loss makes it 30% worse; watching a win makes it 20% better

### `jason_bet_on_game`
- **Type**: `List[bool]`
- **Impact**: Losing a bet adds extra pain; winning a bet feels great

### `jason_bet_amount`
- **Type**: `List[float]`
- **Impact**: Higher bet = more pain if lost (up to 2x multiplier)

### `social_media_reactions`
- **Type**: `List[int]`
- **Values**: 1-10 scale (10 = worst reactions)
- **Impact**: Bad reactions (7+) add 20% more pain

### `friend_reactions`
- **Type**: `List[int]`
- **Values**: 1-10 scale (10 = most mocking)
- **Impact**: Friends mocking (7+) adds 30% more pain

### `game_importance`
- **Type**: `List[int]`
- **Values**: 1-10 scale (10 = most important)
- **Impact**: Important games (8+) matter 40% more for losses, 30% more for wins

### `jason_was_stressed`
- **Type**: `List[bool]`
- **Impact**: Already stressed = losses hurt 10% more

### `jason_was_drunk`
- **Type**: `List[bool]`
- **Impact**: Drinking during game affects emotional state

### `jason_was_with_friends`
- **Type**: `List[bool]`
- **Impact**: Watching with friends affects experience

## Team-Specific Parameters (6)

### `key_player_injured`
- **Type**: `bool`
- **Impact**: +5 points × injury severity

### `key_player_injury_severity`
- **Type**: `int`
- **Values**: 1-10 scale
- **Impact**: Multiplies injury penalty

### `coaching_controversy`
- **Type**: `bool`
- **Impact**: +3 points (drama adds stress)

### `team_chemistry_issues`
- **Type**: `bool`
- **Impact**: +2 points (team dysfunction)

### `referee_controversy`
- **Type**: `List[bool]`
- **Impact**: Bad ref calls make losses 20% more frustrating

### `weather_affected_game`
- **Type**: `List[bool]`
- **Impact**: Weather can affect game outcome

## Historical Context Parameters (10)

### `head_to_head_record`
- **Type**: `Dict[str, Dict]`
- **Format**: `{"Opponent": {"wins": X, "losses": Y}}`
- **Impact**: Historical dominance affects expectations

### `championship_drought_years`
- **Type**: `int`
- **Impact**: >20 years = +2 points (long suffering)

### `franchise_legacy`
- **Type**: `int`
- **Values**: 1-10 scale
- **Impact**: Storied franchises have higher expectations

### `longest_win_streak`
- **Type**: `int`
- **Impact**: Shows team's potential

### `longest_lose_streak`
- **Type**: `int`
- **Impact**: Shows team's struggles

### `current_win_streak`
- **Type**: `int`
- **Impact**: Active streaks affect mood

### `current_lose_streak`
- **Type**: `int`
- **Impact**: 3+ losses = +2 points, 5+ losses = +4 points

## Personal Context Parameters (3)

### `game_day_of_week`
- **Type**: `List[str]`
- **Values**: `"Monday"`, `"Sunday"`, etc.
- **Impact**: Weekend games might matter more

### `game_time_of_day`
- **Type**: `List[str]`
- **Values**: `"morning"`, `"afternoon"`, `"evening"`, `"night"`
- **Impact**: Prime time games might matter more

## Example Configuration

```json
{
  "name": "Dallas Cowboys",
  "recent_streak": ["L", "W", "L"],
  "recent_opponents": ["Eagles", "Giants", "Commanders"],
  "recent_game_locations": ["away", "home", "away"],
  "recent_score_margins": [-7, 14, -3],
  "recent_overtime_games": [false, false, true],
  "recent_comeback_losses": [false, false, true],
  "recent_blowout_losses": [false, false, false],
  "playoff_position": 3,
  "playoff_clinched": false,
  "season_progress": 0.75,
  "jason_watched_game": [true, true, true],
  "jason_bet_on_game": [true, false, true],
  "jason_bet_amount": [50, 0, 100],
  "social_media_reactions": [8, 3, 9],
  "friend_reactions": [7, 2, 8],
  "game_importance": [9, 5, 8],
  "key_player_injured": true,
  "key_player_injury_severity": 7,
  "current_lose_streak": 2,
  "championship_drought_years": 28
}
```

## Impact Summary

**Most Painful Scenarios:**
1. Playoff eliminated: +10 points
2. Blowing a lead to lose: 1.6x multiplier
3. Losing to bad rival: 2.2x multiplier
4. Getting blown out: 1.4x multiplier
5. OT loss: 1.3x multiplier
6. Key player injured (severity 10): +5 points
7. Long losing streak (5+): +4 points

**Most Positive Scenarios:**
1. Playoff clinched: -8 points
2. Comeback win: 1.4x bonus
3. OT win: 1.3x bonus
4. Division/Conference leader: -3 points
5. Beating rival: 1.5x bonus

The algorithm now considers **everything** that could affect your emotional state!

