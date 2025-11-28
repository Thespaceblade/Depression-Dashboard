# Quick Deploy Guide

## Fastest Path to Autonomous Deployment

### Step 1: Backend on Railway (5 minutes)

1. **Sign up**: https://railway.app
2. **New Project** → **Deploy from GitHub**
3. **Select your repo**
4. **Settings** → **Add Environment Variable**:
   - `PORT` = `5001`
   - `FLASK_ENV` = `production`
5. **Deploy** → Railway auto-detects Python and deploys!

### Step 2: Add Cron Job for Auto-Updates

1. In Railway dashboard, click **+ New**
2. Select **Cron Job**
3. **Schedule**: `0 */6 * * *` (every 6 hours)
4. **Command**: `python fetch_all_data.py`
5. **Deploy**

### Step 3: Frontend on Vercel (3 minutes)

1. **Sign up**: https://vercel.com
2. **New Project** → **Import from GitHub**
3. **Select your repo**
4. **Settings**:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **Environment Variables**:
   - `VITE_API_URL` = Your Railway URL (e.g., `https://your-app.railway.app`)
6. **Deploy**

### Step 4: Done! 🎉

Your dashboard now:
- ✅ Runs 24/7
- ✅ Auto-updates data every 6 hours
- ✅ No manual intervention needed
- ✅ Accessible from anywhere

## Alternative: All-in-One on Render

1. **Sign up**: https://render.com
2. **New Blueprint** → **Connect GitHub**
3. Render will use `render.yaml` to deploy:
   - Backend API (web service)
   - Cron job (auto-fetch)
4. **Frontend**: Deploy separately on Netlify/Vercel

## Testing

After deployment:

```bash
# Test backend
curl https://your-backend-url.com/api/health

# Test frontend
# Visit your frontend URL in browser
```

## Monitoring

- **Railway**: Check logs in dashboard
- **Vercel**: Check logs in dashboard
- **Cron Jobs**: Check execution logs

## Troubleshooting

**Backend not starting?**
- Check Railway logs
- Verify `requirements.txt` has all dependencies
- Check environment variables

**Data not updating?**
- Check cron job logs
- Verify `fetch_all_data.py` runs successfully
- Check `teams_config.json` is being updated

**Frontend can't reach backend?**
- Verify `VITE_API_URL` is set correctly
- Check CORS settings in backend
- Check backend is running

---

**That's it!** Your dashboard is now fully autonomous. 🚀

