# Autonomous Deployment Setup

This document explains how your Depression Dashboard runs completely independently with automatic data fetching.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS SYSTEM                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Backend API (Railway/Render)                            │
│     └─> Runs 24/7, serves data to frontend                  │
│                                                               │
│  2. Cron Job (Scheduled Task)                                │
│     └─> Runs every 6 hours                                  │
│     └─> Executes: python fetch_all_data.py                  │
│     └─> Updates: teams_config.json                          │
│                                                               │
│  3. Frontend (Vercel/Netlify)                                │
│     └─> Static site, calls backend API                      │
│     └─> Auto-refreshes every 60 seconds                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Key Files Created

### Deployment Configuration
- `Procfile` - Heroku/Railway process definition
- `runtime.txt` - Python version specification
- `railway.json` - Railway-specific config
- `render.yaml` - Render.com deployment config

### Automation
- `fetch_all_data.py` - Automated data fetching script
- `.github/workflows/auto-update-data.yml` - GitHub Actions workflow (optional)

### Documentation
- `DEPLOYMENT_GUIDE.md` - Complete deployment instructions
- `QUICK_DEPLOY.md` - Fast deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-flight checklist

## Deployment Options

### Option 1: Railway + Vercel (Recommended - Easiest)

**Backend (Railway):**
- Free tier: $5/month credit
- Auto-detects Python
- Built-in cron jobs
- Easy GitHub integration

**Frontend (Vercel):**
- Free tier available
- Auto-deploys on push
- Fast CDN
- Easy environment variables

**Setup Time:** ~10 minutes

### Option 2: Render (All-in-One)

**Both Backend & Cron:**
- Free tier available
- Single `render.yaml` config
- Handles everything

**Frontend:**
- Deploy separately on Netlify/Vercel

**Setup Time:** ~15 minutes

### Option 3: Self-Hosted VPS

**Full Control:**
- DigitalOcean, Linode, etc.
- ~$6-12/month
- Complete control
- Requires server management

**Setup Time:** ~30 minutes

## Automated Data Fetching

### How It Works

1. **Cron Job** runs every 6 hours
2. Executes `fetch_all_data.py`
3. Script fetches data from all sports APIs:
   - NFL (Cowboys)
   - NBA (Mavericks, Warriors)
   - MLB (Rangers)
   - F1 (Verstappen)
   - NCAA (UNC Basketball & Football)
4. Updates `teams_config.json` with latest data
5. Backend automatically uses updated config

### Schedule Options

- **Every 6 hours**: `0 */6 * * *` (recommended)
- **Every 3 hours**: `0 */3 * * *`
- **Every hour**: `0 * * * *`
- **Twice daily**: `0 6,18 * * *` (6 AM & 6 PM)

### Manual Trigger

You can also trigger updates manually:
- Railway: Click "Run" on cron job
- Render: Trigger cron job manually
- GitHub Actions: Use "workflow_dispatch"

## Environment Variables

### Backend
```bash
PORT=5001                    # Usually auto-set by platform
FLASK_ENV=production         # Production mode
PYTHONUNBUFFERED=1          # Better logging
```

### Frontend
```bash
VITE_API_URL=https://your-backend-url.com
```

## Data Storage

### Option A: Git-Based (Simplest)
- `teams_config.json` committed to repo
- Cron job updates and commits
- Auto-deploys trigger on commit
- **Pros**: Simple, versioned
- **Cons**: Git history gets cluttered

### Option B: Cloud Storage (Better)
- Store config in S3/Google Cloud Storage
- Script reads/writes to cloud
- **Pros**: Clean git history
- **Cons**: Requires cloud storage setup

### Option C: Database (Most Robust)
- Store in PostgreSQL/MySQL
- API reads from database
- **Pros**: Scalable, queryable
- **Cons**: More complex setup

**Current Setup:** Uses Option A (Git-based)

## Monitoring

### What to Monitor

1. **Backend Health**
   - Endpoint: `/api/health`
   - Should return: `{"status": "healthy"}`

2. **Data Freshness**
   - Check last update timestamp
   - Should update every 6 hours

3. **Cron Job Execution**
   - Check logs for successful runs
   - Should see "✅ Data fetch complete!"

4. **API Response Times**
   - Should be < 1 second
   - Monitor for slowdowns

### Tools

- **UptimeRobot**: Free uptime monitoring
- **Pingdom**: Advanced monitoring
- **Platform Logs**: Railway/Render/Vercel dashboards

## Troubleshooting

### Data Not Updating

**Check:**
1. Cron job is running (check logs)
2. `fetch_all_data.py` executes successfully
3. `teams_config.json` has write permissions
4. APIs are accessible (no rate limits)

**Fix:**
- Check cron job logs
- Test `fetch_all_data.py` manually
- Verify API keys/credentials if needed

### Backend Not Starting

**Check:**
1. All dependencies installed
2. Environment variables set
3. Port is correct
4. `teams_config.json` exists

**Fix:**
- Check deployment logs
- Verify `requirements.txt`
- Test locally first

### Frontend Can't Reach Backend

**Check:**
1. `VITE_API_URL` is set correctly
2. Backend is running
3. CORS is enabled
4. No firewall blocking

**Fix:**
- Verify environment variable
- Check backend logs
- Test backend directly with curl

## Cost Breakdown

### Free Tier (Recommended)
- **Railway**: $5/month credit (usually enough)
- **Vercel**: Free (generous limits)
- **Total**: $0-5/month

### Paid Tier
- **Railway**: $5-20/month
- **Render**: $7-25/month
- **Vercel Pro**: $20/month (optional)
- **Total**: $12-45/month

### Self-Hosted
- **VPS**: $6-12/month
- **Domain**: $10-15/year
- **Total**: ~$7-13/month

## Next Steps

1. **Choose Platform**: Railway + Vercel (easiest)
2. **Deploy Backend**: Follow `QUICK_DEPLOY.md`
3. **Set Up Cron**: Configure automated fetching
4. **Deploy Frontend**: Connect to backend
5. **Test**: Verify everything works
6. **Monitor**: Set up basic monitoring

## Success Indicators

✅ Dashboard accessible from internet
✅ Data updates automatically
✅ No manual intervention needed
✅ All features working
✅ Fast load times

---

**Your dashboard is now fully autonomous!** 🚀

It will:
- Run 24/7 without you
- Update data every 6 hours
- Serve users from anywhere
- Handle errors gracefully
- Scale automatically

No more manual pushes or updates needed!



