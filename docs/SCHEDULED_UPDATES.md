# Automatic Evening Updates Setup

The depression calculator can automatically fetch new scores every evening and calculate your depression level.

## Quick Setup (macOS/Linux)

Run the setup script:

```bash
chmod +x setup_scheduled_updates.sh
./setup_scheduled_updates.sh
```

This will:
- Add a cron job to run at 6:00 PM daily
- Create logs directory for tracking
- Create reports directory for historical depression scores

## Manual Setup

### macOS/Linux (Cron)

1. Open your crontab:
   ```bash
   crontab -e
   ```

2. Add this line (update paths as needed):
   ```
   0 18 * * * cd /path/to/DepressionDashboard && /usr/bin/python3 auto_update.py >> /path/to/DepressionDashboard/logs/auto_update.log 2>&1
   ```

3. Save and exit

**Time Format**: `0 18 * * *` means:
- `0` - minute (0)
- `18` - hour (6 PM)
- `*` - every day of month
- `*` - every month
- `*` - every day of week

To change the time, modify the hour (18 = 6 PM). Examples:
- `0 19 * * *` = 7:00 PM
- `0 20 * * *` = 8:00 PM
- `0 17 * * *` = 5:00 PM

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name it "Depression Calculator Daily Update"
4. Trigger: Daily at 6:00 PM
5. Action: Start a program
   - Program: `python.exe` (or full path to python)
   - Arguments: `auto_update.py`
   - Start in: `C:\path\to\DepressionDashboard`

## What It Does

Every evening, the script will:
1. ✅ Fetch latest scores from all APIs
2. ✅ Update `teams_config.json` with fresh data
3. ✅ Calculate your depression level
4. ✅ Save a timestamped report to `depression_reports/`
5. ✅ Log everything to `logs/auto_update.log`

## Viewing Results

### Check Latest Report
```bash
ls -lt depression_reports/ | head -1
```

### View Logs
```bash
tail -f logs/auto_update.log
```

### Run Manually
```bash
python3 auto_update.py
```

## Troubleshooting

**Cron job not running?**
- Check if cron has permission: `crontab -l`
- Check logs: `tail -f logs/auto_update.log`
- Verify Python path: `which python3`
- Test manually: `python3 auto_update.py`

**API errors?**
- Some APIs may be rate-limited
- Check internet connection
- APIs may be down - script will continue with existing data

**Want to change update time?**
- Edit crontab: `crontab -e`
- Change the hour number (18 = 6 PM, 19 = 7 PM, etc.)

## Removing Scheduled Updates

```bash
crontab -e
# Delete the line with auto_update.py
# Save and exit
```

Or:
```bash
crontab -l | grep -v "auto_update.py" | crontab -
```

