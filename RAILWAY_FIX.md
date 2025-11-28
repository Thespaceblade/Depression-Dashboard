# Railway Deployment Fix

Railway is showing "No start command was found" because your Flask app is in the `backend/` folder, not the root.

## Quick Fix (Choose One)

### Option 1: Set Root Directory in Railway Dashboard (Easiest)

1. Go to your Railway project dashboard
2. Click on your service
3. Go to **Settings** tab
4. Scroll to **Source** section
5. Set **Root Directory** to: `backend`
6. Click **Save**
7. Railway will redeploy automatically

This tells Railway to treat the `backend/` folder as the project root, so it will find `app.py` there.

### Option 2: Use the Configuration Files (After Committing)

I've updated these files:
- ✅ `Procfile` - Has the start command
- ✅ `railway.json` - Has the start command
- ✅ `requirements.txt` - Now includes `gunicorn`

After you commit and push these changes:
1. Railway should automatically detect the start command
2. If not, go to Settings → Deploy and manually set:
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --chdir backend app:app`

### Option 3: Manual Start Command in Railway

1. Go to Railway dashboard → Your service → Settings
2. Find **Deploy** section
3. Set **Start Command** to:
   ```
   gunicorn --bind 0.0.0.0:$PORT --chdir backend app:app
   ```
4. Save and redeploy

## What Changed

- ✅ Added `gunicorn>=21.2.0` to `requirements.txt`
- ✅ Updated `Procfile` with gunicorn command
- ✅ Updated `railway.json` with start command
- ✅ Created `start.sh` script (backup option)

## Verify It's Working

After deployment, check:
1. Railway logs should show: "Starting gunicorn..."
2. Your service should show as "Active"
3. Click on the service to get the public URL
4. Test: `https://your-app.railway.app/api/health`

The health endpoint should return:
```json
{"status": "healthy", "timestamp": "..."}
```



