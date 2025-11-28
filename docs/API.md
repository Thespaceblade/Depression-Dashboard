# Sports APIs & Integration Guide

## Current API Status

### ✅ Working APIs

#### NFL (Dallas Cowboys)
- **Source**: ESPN API
- **Team ID**: 6
- **Status**: ✅ Working
- **Current Record**: Fetched from `https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/6`
- **Recent Games**: Events endpoint returns empty (may need different endpoint)

#### NBA (Dallas Mavericks & Golden State Warriors)
- **Source**: ESPN API
- **Team IDs**: Mavericks = 6, Warriors = 9
- **Status**: ✅ Working
- **Current Records**: Fetched from ESPN team endpoints
- **Recent Games**: Events endpoint may need adjustment

#### College Sports (UNC)
- **Source**: ESPN API
- **Status**: ✅ Working
- **Basketball & Football**: Both fetching correctly

### ❌ Issues

#### F1 (Max Verstappen)
- **Problem**: Ergast API (ergast.com) is completely down/unreachable
- **Error**: Connection refused on both HTTP and HTTPS
- **Status**: ❌ Not Working
- **Solution**: 
  1. Manual input required in config file
  2. Or use FastF1 library (requires session data, more complex)
  3. Or find alternative F1 API

#### Recent Games
- **Problem**: Events endpoints returning empty arrays
- **Status**: ⚠️ Partial - Records work, recent games don't
- **Solution**: May need to use different endpoint or parse schedule differently

## Recommended Solutions (Free/Open Source)

### 1. **Ergast F1 API** (Formula 1) - FREE ✅
- **URL**: http://ergast.com/mrd/
- **Status**: Free, no API key required (currently down)
- **Coverage**: Historical and current F1 data
- **Python Library**: `fastf1` (unofficial, but excellent)
  ```bash
  pip install fastf1
  ```
- **What it provides**: Race results, driver standings, lap times, DNFs
- **Perfect for**: Tracking Max Verstappen's position, race results, DNFs

### 2. **sportsipy** (NFL, NBA, MLB) - FREE ✅
- **GitHub**: https://github.com/roclark/sportsipy
- **Status**: Free, scrapes ESPN data
- **Installation**:
  ```bash
  pip install sportsipy
  ```
- **Coverage**: 
  - NFL (Cowboys)
  - NBA (Mavericks, Warriors)
  - MLB (Rangers)
- **What it provides**: Scores, schedules, standings, team stats
- **Note**: Scrapes ESPN, so may break if ESPN changes their site

### 3. **nba_api** (NBA) - FREE ✅
- **GitHub**: https://github.com/swar/nba_api
- **Status**: Free, official NBA stats API wrapper
- **Installation**:
  ```bash
  pip install nba_api
  ```
- **Coverage**: Comprehensive NBA data
- **What it provides**: Live scores, box scores, standings, player stats
- **Best for**: Detailed Mavericks and Warriors tracking

### 4. **espn-api** (Multiple Sports) - FREE ✅
- **GitHub**: https://github.com/cwendt94/espn-api
- **Status**: Free, scrapes ESPN
- **Installation**:
  ```bash
  pip install espn-api
  ```
- **Coverage**: NFL, NBA, MLB, College sports
- **What it provides**: Scores, schedules, standings
- **Note**: Also scrapes ESPN, may be fragile

## Paid Options (If Free Options Don't Work)

### 5. **API-Football** (Multiple Sports)
- **URL**: https://www.api-football.com/
- **Status**: Free tier available (100 requests/day)
- **Coverage**: NFL, NBA, MLB, F1
- **Cost**: Free tier, then paid plans
- **Good for**: All-in-one solution

### 6. **SportsDataIO**
- **URL**: https://sportsdata.io/
- **Status**: Paid, but has free trial
- **Coverage**: NFL, NBA, MLB, comprehensive stats
- **Cost**: Varies by sport/plan
- **Good for**: Professional, reliable data

### 7. **Sportradar**
- **URL**: https://sportradar.com/
- **Status**: Paid, enterprise-focused
- **Coverage**: NFL, NBA, MLB, F1
- **Cost**: Enterprise pricing
- **Good for**: Production applications

## Fantasy Football APIs

### 8. **Yahoo Fantasy Sports API**
- **URL**: https://developer.yahoo.com/fantasy-sports/
- **Status**: Free, requires OAuth
- **Coverage**: Yahoo Fantasy leagues
- **Good for**: If Jason uses Yahoo Fantasy

### 9. **ESPN Fantasy API** (Unofficial)
- **GitHub**: https://github.com/cwendt94/espn-api (has fantasy support)
- **Status**: Free, scrapes ESPN Fantasy
- **Coverage**: ESPN Fantasy leagues
- **Good for**: If Jason uses ESPN Fantasy

## Recommended Implementation Strategy

### Phase 1: Free Solutions (Start Here)
1. **F1**: Use `fastf1` library (Ergast API) - currently down, manual input needed
2. **NBA**: Use `nba_api` (official NBA API)
3. **NFL/MLB**: Use `sportsipy` or `espn-api`
4. **Fantasy**: Use `espn-api` if ESPN, or Yahoo API if Yahoo

### Phase 2: If Free Solutions Fail
- Consider API-Football free tier
- Or SportsDataIO trial

## Python Libraries to Install

```bash
# Core sports data
pip install sportsipy nba_api fastf1 espn-api

# HTTP requests (if needed)
pip install requests

# Date handling
pip install python-dateutil
```

## Example Integration Code Structure

```python
# F1 - Max Verstappen
from fastf1 import api

# NBA - Mavericks, Warriors
from nba_api.stats.endpoints import scoreboard, teamgamelog

# NFL/MLB - Cowboys, Rangers
from sportsipy.nfl.teams import Teams
from sportsipy.mlb.teams import Teams

# Fantasy
from espn_api.football import League
```

## API Parameter Availability

### ✅ Automatically Retrievable: 20 parameters (36%)
- Basic team data (wins, losses)
- Recent game data (streaks, opponents, locations, scores)
- Standings & playoffs (position, games back, clinched status)
- Calculable metrics (season progress, streaks)

### ⚠️ Partially Available: 6 parameters (11%)
- Blowout wins/losses (calculate from score margins)
- Comeback wins/losses (need play-by-play - not in basic ESPN API)
- Longest streaks (calculate from full season game log)

### ❌ Manual Input Required: 30 parameters (53%)
- Emotional/personal context (watched, bet, reactions)
- Team-specific issues (injuries, drama) - need specialized APIs
- Subjective assessments (importance, legacy)

See `docs/API_PARAMETER_ANALYSIS.md` for complete breakdown.

## Manual F1 Input

Since the F1 API is down, update `teams_config.json` manually:

```json
"f1_driver": {
  "name": "Max Verstappen",
  "championship_position": 1,
  "expected_performance": 10,
  "jasons_expectations": 10,
  "recent_races": ["W", "P2", "W", "W", "P3"],
  "recent_dnfs": 0,
  "rivals": ["Lewis Hamilton", "Charles Leclerc", "Lando Norris"],
  "notes": "Huge fan - Red Bull dominance"
}
```

## Next Steps

1. ✅ Fixed Cowboys team ID (was 2, now 6)
2. ✅ Fixed NBA team IDs and parsing
3. ⚠️ Need to fix recent games endpoints
4. ❌ Need alternative F1 API or manual input
5. Test each library to see which works best
6. Create API wrapper classes for each sport
7. Integrate into depression calculator
8. Add automatic score fetching
9. Schedule updates (cron job or scheduled task)

