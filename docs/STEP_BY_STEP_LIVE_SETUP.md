# Step-by-Step: Live Scores Setup Guide

Follow these steps in order to get live scores working.

---

## Prerequisites Checklist

Before starting, make sure you have:
- [ ] GitHub account (your code is already there)
- [ ] Railway account (we'll create this)
- [ ] Vercel account (you probably already have this)
- [ ] Code editor ready
- [ ] Terminal/command line access

---

## PART 1: Set Up Railway Backend (30 minutes)

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Sign up with GitHub (easiest - connects automatically)
4. You'll see your dashboard

### Step 2: Create New Project on Railway

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select your `Depression-Dashboard` repository
4. Railway will start detecting your project

### Step 3: Configure Railway Service

1. Railway should auto-detect Python
2. If it asks for build settings:
   - **Build Command:** Leave empty (Railway auto-detects)
   - **Start Command:** `cd backend && python app.py`
   - **Root Directory:** Leave as `/` (root)

3. Click **"Deploy"** or **"Settings"** to configure:

### Step 4: Set Environment Variables

1. In Railway, go to your service → **"Variables"** tab
2. Add these environment variables:
   ```
   PORT=5001
   FLASK_ENV=production
   PYTHONUNBUFFERED=1
   ```
3. Railway will auto-set `PORT`, but add it anyway to be safe

### Step 5: Update railway.json (if needed)

Check your `railway.json` file. It should look like:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

If it's different, update it to match above.

### Step 6: Deploy and Get URL

1. Railway will automatically deploy
2. Wait for build to complete (2-5 minutes)
3. Once deployed, click on your service
4. Go to **"Settings"** → **"Networking"**
5. Click **"Generate Domain"** or use the default one
6. **Copy your Railway URL** (e.g., `https://your-app-name.railway.app`)
7. **Save this URL** - you'll need it!

### Step 7: Test Your Backend

1. Open a new browser tab
2. Go to: `https://your-railway-url.railway.app/api/health`
3. You should see: `{"status":"healthy","timestamp":"..."}`
4. If it works, ✅ **Backend is live!**

**If it doesn't work:**
- Check Railway logs (click "Logs" tab)
- Make sure deployment completed successfully
- Check for errors in logs

---

## PART 2: Add Live Score Polling Code (45 minutes)

### Step 8: Create Live Updates Module

1. Open your code editor
2. Create new file: `backend/live_updates.py`
3. Copy this code into it:

```python
#!/usr/bin/env python3
"""
Background thread for polling live scores
Runs continuously and updates in-memory state
"""

import threading
import time
import os
from datetime import datetime
from typing import Dict, List, Optional
import requests

class LiveScoreMonitor:
    """Monitors live games and updates state"""
    
    def __init__(self):
        self.active_games: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def start(self):
        """Start background monitoring thread"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print("✅ Live score monitor started")
    
    def stop(self):
        """Stop monitoring thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("⏹️ Live score monitor stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop - runs in background thread"""
        while self.running:
            try:
                # Check for active games
                active = self._get_active_games()
                
                if active:
                    # Poll every 10 seconds during games
                    self._update_live_scores(active)
                    time.sleep(10)
                else:
                    # Poll every 60 seconds when no games
                    time.sleep(60)
                    
            except Exception as e:
                print(f"❌ Error in live monitor: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(30)  # Wait before retrying
    
    def _get_active_games(self) -> List[Dict]:
        """Get list of games currently in progress"""
        active = []
        
        try:
            # Check NFL games (Cowboys - Team ID 6)
            team_id = 6
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                
                for event in events:
                    competitions = event.get('competitions', [])
                    if not competitions:
                        continue
                    
                    comp = competitions[0]
                    status = comp.get('status', {})
                    status_type = status.get('type', {})
                    
                    # Check if game is in progress
                    status_name = status_type.get('name', '').upper() if isinstance(status_type, dict) else str(status_type).upper()
                    completed = status_type.get('completed', False) if isinstance(status_type, dict) else False
                    
                    # Game is live if: not completed AND has scores
                    competitors = comp.get('competitors', [])
                    if len(competitors) == 2:
                        team1_score = competitors[0].get('score')
                        team2_score = competitors[1].get('score')
                        
                        # Extract score values
                        def get_score(score_obj):
                            if score_obj is None:
                                return None
                            if isinstance(score_obj, dict):
                                return score_obj.get('value')
                            return score_obj
                        
                        score1 = get_score(team1_score)
                        score2 = get_score(team2_score)
                        
                        # If scores exist and game not completed, it's live
                        if score1 is not None and score2 is not None and not completed:
                            team = next((c for c in competitors if c.get('team', {}).get('id') == str(team_id)), None)
                            opponent = next((c for c in competitors if c.get('team', {}).get('id') != str(team_id)), None)
                            
                            if team and opponent:
                                team_score = get_score(team.get('score'))
                                opp_score = get_score(opponent.get('score'))
                                
                                active.append({
                                    'game_id': event.get('id'),
                                    'team': 'Dallas Cowboys',
                                    'sport': 'NFL',
                                    'team_score': team_score or 0,
                                    'opponent': opponent.get('team', {}).get('displayName', 'Unknown'),
                                    'opponent_score': opp_score or 0,
                                    'status': status_name,
                                    'quarter': status.get('period', 0),
                                    'clock': status.get('displayClock', ''),
                                    'last_updated': datetime.now().isoformat()
                                })
            
            # Check NBA games (Mavericks - Team ID 6, Warriors - Team ID 9)
            for team_name, team_id in [('Dallas Mavericks', 6), ('Golden State Warriors', 9)]:
                url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/schedule"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    events = data.get('events', [])
                    
                    for event in events:
                        competitions = event.get('competitions', [])
                        if not competitions:
                            continue
                        
                        comp = competitions[0]
                        status = comp.get('status', {})
                        status_type = status.get('type', {})
                        
                        status_name = status_type.get('name', '').upper() if isinstance(status_type, dict) else str(status_type).upper()
                        completed = status_type.get('completed', False) if isinstance(status_type, dict) else False
                        
                        competitors = comp.get('competitors', [])
                        if len(competitors) == 2:
                            team1_score = competitors[0].get('score')
                            team2_score = competitors[1].get('score')
                            
                            def get_score(score_obj):
                                if score_obj is None:
                                    return None
                                if isinstance(score_obj, dict):
                                    return score_obj.get('value')
                                return score_obj
                            
                            score1 = get_score(team1_score)
                            score2 = get_score(team2_score)
                            
                            if score1 is not None and score2 is not None and not completed:
                                team = next((c for c in competitors if c.get('team', {}).get('id') == str(team_id)), None)
                                opponent = next((c for c in competitors if c.get('team', {}).get('id') != str(team_id)), None)
                                
                                if team and opponent:
                                    team_score = get_score(team.get('score'))
                                    opp_score = get_score(opponent.get('score'))
                                    
                                    active.append({
                                        'game_id': event.get('id'),
                                        'team': team_name,
                                        'sport': 'NBA',
                                        'team_score': team_score or 0,
                                        'opponent': opponent.get('team', {}).get('displayName', 'Unknown'),
                                        'opponent_score': opp_score or 0,
                                        'status': status_name,
                                        'quarter': status.get('period', 0),
                                        'clock': status.get('displayClock', ''),
                                        'last_updated': datetime.now().isoformat()
                                    })
            
        except Exception as e:
            print(f"Error checking active games: {e}")
            import traceback
            traceback.print_exc()
        
        return active
    
    def _update_live_scores(self, active_games: List[Dict]):
        """Update in-memory state with latest scores"""
        with self.lock:
            for game in active_games:
                game_id = game['game_id']
                self.active_games[game_id] = game
                print(f"📊 Live: {game['team']} {game['team_score']} - {game['opponent_score']} {game['opponent']} ({game.get('quarter', '?')}Q)")
    
    def get_live_games(self) -> List[Dict]:
        """Get current live games (thread-safe)"""
        with self.lock:
            return list(self.active_games.values())
    
    def get_live_game(self, team_name: str) -> Optional[Dict]:
        """Get live game for specific team"""
        with self.lock:
            for game in self.active_games.values():
                if team_name.lower() in game['team'].lower():
                    return game
        return None

# Global instance
live_monitor = LiveScoreMonitor()
```

4. **Save the file**

### Step 9: Update backend/app.py

1. Open `backend/app.py`
2. At the top, after the imports, add:

```python
# Import live monitor
try:
    from backend.live_updates import live_monitor
    LIVE_UPDATES_AVAILABLE = True
except ImportError:
    LIVE_UPDATES_AVAILABLE = False
    print("⚠️ Live updates module not available")
```

3. Find the `get_calculator()` function and add this right after it:

```python
# Initialize live monitor when app starts
if LIVE_UPDATES_AVAILABLE and not live_monitor.running:
    live_monitor.start()
    print("✅ Live score monitor initialized")
```

4. Add this new endpoint before the `if __name__ == '__main__':` line:

```python
@app.route('/api/live-games', methods=['GET'])
def get_live_games():
    """Get currently active live games"""
    try:
        if not LIVE_UPDATES_AVAILABLE:
            return jsonify({
                "success": False,
                "error": "Live updates not available"
            }), 503
        
        games = live_monitor.get_live_games()
        return jsonify({
            "success": True,
            "games": games,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

5. **Save the file**

### Step 10: Test Locally (Optional but Recommended)

1. Open terminal in your project directory
2. Run:
   ```bash
   cd backend
   python app.py
   ```
3. You should see: `✅ Live score monitor started`
4. In another terminal, test:
   ```bash
   curl http://localhost:5001/api/live-games
   ```
5. Should return JSON (empty array if no games)
6. Press `Ctrl+C` to stop

---

## PART 3: Update Frontend (30 minutes)

### Step 11: Update API Configuration

1. Open `frontend/src/api.ts`
2. Find the `API_BASE` line (should be around line 5)
3. Update it to:

```typescript
// For production, use Railway backend
// For development, use localhost
const API_BASE = import.meta.env.VITE_API_URL || 
  (import.meta.env.PROD ? 'https://your-railway-url.railway.app/api' : 'http://localhost:5001/api');
```

**Replace `your-railway-url.railway.app` with your actual Railway URL!**

4. Add this new function at the end of the file:

```typescript
export async function fetchLiveGames(): Promise<{ success: boolean; games: any[] }> {
  const response = await fetch(`${API_BASE}/live-games`);
  if (!response.ok) {
    throw new Error('Failed to fetch live games');
  }
  return response.json();
}
```

5. **Save the file**

### Step 12: Update Types

1. Open `frontend/src/types/index.ts`
2. Add this interface:

```typescript
export interface LiveGame {
  game_id: string;
  team: string;
  sport: string;
  team_score: number;
  opponent: string;
  opponent_score: number;
  status: string;
  quarter: number;
  clock: string;
  last_updated: string;
}

export interface LiveGamesData {
  success: boolean;
  games: LiveGame[];
  timestamp: string;
}
```

3. **Save the file**

### Step 13: Create Live Game Card Component

1. Create new file: `frontend/src/components/LiveGameCard.tsx`
2. Copy this code:

```typescript
import type { LiveGame } from '../types';

interface LiveGameCardProps {
  game: LiveGame;
}

export default function LiveGameCard({ game }: LiveGameCardProps) {
  const isWinning = game.team_score > game.opponent_score;
  const isLosing = game.team_score < game.opponent_score;
  const isTied = game.team_score === game.opponent_score;
  
  return (
    <div className="bg-gray-800 rounded-lg p-4 border-2 border-red-500 animate-pulse">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
          <span className="text-red-500 font-bold text-sm">LIVE</span>
        </div>
        <span className="text-gray-400 text-xs">
          {game.sport} • Q{game.quarter} {game.clock && `• ${game.clock}`}
        </span>
      </div>
      
      <div className="space-y-2">
        <div className={`flex justify-between items-center ${isWinning ? 'text-green-400' : ''}`}>
          <span className="font-medium">{game.team}</span>
          <span className="font-bold text-xl">{game.team_score}</span>
        </div>
        <div className={`flex justify-between items-center ${isLosing ? 'text-red-400' : ''}`}>
          <span className="font-medium">{game.opponent}</span>
          <span className="font-bold text-xl">{game.opponent_score}</span>
        </div>
      </div>
      
      {isTied && (
        <div className="mt-2 text-center text-yellow-400 text-sm">Tied</div>
      )}
    </div>
  );
}
```

3. **Save the file**

### Step 14: Update App.tsx

1. Open `frontend/src/App.tsx`
2. Add to imports at top:

```typescript
import { fetchLiveGames } from './api';
import type { LiveGamesData } from './types';
import LiveGameCard from './components/LiveGameCard';
```

3. Add state after other useState declarations:

```typescript
const [liveGames, setLiveGames] = useState<LiveGame[]>([]);
```

4. Update the `loadData` function to also fetch live games:

```typescript
const loadData = async () => {
  try {
    setLoading(true);
    setError(null);
    
    const [depression, teams, games, upcoming, live] = await Promise.all([
      fetchDepression(),
      fetchTeams(),
      fetchRecentGames(),
      fetchUpcomingEvents(),
      fetchLiveGames().catch(() => ({ success: false, games: [] })) // Don't fail if live games fail
    ]);
    
    setDepressionData(depression);
    setTeamsData(teams);
    setGamesData(games);
    setUpcomingEventsData(upcoming);
    setLiveGames(live.games || []);
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Failed to load data');
    console.error('Error loading data:', err);
  } finally {
    setLoading(false);
  }
};
```

5. Update the useEffect to poll more frequently during live games:

```typescript
useEffect(() => {
  loadData();
  
  // Poll more frequently if live games exist
  const pollInterval = liveGames.length > 0 ? 10000 : 60000; // 10s or 60s
  
  const interval = setInterval(loadData, pollInterval);
  
  return () => clearInterval(interval);
}, [liveGames.length]); // Re-run when live games change
```

6. Add live games display in the JSX. Find the section after the Depression Score Card and add:

```typescript
{/* Live Games Section */}
{liveGames.length > 0 && (
  <section className="mb-8">
    <h2 className="text-3xl font-bold text-white mb-4">🔴 Live Games</h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {liveGames.map((game) => (
        <LiveGameCard key={game.game_id} game={game} />
      ))}
    </div>
  </section>
)}
```

7. **Save the file**

### Step 15: Test Frontend Locally

1. In terminal, go to frontend directory:
   ```bash
   cd frontend
   npm run dev
   ```
2. Open browser to `http://localhost:5173` (or whatever port it shows)
3. Check browser console for errors
4. If no errors, ✅ Frontend is ready!

---

## PART 4: Deploy Everything (20 minutes)

### Step 16: Commit and Push Code

1. Make sure all files are saved
2. In terminal, from project root:
   ```bash
   git add .
   git commit -m "Add live score monitoring"
   git push origin main
   ```

### Step 17: Railway Auto-Deploys

1. Railway should automatically detect the push
2. Go to Railway dashboard
3. Watch the deployment logs
4. Wait for "Deploy successful" message
5. Test: `https://your-railway-url.railway.app/api/live-games`

### Step 18: Update Vercel Environment Variable

1. Go to https://vercel.com
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://your-railway-url.railway.app/api`
   - **Environment:** Production, Preview, Development (check all)
5. Click **Save**
6. Go to **Deployments** tab
7. Click **"Redeploy"** on the latest deployment
8. Wait for redeploy to complete

### Step 19: Test Production

1. Visit your Vercel frontend URL
2. Open browser DevTools (F12) → Console tab
3. Check for errors
4. During a live game, you should see:
   - Live game cards appear
   - Scores update every 10 seconds
   - "LIVE" indicator pulsing

---

## PART 5: Verification Checklist

### Backend Tests:
- [ ] Railway backend is running
- [ ] `/api/health` returns success
- [ ] `/api/live-games` returns JSON (empty array if no games)
- [ ] Railway logs show "Live score monitor started"

### Frontend Tests:
- [ ] Frontend loads without errors
- [ ] Console shows no API errors
- [ ] During live games, live cards appear
- [ ] Scores update automatically

### During Live Game:
- [ ] Live game card shows correct scores
- [ ] Scores update every 10 seconds
- [ ] "LIVE" indicator is visible
- [ ] Quarter/clock information displays

---

## Troubleshooting

### Backend won't start:
- Check Railway logs for errors
- Verify `live_updates.py` is in `backend/` folder
- Check Python version (should be 3.11+)
- Make sure `requests` is in `requirements.txt`

### Live games not showing:
- Check if game is actually live (ESPN)
- Check Railway logs for API errors
- Test `/api/live-games` endpoint directly
- Verify ESPN API is responding

### Frontend can't connect:
- Check `VITE_API_URL` is set correctly in Vercel
- Verify Railway URL is correct
- Check CORS settings (should be fine)
- Test API URL in browser directly

### Scores not updating:
- Check Railway logs for polling activity
- Verify background thread is running
- Check polling interval (should be 10s during games)
- Look for errors in Railway logs

---

## Cost Monitoring

### Check Railway Usage:
1. Go to Railway dashboard
2. Click on your project
3. Check **"Usage"** tab
4. Monitor monthly spend

### Expected Costs:
- **Free tier:** $5/month credit
- **Usage:** ~$0.50-2/month for small app
- **Should be free or very cheap!**

### If costs are high:
- Reduce polling to 30 seconds (instead of 10)
- Only poll during game windows
- Add more caching

---

## You're Done! 🎉

Your live scores should now be working! During games, you'll see:
- Live game cards with current scores
- Automatic updates every 10 seconds
- Real-time depression score changes

**Next time there's a game, check your dashboard and watch the scores update live!**

---

## Quick Reference

**Railway URL:** `https://your-app.railway.app`  
**API Health:** `https://your-app.railway.app/api/health`  
**Live Games:** `https://your-app.railway.app/api/live-games`  
**Vercel Frontend:** `https://your-app.vercel.app`

**Files Modified:**
- `backend/live_updates.py` (new)
- `backend/app.py` (updated)
- `frontend/src/api.ts` (updated)
- `frontend/src/types/index.ts` (updated)
- `frontend/src/components/LiveGameCard.tsx` (new)
- `frontend/src/App.tsx` (updated)




