# Depression Dashboard

A script that calculates how depressed Jason is based on how his favorite teams are performing.

## Jason's Teams

- **NFL**: Dallas Cowboys
- **NBA**: Dallas Mavericks, Golden State Warriors  
- **MLB**: Texas Rangers (low interest: barely watches)
- **F1**: Max Verstappen (huge fan!)
- **College Basketball**: North Carolina Tar Heels (big fan!)
- **College Football**: North Carolina Tar Heels (big fan!)

## Features

- Accounts for **expectation gaps** (high expectations + poor performance = major depression)
- **Rivalry losses** hurt 2.5x more
- **Consecutive losses** add extra pain
- **Fantasy team** performance included
- **F1-specific** tracking (championship position, DNFs)
- **Interest level multipliers** (Texas Rangers barely watched = less impact)

## Installation

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

This installs:
- `sportsipy` - NFL and MLB data
- `nba_api` - NBA data
- `fastf1` - F1 data
- `espn-api` - ESPN data (optional)
- `requests` - HTTP requests

## Quick Start

### Basic Usage

Just run the script to see your current depression level:

```bash
python3 depression_calculator.py
```

### Automatic Data Fetching

Fetch the latest scores from APIs automatically:

```bash
python3 depression_calculator.py --fetch
```

This will:
- Fetch current records for all teams
- Update Max Verstappen's championship position
- Get recent game results
- Update the config file
- Calculate your depression level

**Note**: Some APIs may have rate limits or require internet connection.

### Automatic Evening Updates ⏰

Set up automatic daily updates that run every evening:

```bash
# Quick setup (macOS/Linux)
./setup_scheduled_updates.sh
```

This will automatically:
- Fetch new scores every evening at 6 PM
- Calculate your depression level
- Save timestamped reports
- Log everything for tracking

See `docs/DAILY_FETCH.md` for detailed setup instructions.

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

## Depression Levels

- **0-10**: 😊 Feeling Great!
- **11-25**: 😐 Mildly Disappointed
- **26-50**: 😔 Pretty Depressed
- **51-75**: 😢 Very Depressed
- **76-100**: 😭 Rock Bottom
- **100+**: 💀 Call for Help

## API Integration

The script can automatically fetch data from free sports APIs:

- **NFL (Cowboys)**: Uses `sportsipy` to scrape ESPN
- **NBA (Mavericks, Warriors)**: Uses `nba_api` (official NBA API)
- **MLB (Rangers)**: Uses `sportsipy` to scrape ESPN
- **F1 (Max Verstappen)**: Uses Ergast API (free, no key needed)

See `docs/API.md` for more details on available APIs and alternatives.

### Manual API Testing

Test the API integration separately:

```bash
python3 sports_api.py
```

This will fetch data for all teams and update the config file.

## Configuration

Edit `teams_config.json` to:
- Set expectations for each team
- Add/remove rivals
- Adjust interest levels
- Update records manually

## How It Works

The calculator considers:

1. **Base Losses**: 5 points per loss (scaled by interest level)
2. **Expectation Gap**: Teams expected to be good (8-10) but performing poorly get +15-30 points
3. **Rivalry Losses**: 2.5x multiplier on base loss points
4. **Losing Streaks**: +3 points per game in a streak
5. **F1 Position**: Penalty for not being #1 (Max should always be #1!)
6. **F1 DNFs**: +12 points each (devastating!)
7. **Fantasy Losses**: +8 points each (emotionally painful)

### ⏰ Time-Weighted Algorithm

**Recent events have MUCH more impact than older ones:**
- **Just happened (0 hours)**: 100% weight 💀
- **6 hours ago**: 83% weight
- **1 day ago**: 61% weight
- **2 days ago**: 37% weight
- **3 days ago**: 22% weight
- **1 week ago**: 3% weight 😊

**Example**: A Max Verstappen DNF that just happened = 8.0 points. The same DNF from 2 days ago = 3.0 points. From 1 week ago = 0.3 points.

See `docs/TIME_WEIGHTING.md` for detailed examples.

### 🎯 Opponent Context Algorithm (NEW!)

**Who you lost to matters!**

- **Losing to a great team (65%+ win rate)**: 0.6x multiplier (expected loss)
- **Losing to a bad team (<35% win rate)**: 1.5x multiplier (embarrassing!)
- **Losing to a bad RIVAL**: 2.2x multiplier 💀 (most painful!)

**Examples:**
- Cowboys lose to Chiefs (great team): 2.1 points
- Cowboys lose to Commanders (bad rival): 4.5 points (2x more painful!)

**Wins also get context:**
- Beating a rival: 1.5x bonus (feels extra good!)
- Beating a good team: 1.3x bonus

See `docs/OPPONENT_CONTEXT.md` for detailed examples.

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
