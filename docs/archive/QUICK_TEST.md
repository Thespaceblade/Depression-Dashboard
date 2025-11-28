# Quick Test Guide - Dashboard with Dummy Data

The dashboard has been set up with dummy data to test all features. Here's how to test it:

## Dummy Data Summary

The `teams_config.json` has been updated with realistic test data:

- **Dallas Cowboys**: 8-5 record, recent rivalry loss to Eagles, mixed recent streak
- **Dallas Mavericks**: 15-12 record, decent performance
- **Golden State Warriors**: 12-15 record, losing streak, rivalry loss
- **Texas Rangers**: 45-50 record, low interest level
- **Max Verstappen (F1)**: P1 position, recent wins
- **Fantasy Team**: 5-8 record, underperforming

This should generate a depression score showing various levels of contribution from each team.

## Testing Steps

### Option 1: Manual Testing

#### Terminal 1 - Start Backend
```bash
cd backend
python3 app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

#### Terminal 2 - Test API (Optional)
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test depression endpoint
curl http://localhost:5000/api/depression | python3 -m json.tool

# Test teams endpoint
curl http://localhost:5000/api/teams | python3 -m json.tool
```

#### Terminal 3 - Start Frontend
```bash
cd frontend
npm install  # First time only
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

#### Open Browser
Visit `http://localhost:3000` to see the dashboard!

### Option 2: Use Test Script

```bash
# Start backend first (Terminal 1)
cd backend
python3 app.py

# In another terminal, test the API
python3 test_dashboard.py
```

## What You Should See

### Dashboard Features to Test:

1. **Hero Depression Score Card**
   - Large emoji (should show 😢 or 😭 based on score)
   - Depression score (should be high with dummy data)
   - Color-coded gradient background
   - Animated progress bar
   - Top 3 contributors

2. **Team Cards (6 cards)**
   - Cowboys, Mavericks, Warriors, Rangers, Verstappen, Fantasy
   - Each showing:
     - Record (W-L)
     - Win percentage bar
     - Recent streak (colored dots)
     - Depression points
   - **Click to expand** for detailed breakdown

3. **Recent Games Timeline**
   - List of recent games/races
   - Color-coded results (green=win, red=loss)
   - Sport emojis
   - Rivalry badges

4. **Depression Breakdown**
   - Interactive donut chart
   - Top contributors list with percentages
   - Color-coded bars

5. **Header**
   - Refresh button (try clicking it!)
   - Last updated timestamp

## Expected Depression Score

With the dummy data, you should see a depression score around **300-350 points**, which puts Jason in the "💀 Call for Help" category. This is because:
- Cowboys have a rivalry loss
- Warriors are on a losing streak with a rivalry loss
- Fantasy team is underperforming
- Multiple teams below expectations

## Troubleshooting

### Backend won't start
- Make sure you're in the `backend` directory
- Check that Flask is installed: `pip install flask flask-cors`
- Verify `teams_config.json` exists in the parent directory

### Frontend won't start
- Make sure Node.js 18+ is installed: `node --version`
- Run `npm install` in the `frontend` directory
- Check that port 3000 is not in use

### No data showing
- Verify backend is running on port 5000
- Check browser console (F12) for errors
- Make sure CORS is working (backend should have flask-cors installed)

### API returns errors
- Check backend terminal for error messages
- Verify `teams_config.json` is valid JSON
- Make sure `depression_calculator.py` is in the parent directory

## Next Steps After Testing

Once you've verified everything works:
1. Update `teams_config.json` with real data
2. Use the refresh button to fetch live data from sports APIs
3. Customize colors, styling, or add features as needed

Enjoy testing! 🎉

