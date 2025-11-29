# Deployment Verification Checklist

## ✅ Configuration Files Verified

### Railway Backend Configuration

1. **nixpacks.toml** ✅
   - Uses Python 3.11
   - Installs from root `requirements.txt`
   - Starts with: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`
   - ✅ Correct module path: `backend.app:app`

2. **railway.json** ✅
   - Uses NIXPACKS builder
   - Start command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`
   - ✅ Matches nixpacks.toml

3. **Procfile** ✅
   - Command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`
   - ✅ Correct for Railway/Heroku

4. **requirements.txt** ✅
   - ✅ Includes Flask (3.0.0+)
   - ✅ Includes flask-cors (4.0.0+)
   - ✅ Includes gunicorn (21.2.0+)
   - ✅ Includes all sports API dependencies

### Vercel Frontend Configuration

1. **vercel.json** ✅
   - Build command: `cd frontend && npm install && npm run build`
   - Output directory: `frontend/dist`
   - ✅ No serverless functions (frontend only)

2. **frontend/src/api.ts** ✅
   - ✅ Uses `VITE_API_URL` environment variable
   - ✅ Fallback to Railway URL
   - ✅ All endpoints include `/api` prefix:
     - `/api/depression` ✅
     - `/api/teams` ✅
     - `/api/recent-games` ✅
     - `/api/upcoming-events` ✅
     - `/api/refresh` ✅

## ✅ API Endpoints Verification

### Backend Routes (backend/app.py)
- ✅ `GET /api/health` - Health check
- ✅ `GET /api/depression` - Depression score
- ✅ `GET /api/teams` - Team data
- ✅ `GET /api/recent-games` - Recent games
- ✅ `GET /api/upcoming-events` - Upcoming events
- ✅ `POST /api/refresh` - Refresh data

### Frontend API Calls (frontend/src/api.ts)
- ✅ `fetchDepression()` → `${API_BASE}/api/depression`
- ✅ `fetchTeams()` → `${API_BASE}/api/teams`
- ✅ `fetchRecentGames()` → `${API_BASE}/api/recent-games`
- ✅ `fetchUpcomingEvents()` → `${API_BASE}/api/upcoming-events`
- ✅ `refreshData()` → `${API_BASE}/api/refresh` (POST)

**All endpoints match! ✅**

## ✅ CORS Configuration

- ✅ `backend/app.py` has `CORS(app)` enabled
- ✅ Allows all origins (frontend on Vercel can access)

## ✅ File Paths Verification

### Backend File Resolution
- ✅ `teams_config.json` path: `os.path.dirname(os.path.dirname(__file__))` → project root
- ✅ `src/` imports: `sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))` → project root
- ✅ Calculator loads from: `src.depression_calculator`

### Required Files
- ✅ `teams_config.json` exists in project root
- ✅ `src/depression_calculator.py` exists
- ✅ `src/sports_api.py` exists (if used)
- ✅ `backend/app.py` exists

## ✅ Response Format Verification

### DepressionData Response
```json
{
  "success": true,
  "score": 123.4,
  "level": "Severe",
  "emoji": "😭",
  "breakdown": {...},
  "timestamp": "2024-..."
}
```
✅ Matches TypeScript interface

### TeamsData Response
```json
{
  "success": true,
  "teams": [...],
  "timestamp": "2024-..."
}
```
✅ Matches TypeScript interface

### RecentGamesData Response
```json
{
  "success": true,
  "games": [...],
  "timestamp": "2024-..."
}
```
✅ Matches TypeScript interface

### UpcomingEventsData Response
```json
{
  "success": true,
  "events": [...],
  "timestamp": "2024-..."
}
```
✅ Matches TypeScript interface

## ⚠️ Required Environment Variables

### Vercel Environment Variables
**MUST SET IN VERCEL DASHBOARD:**

1. **VITE_API_URL**
   - Key: `VITE_API_URL`
   - Value: Your Railway backend URL
   - Example: `https://depression-dashboard-production.up.railway.app`
   - ⚠️ **No trailing slash**
   - ⚠️ **Must include `https://`**
   - Environment: Production, Preview, Development

### Railway Environment Variables
- ✅ `PORT` - Automatically set by Railway
- ✅ No additional env vars required (uses teams_config.json)

## 🧪 Testing Checklist

### Before Deployment

1. **Test Backend Locally:**
   ```bash
   # Install dependencies first
   pip install -r requirements.txt
   
   # Option 1: Use start script
   ./scripts/start_backend.sh
   
   # Option 2: Run directly
   cd backend
   python3 app.py
   # Test: curl http://localhost:5001/api/health
   ```

2. **Test Frontend Locally:**
   ```bash
   cd frontend
   npm install
   npm run dev
   # Should connect to localhost:5001 via proxy
   ```

### After Railway Deployment

1. **Test Health Endpoint:**
   ```bash
   curl https://your-railway-url.up.railway.app/api/health
   # Should return: {"status": "healthy", ...}
   ```

2. **Test Depression Endpoint:**
   ```bash
   curl https://your-railway-url.up.railway.app/api/depression
   # Should return depression data
   ```

3. **Test Teams Endpoint:**
   ```bash
   curl https://your-railway-url.up.railway.app/api/teams
   # Should return teams array
   ```

4. **Check CORS:**
   ```bash
   curl -H "Origin: https://your-vercel-url.vercel.app" \
        -H "Access-Control-Request-Method: GET" \
        -X OPTIONS \
        https://your-railway-url.up.railway.app/api/health
   # Should return CORS headers
   ```

### After Vercel Deployment

1. **Check Environment Variable:**
   - Go to Vercel Dashboard → Project → Settings → Environment Variables
   - Verify `VITE_API_URL` is set correctly

2. **Test Frontend:**
   - Visit your Vercel URL
   - Open browser DevTools (F12) → Network tab
   - Check if API calls are going to Railway backend
   - Verify responses are successful

3. **Check Console for Errors:**
   - Open browser DevTools → Console
   - Look for CORS errors or network failures

## 🐛 Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution:** ✅ Fixed - Using `backend.app:app` in all configs

### Issue: "Failed to fetch" in browser
**Possible Causes:**
1. ❌ `VITE_API_URL` not set in Vercel
2. ❌ Railway backend not running
3. ❌ CORS issue (check Network tab for CORS errors)
4. ❌ Wrong URL format (missing https:// or has trailing slash)

**Solution:**
- Verify Railway backend is accessible
- Check Vercel environment variable
- Check browser console for specific error

### Issue: "teams_config.json not found"
**Solution:** ✅ File path is correct - uses `os.path.dirname(os.path.dirname(__file__))` which resolves to project root

### Issue: Backend returns 500 errors
**Check:**
- Railway logs for Python errors
- Verify all dependencies installed
- Check if `teams_config.json` is accessible
- Verify `src/` directory structure

## 📋 Deployment Steps Summary

### Railway (Backend)
1. ✅ Connect GitHub repo to Railway
2. ✅ Railway auto-detects `nixpacks.toml`
3. ✅ Deploys automatically on push
4. ✅ Get Railway URL from dashboard

### Vercel (Frontend)
1. ✅ Connect GitHub repo to Vercel
2. ✅ Set `VITE_API_URL` environment variable to Railway URL
3. ✅ Vercel auto-detects `vercel.json`
4. ✅ Deploys automatically on push

## ✅ All Systems Ready!

All configurations verified. The deployment should work correctly when:
1. Railway backend is deployed and accessible
2. Vercel frontend has `VITE_API_URL` set
3. Both services are running

