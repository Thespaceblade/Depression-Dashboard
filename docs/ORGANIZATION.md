# Project Organization

This document describes the current organization of the Depression Dashboard project.

## Directory Structure

```
Depression-Dashboard/
├── src/                      # Core Python modules
│   ├── __init__.py          # Package initialization
│   ├── depression_calculator.py  # Main depression calculator
│   ├── sports_api.py        # Sports API integrations
│   └── espn_fantasy.py      # ESPN Fantasy integration
│
├── backend/                  # Flask API server
│   ├── app.py               # Main Flask application
│   └── requirements.txt     # Backend dependencies
│
├── frontend/                 # React/Vite frontend
│   ├── src/                 # Frontend source code
│   └── package.json         # Frontend dependencies
│
├── api/                      # Vercel serverless functions
│   ├── _utils.py            # Shared utilities
│   ├── depression.py        # Depression endpoint
│   ├── teams.py             # Teams endpoint
│   └── cron/                # Cron job functions
│
├── scripts/                  # Utility scripts
│   ├── fetch_all_data.py    # Automated data fetching
│   ├── auto_update.py        # Auto-update script
│   ├── diagnose_config.py   # Config diagnostic
│   ├── start_backend.sh     # Start backend server
│   ├── start_frontend.sh    # Start frontend dev server
│   ├── setup_daily_fetch.sh # Setup cron job
│   └── setup_scheduled_updates.sh
│
├── tests/                    # Test files
│   ├── test_api_simple.py   # Simple API tests
│   ├── test_dashboard.py     # Dashboard tests
│   └── show_dummy_data.py   # Dummy data test
│
├── docs/                     # Documentation
│   ├── SETUP.md             # Setup guide
│   ├── API.md               # API documentation
│   ├── DAILY_FETCH.md       # Daily fetch guide
│   ├── deployment/          # Deployment guides
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   ├── VERCEL_DEPLOY.md
│   │   └── ...
│   └── archive/             # Historical docs
│
├── logs/                     # Log files (gitignored)
├── f1_cache/                # F1 cache data (gitignored)
│
├── teams_config.json        # Configuration (gitignored)
├── requirements.txt         # Python dependencies
└── README.md                # Main readme
```

## Import Paths

All imports should use the `src.` prefix:

```python
# Correct
from src.depression_calculator import DepressionCalculator
from src.sports_api import SportsDataFetcher
from src.espn_fantasy import ESPNFantasyClient

# Or using relative imports within src/
from .sports_api import SportsDataFetcher
from .espn_fantasy import ESPNFantasyClient
```

## Running Scripts

### Main Calculator
```bash
# As module
python3 -m src.depression_calculator --fetch

# Direct (if src is in path)
python3 src/depression_calculator.py --fetch
```

### Data Fetching
```bash
python3 scripts/fetch_all_data.py
```

### Backend
```bash
./scripts/start_backend.sh
# or
cd backend && python3 app.py
```

### Frontend
```bash
./scripts/start_frontend.sh
# or
cd frontend && npm run dev
```

## File Organization Principles

1. **Core modules** → `src/` - Reusable Python modules
2. **Scripts** → `scripts/` - Executable scripts and utilities
3. **Tests** → `tests/` - Test files
4. **Documentation** → `docs/` - All markdown documentation
5. **Deployment docs** → `docs/deployment/` - Deployment-specific guides
6. **Archive** → `docs/archive/` - Historical/planning documents

## Benefits

- **Clear separation** of concerns
- **Easy to find** files by purpose
- **Scalable** structure for growth
- **Standard Python** package layout
- **Organized documentation** by topic

