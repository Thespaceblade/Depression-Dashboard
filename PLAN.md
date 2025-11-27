# Jason's Depression Calculator - Plan

## Overview
A script that calculates Jason's depression level based on his favorite teams' performance, accounting for various emotional factors.

## Core Components

### 1. Team Data Structure
Each team should track:
- **Team Name** (e.g., "49ers", "Lakers", etc.)
- **Sport** (NFL, NBA, MLB, etc.)
- **Current Record** (wins, losses, ties)
- **Expected Performance Level** (1-10 scale: 1=terrible, 10=championship contender)
- **Jason's Expectations** (1-10 scale: how much he expected from them)
- **Rivalry Teams** (list of teams that are rivals)
- **Recent Rivalry Losses** (track if they lost to a rival recently)
- **Recent Performance** (last 5 games or recent streak)

### 2. Fantasy Team Data
- **Fantasy Team Name**
- **Current Record** (wins, losses)
- **Expected Performance** (1-10 scale)
- **Recent Performance** (last few weeks)
- **Key Player Injuries/Underperformances**

### 3. Depression Calculation Algorithm

#### Base Depression Score
Start at 0 (completely happy) and add points for negative events:

**Team Performance Factors:**
- **Loss Multiplier**: Base points per loss (e.g., 5 points)
- **Expectation Gap Penalty**: 
  - If team was expected to be good (8-10) but performing poorly: +15 points
  - If team was expected to be decent (5-7) but performing poorly: +10 points
  - If team was expected to be bad (1-4) and performing badly: +3 points
- **Rivalry Loss Multiplier**: Loss to a rival = base loss × 2.5
- **Blowout Loss**: Loss by 20+ points = base loss × 1.5
- **Consecutive Losses**: Each loss in a streak adds +2 points
- **Playoff Implications**: Loss that hurts playoff chances = +10 points

**Fantasy Team Factors:**
- **Fantasy Loss**: +8 points per loss
- **Fantasy Expectation Gap**: Similar to team expectation gap
- **Key Player Injury**: +5 points per key player out
- **Bad Trade/Decision**: +10 points (manual input)

**Positive Factors (Reduce Depression):**
- **Unexpected Win**: Win when team was expected to lose = -5 points
- **Rivalry Win**: Win against rival = -8 points
- **Fantasy Win**: +3 points reduction
- **Playoff Clinch**: -15 points

### 4. Depression Level Interpretation
Convert score to depression level:
- **0-10**: 😊 "Feeling Great!"
- **11-25**: 😐 "Mildly Disappointed"
- **26-50**: 😔 "Pretty Depressed"
- **51-75**: 😢 "Very Depressed"
- **76-100**: 😭 "Rock Bottom"
- **100+**: 💀 "Call for Help"

### 5. Input Format
Options:
- **JSON Configuration File**: Teams, expectations, records
- **Command Line Arguments**: Quick updates
- **Interactive Mode**: Ask questions and update

### 6. Output Format
- Depression score (numeric)
- Depression level (emoji + description)
- Breakdown by team (which teams are contributing most)
- Recent events summary
- Suggestions for improvement (if any)

### 7. Features to Include
- **Historical Tracking**: Save depression scores over time
- **Trend Analysis**: "Getting better" or "Getting worse"
- **Team-Specific Breakdown**: See which team hurts the most
- **Quick Update Mode**: Just update one team's record
- **Preset Configurations**: Common scenarios (e.g., "All teams lost this week")

## Implementation Structure

```
depression_calculator.py
├── Team class
│   ├── Calculate team-specific depression contribution
│   └── Track rivalry games and expectations
├── FantasyTeam class
│   └── Calculate fantasy-specific depression
├── DepressionCalculator class
│   ├── Aggregate all depression sources
│   ├── Calculate total score
│   └── Generate report
├── Config loader (JSON)
└── Main script with CLI
```

## Example Usage

```python
# Quick update
python depression_calculator.py --team "49ers" --loss --rivalry "Seahawks"

# Full calculation
python depression_calculator.py --config teams.json

# Interactive mode
python depression_calculator.py --interactive
```

## Sample Config File Structure

```json
{
  "teams": [
    {
      "name": "San Francisco 49ers",
      "sport": "NFL",
      "record": {"wins": 5, "losses": 3},
      "expected_performance": 9,
      "jasons_expectations": 10,
      "rivals": ["Seattle Seahawks", "Los Angeles Rams"],
      "recent_rivalry_losses": ["Seattle Seahawks"],
      "recent_streak": ["L", "W", "L", "L"]
    }
  ],
  "fantasy_team": {
    "name": "Jason's Squad",
    "record": {"wins": 4, "losses": 4},
    "expected_performance": 7,
    "jasons_expectations": 8
  }
}
```

## Next Steps
1. Implement core Team and FantasyTeam classes
2. Build depression calculation algorithm
3. Create config file format and loader
4. Build CLI interface
5. Add output formatting and reporting
6. Test with various scenarios

