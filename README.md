# Depression Dashboard

Calculates depression level based on favorite teams' performance.

## Teams

- NFL: Dallas Cowboys
- NBA: Dallas Mavericks, Golden State Warriors
- MLB: Texas Rangers
- F1: Max Verstappen
- College Basketball: North Carolina Tar Heels
- College Football: North Carolina Tar Heels

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the calculator:

```bash
python3 -m src.depression_calculator
```

Fetch latest data and calculate:

```bash
python3 -m src.depression_calculator --fetch
```

Update team records:

```bash
python3 -m src.depression_calculator --update-team "Cowboys" --wins 8 --losses 3
python3 -m src.depression_calculator --update-team "Cowboys" --rivalry-loss "Eagles"
```

Update F1 status:

```bash
python3 -m src.depression_calculator --f1-position 2
python3 -m src.depression_calculator --f1-dnf 1
```

Update fantasy team:

```bash
python3 -m src.depression_calculator --fantasy-wins 5 --fantasy-losses 7
```

## Depression Levels

- 0-10: Feeling Great
- 11-25: Mildly Disappointed
- 26-50: Pretty Depressed
- 51-75: Very Depressed
- 76-100: Rock Bottom
- 100+: Call for Help

## Calculation

- Base loss: 5 points per loss (scaled by interest level)
- Expectation gap: +15-30 points for teams expected to be good but performing poorly
- Rivalry losses: 2.5x multiplier
- Losing streaks: +3 points per game
- F1 position: penalty for not being #1
- F1 DNFs: +12 points each
- Fantasy losses: +8 points each

Time-weighted: recent events have more impact than older ones.

Opponent context: losing to bad teams multiplies points, losing to good teams reduces them.

## Configuration

Edit `teams_config.json` to set expectations, rivals, interest levels, and records.
