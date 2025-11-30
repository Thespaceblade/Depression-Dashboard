# Live Updates Setup Guide

## Quick Start: Migrating to Persistent Backend for Live Scores

This guide shows how to set up a persistent backend server that can poll for live scores every 10-30 seconds.

---

## Step 1: Choose Your Hosting Platform

### Recommended: Railway (Easiest)

**Why:**
- Already configured (`railway.json` exists)
- $5/month free credit (usually enough)
- Simple deployment
- Good for development and production

**Alternative: Render**
- Free tier available
- Already configured (`render.yaml` exists)
- May spin down on free tier (not ideal for live updates)

---

## Step 2: Deploy Backend to Railway

### Option A: Via Railway Dashboard

1. **Sign up:** https://railway.app
2. **Create New Project**
3. **Deploy from GitHub:**
   - Connect your GitHub repo
   - Railway auto-detects Python
   - Uses `railway.json` for config

4. **Set Environment Variables:**
   ```
   PORT=5001
   FLASK_ENV=production
   PYTHONUNBUFFERED=1
   ```

5. **Deploy:**
   - Railway will build and deploy automatically
   - Get your backend URL (e.g., `https://your-app.railway.app`)

### Option B: Via Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

---

## Step 3: Update Frontend to Use New Backend

### Update `frontend/src/api.ts`:

```typescript
// For Railway/Render deployment
const API_BASE = import.meta.env.VITE_API_URL || 'https://your-app.railway.app/api';

// Or keep localhost for development
// const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';
```

### Update Vercel Environment Variables:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add:
   ```
   VITE_API_URL=https://your-app.railway.app
   ```
3. Redeploy frontend

---

## Step 4: Add Live Score Polling to Backend

### Create `backend/live_updates.py`:

```python
#!/usr/bin/env python3
"""
Background thread for polling live scores
Runs continuously and updates in-memory state
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from src.sports_api import SportsDataFetcher

class LiveScoreMonitor:
    """Monitors live games and updates state"""
    
    def __init__(self):
        self.active_games: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        self.fetcher = SportsDataFetcher()
    
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
                time.sleep(30)  # Wait before retrying
    
    def _get_active_games(self) -> List[Dict]:
        """Get list of games currently in progress"""
        active = []
        
        try:
            # Check NFL games (Cowboys)
            team_id = 6
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
            response = self.fetcher.nfl.session.get(url, timeout=10)
            
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
                    
                    if not completed and 'IN_PROGRESS' in status_name or 'LIVE' in status_name:
                        # Game is live!
                        competitors = comp.get('competitors', [])
                        if len(competitors) == 2:
                            team = next((c for c in competitors if c.get('team', {}).get('id') == str(team_id)), None)
                            opponent = next((c for c in competitors if c.get('team', {}).get('id') != str(team_id)), None)
                            
                            if team and opponent:
                                active.append({
                                    'game_id': event.get('id'),
                                    'team': 'Dallas Cowboys',
                                    'sport': 'NFL',
                                    'team_score': team.get('score', {}).get('value', 0) if isinstance(team.get('score'), dict) else team.get('score', 0),
                                    'opponent': opponent.get('team', {}).get('displayName', 'Unknown'),
                                    'opponent_score': opponent.get('score', {}).get('value', 0) if isinstance(opponent.get('score'), dict) else opponent.get('score', 0),
                                    'status': status_name,
                                    'quarter': status.get('period', 0),
                                    'clock': status.get('displayClock', ''),
                                    'last_updated': datetime.now().isoformat()
                                })
            
            # Similar logic for NBA teams (Mavericks, Warriors)
            # ... (add NBA checking here)
            
        except Exception as e:
            print(f"Error checking active games: {e}")
        
        return active
    
    def _update_live_scores(self, active_games: List[Dict]):
        """Update in-memory state with latest scores"""
        with self.lock:
            for game in active_games:
                game_id = game['game_id']
                self.active_games[game_id] = game
                print(f"📊 Live: {game['team']} {game['team_score']} - {game['opponent_score']} {game['opponent']} ({game['quarter']}Q)")
    
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

### Update `backend/app.py`:

Add to the top of `app.py`:

```python
# ... existing imports ...
from backend.live_updates import live_monitor

# Start live monitor when app starts
@app.before_first_request
def initialize_live_monitor():
    live_monitor.start()

# Add new endpoint for live games
@app.route('/api/live-games', methods=['GET'])
def get_live_games():
    """Get currently active live games"""
    try:
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

**Note:** `@app.before_first_request` is deprecated in newer Flask. Use this instead:

```python
# At module level, after app creation
def initialize_app():
    live_monitor.start()

# Call on app startup
if __name__ == '__main__':
    initialize_app()
    app.run(...)
```

Or use a startup script:

### Create `backend/startup.py`:

```python
#!/usr/bin/env python3
"""Startup script that initializes live monitor"""

from backend.live_updates import live_monitor
from backend.app import app

# Start live monitor
live_monitor.start()

# Run app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, port=port, host='0.0.0.0')
```

Update `railway.json`:

```json
{
  "deploy": {
    "startCommand": "cd backend && python startup.py"
  }
}
```

---

## Step 5: Update Frontend for Live Updates

### Update `frontend/src/App.tsx`:

```typescript
// Add state for live games
const [liveGames, setLiveGames] = useState<LiveGame[]>([]);

// Add function to fetch live games
const fetchLiveGames = async () => {
  try {
    const response = await fetch(`${API_BASE}/live-games`);
    const data = await response.json();
    if (data.success) {
      setLiveGames(data.games);
    }
  } catch (err) {
    console.error('Error fetching live games:', err);
  }
};

// Update polling strategy
useEffect(() => {
  loadData();
  fetchLiveGames();
  
  // Poll more frequently if live games exist
  const pollInterval = liveGames.length > 0 ? 10000 : 60000; // 10s or 60s
  
  const interval = setInterval(() => {
    loadData();
    fetchLiveGames();
  }, pollInterval);
  
  return () => clearInterval(interval);
}, [liveGames.length]);
```

### Create `frontend/src/components/LiveGameCard.tsx`:

```typescript
interface LiveGameCardProps {
  game: {
    team: string;
    opponent: string;
    team_score: number;
    opponent_score: number;
    quarter: number;
    clock: string;
    sport: string;
  };
}

export default function LiveGameCard({ game }: LiveGameCardProps) {
  const isWinning = game.team_score > game.opponent_score;
  const isLosing = game.team_score < game.opponent_score;
  
  return (
    <div className="bg-gray-800 rounded-lg p-4 border-2 border-red-500 animate-pulse">
      <div className="flex items-center justify-between mb-2">
        <span className="text-red-500 font-bold text-sm">🔴 LIVE</span>
        <span className="text-gray-400 text-sm">
          {game.sport} • Q{game.quarter} • {game.clock}
        </span>
      </div>
      
      <div className="space-y-2">
        <div className={`flex justify-between ${isWinning ? 'text-green-400' : ''}`}>
          <span>{game.team}</span>
          <span className="font-bold">{game.team_score}</span>
        </div>
        <div className={`flex justify-between ${isLosing ? 'text-red-400' : ''}`}>
          <span>{game.opponent}</span>
          <span className="font-bold">{game.opponent_score}</span>
        </div>
      </div>
    </div>
  );
}
```

---

## Step 6: Test the Setup

### Local Testing:

1. **Start backend:**
   ```bash
   cd backend
   python startup.py
   ```

2. **Check logs:**
   - Should see "✅ Live score monitor started"
   - During games, should see score updates every 10 seconds

3. **Test API:**
   ```bash
   curl http://localhost:5001/api/live-games
   ```

### Production Testing:

1. **Deploy to Railway:**
   ```bash
   railway up
   ```

2. **Check Railway logs:**
   - Should see monitor starting
   - Should see periodic updates during games

3. **Test from frontend:**
   - Visit your Vercel frontend
   - During a live game, should see live score card
   - Scores should update every 10 seconds

---

## Step 7: Monitor Costs

### Railway:
- Free tier: $5/month credit
- Usage: ~$0.50-2/month for small app
- **Should be free or very cheap**

### Render:
- Free tier: Limited (may spin down)
- Paid: $7/month for 24/7 uptime
- **Recommended for production**

### Monitoring:
- Check Railway dashboard for usage
- Set up alerts if approaching limits
- Monitor API response times

---

## Troubleshooting

### Backend won't start:
- Check Railway logs
- Verify `startup.py` is correct
- Check environment variables

### Live games not showing:
- Check if game is actually live (ESPN API)
- Check Railway logs for errors
- Verify `/api/live-games` endpoint works

### Scores not updating:
- Check background thread is running
- Check ESPN API responses
- Verify polling interval

### High costs:
- Reduce polling frequency (30s instead of 10s)
- Only poll during game windows
- Use caching more aggressively

---

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Test live game detection
3. ✅ Add live score UI components
4. ✅ Test during actual games
5. ✅ Monitor costs and performance
6. ✅ Optimize polling strategy

---

## Cost Summary

**Estimated Monthly Costs:**
- Railway: $0-5 (free tier usually sufficient)
- Render: $0-7 (free tier with limitations)
- **Total: ~$5-10/month for live updates**

**Worth it?** 
- If you watch games regularly: **Yes!** 🎯
- If you just check scores occasionally: Maybe not

---

## Alternative: Simpler "Near-Live" Approach

If you want to keep it simpler:

1. **Keep current setup** (Vercel + GitHub Actions)
2. **Poll every 5 minutes** (GitHub Actions minimum)
3. **Show "Last updated: 5m ago"** indicator
4. **Calculate depression from most recent completed games**

**Pros:**
- No hosting migration needed
- Free (GitHub Actions free tier)
- Simpler implementation

**Cons:**
- Not truly "live" (5 minute delay)
- Less engaging during games

**Estimated Effort:** 1-2 days (vs 3-5 days for full live)

---

Your live updates system is now ready! 🚀




