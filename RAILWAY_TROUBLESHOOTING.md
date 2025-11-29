# Railway Troubleshooting Guide

## Issue: "Application failed to respond"

This error means Railway can't start your app. Here's how to fix it:

## ✅ Fixed Issues

1. **Module Path** - Fixed in all config files:
   - ✅ Root `nixpacks.toml`: `backend.app:app`
   - ✅ `backend/nixpacks.toml`: `backend.app:app` (just fixed)
   - ✅ `railway.json`: `backend.app:app`
   - ✅ `Procfile`: `backend.app:app`

## 🔍 Check Railway Logs

1. Go to Railway Dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Check the "Logs" tab

Look for errors like:
- `ModuleNotFoundError: No module named 'app'` → Module path issue
- `ModuleNotFoundError: No module named 'flask'` → Missing dependencies
- `FileNotFoundError: teams_config.json` → Missing config file
- Import errors → Missing Python packages

## 🛠️ Common Fixes

### 1. Force Railway to Use Root nixpacks.toml

Railway might be using `backend/nixpacks.toml` instead of root. Options:

**Option A: Delete backend/nixpacks.toml** (Recommended)
```bash
# Railway will use root nixpacks.toml
rm backend/nixpacks.toml
```

**Option B: Ensure both are correct** (Already done)
- Both files now have `backend.app:app`

### 2. Check Working Directory

Railway should run from project root. Verify in Railway:
- Settings → Service Settings
- Check "Working Directory" (should be empty or `/`)

### 3. Verify Dependencies

Check Railway build logs for:
```
ERROR: Could not find a version that satisfies the requirement
```

If you see this, the dependency might not be available. Check `requirements.txt`:
- ✅ flask>=3.0.0
- ✅ flask-cors>=4.0.0
- ✅ gunicorn>=21.2.0
- ✅ All sports APIs listed

### 4. Check File Structure

Railway needs these files in the root:
- ✅ `requirements.txt` (with all dependencies)
- ✅ `nixpacks.toml` (or `railway.json`)
- ✅ `teams_config.json`
- ✅ `backend/app.py`
- ✅ `src/` directory with Python modules

### 5. Test Locally First

Before deploying, test locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Test import
python3 -c "from backend.app import app; print('✅ Import works')"

# Test running
cd backend
python3 app.py
# Should start on http://localhost:5001
```

## 📋 Railway Configuration Priority

Railway uses configuration in this order:
1. `railway.json` → `deploy.startCommand` (highest priority)
2. `nixpacks.toml` → `[start]` cmd
3. `Procfile` → web command
4. Auto-detection

**Current setup:**
- `railway.json` has: `gunicorn --bind 0.0.0.0:$PORT backend.app:app` ✅
- `nixpacks.toml` has: `/opt/venv/bin/gunicorn --bind 0.0.0.0:$PORT backend.app:app` ✅
- Both are correct!

## 🚨 If Still Not Working

### Step 1: Check Railway Logs
- Look for the exact error message
- Check if gunicorn is starting
- Check if the module is being imported

### Step 2: Try Explicit Start Command
In Railway dashboard:
- Go to Settings → Service Settings
- Set "Start Command" to: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`
- This overrides all config files

### Step 3: Verify Build Success
Check Railway build logs:
- Should see: "Installing dependencies from requirements.txt"
- Should see: "Successfully installed flask flask-cors gunicorn..."
- Should NOT see: "ERROR" or "FAILED"

### Step 4: Check Port Binding
Railway sets `$PORT` automatically. The command should be:
```bash
gunicorn --bind 0.0.0.0:$PORT backend.app:app
```

NOT:
```bash
gunicorn --bind 0.0.0.0:5001 backend.app:app  # ❌ Wrong port
```

## 🔄 Redeploy After Fixes

After making changes:
1. Commit and push to GitHub
2. Railway will auto-deploy
3. Or manually trigger redeploy in Railway dashboard
4. Watch the logs in real-time

## ✅ Verification Checklist

- [ ] All config files have `backend.app:app`
- [ ] `requirements.txt` has Flask, flask-cors, gunicorn
- [ ] `teams_config.json` exists in root
- [ ] Railway logs show successful build
- [ ] Railway logs show gunicorn starting
- [ ] No import errors in logs
- [ ] Port is `$PORT` not hardcoded

## 📞 Still Having Issues?

Share these from Railway logs:
1. Build logs (installation phase)
2. Runtime logs (startup phase)
3. Any error messages
4. The exact command Railway is using to start

