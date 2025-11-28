# Setup Guide

## Prerequisites

- Python 3.8+
- Node.js 18+ and npm (for dashboard)
- All Python dependencies from `requirements.txt`

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test API Integration (Optional)

```bash
python3 sports_api.py
```

### 3. Calculate Depression with Live Data

```bash
python3 depression_calculator.py --fetch
```

## Dashboard Setup

The dashboard requires both the backend and frontend to be running.

### Backend Setup

1. Make sure `teams_config.json` exists in the root directory

2. Start the Flask backend server:
   ```bash
   python3 backend/app.py
   ```
   The backend will run on `http://localhost:5001`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:3000` and automatically proxy API requests to the backend.

### Quick Start Scripts

You can also use the convenience scripts:

```bash
# Start backend
./scripts/start_backend.sh

# Start frontend (in another terminal)
./scripts/start_frontend.sh
```

## Usage

1. Start the backend first (in one terminal)
2. Start the frontend (in another terminal)
3. Open `http://localhost:3000` in your browser
4. The dashboard will automatically fetch and display:
   - Current depression score
   - All team performance data
   - Recent games timeline
   - Breakdown charts

## Features

- **Auto-refresh**: Data refreshes every 60 seconds automatically
- **Manual Refresh**: Click the "Refresh Data" button to update immediately
- **Interactive Cards**: Click on team cards to see detailed breakdowns
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## API Endpoints

- `GET /api/depression` - Get current depression score and breakdown
- `GET /api/teams` - Get all team data
- `GET /api/recent-games` - Get recent games timeline
- `POST /api/refresh` - Trigger data refresh from sports APIs
- `GET /api/health` - Health check

## What Each File Does

- **`depression_calculator.py`** - Main script that calculates depression level
- **`sports_api.py`** - Fetches data from sports APIs
- **`fetch_all_data.py`** - Automated data fetching script
- **`teams_config.json`** - Configuration with your teams and expectations
- **`requirements.txt`** - Python dependencies
- **`backend/app.py`** - Flask API server
- **`frontend/`** - React/Vite frontend application

## API Status

### Currently Implemented (Free):
- ✅ **F1 (Ergast API)** - Free, no key needed, very reliable
- ✅ **NBA (nba_api)** - Official NBA API wrapper, free
- ⚠️ **NFL/MLB (sportsipy)** - Scrapes ESPN, may break if ESPN changes site

See `docs/API.md` for detailed API options and alternatives.

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Backend won't start
- Make sure all Python dependencies are installed
- Check that `teams_config.json` exists
- Verify port 5001 is not in use (change in `backend/app.py` if needed)

### Frontend won't start
- Make sure Node.js 18+ is installed
- Run `npm install` in the frontend directory
- Check that port 3000 is not in use (Vite will auto-use next available port)

### "Error Loading Data" or "Failed to load depression data"
**Solution**: Make sure the backend is running!

1. Check if backend is running:
   ```bash
   curl http://localhost:5001/api/health
   ```
   Should return: `{"status":"healthy",...}`

2. If not running, start it:
   ```bash
   python3 backend/app.py
   ```

3. Check browser console (F12) for specific error messages

### API errors
- Some APIs may be rate-limited
- ESPN scraping may break if site changes
- Check `docs/API.md` for alternatives

### No data returned
- Check internet connection
- Some APIs may be down
- Try running `sports_api.py` separately to debug

### CORS errors
- The backend includes CORS headers, but if you see errors, check that `flask-cors` is installed

## Testing the Backend Directly

Test if the backend works:

```bash
# Health check
curl http://localhost:5001/api/health

# Get depression data
curl http://localhost:5001/api/depression

# Get teams data
curl http://localhost:5001/api/teams
```

Or use the test scripts:

```bash
# Simple API test
python3 tests/test_api_simple.py

# Full dashboard test
python3 tests/test_dashboard.py
```

## Production Build

To build the frontend for production:

```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

## Next Steps

1. Test all APIs to see which work best
2. Set up automatic daily data fetching (see `docs/DAILY_FETCH.md`)
3. Add fantasy football API integration (requires league credentials)
4. Add notifications (email, Slack, etc.) when depression gets too high

