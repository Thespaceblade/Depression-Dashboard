#!/bin/bash
# Setup script for automatic evening updates
# This will add a cron job to run the depression calculator every evening at 6 PM

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_PATH=$(which python3)
CRON_TIME="0 18"  # 6:00 PM (18:00)

echo "Setting up automatic evening updates..."
echo "Script directory: $SCRIPT_DIR"
echo "Python path: $PYTHON_PATH"
echo "Update time: 6:00 PM daily"
echo ""

# Create the cron job entry
CRON_JOB="$CRON_TIME * * * cd $SCRIPT_DIR && $PYTHON_PATH scripts/auto_update.py >> $SCRIPT_DIR/logs/auto_update.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "auto_update.py"; then
    echo "Cron job already exists. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "auto_update.py" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

# Create logs directory
mkdir -p "$SCRIPT_DIR/logs"
mkdir -p "$SCRIPT_DIR/depression_reports"

echo "✓ Cron job added successfully!"
echo ""
echo "Current crontab:"
crontab -l | grep "auto_update.py"
echo ""
echo "To remove the scheduled update, run:"
echo "  crontab -e"
echo "  (then delete the auto_update.py line)"
echo ""
echo "To view logs:"
echo "  tail -f $SCRIPT_DIR/logs/auto_update.log"

