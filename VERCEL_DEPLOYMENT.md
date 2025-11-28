# Vercel Deployment Guide

## Current Setup

You've connected Vercel to this repository. Here's what you need to know:

### ✅ What Works on Vercel
- **Frontend** (React/Vite app in `frontend/` folder) - ✅ Will work perfectly
- Vercel will automatically detect and deploy the frontend

### ❌ What Doesn't Work on Vercel
- **Backend** (Flask server in `backend/` folder) - ❌ Won't work
- Vercel doesn't support long-running Flask servers
- Vercel is for serverless functions, not persistent backend services

## Solution: Deploy Backend Separately

You have two options:

### Option 1: Deploy Backend to Railway/Render (Recommended)

1. **Deploy Backend to Railway** (easiest):
   - Go to https://railway.app
   - Create new project from GitHub repo
   - Railway will auto-detect the Flask app
   - It will deploy from the `backend/` folder
   - Railway will give you a URL like: `https://your-app.railway.app`

2. **Configure Frontend to Use Backend**:
   - In Vercel dashboard, go to your project
   - Go to Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend-url.railway.app`
   - Redeploy the frontend

3. **That's it!** The frontend will now call your backend API.

### Option 2: Convert to Vercel Serverless Functions

This is more work but keeps everything on Vercel. You'd need to:
- Convert each Flask endpoint to a Vercel serverless function
- Put them in the `api/` folder (you already have a start with `api/depression.py`)
- Update the function signatures to match Vercel's Python runtime format

## Quick Setup Steps (Option 1 - Recommended)

1. **Deploy Backend**:
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login and deploy
   railway login
   railway init
   railway up
   ```

2. **Get Backend URL**:
   - Railway will show you the URL in the dashboard
   - Copy it (e.g., `https://depression-dashboard-backend.railway.app`)

3. **Configure Vercel**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add: `VITE_API_URL` = `https://your-backend-url.railway.app`
   - **Important**: Don't include `/api` in the URL - the frontend adds that automatically

4. **Redeploy Frontend**:
   - In Vercel, go to Deployments
   - Click "Redeploy" on the latest deployment
   - Or push a new commit to trigger a redeploy

## Testing

After deployment:
1. Visit your Vercel frontend URL
2. Open browser DevTools (F12) → Network tab
3. Check if API calls are going to your backend URL
4. If you see CORS errors, make sure `flask-cors` is installed in your backend

## Troubleshooting

### Frontend shows "Failed to load depression data"
- Check that `VITE_API_URL` is set correctly in Vercel
- Make sure backend is running and accessible
- Check browser console for CORS errors

### CORS Errors
- Backend already has `CORS(app)` configured
- Make sure `flask-cors` is in `requirements.txt`
- Verify backend is accessible from browser

### Backend Not Starting on Railway
- Check Railway logs
- Make sure `requirements.txt` includes all dependencies
- Verify `Procfile` or `railway.json` has correct start command

## Current Configuration

- **Frontend**: Configured in `vercel.json` to build from `frontend/` folder
- **Backend**: Needs separate deployment (Railway/Render recommended)
- **API Connection**: Frontend uses `VITE_API_URL` environment variable

The `vercel.json` file is already configured to:
- Build the frontend from the `frontend/` directory
- Serve the built files from `frontend/dist/`
- Handle React Router (SPA routing)

