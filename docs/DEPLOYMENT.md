# Deployment Guide

## Architecture Overview

This project uses a **split deployment** strategy:

- **Railway**: Backend API (Flask) - Handles data fetching from sports APIs
- **Vercel**: Frontend (React) - Displays the dashboard UI

```
┌─────────────┐         HTTP Requests          ┌──────────────┐
│   Vercel    │ ────────────────────────────> │   Railway    │
│  (Frontend) │                                │   (Backend)  │
│   React     │ <──────────────────────────── │   Flask API  │
└─────────────┘         JSON Responses        └──────────────┘
                                                      │
                                                      │ Fetches data
                                                      ▼
                                            ┌─────────────────┐
                                            │  Sports APIs    │
                                            │  (ESPN, NBA,    │
                                            │   F1, etc.)     │
                                            └─────────────────┘
```

## Railway Backend Setup

### 1. Deploy to Railway

1. Connect your GitHub repo to Railway
2. Railway will auto-detect the `nixpacks.toml` configuration
3. The backend will be deployed at: `https://your-app-name.up.railway.app`

### 2. Verify Backend is Running

Test the health endpoint:
```bash
curl https://your-app-name.up.railway.app/api/health
```

Should return:
```json
{"status": "healthy", "timestamp": "2024-..."}
```

### 3. Backend Configuration Files

- `nixpacks.toml` - Railway build configuration
- `railway.json` - Railway deployment settings
- `requirements.txt` - Python dependencies (must include Flask, gunicorn)
- `backend/app.py` - Flask application

## Vercel Frontend Setup

### 1. Deploy to Vercel

1. Connect your GitHub repo to Vercel
2. Configure build settings:
   - **Root Directory**: Leave empty (or set to project root)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `cd frontend && npm install`

### 2. Set Environment Variable

In Vercel dashboard, go to your project → Settings → Environment Variables:

- **Key**: `VITE_API_URL`
- **Value**: Your Railway backend URL (e.g., `https://depression-dashboard-production.up.railway.app`)
- **Environment**: Production, Preview, Development (all)

### 3. Redeploy

After setting the environment variable, trigger a new deployment so the frontend can connect to your Railway backend.

### 4. Frontend Configuration Files

- `vercel.json` - Vercel deployment configuration
- `frontend/package.json` - Frontend dependencies
- `frontend/vite.config.ts` - Vite build configuration
- `frontend/src/api.ts` - API client (points to Railway backend)

## How It Works

1. **User visits Vercel frontend** → React app loads
2. **Frontend makes API calls** → Requests go to Railway backend URL
3. **Railway backend processes** → Fetches data from sports APIs, calculates depression scores
4. **Backend returns JSON** → Frontend receives data and displays it
5. **Auto-refresh** → Frontend polls backend every 60 seconds

## API Endpoints (Railway Backend)

All endpoints are prefixed with `/api`:

- `GET /api/health` - Health check
- `GET /api/depression` - Get current depression score
- `GET /api/teams` - Get all team data
- `GET /api/recent-games` - Get recent games timeline
- `GET /api/upcoming-events` - Get upcoming events
- `POST /api/refresh` - Trigger data refresh

## CORS Configuration

The Railway backend has CORS enabled to allow requests from the Vercel frontend:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Allows all origins
```

## Troubleshooting

### Frontend can't connect to backend

1. **Check Railway backend is running**:
   ```bash
   curl https://your-railway-url.up.railway.app/api/health
   ```

2. **Check Vercel environment variable**:
   - Go to Vercel dashboard → Settings → Environment Variables
   - Verify `VITE_API_URL` is set correctly
   - Make sure it includes `https://` (not `http://`)
   - No trailing slash

3. **Check browser console**:
   - Open browser DevTools (F12)
   - Look for CORS errors or network failures
   - Check the Network tab to see if requests are being made

### Backend not starting on Railway

1. **Check Railway logs**:
   - Go to Railway dashboard → Your service → Deployments → View logs
   - Look for import errors or missing dependencies

2. **Verify requirements.txt**:
   - Must include: `flask`, `flask-cors`, `gunicorn`
   - All sports API dependencies should be listed

3. **Check module path**:
   - Railway should use: `backend.app:app`
   - Not: `app:app` (this won't work)

### Data not updating

1. **Check if teams_config.json exists**:
   - Should be in project root
   - Railway needs access to this file

2. **Manual refresh**:
   - Use the "Refresh Data" button in the frontend
   - Or call: `POST /api/refresh` directly

## Local Development

### Backend (Railway equivalent)
```bash
# Install dependencies first
pip install -r requirements.txt

# Option 1: Use start script (easiest)
./scripts/start_backend.sh

# Option 2: Run directly
cd backend
python3 app.py
# Runs on http://localhost:5001
```

### Frontend (Vercel equivalent)
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
# Automatically proxies /api requests to localhost:5001
```

The frontend's `vite.config.ts` has a proxy configured for local development.

## Summary

- ✅ **Railway**: Backend API (Flask + gunicorn)
- ✅ **Vercel**: Frontend (React + Vite)
- ✅ **CORS**: Enabled on backend
- ✅ **Environment Variable**: `VITE_API_URL` in Vercel points to Railway
- ✅ **No serverless functions needed**: All API logic is in Railway backend

