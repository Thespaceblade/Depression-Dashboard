# Quick Vercel Deployment

## 🚀 3-Step Deployment

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Configure for Vercel"
git push
```

### Step 2: Deploy on Vercel
1. Go to https://vercel.com
2. Click **Add New Project**
3. Import your GitHub repository
4. Click **Deploy** (settings are auto-detected)

### Step 3: Done! 🎉
Your dashboard is live at `https://your-project.vercel.app`

## What Was Configured

✅ **Backend** → Converted to Vercel serverless functions in `/api/`
✅ **Frontend** → Served from `frontend/dist`
✅ **Cron Job** → Auto-fetches data every 6 hours
✅ **CORS** → Already configured
✅ **Build** → Auto-configured in `vercel.json`

## API Endpoints

All endpoints work automatically:
- `/api/health` - Health check
- `/api/depression` - Depression score
- `/api/teams` - Team data
- `/api/recent-games` - Recent games
- `/api/upcoming-events` - Upcoming events
- `/api/refresh` - Manual refresh (triggers cron)

## Cron Schedule

Runs every 6 hours: `0 */6 * * *`

To change: Edit `vercel.json` → `crons` → `schedule`

## Troubleshooting

**Build fails?**
- Check Vercel logs in dashboard
- Verify `requirements.txt` exists
- Verify `frontend/package.json` exists

**API not working?**
- Check Functions tab in Vercel dashboard
- View function logs for errors

**Cron not running?**
- Check Crons tab in Vercel dashboard
- Verify schedule in `vercel.json`

## That's It!

Your dashboard is now:
- ✅ Fully deployed on Vercel
- ✅ Auto-updates every 6 hours
- ✅ No manual intervention needed
- ✅ Free tier available

See `VERCEL_DEPLOY.md` for detailed instructions.





