# Deploy to Vercel - Complete Guide

This guide shows you how to deploy your Depression Dashboard entirely on Vercel.

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Vercel Account** - Sign up at https://vercel.com (free tier available)

## Step-by-Step Deployment

### Step 1: Push Code to GitHub

Make sure all your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### Step 2: Sign Up / Login to Vercel

1. Go to https://vercel.com
2. Click **Sign Up** (or **Log In** if you have an account)
3. Choose **Continue with GitHub** to connect your GitHub account

### Step 3: Import Your Project

1. In Vercel dashboard, click **Add New...** → **Project**
2. Find your repository in the list
3. Click **Import**

### Step 4: Configure Project Settings

Vercel should auto-detect most settings, but verify:

**Framework Preset:** Other (or leave blank)

**Root Directory:** Leave as `.` (root)

**Build Command:** 
```
cd frontend && npm install && npm run build
```

**Output Directory:** 
```
frontend/dist
```

**Install Command:**
```
cd frontend && npm install
```

### Step 5: Add Environment Variables (Optional)

If you need any environment variables, add them in **Environment Variables** section:

- `VITE_API_URL` - Not needed (uses relative paths)
- Any other vars your app needs

### Step 6: Deploy

1. Click **Deploy**
2. Wait for build to complete (2-5 minutes)
3. Your site will be live at `https://your-project.vercel.app`

## How It Works

### Frontend
- Vercel serves your React app from `frontend/dist`
- Auto-deploys on every git push

### Backend (Serverless Functions)
- All API routes in `/api/` folder become serverless functions
- Automatically deployed with your frontend
- No separate backend needed!

### Automated Data Fetching
- Vercel Cron runs `/api/cron/fetch-data` every 6 hours
- Updates `teams_config.json` automatically
- Next deployment includes updated data

## File Structure

```
project-root/
├── api/                    # Serverless functions (backend)
│   ├── _utils.py          # Shared utilities
│   ├── depression.py      # /api/depression
│   ├── teams.py           # /api/teams
│   ├── recent-games.py    # /api/recent-games
│   ├── upcoming-events.py # /api/upcoming-events
│   ├── refresh.py         # /api/refresh
│   ├── health.py          # /api/health
│   └── cron/
│       └── fetch-data.py  # Scheduled task
├── frontend/              # React app
│   ├── src/
│   └── dist/             # Build output
├── teams_config.json      # Data file
├── depression_calculator.py
├── sports_api.py
├── requirements.txt
├── vercel.json           # Vercel configuration
└── package.json          # Frontend dependencies
```

## Testing Your Deployment

### 1. Check Frontend
Visit your Vercel URL: `https://your-project.vercel.app`

### 2. Test API Endpoints

```bash
# Health check
curl https://your-project.vercel.app/api/health

# Depression data
curl https://your-project.vercel.app/api/depression

# Teams data
curl https://your-project.vercel.app/api/teams
```

### 3. Check Cron Job

1. Go to Vercel dashboard
2. Click on your project
3. Go to **Crons** tab
4. Check execution logs

## Updating Data

### Automatic (Recommended)
- Cron job runs every 6 hours
- Updates `teams_config.json`
- Next deployment includes new data

### Manual Update
1. Make changes to `teams_config.json`
2. Commit and push to GitHub
3. Vercel auto-deploys

## Troubleshooting

### Build Fails

**Error: "Module not found"**
- Check `requirements.txt` has all Python dependencies
- Check `frontend/package.json` has all npm dependencies

**Error: "Python runtime not found"**
- Vercel should auto-detect Python from `requirements.txt`
- Make sure `requirements.txt` exists in root

### API Endpoints Not Working

**404 Errors:**
- Check files are in `api/` folder
- Verify file names match routes (e.g., `depression.py` → `/api/depression`)

**500 Errors:**
- Check Vercel function logs
- Go to project → **Functions** tab → View logs

### Cron Job Not Running

**Check:**
1. `vercel.json` has cron configuration
2. Cron path is correct: `/api/cron/fetch-data`
3. Schedule is valid: `0 */6 * * *` (every 6 hours)

**View Logs:**
- Go to project → **Crons** tab
- Check execution history

### CORS Errors

- All API functions include CORS headers
- Should work automatically
- If issues persist, check `_utils.py` headers

## Cost

### Free Tier
- **100GB** bandwidth/month
- **100 hours** function execution/month
- **Unlimited** deployments
- **Perfect for this project!**

### Pro Tier ($20/month)
- More bandwidth
- More function execution time
- Team features
- Only needed if you exceed free limits

## Custom Domain (Optional)

1. Go to project → **Settings** → **Domains**
2. Add your domain
3. Follow DNS configuration instructions
4. SSL certificate auto-provisioned

## Monitoring

### View Logs
- **Project** → **Deployments** → Click deployment → **Functions** tab
- See real-time logs for each API call

### View Cron Executions
- **Project** → **Crons** tab
- See execution history and logs

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test all endpoints
3. ✅ Verify cron job runs
4. ✅ Share your dashboard URL!

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Vercel Discord**: https://vercel.com/discord
- **Function Logs**: Check in Vercel dashboard

---

**That's it!** Your dashboard is now fully deployed on Vercel and runs completely autonomously! 🚀



