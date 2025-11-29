# Live Scores & Live Depression Analytics - Feasibility Assessment

## Executive Summary

**Overall Feasibility: MODERATE to HIGH** ⚠️✅

The application has a **solid foundation** for live scores and live depression analytics, but requires **significant architectural changes** and **infrastructure improvements** to make it production-ready.

**⚠️ CRITICAL HOSTING REQUIREMENT:** Live scores require a **persistent server** that can run continuously. Vercel (serverless) and GitHub Actions (scheduled) **cannot** support live updates that poll every 10-30 seconds.

---

## Current Architecture Analysis

### ✅ What's Already in Place

1. **Time-Weighted Depression Algorithm**
   - The system already uses exponential decay for recent events
   - `calculate_time_weight()` function supports hours-level granularity
   - Very recent events (0-6 hours) get 100-83% weight
   - This is **perfect** for live analytics - recent losses hurt more!

2. **API Infrastructure**
   - ESPN API integration already exists (NFL, NBA, College)
   - Schedule endpoints are being used (`/teams/{id}/schedule`)
   - Status checking exists (`completed` field detection)
   - Frontend already polls every 60 seconds

3. **Game Status Detection**
   - Code already checks `comp_status.get('completed', False)`
   - Can detect if games have scores (in progress vs completed)
   - Overtime detection exists (`'OT' in status_name`)

4. **Frontend Auto-Refresh**
   - Already refreshes every 60 seconds
   - Could be adjusted to 10-30 seconds during live games

### ❌ What's Missing

1. **Live Game Detection**
   - No logic to detect "in progress" games (only "completed" vs "upcoming")
   - No game start time tracking
   - No active game monitoring

2. **Real-Time Data Updates**
   - Data stored in static JSON file (`teams_config.json`)
   - No in-memory state management
   - No WebSocket/SSE for push updates
   - Relies on file-based persistence

3. **Rate Limiting & API Management**
   - No rate limiting strategy
   - No caching for live scores
   - Could hit API limits with frequent polling

4. **Backend Architecture**
   - Flask app uses global calculator instance
   - No database for live state
   - File writes could conflict with concurrent requests

---

## Technical Feasibility by Component

### 1. Live Score Display ⚠️ **MODERATE**

**What's Needed:**
- Detect games "in progress" (not just completed/upcoming)
- Poll ESPN API more frequently during games (every 10-30 seconds)
- Display live scores in UI
- Handle score updates gracefully

**ESPN API Capabilities:**
```python
# ESPN API provides:
status = comp.get('status', {})
status_type = status.get('type', {})
# Possible values: "STATUS_SCHEDULED", "STATUS_IN_PROGRESS", "STATUS_FINAL"
```

**Implementation Complexity:** Medium
- Need to add status parsing for "in progress"
- Need to track which games are currently live
- Need to update frontend to show live indicator
- Need to handle score updates without full page refresh

**Estimated Effort:** 2-3 days

---

### 2. Live Depression Analytics ⚠️ **MODERATE to HIGH**

**What's Needed:**
- Recalculate depression score as game progresses
- Update in real-time as scores change
- Show "projected" depression based on current game state
- Handle edge cases (overtime, comebacks, blowouts)

**Current Algorithm Support:**
The depression calculator already supports this conceptually:
- Time-weighted scoring (recent = more impact)
- Game context (score margins, overtime, comebacks)
- Opponent quality multipliers

**Example Scenario:**
```
Game: Cowboys vs Eagles (Rival)
Current Score: Eagles 21, Cowboys 7 (2nd quarter)
- Depression increases as deficit grows
- If Cowboys come back and win: depression drops
- If they lose: depression spikes (rivalry loss = 2.2x multiplier)
```

**Implementation Complexity:** Medium-High
- Need to calculate depression "as if game ended now"
- Need to handle partial game data
- Need to update UI smoothly without jarring changes
- Need to handle game state transitions (in progress → final)

**Estimated Effort:** 3-5 days

---

### 3. Real-Time Updates Architecture ⚠️ **HIGH COMPLEXITY**

**Current Approach:**
- Frontend polls every 60 seconds
- Backend reads from JSON file
- No push notifications

**Better Approaches:**

**Option A: Frequent Polling (Easiest)**
- Increase polling to 10-30 seconds during live games
- Keep current architecture
- **Pros:** Simple, no new infrastructure
- **Cons:** More API calls, not truly "real-time"

**Option B: Server-Sent Events (SSE)**
- Backend pushes updates when scores change
- Frontend subscribes to event stream
- **Pros:** True push updates, efficient
- **Cons:** Requires backend changes, connection management

**Option C: WebSockets**
- Full bidirectional communication
- **Pros:** Most flexible, true real-time
- **Cons:** Most complex, requires WebSocket server

**Recommended:** Start with **Option A**, upgrade to **Option B** if needed

**Estimated Effort:**
- Option A: 1-2 days
- Option B: 3-5 days
- Option C: 5-7 days

---

## ⚠️ CRITICAL: Hosting Requirements for Live Updates

### Why Current Setup Won't Work

**Vercel (Serverless Functions):**
- ❌ Execution time limits (10 seconds on free tier, 60s on pro)
- ❌ Cold starts cause delays
- ❌ Not designed for long-running processes
- ❌ Can't maintain in-memory state between requests
- **Verdict:** Cannot support live score polling

**GitHub Actions (Scheduled Jobs):**
- ❌ Can't run every 10-30 seconds (minimum is 5 minutes)
- ❌ Would create thousands of commits per day
- ❌ Not designed for real-time data
- **Verdict:** Cannot support live updates

### Required: Persistent Server

For live scores, you need a **persistent backend server** that:
- ✅ Runs 24/7 (not serverless)
- ✅ Can maintain in-memory state
- ✅ Can poll APIs every 10-30 seconds
- ✅ Can handle WebSocket/SSE connections (optional)
- ✅ Supports background workers/threads

### Recommended Hosting Options

#### Option 1: Railway (✅ Already Configured!)

**Why Railway:**
- ✅ Already has `railway.json` configured
- ✅ Supports long-running processes
- ✅ Free tier: $5/month credit (usually enough)
- ✅ Easy deployment from GitHub
- ✅ Built-in logging and monitoring
- ✅ Can run background workers

**Setup for Live Updates:**
```yaml
# railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python app.py",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

**Cost:** ~$5-10/month (free tier usually sufficient)

**Implementation:**
- Backend runs continuously
- Background thread polls ESPN API every 10-30s during games
- In-memory state for live scores
- Persists to file every 5 minutes

---

#### Option 2: Render (✅ Already Configured!)

**Why Render:**
- ✅ Already has `render.yaml` configured
- ✅ Free tier available (with limitations)
- ✅ Supports web services (long-running)
- ✅ Built-in cron jobs
- ✅ Easy GitHub integration

**Setup for Live Updates:**
```yaml
# render.yaml
services:
  - type: web
    name: depression-dashboard-api
    env: python
    startCommand: cd backend && python app.py
    # Runs continuously
```

**Cost:** Free tier available, or ~$7/month for better performance

**Limitations:**
- Free tier spins down after 15 minutes of inactivity
- Paid tier needed for 24/7 uptime

---

#### Option 3: Fly.io (Recommended for Production)

**Why Fly.io:**
- ✅ Excellent for persistent processes
- ✅ Generous free tier
- ✅ Global edge network
- ✅ Built-in health checks
- ✅ Supports WebSockets natively

**Setup:**
```toml
# fly.toml
[app]
  name = "depression-dashboard"

[build]
  builder = "paketobuildpacks/builder:base"

[[services]]
  internal_port = 5001
  protocol = "tcp"
```

**Cost:** Free tier available, ~$3-5/month for production

---

#### Option 4: DigitalOcean App Platform

**Why DigitalOcean:**
- ✅ Reliable and well-documented
- ✅ Supports workers and web services
- ✅ Good for production apps
- ✅ Built-in database options

**Cost:** ~$5-12/month

---

#### Option 5: VPS (Most Control, Most Work)

**Why VPS:**
- ✅ Full control over environment
- ✅ Can run anything
- ✅ Most cost-effective for high traffic
- ❌ Requires server management

**Options:**
- DigitalOcean Droplet: $6-12/month
- Linode: $5-10/month
- Vultr: $6-12/month
- AWS EC2: Pay-as-you-go

**Setup Complexity:** High (need to configure nginx, systemd, etc.)

---

### Recommended Architecture for Live Updates

```
┌─────────────────────────────────────────┐
│  Frontend (Vercel/Netlify)             │
│  - Static React app                     │
│  - Polls API every 10-30s during games  │
└──────────────┬──────────────────────────┘
               │ HTTPS
               ↓
┌─────────────────────────────────────────┐
│  Backend (Railway/Render/Fly.io)       │
│  - Flask app running 24/7              │
│  - In-memory state for live games       │
│  - Background thread polls ESPN API    │
│  - Updates every 10-30s during games    │
│  - Persists to file every 5 minutes     │
└──────────────┬──────────────────────────┘
               │
               ↓
         ┌─────────────┐
         │  ESPN API   │
         │  (External) │
         └─────────────┘
```

### Migration Path

**Current Setup:**
- Frontend: Vercel ✅ (can stay)
- Backend: Vercel serverless functions ❌ (needs to change)

**New Setup:**
- Frontend: Vercel ✅ (stays the same)
- Backend: Railway/Render/Fly.io ✅ (persistent server)

**Steps:**
1. Deploy backend to Railway/Render
2. Update frontend `API_BASE` to point to new backend
3. Add background polling thread to backend
4. Test with live games
5. Monitor costs and performance

---

## Infrastructure Requirements

### 1. Backend State Management

**Current:** File-based (`teams_config.json`)
**Needed:** In-memory state + periodic persistence

**Solution:**
```python
# In-memory game state
live_games = {
    "game_id": {
        "status": "in_progress",
        "team_score": 21,
        "opponent_score": 7,
        "quarter": 2,
        "last_updated": datetime.now()
    }
}

# Update every 10-30 seconds during games
# Persist to file every 5 minutes or on game completion
```

**Estimated Effort:** 1-2 days

---

### 2. API Rate Limiting

**Concerns:**
- ESPN API may have rate limits
- Frequent polling could hit limits
- Need caching strategy

**Solutions:**
- Cache live scores for 10-30 seconds
- Only poll teams with active games
- Use exponential backoff on errors
- Consider API key if available

**Estimated Effort:** 1 day

---

### 3. Game Detection & Scheduling

**Needed:**
- Detect when games start (from schedule)
- Start polling when game begins
- Stop polling when game ends
- Handle multiple simultaneous games

**Implementation:**
```python
def get_active_games():
    """Get all games currently in progress"""
    upcoming = get_upcoming_events()
    active = []
    for game in upcoming:
        if game['status'] == 'in_progress':
            active.append(game)
    return active

# Poll every 10 seconds if active games exist
# Poll every 60 seconds if no active games
```

**Estimated Effort:** 2-3 days

---

## Frontend Changes Required

### 1. Live Score Display Component

**New Component:** `LiveGameCard.tsx`
- Shows current score
- Shows game clock/quarter
- Shows "LIVE" indicator
- Updates smoothly without full refresh

**Estimated Effort:** 1-2 days

### 2. Live Depression Score Updates

**Changes to `DepressionScoreCard.tsx`:**
- Animate score changes
- Show "projected" vs "current" score
- Highlight when score changes during live game

**Estimated Effort:** 1 day

### 3. Polling Strategy

**Current:** 60 seconds always
**New:** 
- 10-30 seconds during live games
- 60 seconds otherwise
- Detect active games from API response

**Estimated Effort:** 0.5 days

---

## Data Flow for Live Updates

### Current Flow:
```
Frontend (60s poll) → Backend API → Read teams_config.json → Calculate → Return
```

### Proposed Flow:
```
Frontend (10-30s poll during games) 
  → Backend API 
  → Check for active games
  → Fetch live scores from ESPN API
  → Update in-memory state
  → Calculate depression (with live game context)
  → Return updated data
  → Persist to file periodically
```

---

## Depression Calculation During Live Games

### Challenge: How to calculate depression for an incomplete game?

**Approach 1: Projected Loss (Conservative)**
- If losing: Calculate as if game ends now (loss)
- If winning: Don't reduce depression yet (game not over)
- **Pros:** Realistic, doesn't over-optimize
- **Cons:** May show high depression even if winning

**Approach 2: Current State Only**
- Only count completed games
- Show "projected" depression separately
- **Pros:** Accurate for completed games
- **Cons:** Doesn't show live impact

**Approach 3: Weighted Projection**
- If losing by 2+ scores: Count as likely loss (0.7x weight)
- If winning: Count as likely win (-0.5x weight, reduces depression)
- If close: Don't count yet
- **Pros:** Most realistic
- **Cons:** Most complex

**Recommended:** Start with **Approach 1**, refine based on feedback

---

## Cost & Performance Considerations

### API Costs
- **Current:** ~4 API calls per hour (every 6 hours for 4 teams)
- **With Live:** ~120-360 calls per hour during games (every 10-30s for active games)
- **Risk:** ESPN API may rate limit or require paid tier

### Server Costs
- **Current:** Minimal (static file reads)
- **With Live:** Slightly higher (more frequent API calls, in-memory state)
- **Impact:** Low (unless hitting rate limits)

### User Experience
- **Current:** 60-second delay acceptable
- **With Live:** 10-30 second updates feel "real-time"
- **Benefit:** Much more engaging during games

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
1. ✅ Add game status detection ("in progress" vs "completed")
2. ✅ Add in-memory state management
3. ✅ Update frontend polling strategy
4. ✅ Add live game detection logic

**Deliverable:** Can detect and display live games

### Phase 2: Live Scores (Week 2)
1. ✅ Fetch live scores from ESPN API
2. ✅ Display live scores in UI
3. ✅ Add "LIVE" indicators
4. ✅ Handle score updates smoothly

**Deliverable:** Live scores displayed during games

### Phase 3: Live Analytics (Week 3)
1. ✅ Calculate depression with live game context
2. ✅ Show projected depression scores
3. ✅ Animate score changes
4. ✅ Handle game completion transitions

**Deliverable:** Live depression analytics working

### Phase 4: Optimization (Week 4)
1. ✅ Add caching for API calls
2. ✅ Implement rate limiting
3. ✅ Add error handling for API failures
4. ✅ Consider SSE/WebSocket upgrade

**Deliverable:** Production-ready live system

---

## Risks & Mitigations

### Risk 1: ESPN API Rate Limits
**Mitigation:** 
- Cache responses for 10-30 seconds
- Only poll active games
- Add exponential backoff
- Monitor API response headers for rate limit info

### Risk 2: Backend Performance
**Mitigation:**
- Use in-memory state (fast)
- Persist to file asynchronously
- Add request queuing if needed

### Risk 3: Data Consistency
**Mitigation:**
- Use atomic file writes
- Handle concurrent requests gracefully
- Add error recovery

### Risk 4: User Experience
**Mitigation:**
- Smooth animations for score changes
- Show loading states during updates
- Graceful degradation if API fails

---

## Alternative: Simpler Approach

### "Near-Live" Updates (Easier)

Instead of true real-time, implement:
- Poll every 30 seconds (instead of 60)
- Only during game windows (detect from schedule)
- Show "Last updated: 30s ago" indicator
- Calculate depression from most recent completed games

**Benefits:**
- Much simpler implementation
- Still feels "live" to users
- Lower API usage
- Less infrastructure complexity

**Estimated Effort:** 2-3 days total

---

## Conclusion

### Feasibility Rating: **7/10** ⚠️✅ (with proper hosting)

**The Good:**
- Algorithm already supports time-weighted recent events
- API infrastructure exists
- Frontend polling already in place
- ESPN API provides necessary data
- Railway/Render already configured ✅

**The Challenges:**
- ⚠️ **CRITICAL:** Must migrate backend from Vercel to persistent server
- Need to detect "in progress" games (not just completed)
- Need in-memory state management
- Need more frequent polling strategy
- Need to handle live game → completed transitions

**Recommendation:**
1. **First:** Migrate backend to Railway or Render (already configured!)
2. **Then:** Implement "Near-Live" approach (30-second polling during games)
3. **Later:** Upgrade to SSE/WebSocket if needed

This gives 80% of the value with manageable complexity.

**Total Estimated Effort:**
- Hosting Migration: 1-2 days (Railway/Render setup)
- Minimum (Near-Live): 2-3 days
- Full Implementation: 1-2 weeks
- Production-Ready: 2-3 weeks

**Cost Estimate:**
- Railway: $5-10/month (free tier usually sufficient)
- Render: $0-7/month (free tier with limitations)
- Fly.io: $0-5/month (generous free tier)
- **Total:** ~$5-10/month for live updates

---

## Next Steps

### Phase 0: Hosting Migration (CRITICAL - Do First!)

1. **Choose Hosting Platform:**
   - ✅ Railway (recommended - already configured)
   - ✅ Render (alternative - already configured)
   - Fly.io (best for production)

2. **Deploy Backend:**
   - Push code to Railway/Render
   - Configure environment variables
   - Test API endpoints
   - Update frontend `API_BASE` URL

3. **Verify Setup:**
   - Backend runs 24/7
   - API responds correctly
   - Frontend can connect
   - Logs are accessible

### Phase 1: Implementation

1. **Proof of Concept:** Test ESPN API for live game status
2. **Architecture Decision:** File-based vs in-memory state
3. **Polling Strategy:** Decide on frequency and conditions
4. **UI Design:** Design live score components
5. **Testing:** Test with actual live games

---

## Questions to Answer

1. **How important is true real-time?** (10s updates vs 30s updates)
2. **Which games matter most?** (All games or just certain teams?)
3. **Budget for API costs?** (Free tier vs paid ESPN API)
4. **Infrastructure preference?** (Keep simple or invest in SSE/WebSocket?)
5. **User expectations?** (Do users want live updates or is near-live sufficient?)

