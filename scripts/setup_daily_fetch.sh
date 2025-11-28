#!/bin/bash
# Setup daily data fetching via cron
# This will run fetch_all_data.py every day at 6:00 PM

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FETCH_SCRIPT="$SCRIPT_DIR/fetch_all_data.py"
PYTHON_PATH=$(which python3)

echo "Setting up daily data fetching..."
echo ""

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"

# Create cron entry (runs daily at 6:00 PM)
CRON_TIME="0 18 * * *"
CRON_ENTRY="$CRON_TIME cd $SCRIPT_DIR && $PYTHON_PATH $FETCH_SCRIPT >> $SCRIPT_DIR/logs/cron.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "fetch_all_data.py"; then
    echo "⚠ Cron job already exists. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "fetch_all_data.py" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✓ Daily data fetch scheduled!"
echo ""
echo "Schedule: Every day at 6:00 PM"
echo "Script: $FETCH_SCRIPT"
echo "Logs: $SCRIPT_DIR/logs/"
echo ""
echo "To view current cron jobs:"
echo "  crontab -l"
echo ""
echo "To remove this cron job:"
echo "  crontab -l | grep -v 'fetch_all_data.py' | crontab -"
echo ""
echo "To test the script manually:"
echo "  $PYTHON_PATH $FETCH_SCRIPT"

