# Deployment Guide - Autonomous Hosting

This guide shows how to deploy the Depression Dashboard to run completely independently with automatic data fetching.

## Architecture Overview

```
┌─────────────────┐
│  Frontend       │  (Vercel/Netlify)
│  React App      │  → Static hosting
└────────┬────────┘
         │ API calls
         ↓
┌─────────────────┐
│  Backend API    │  (Railway/Render/Heroku)
│  Flask Server   │  → Runs 24/7
└────────┬────────┘
         │
         ├─→ Scheduled Tasks (cron)
         │   └─→ Auto-fetch data every 6 hours
         │
         └─→ Config Storage
             └─→ teams_config.json (in repo or cloud storage)
```

## Option 1: Railway (Recommended - Easiest)

Railway is great because it handles both backend and scheduled tasks easily.

### Backend Setup

1. **Create Railway Account**: https://railway.app

2. **Create New Project**:
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Initialize project
   railway init
   ```

3. **Create `railway.json`** (in project root):
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

4. **Create `Procfile`** (in project root):
   ```
   web: cd backend && python app.py
   ```

5. **Create `runtime.txt`** (in project root):
   ```
   python-3.11
   ```

6. **Environment Variables** (set in Railway dashboard):
   - `PORT=5001` (Railway will set this automatically)
   - `FLASK_ENV=production`
   - `PYTHONUNBUFFERED=1`

7. **Deploy**:
   ```bash
   railway up
   ```

### Scheduled Data Fetching

Railway supports cron jobs via their "Cron" service:

1. **Create `railway-cron.json`**:
   ```json
   {
     "crons": [
       {
         "name": "fetch-sports-data",
         "schedule": "0 */6 * * *",
         "command": "python scripts/fetch_all_data.py"
       }
     ]
   }
   ```

2. **Or use Railway's Cron Service**:
   - Add a new service in Railway dashboard
   - Set it to run: `python scripts/fetch_all_data.py`
   - Schedule: Every 6 hours (`0 */6 * * *`)

### Frontend Setup (Vercel)

1. **Create Vercel Account**: https://vercel.com

2. **Connect GitHub Repo**:
   - Import your repository
   - Set root directory: `frontend`
   - Build command: `npm run build`
   - Output directory: `dist`

3. **Environment Variables**:
   - `VITE_API_URL`: Your Railway backend URL (e.g., `https://your-app.railway.app`)

4. **Update `frontend/src/api.ts`**:
   ```typescript
   const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5001';
   ```

5. **Deploy**: Vercel will auto-deploy on git push

---

## Option 2: Render (Free Tier Available)

### Backend Setup

1. **Create Render Account**: https://render.com

2. **Create New Web Service**:
   - Connect GitHub repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `cd backend && python app.py`
   - Environment: Python 3
   - Plan: Free (or paid for better performance)

3. **Environment Variables**:
   - `PORT=5001`
   - `PYTHON_VERSION=3.11`

4. **Create `render.yaml`** (in project root):
   ```yaml
   services:
     - type: web
       name: depression-dashboard-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: cd backend && python app.py
       envVars:
         - key: PORT
           value: 5001
         - key: FLASK_ENV
           value: production
   
     - type: cron
       name: fetch-sports-data
       schedule: "0 */6 * * *"
       buildCommand: pip install -r requirements.txt
       startCommand: python scripts/fetch_all_data.py
   ```

### Frontend Setup (Netlify)

1. **Create Netlify Account**: https://netlify.com

2. **Deploy**:
   - Connect GitHub repo
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`

3. **Environment Variables**:
   - `VITE_API_URL`: Your Render backend URL

---

## Option 3: Heroku (Classic, but requires credit card)

### Backend Setup

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Create `Procfile`**:
   ```
   web: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT
   ```

3. **Create `runtime.txt`**:
   ```
   python-3.11.0
   ```

4. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

5. **Add Heroku Scheduler** (for cron):
   - Install addon: `heroku addons:create scheduler:standard`
   - Set command: `python scripts/fetch_all_data.py`
   - Schedule: Every 6 hours

---

## Option 4: Self-Hosted (VPS/DigitalOcean)

### Setup on Ubuntu VPS

1. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

2. **Clone Repo**:
   ```bash
   git clone <your-repo-url>
   cd Depression-Dashboard
   ```

3. **Setup Python Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Create Systemd Service** (`/etc/systemd/system/depression-api.service`):
   ```ini
   [Unit]
   Description=Depression Dashboard API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/Depression-Dashboard
   Environment="PATH=/path/to/Depression-Dashboard/venv/bin"
   ExecStart=/path/to/Depression-Dashboard/venv/bin/gunicorn --bind 0.0.0.0:5001 --chdir backend app:app

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start Service**:
   ```bash
   sudo systemctl start depression-api
   sudo systemctl enable depression-api
   ```

6. **Setup Nginx** (`/etc/nginx/sites-available/depression-dashboard`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location /api {
           proxy_pass http://localhost:5001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location / {
           root /path/to/Depression-Dashboard/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
   }
   ```

7. **Setup Cron for Data Fetching**:
   ```bash
   crontab -e
   # Add:
   0 */6 * * * cd /path/to/Depression-Dashboard && /path/to/venv/bin/python scripts/fetch_all_data.py
   ```

---

## Making It Fully Autonomous

### 1. Automated Data Fetching Script

Create `scripts/fetch_all_data.py` (if it doesn't exist):

```python
#!/usr/bin/env python3
"""
Automated data fetching script
Runs on schedule to update teams_config.json
"""

import sys
import os
from src.sports_api import SportsDataFetcher

def main():
    config_path = os.path.join(os.path.dirname(__file__), "teams_config.json")
    fetcher = SportsDataFetcher()
    
    print("🔄 Fetching latest sports data...")
    fetcher.update_config_file(config_path)
    print("✅ Data fetch complete!")

if __name__ == "__main__":
    main()
```

### 2. Config File Storage

**Option A: Store in Git** (simplest)
- Commit `teams_config.json` to repo
- Cron job updates it and commits
- Auto-deploys trigger on commit

**Option B: Cloud Storage** (better for production)
- Use S3, Google Cloud Storage, or similar
- Script reads/writes to cloud storage
- No git commits needed

**Option C: Database** (most robust)
- Store config in PostgreSQL/MySQL
- API reads from database
- Cron updates database

### 3. Git Auto-Commit (if using Option A)

Create `.github/workflows/auto-update.yml`:

```yaml
name: Auto Update Data

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Fetch data
        run: python scripts/fetch_all_data.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add teams_config.json
          git diff --staged --quiet || git commit -m "Auto-update: $(date +'%Y-%m-%d %H:%M:%S')"
          git push
```

### 4. Environment Variables

Create `.env.example`:

```bash
# Backend
PORT=5001
FLASK_ENV=production
PYTHONUNBUFFERED=1

# Frontend
VITE_API_URL=https://your-backend-url.com
```

---

## Recommended Setup (Easiest Path)

### Step 1: Backend on Railway
1. Push code to GitHub
2. Connect Railway to GitHub
3. Railway auto-detects Python and deploys
4. Add cron service for data fetching

### Step 2: Frontend on Vercel
1. Connect Vercel to GitHub
2. Set root to `frontend/`
3. Add environment variable: `VITE_API_URL`
4. Deploy

### Step 3: Automated Updates
1. Use Railway cron to run `scripts/fetch_all_data.py` every 6 hours
2. Config file updates automatically
3. Backend reloads config on next request

---

## Testing Deployment

### Test Backend
```bash
curl https://your-backend-url.com/api/health
curl https://your-backend-url.com/api/depression
```

### Test Frontend
- Visit your frontend URL
- Check browser console for errors
- Verify API calls are working

### Test Auto-Fetch
- Check Railway/Render logs for cron job execution
- Verify `teams_config.json` is being updated
- Check timestamps in logs

---

## Monitoring & Maintenance

### Health Checks
- Backend should respond to `/api/health`
- Set up uptime monitoring (UptimeRobot, Pingdom)
- Monitor error logs

### Logs
- Railway: View logs in dashboard
- Render: View logs in dashboard
- Vercel: View logs in dashboard

### Alerts
- Set up email alerts for deployment failures
- Monitor API response times
- Check data freshness (last update timestamp)

---

## Cost Estimates

### Free Tier Options:
- **Railway**: $5/month free credit (enough for small app)
- **Render**: Free tier available (with limitations)
- **Vercel**: Free tier (generous)
- **Netlify**: Free tier (generous)

### Paid Options:
- **Railway**: ~$5-20/month
- **Render**: ~$7-25/month
- **Heroku**: ~$7-25/month
- **VPS (DigitalOcean)**: ~$6-12/month

---

## Troubleshooting

### Backend won't start
- Check logs for errors
- Verify all dependencies in `requirements.txt`
- Check environment variables

### Data not updating
- Verify cron job is running
- Check cron logs
- Verify `scripts/fetch_all_data.py` has execute permissions

### Frontend can't reach backend
- Check CORS settings
- Verify `VITE_API_URL` is set correctly
- Check backend is running

### Config file not updating
- Check file permissions
- Verify cron job has write access
- Check disk space

---

## Next Steps

1. Choose your hosting platform
2. Set up backend deployment
3. Set up frontend deployment
4. Configure automated data fetching
5. Test everything
6. Set up monitoring

Your dashboard will now run completely independently! 🚀





