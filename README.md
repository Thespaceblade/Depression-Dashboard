# Jason's Depression Calculator

A script that calculates how depressed Jason is based on how his favorite teams are performing.

## Jason's Teams

- **NFL**: Dallas Cowboys
- **NBA**: Dallas Mavericks, Golden State Warriors  
- **MLB**: Texas Rangers (low interest: barely watches)
- **F1**: Max Verstappen (huge fan!)

## Features

- Accounts for **expectation gaps** (high expectations + poor performance = major depression)
- **Rivalry losses** hurt 2.5x more
- **Consecutive losses** add extra pain
- **Fantasy team** performance included
- **F1-specific** tracking (championship position, DNFs)
- **Interest level multipliers** (Texas Rangers barely watched = less impact)

## Quick Start

### Basic Usage

Just run the script to see your current depression level:

```bash
python3 depression_calculator.py
```

### Update Team Records

Update a team's record:

```bash
# Update Cowboys to 8-3
python3 depression_calculator.py --update-team "Cowboys" --wins 8 --losses 3

# Add a rivalry loss
python3 depression_calculator.py --update-team "Cowboys" --rivalry-loss "Eagles"
```

### Update F1 Status

```bash
# Max drops to 2nd place
python3 depression_calculator.py --f1-position 2

# Max has a DNF
python3 depression_calculator.py --f1-dnf 1
```

### Update Fantasy Team

```bash
# Fantasy team is 5-7
python3 depression_calculator.py --fantasy-wins 5 --fantasy-losses 7
```

## How It Works

The calculator considers:

1. **Base Losses**: 5 points per loss (scaled by interest level)
2. **Expectation Gap**: Teams expected to be good (8-10) but performing poorly get +15-30 points
3. **Rivalry Losses**: 2.5x multiplier on base loss points
4. **Losing Streaks**: +3 points per game in a streak
5. **F1 Position**: Penalty for not being #1 (Max should always be #1!)
6. **F1 DNFs**: +12 points each (devastating!)
7. **Fantasy Losses**: +8 points each (emotionally painful)

## Example Scenarios

**Scenario 1: Cowboys lose to Eagles**
- Base loss: 5 points
- Rivalry multiplier: 2.5x = 12.5 points
- Total: ~12.5 points (Mildly Disappointed)

**Scenario 2: Max Verstappen DNFs**
- DNF penalty: 12 points
- If he drops from #1: +3 points per position
- Total: ~15+ points (Mildly to Pretty Depressed)

**Scenario 3: All teams lose + fantasy loses**
- Multiple losses stack up
- Can easily hit 50+ points (Pretty to Very Depressed)
