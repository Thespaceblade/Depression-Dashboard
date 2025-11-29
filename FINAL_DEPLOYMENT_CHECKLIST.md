# Final Deployment Checklist - Get Everything Working on Vercel

This is your complete step-by-step guide to get your Depression Dashboard fully working on Vercel with Railway backend.

---

## 📋 Pre-Deployment Checklist

### ✅ Verify Local Setup
- [✅] **Code is committed to GitHub**
  ```bash
  git status  # Check for uncommitted changes
  git add .
  git commit -m "Ready for deployment"
  git push origin main
  ```

- [✅] **Verify `teams_config.json` exists** (should be in root directory)
  ```bash
  ls teams_config.json  # Should exist
  ```

- [ ] **Test backend locally** (optional but recommended)
  ```bash
  # First, install Python dependencies
  pip install -r requirements.txt
  
  # Option 1: Use the start script (easiest)
  ./scripts/start_backend.sh
  
  # Option 2: Run directly
  cd backend
  python3 app.py
  
  # Backend will run on http://localhost:5001
  # Visit http://localhost:5001/api/health
  # Should return: {"status": "healthy", ...}
  ```
  
  **Note:** The backend is a Python Flask app, NOT Node.js. Use `python3` or `pip`, not `npm`.

- [ ] **Test frontend locally** (optional but recommended)
  ```bash
  cd frontend
  npm install
  npm run dev
  # Visit http://localhost:5173
  # Should show dashboard (may not have data if backend not running)
  ```

---

## 🚂 Step 1: Deploy Backend to Railway

### 1.1 Connect Railway to GitHub
- [ ] Go to [railway.app](https://railway.app)
- [ ] Sign up/Login (use GitHub OAuth)
- [ ] Click **"New Project"**
- [ ] Select **"Deploy from GitHub repo"**
- [ ] Choose your **Depression-Dashboard** repository
- [ ] Railway will auto-detect it's a Python project

### 1.2 Configure Railway Service
- [ ] Railway should auto-detect:
  - ✅ Root directory: `.` (root)
  - ✅ Build command: Auto-detected from `nixpacks.toml`
  - ✅ Start command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`

- [ ] **Verify settings match:**
  - Build command: Should use `nixpacks.toml` (auto-detected)
  - Start command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`
  - Port: Auto-set via `$PORT` environment variable

### 1.3 Add Required Files to Railway
- [ ] **Verify these files exist in your repo:**
  - ✅ `backend/nixpacks.toml` (Railway build config)
  - ✅ `railway.json` (Railway deployment config)
  - ✅ `requirements.txt` (Python dependencies - in root)
  - ✅ `backend/requirements.txt` (Backend-specific dependencies)
  - ✅ `teams_config.json` (Data file - in root)

### 1.4 Deploy and Get URL
- [ ] Click **"Deploy"** (or Railway auto-deploys on push)
- [ ] Wait for build to complete (2-5 minutes)
- [ ] **Copy your Railway URL** from the service settings
  - Format: `https://your-app-name.up.railway.app`
  - Example: `https://depression-dashboard-production.up.railway.app`
  - ⚠️ **Save this URL - you'll need it for Vercel!**

### 1.5 Test Railway Backend
- [ ] **Test health endpoint:**
  ```bash
  curl https://your-railway-url.up.railway.app/api/health
  ```
  - Should return: `{"status": "healthy", "timestamp": "..."}`

- [ ] **Test depression endpoint:**
  ```bash
  curl https://your-railway-url.up.railway.app/api/depression
  ```
  - Should return JSON with depression score

- [ ] **Check Railway logs** if errors:
  - Go to Railway dashboard → Your service → **Logs** tab
  - Look for any error messages

### 1.6 Fix Common Railway Issues (if needed)
- [ ] **If build fails:**
  - Check `backend/nixpacks.toml` exists
  - Check `requirements.txt` has all dependencies
  - Check Railway logs for specific error

- [ ] **If app crashes:**
  - Check `teams_config.json` exists in root
  - Check `backend/app.py` imports are correct
  - Check Railway logs for Python errors

- [ ] **If 500 errors:**
  - Check Railway logs
  - Verify `teams_config.json` is valid JSON
  - Check all Python dependencies installed

---

## 🎨 Step 2: Deploy Frontend to Vercel

### 2.1 Connect Vercel to GitHub
- [ ] Go to [vercel.com](https://vercel.com)
- [ ] Sign up/Login (use GitHub OAuth)
- [ ] Click **"Add New..."** → **"Project"**
- [ ] Find and select your **Depression-Dashboard** repository
- [ ] Click **"Import"**

### 2.2 Configure Vercel Project
- [ ] **Framework Preset:** Leave as **"Other"** (or blank)
- [ ] **Root Directory:** Leave as `.` (root)
- [ ] **Build Command:** 
  ```
  cd frontend && npm install && npm run build
  ```
- [ ] **Output Directory:** 
  ```
  frontend/dist
  ```
- [ ] **Install Command:** 
  ```
  cd frontend && npm install
  ```

### 2.3 Set Environment Variable (CRITICAL!)
- [ ] Go to **"Environment Variables"** section
- [ ] Click **"Add"**
- [ ] **Key:** `VITE_API_URL`
- [ ] **Value:** Your Railway backend URL (from Step 1.4)
  - Example: `https://depression-dashboard-production.up.railway.app`
  - ⚠️ **NO trailing slash!**
  - ⚠️ **Must include `https://`**
- [ ] **Environments:** Check all three:
  - ✅ Production
  - ✅ Preview
  - ✅ Development
- [ ] Click **"Save"**

### 2.4 Deploy Frontend
- [ ] Click **"Deploy"**
- [ ] Wait for build to complete (2-5 minutes)
- [ ] **Copy your Vercel URL**
  - Format: `https://your-project.vercel.app`
  - Example: `https://depression-dashboard.vercel.app`

### 2.5 Test Vercel Frontend
- [ ] **Visit your Vercel URL** in browser
- [ ] **Open DevTools** (F12) → **Network** tab
- [ ] **Check API calls:**
  - Should see requests to: `https://your-railway-url.up.railway.app/api/...`
  - Should return 200 status codes
  - Should see JSON responses

- [ ] **Verify dashboard displays:**
  - ✅ Depression score card
  - ✅ Teams list
  - ✅ Recent games timeline
  - ✅ Upcoming events

### 2.6 Fix Common Vercel Issues (if needed)
- [ ] **If build fails:**
  - Check `frontend/package.json` exists
  - Check `vercel.json` configuration
  - Check Vercel build logs

- [ ] **If "Failed to fetch" errors:**
  - ✅ Verify `VITE_API_URL` is set in Vercel
  - ✅ Verify Railway backend is running
  - ✅ Check browser console for CORS errors
  - ✅ Verify Railway URL is correct (no trailing slash)

- [ ] **If CORS errors:**
  - Check `backend/app.py` has `CORS(app)` enabled
  - Check Railway logs for CORS-related errors

- [ ] **If data doesn't load:**
  - Check browser console for errors
  - Check Network tab for failed API calls
  - Verify Railway backend endpoints work (test with curl)

---

## 🔄 Step 3: Set Up Automatic Data Updates (Optional but Recommended)

### 3.1 Option A: GitHub Actions (Recommended)
- [ ] **Check if `.github/workflows/auto-update-data.yml` exists**
  - If yes, it should auto-run on schedule
  - If no, you can skip this step

- [ ] **Verify GitHub Actions is enabled:**
  - Go to your GitHub repo → **Settings** → **Actions** → **General**
  - Ensure "Allow all actions and reusable workflows" is enabled

- [ ] **Test the workflow:**
  - Go to **Actions** tab in GitHub
  - Manually trigger the workflow
  - Check it completes successfully

### 3.2 Option B: Railway Cron Job (Alternative)
- [ ] **Create a cron service in Railway:**
  - Add new service → **Cron**
  - Schedule: `0 */6 * * *` (every 6 hours)
  - Command: `python scripts/fetch_all_data.py`

### 3.3 Option C: Manual Updates
- [ ] **You can manually trigger updates:**
  - Visit your Vercel site
  - Click "Refresh Data" button (if you have one)
  - Or manually run: `python scripts/fetch_all_data.py` locally and push

---

## ✅ Step 4: Final Verification

### 4.1 Test All Endpoints
- [ ] **Health Check:**
  ```bash
  curl https://your-railway-url.up.railway.app/api/health
  ```
  - Should return: `{"status": "healthy", ...}`

- [ ] **Depression Score:**
  ```bash
  curl https://your-railway-url.up.railway.app/api/depression
  ```
  - Should return JSON with score, level, emoji, breakdown

- [ ] **Teams:**
  ```bash
  curl https://your-railway-url.up.railway.app/api/teams
  ```
  - Should return JSON with teams array

- [ ] **Recent Games:**
  ```bash
  curl https://your-railway-url.up.railway.app/api/recent-games
  ```
  - Should return JSON with games array

- [ ] **Upcoming Events:**
  ```bash
  curl https://your-railway-url.up.railway.app/api/upcoming-events
  ```
  - Should return JSON with events array

### 4.2 Test Frontend Features
- [ ] **Visit Vercel URL**
- [ ] **Check all sections load:**
  - ✅ Depression score card (with emoji and level)
  - ✅ Teams section (all teams listed)
  - ✅ Recent games timeline (games displayed)
  - ✅ Upcoming events (events displayed)

- [ ] **Test refresh button** (if you have one):
  - Click "Refresh Data"
  - Should update data from APIs
  - Check Network tab for POST to `/api/refresh`

### 4.3 Check Browser Console
- [ ] **Open DevTools (F12)**
- [ ] **Check Console tab:**
  - Should have no errors
  - May have warnings (usually fine)

- [ ] **Check Network tab:**
  - All API calls should return 200 status
  - No CORS errors
  - No 404 or 500 errors

---

## 🎯 Step 5: Share Your Dashboard!

### 5.1 Get Your Final URLs
- [ ] **Frontend (Vercel):** `https://your-project.vercel.app`
- [ ] **Backend (Railway):** `https://your-app-name.up.railway.app`

### 5.2 Optional: Custom Domain
- [ ] **Add custom domain in Vercel:**
  - Go to Vercel project → **Settings** → **Domains**
  - Add your domain
  - Follow DNS instructions

### 5.3 Monitor Your Deployment
- [ ] **Set up monitoring:**
  - Railway: Check logs regularly
  - Vercel: Check deployment status
  - GitHub: Check Actions tab for auto-updates

---

## 🐛 Troubleshooting Guide

### Problem: Frontend shows "Failed to fetch"
**Solutions:**
1. ✅ Check `VITE_API_URL` is set in Vercel (Settings → Environment Variables)
2. ✅ Verify Railway backend is running (test with curl)
3. ✅ Check Railway URL is correct (no trailing slash, includes https://)
4. ✅ Check browser console for specific error message

### Problem: Backend returns 500 errors
**Solutions:**
1. ✅ Check Railway logs (Dashboard → Service → Logs)
2. ✅ Verify `teams_config.json` exists and is valid JSON
3. ✅ Check all Python dependencies installed (check `requirements.txt`)
4. ✅ Verify `src/` directory structure is correct

### Problem: CORS errors in browser
**Solutions:**
1. ✅ Verify `backend/app.py` has `CORS(app)` enabled
2. ✅ Check Railway logs for CORS-related errors
3. ✅ Verify frontend is making requests to correct Railway URL

### Problem: Data is outdated
**Solutions:**
1. ✅ Check if auto-update is configured (GitHub Actions or Railway Cron)
2. ✅ Manually trigger refresh: `POST /api/refresh` endpoint
3. ✅ Check GitHub Actions logs if using auto-update

### Problem: Build fails on Railway
**Solutions:**
1. ✅ Check `backend/nixpacks.toml` exists and is correct
2. ✅ Check `requirements.txt` has all dependencies
3. ✅ Check Railway logs for specific error
4. ✅ Verify Python version in `nixpacks.toml` (should be `python311`)

### Problem: Build fails on Vercel
**Solutions:**
1. ✅ Check `frontend/package.json` exists
2. ✅ Check `vercel.json` configuration is correct
3. ✅ Check Vercel build logs for specific error
4. ✅ Verify Node.js version (Vercel auto-detects)

---

## 📝 Quick Reference

### Railway Backend URL Format
```
https://your-app-name.up.railway.app
```

### Vercel Frontend URL Format
```
https://your-project.vercel.app
```

### Environment Variable (Vercel)
```
Key: VITE_API_URL
Value: https://your-railway-url.up.railway.app
(No trailing slash!)
```

### Test Commands
```bash
# Test Railway health
curl https://your-railway-url.up.railway.app/api/health

# Test Railway depression endpoint
curl https://your-railway-url.up.railway.app/api/depression

# Test Railway teams endpoint
curl https://your-railway-url.up.railway.app/api/teams
```

---

## ✅ Success Criteria

Your deployment is successful when:

- ✅ Railway backend responds to all API endpoints
- ✅ Vercel frontend loads without errors
- ✅ Dashboard displays depression score, teams, games, and events
- ✅ API calls from frontend to backend work (check Network tab)
- ✅ No CORS errors in browser console
- ✅ Data updates automatically (or can be manually refreshed)

---

## 🎉 You're Done!

Once all checkboxes are complete, your Depression Dashboard is fully deployed and working on Vercel!

**Your final product:**
- Frontend: `https://your-project.vercel.app` (Vercel)
- Backend: `https://your-app-name.up.railway.app` (Railway)
- Auto-updates: GitHub Actions or Railway Cron (if configured)

**Share your dashboard URL and enjoy!** 🚀

