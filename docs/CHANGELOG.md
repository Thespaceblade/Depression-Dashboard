# Changelog

## Latest Updates

### ✅ Added UNC Tar Heels Support
- **NCAA Basketball**: North Carolina Tar Heels added
- **NCAA Football**: North Carolina Tar Heels added
- Both teams configured with:
  - High expectations (8-9/10)
  - Rivals: Duke, NC State, Wake Forest, Virginia
  - Full interest level (1.0)

### ✅ Automatic Evening Updates
- Created `auto_update.py` script for scheduled updates
- Created `setup_scheduled_updates.sh` for easy cron setup
- Updates run automatically at 6:00 PM daily
- Saves timestamped reports to `depression_reports/`
- Logs all activity to `logs/auto_update.log`

### ✅ College Sports API Integration
- Added `CollegeBasketballAPI` class
- Added `CollegeFootballAPI` class
- Uses ESPN API endpoints for college data
- Fetches records and recent game results

## How to Use

### Set Up Automatic Updates

```bash
# Quick setup
./setup_scheduled_updates.sh
```

This will:
1. Add a cron job for 6 PM daily updates
2. Create necessary directories
3. Show you the cron entry

### Manual Update

```bash
# Fetch latest data and calculate
python3 depression_calculator.py --fetch
```

### View Historical Reports

```bash
# List all reports
ls -lt depression_reports/

# View latest report
cat depression_reports/$(ls -t depression_reports/ | head -1)
```

## Current Teams (6 total)

1. Dallas Cowboys (NFL)
2. Dallas Mavericks (NBA)
3. Golden State Warriors (NBA)
4. Texas Rangers (MLB)
5. North Carolina Tar Heels (NCAA Basketball) ⭐ NEW
6. North Carolina Tar Heels (NCAA Football) ⭐ NEW
7. Max Verstappen (F1)
8. Jason's Fantasy Squad (Fantasy)

## Files Added

- `auto_update.py` - Scheduled update script
- `setup_scheduled_updates.sh` - Cron setup script
- `SCHEDULED_UPDATES.md` - Detailed setup instructions
- `CHANGELOG.md` - This file

## Files Modified

- `teams_config.json` - Added UNC teams
- `sports_api.py` - Added college sports API classes
- `README.md` - Updated with UNC teams and auto-update info

