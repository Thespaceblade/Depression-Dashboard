#!/bin/bash
# Start the backend server for testing

cd "$(dirname "$0")/../backend"
echo "Starting backend server..."
echo "Backend will run on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""
python3 app.py

