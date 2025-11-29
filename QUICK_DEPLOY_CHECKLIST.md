# Quick Deployment Checklist

## ✅ All Changes Verified - Ready to Deploy!

### Railway Backend ✅
- [x] `nixpacks.toml` - Correct module path: `backend.app:app`
- [x] `railway.json` - Matches nixpacks.toml
- [x] `Procfile` - Correct for Railway
- [x] `requirements.txt` - Includes Flask, flask-cors, gunicorn, all sports APIs
- [x] `backend/app.py` - All routes have `/api` prefix
- [x] CORS enabled - Allows Vercel frontend
- [x] File paths correct - `teams_config.json` in root, `src/` imports work

### Vercel Frontend ✅
- [x] `vercel.json` - Frontend-only deployment
- [x] `frontend/src/api.ts` - Points to Railway backend
- [x] All API calls include `/api` prefix
- [x] Uses `VITE_API_URL` environment variable

### API Endpoints Match ✅
- [x] `/api/health` - Health check
- [x] `/api/depression` - Depression score
- [x] `/api/teams` - Team data
- [x] `/api/recent-games` - Recent games
- [x] `/api/upcoming-events` - Upcoming events
- [x] `/api/refresh` - Refresh data (POST)

### Response Formats Match ✅
- [x] All responses include `success`, `timestamp`
- [x] Depression response: `score`, `level`, `emoji`, `breakdown`
- [x] Teams response: `teams` array
- [x] Games response: `games` array
- [x] Events response: `events` array

## 🚀 Deployment Steps

### 1. Deploy Railway Backend
```bash
# Just push to GitHub - Railway auto-deploys
git add .
git commit -m "Fix deployment configuration"
git push
```

**After deployment:**
- Get your Railway URL: `https://your-app-name.up.railway.app`
- Test: `curl https://your-app-name.up.railway.app/api/health`

### 2. Deploy Vercel Frontend

1. **Connect to Vercel:**
   - Go to vercel.com
   - Import your GitHub repository
   - Vercel will auto-detect `vercel.json`

2. **Set Environment Variable:**
   - Go to: Project → Settings → Environment Variables
   - Add:
     - **Key:** `VITE_API_URL`
     - **Value:** `https://your-app-name.up.railway.app` (your Railway URL)
     - **Environments:** Production, Preview, Development
   - ⚠️ **No trailing slash!**
   - ⚠️ **Must include `https://`**

3. **Deploy:**
   - Vercel will auto-deploy on push
   - Or click "Redeploy" after setting env var

### 3. Verify Deployment

**Test Railway:**
```bash
curl https://your-railway-url.up.railway.app/api/health
# Should return: {"status": "healthy", ...}
```

**Test Vercel:**
- Visit your Vercel URL
- Open DevTools (F12) → Network tab
- Check API calls are going to Railway
- Verify data loads correctly

## 🔍 Troubleshooting

### Frontend shows "Failed to fetch"
1. Check `VITE_API_URL` is set in Vercel
2. Verify Railway backend is running
3. Check browser console for CORS errors
4. Verify Railway URL is correct (no trailing slash)

### Backend returns 500 errors
1. Check Railway logs
2. Verify `teams_config.json` exists
3. Check all dependencies installed
4. Verify `src/` directory structure

### CORS errors
- CORS is enabled in `backend/app.py`
- If issues persist, check Railway logs
- Verify frontend URL is making requests correctly

## 📝 Files Changed Summary

### Modified Files:
1. `nixpacks.toml` - Fixed module path
2. `railway.json` - Fixed start command
3. `Procfile` - Fixed module path
4. `requirements.txt` - Added Flask, gunicorn, sports APIs
5. `frontend/src/api.ts` - Points to Railway backend
6. `vercel.json` - Frontend-only deployment

### Created Files:
1. `docs/DEPLOYMENT.md` - Full deployment guide
2. `DEPLOYMENT_VERIFICATION.md` - Detailed verification
3. `QUICK_DEPLOY_CHECKLIST.md` - This file

## ✅ Everything is Ready!

All configurations are correct. The data flow is:
1. User visits Vercel frontend
2. Frontend makes API calls to Railway backend
3. Railway backend fetches from sports APIs
4. Backend returns JSON to frontend
5. Frontend displays the dashboard

**Just deploy and set the `VITE_API_URL` environment variable in Vercel!**

