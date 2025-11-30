# Depression Dashboard

A web dashboard that calculates and visualizes depression levels based on favorite sports teams' performance. Tracks NFL, NBA, MLB, NCAA, F1, and fantasy teams with automatic data fetching and real-time updates.

## Features

- Real-time depression score calculation based on team performance
- Automatic data fetching from ESPN APIs and other sports data sources
- Web dashboard with interactive visualizations
- RESTful API for programmatic access
- Automatic updates via GitHub Actions
- Support for multiple sports: NFL, NBA, MLB, NCAA Basketball, NCAA Football, F1, Fantasy

## Teams Tracked

- NFL: Dallas Cowboys
- NBA: Dallas Mavericks, Golden State Warriors
- MLB: Texas Rangers
- F1: Max Verstappen
- College Basketball: North Carolina Tar Heels
- College Football: North Carolina Tar Heels
- Fantasy: Jason's Fantasy Squad

## Project Structure

```
Depression-Dashboard/
├── backend/              # Flask API server
│   └── app.py
├── frontend/             # React + TypeScript dashboard
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── types/       # TypeScript definitions
│   │   └── api.ts       # API client
│   └── package.json
├── src/                  # Core Python modules
│   ├── depression_calculator.py
│   ├── sports_api.py
│   └── espn_fantasy.py
├── api/                  # Vercel serverless functions
├── scripts/              # Utility scripts
│   └── fetch_all_data.py
├── teams_config.json     # Team configuration (not in git)
├── teams_config.json.example
└── requirements.txt
```

## Installation

### Backend Setup

```bash
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

## Usage

### Run Calculator

Calculate depression score from current config:

```bash
python3 -m src.depression_calculator
```

### Fetch Latest Data

Fetch latest data from APIs and update config:

```bash
python3 -m src.depression_calculator --fetch
```

Or use the dedicated script:

```bash
python3 scripts/fetch_all_data.py
```

### Update Team Records

```bash
python3 -m src.depression_calculator --update-team "Cowboys" --wins 8 --losses 3
python3 -m src.depression_calculator --update-team "Cowboys" --rivalry-loss "Eagles"
```

### Update F1 Status

```bash
python3 -m src.depression_calculator --f1-position 2
python3 -m src.depression_calculator --f1-dnf 1
```

### Update Fantasy Team

```bash
python3 -m src.depression_calculator --fantasy-wins 5 --fantasy-losses 7
```

### Run Backend Server

```bash
cd backend
python3 app.py
```

Backend runs on `http://localhost:5001`

### Run Frontend

```bash
cd frontend
npm run dev
```

Frontend runs on `http://localhost:3000`

## Depression Levels

- 0-10: Feeling Great
- 11-25: Mildly Disappointed
- 26-50: Pretty Depressed
- 51-75: Very Depressed
- 76-100: Rock Bottom
- 100+: Call for Help

## Calculation Algorithm

The depression score is calculated based on multiple factors:

- Base loss: 5 points per loss (scaled by interest level)
- Expectation gap: +15-30 points for teams expected to be good but performing poorly
- Rivalry losses: 2.5x multiplier on base loss points
- Losing streaks: +3 points per consecutive loss
- F1 position: penalty for not being in first place
- F1 DNFs: +12 points each
- Fantasy losses: +8 points each

Time-weighted: Recent events have more impact than older ones using exponential decay.

Opponent context: Losing to bad teams multiplies points, losing to good teams reduces them.

Offseason multiplier: Teams in offseason contribute only 1% of normal impact.

## Configuration

Edit `teams_config.json` to configure:

- Team records (wins, losses, ties)
- Expected performance (1-10 scale)
- Jason's expectations (1-10 scale)
- Rival teams
- Interest level (0.0-1.0 multiplier)
- Recent game streaks
- Notes

See `teams_config.json.example` for the structure.

## API Endpoints

### Backend (Flask)

- `GET /api/depression` - Get current depression score and breakdown
- `GET /api/teams` - Get all team data
- `GET /api/recent-games` - Get recent games and events
- `GET /api/upcoming-events` - Get upcoming games and events
- `POST /api/refresh` - Trigger data refresh from all APIs
- `GET /api/health` - Health check

### Vercel Serverless Functions

Same endpoints available at `/api/*` when deployed on Vercel.

## Automatic Updates

GitHub Actions workflow runs every 6 hours to:

1. Fetch latest data from all sports APIs
2. Update `teams_config.json` with fresh records
3. Commit and push changes to repository

See `.github/workflows/auto-update-data.yml` for configuration.

## Deployment

### Vercel

Frontend and API serverless functions are deployed on Vercel. See `vercel.json` for configuration.

### Railway

Backend can be deployed on Railway. See `railway.json` and `nixpacks.toml` for configuration.

## Development

### Backend Development

```bash
cd backend
python3 app.py
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Testing

```bash
python3 tests/test_dashboard.py
python3 tests/test_api_simple.py
```

## Dependencies

### Python

- Flask - Web framework
- flask-cors - CORS support
- requests - HTTP requests
- fastf1 - F1 data
- pytz - Timezone handling

### Node.js

- React 18
- TypeScript
- Vite
- Tailwind CSS
- Chart.js

## License

Private project.
