# Daily Data Fetching Setup

This guide explains how to set up automatic daily data fetching for all your sports teams.

## Quick Setup

Run the setup script:

```bash
./scripts/setup_daily_fetch.sh
```

This will:
- Schedule `fetch_all_data.py` to run daily at 6:00 PM
- Create logs directory
- Set up cron job

## What Gets Fetched

The `fetch_all_data.py` script automatically fetches:

### ✅ Sports Data
- **NFL**: Dallas Cowboys (record, recent games)
- **NBA**: Dallas Mavericks, Golden State Warriors (records, recent games)
- **MLB**: Texas Rangers (record - reduced impact in offseason)
- **College**: UNC Basketball & Football (records, recent games)
- **F1**: Max Verstappen (championship position, recent race results)

### ✅ Fantasy Data
- **ESPN Fantasy**: Your team record, recent matchups (if configured)

## Manual Run

To run the fetch script manually:

```bash
python3 fetch_all_data.py
```

## Scheduling Options

### Option 1: Cron (Linux/macOS) - Recommended

Already set up by `scripts/setup_daily_fetch.sh`:
- Runs daily at 6:00 PM
- Logs to `logs/cron.log`

**View cron jobs:**
```bash
crontab -l
```

**Edit schedule:**
```bash
crontab -e
```

**Example schedules:**
- `0 18 * * *` - Daily at 6:00 PM (default)
- `0 9,18 * * *` - Twice daily at 9 AM and 6 PM
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Daily at midnight

### Option 2: Systemd Timer (Linux)

Create `/etc/systemd/system/depression-fetch.service`:
```ini
[Unit]
Description=Daily Depression Data Fetch
After=network.target

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/path/to/Depression-Dashboard
ExecStart=/usr/bin/python3 /path/to/Depression-Dashboard/fetch_all_data.py
```

Create `/etc/systemd/system/depression-fetch.timer`:
```ini
[Unit]
Description=Daily Depression Data Fetch Timer
Requires=depression-fetch.service

[Timer]
OnCalendar=daily
OnCalendar=18:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
sudo systemctl enable depression-fetch.timer
sudo systemctl start depression-fetch.timer
```

### Option 3: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Daily Depression Data Fetch"
4. Trigger: Daily at 6:00 PM
5. Action: Start a program
   - Program: `python.exe`
   - Arguments: `fetch_all_data.py`
   - Start in: `C:\path\to\Depression-Dashboard`

### Option 4: Cloud Hosting (Heroku, Railway, etc.)

Use their built-in scheduler:
- **Heroku**: `heroku addons:create scheduler:standard`
- **Railway**: Use Cron Jobs in project settings
- **Render**: Use Cron Jobs in dashboard

Add to your scheduler:
```bash
python3 fetch_all_data.py
```

## Logs

Logs are saved to:
- `logs/data_fetch_YYYYMMDD.log` - Daily detailed logs
- `logs/fetch_summary_YYYYMMDD.json` - JSON summary
- `logs/cron.log` - Cron output (if using cron)

## Monitoring

Check if the script ran successfully:

```bash
# View latest log
tail -50 logs/data_fetch_$(date +%Y%m%d).log

# View summary
cat logs/fetch_summary_$(date +%Y%m%d).json

# Check cron logs
tail -50 logs/cron.log
```

## Troubleshooting

### Script Not Running

1. **Check cron is running:**
   ```bash
   ps aux | grep cron
   ```

2. **Check cron permissions:**
   ```bash
   ls -la /var/spool/cron/crontabs/  # Linux
   ls -la /usr/lib/cron/tabs/        # macOS
   ```

3. **Test script manually:**
   ```bash
   python3 fetch_all_data.py
   ```

### API Errors

- Some APIs may be temporarily unavailable
- Script will continue with available data
- Check logs for specific errors

### Permission Errors

Make sure the script is executable:
```bash
chmod +x fetch_all_data.py
```

## Environment Variables

You can set these environment variables:

- `CONFIG_PATH`: Path to config file (default: `teams_config.json`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

Example:
```bash
export CONFIG_PATH="/path/to/custom_config.json"
python3 fetch_all_data.py
```

## What Happens

1. **Fetches all sports data** from APIs
2. **Updates config file** with latest records
3. **Fetches fantasy data** from ESPN (if configured)
4. **Calculates depression score**
5. **Saves logs** for monitoring
6. **Exits with code 0** (success) or 1 (failure)

The config file is always updated, so your dashboard will show the latest data!



