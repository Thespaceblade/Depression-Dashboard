# Path Updates Summary

This document tracks all file path updates made during the reorganization.

## Files Moved

### Python Core Modules → `src/`
- `depression_calculator.py` → `src/depression_calculator.py`
- `sports_api.py` → `src/sports_api.py`
- `espn_fantasy.py` → `src/espn_fantasy.py`

### Scripts → `scripts/`
- `fetch_all_data.py` → `scripts/fetch_all_data.py`
- `auto_update.py` → `scripts/auto_update.py`
- `diagnose_config.py` → `scripts/diagnose_config.py`

### Documentation → `docs/`
- All `.md` files → `docs/` or `docs/deployment/` or `docs/archive/`

## Import Updates

All imports updated to use `src.` prefix:

```python
# Old
from depression_calculator import DepressionCalculator
from sports_api import SportsDataFetcher
from espn_fantasy import ESPNFantasyClient

# New
from src.depression_calculator import DepressionCalculator
from src.sports_api import SportsDataFetcher
from src.espn_fantasy import ESPNFantasyClient
```

## Command Updates

### Running the Calculator
```bash
# Old
python3 depression_calculator.py --fetch

# New
python3 -m src.depression_calculator --fetch
# or
python3 src/depression_calculator.py --fetch
```

### Running Data Fetch
```bash
# Old
python3 fetch_all_data.py

# New
python3 scripts/fetch_all_data.py
```

### Running Tests
```bash
# Old
python3 sports_api.py

# New
python3 -m src.sports_api
```

## Files Updated

### Python Files
- ✅ `backend/app.py` - Updated imports and paths
- ✅ `api/_utils.py` - Updated imports
- ✅ `api/recent-games.py` - Updated imports
- ✅ `api/upcoming-events.py` - Updated imports
- ✅ `api/cron/fetch-data.py` - Updated imports
- ✅ `scripts/auto_update.py` - Updated imports and paths
- ✅ `scripts/fetch_all_data.py` - Updated imports and paths
- ✅ `tests/show_dummy_data.py` - Updated imports
- ✅ `src/depression_calculator.py` - Updated relative imports

### Configuration Files
- ✅ `render.yaml` - Updated cron command
- ✅ `vercel.json` - Updated includeFiles
- ✅ `.github/workflows/auto-update-data.yml` - Updated script path

### Documentation Files
- ✅ `README.md` - Updated all command examples
- ✅ `docs/SETUP.md` - Updated commands and file references
- ✅ `docs/DAILY_FETCH.md` - Updated all script paths
- ✅ `docs/ESPN_SETUP.md` - Updated commands
- ✅ `docs/GET_COOKIES.md` - Updated commands
- ✅ `docs/deployment/DEPLOYMENT_GUIDE.md` - Updated all paths and imports
- ✅ `docs/deployment/AUTONOMOUS_SETUP.md` - Updated paths
- ✅ `docs/deployment/QUICK_DEPLOY.md` - Updated paths
- ✅ `docs/deployment/DEPLOYMENT_CHECKLIST.md` - Updated paths

### Scripts
- ✅ `scripts/setup_daily_fetch.sh` - Updated script path
- ✅ `scripts/setup_scheduled_updates.sh` - Updated paths

## Path Resolution

All scripts use proper path resolution:

```python
# Get project root
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import from src
from src.depression_calculator import DepressionCalculator

# Config file path
config_path = os.path.join(parent_dir, "teams_config.json")
```

## Verification Checklist

- [x] All Python imports updated
- [x] All command examples updated in docs
- [x] All deployment configs updated
- [x] All script paths updated
- [x] All GitHub Actions workflows updated
- [x] All config file paths verified
- [x] All sys.path.insert statements verified

## Notes

- Archive files (`docs/archive/`) and changelog (`docs/CHANGELOG.md`) contain historical references that are intentionally left as-is
- All active code and documentation has been updated
- The `src/` directory includes `__init__.py` for proper package imports

