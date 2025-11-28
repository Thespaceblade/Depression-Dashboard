#!/bin/bash
# Start the frontend dev server for testing

cd "$(dirname "$0")/../frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting frontend dev server..."
echo "Frontend will run on http://localhost:3000"
echo "Press Ctrl+C to stop"
echo ""
npm run dev

