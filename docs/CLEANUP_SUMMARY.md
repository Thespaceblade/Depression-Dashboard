# Directory Cleanup Summary

This document summarizes the directory cleanup and reorganization performed.

## Changes Made

### 1. Created Organized Directory Structure

- **`docs/`** - All documentation files
  - `SETUP.md` - Consolidated setup guide (merged SETUP.md, SETUP_DASHBOARD.md, QUICK_START.md)
  - `DAILY_FETCH.md` - Consolidated daily fetch guide (merged DAILY_FETCH_SETUP.md, README_DAILY_FETCH.md)
  - `API.md` - Consolidated API documentation (merged API_OPTIONS.md, API_STATUS.md, API_AVAILABILITY.md)
  - `archive/` - Historical/planning documents
    - `PLAN.md`
    - `VISUAL_IMPLEMENTATION_PLAN.md`
    - `UI_REDESIGN.md`
    - `IMPLEMENTATION_SUMMARY.md`
    - `TEST_RESULTS.md`
    - `QUICK_TEST.md`
  - Other docs: `CHANGELOG.md`, `ESPN_SETUP.md`, `GET_COOKIES.md`, `OPPONENT_CONTEXT.md`, `PARAMETERS.md`, `SCHEDULED_UPDATES.md`, `TIME_WEIGHTING.md`, `UNFINISHED_WORK.md`

- **`scripts/`** - All shell scripts and utility scripts
  - `start_backend.sh` - Start backend server
  - `start_frontend.sh` - Start frontend dev server
  - `setup_daily_fetch.sh` - Setup daily data fetching cron job
  - `setup_scheduled_updates.sh` - Setup scheduled updates
  - `auto_update.py` - Auto-update utility
  - `diagnose_config.py` - Config diagnostic utility

- **`tests/`** - All test files
  - `test_api_simple.py` - Simple API test
  - `test_dashboard.py` - Dashboard API test
  - `show_dummy_data.py` - Dummy data test utility

### 2. Consolidated Documentation

**Removed redundant files:**
- `SETUP.md` → merged into `docs/SETUP.md`
- `SETUP_DASHBOARD.md` → merged into `docs/SETUP.md`
- `QUICK_START.md` → merged into `docs/SETUP.md`
- `DAILY_FETCH_SETUP.md` → merged into `docs/DAILY_FETCH.md`
- `README_DAILY_FETCH.md` → merged into `docs/DAILY_FETCH.md`
- `API_OPTIONS.md` → merged into `docs/API.md`
- `API_STATUS.md` → merged into `docs/API.md`
- `API_AVAILABILITY.md` → merged into `docs/API.md`
- `API_CALLABLE_PARAMETERS.md` → removed (content in API.md)
- `API_PARAMETER_ANALYSIS.md` → removed (content in API.md)

**Moved to archive:**
- `PLAN.md` → `docs/archive/PLAN.md`
- `VISUAL_IMPLEMENTATION_PLAN.md` → `docs/archive/VISUAL_IMPLEMENTATION_PLAN.md`
- `UI_REDESIGN.md` → `docs/archive/UI_REDESIGN.md`
- `IMPLEMENTATION_SUMMARY.md` → `docs/archive/IMPLEMENTATION_SUMMARY.md`
- `TEST_RESULTS.md` → `docs/archive/TEST_RESULTS.md`
- `QUICK_TEST.md` → `docs/archive/QUICK_TEST.md`

**Moved to docs:**
- `UNFINISHED_WORK.md` → `docs/UNFINISHED_WORK.md`
- All other `.md` files → `docs/`

### 3. Updated Scripts

All scripts in `scripts/` directory were updated to use correct relative paths:
- `start_backend.sh` - Fixed path to backend directory
- `start_frontend.sh` - Fixed path to frontend directory
- `setup_daily_fetch.sh` - Fixed path to project root
- `setup_scheduled_updates.sh` - Fixed path to project root and script location

### 4. Updated .gitignore

Added entries for:
- `frontend/dist/` - Build artifacts
- `frontend/node_modules/` - Dependencies
- `logs/*.log` and `logs/*.json` - Log files
- `f1_cache/` and `*.sqlite` - Cache files

### 5. Updated README.md

Updated all documentation references to point to new `docs/` structure:
- `SCHEDULED_UPDATES.md` → `docs/DAILY_FETCH.md`
- `API_OPTIONS.md` → `docs/API.md`
- `TIME_WEIGHTING.md` → `docs/TIME_WEIGHTING.md`
- `OPPONENT_CONTEXT.md` → `docs/OPPONENT_CONTEXT.md`

## Current Directory Structure

```
Depression-Dashboard/
├── backend/              # Flask API server
├── frontend/             # React/Vite frontend
├── docs/                 # All documentation
│   ├── archive/          # Historical/planning docs
│   ├── SETUP.md          # Consolidated setup guide
│   ├── DAILY_FETCH.md    # Consolidated daily fetch guide
│   ├── API.md            # Consolidated API documentation
│   └── ...               # Other documentation
├── scripts/              # Shell scripts and utilities
│   ├── start_backend.sh
│   ├── start_frontend.sh
│   ├── setup_daily_fetch.sh
│   └── ...
├── tests/                # Test files
│   ├── test_api_simple.py
│   ├── test_dashboard.py
│   └── ...
├── logs/                 # Log files (gitignored)
├── f1_cache/            # F1 cache (gitignored)
├── depression_calculator.py  # Main calculator
├── sports_api.py         # Sports API integration
├── fetch_all_data.py     # Data fetching script
├── espn_fantasy.py       # ESPN Fantasy integration
├── teams_config.json     # Configuration (gitignored)
├── requirements.txt      # Python dependencies
└── README.md             # Main readme
```

## Benefits

1. **Cleaner root directory** - Only essential files at root level
2. **Better organization** - Related files grouped together
3. **Easier navigation** - Clear structure for docs, scripts, tests
4. **Reduced redundancy** - Consolidated overlapping documentation
5. **Improved maintainability** - Easier to find and update files

## Migration Notes

If you have any scripts or documentation that reference the old file locations, update them to use the new paths:

- Scripts: Use `./scripts/` prefix
- Tests: Use `./tests/` prefix  
- Documentation: Use `./docs/` prefix
- Archive docs: Use `./docs/archive/` prefix

