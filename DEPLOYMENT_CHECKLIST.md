# Deployment Checklist

Use this checklist to ensure your deployment is complete and working.

## Pre-Deployment

- [ ] Code is pushed to GitHub
- [ ] `teams_config.json` exists and is valid
- [ ] All dependencies are in `requirements.txt`
- [ ] Frontend dependencies are in `package.json`
- [ ] Environment variables documented in `.env.example`

## Backend Deployment

- [ ] Backend service created (Railway/Render/Heroku)
- [ ] Environment variables set:
  - [ ] `PORT` (usually auto-set by platform)
  - [ ] `FLASK_ENV=production`
  - [ ] `PYTHONUNBUFFERED=1`
- [ ] Backend is running and accessible
- [ ] Health check endpoint works: `/api/health`
- [ ] Depression endpoint works: `/api/depression`
- [ ] Teams endpoint works: `/api/teams`

## Automated Data Fetching

- [ ] Cron job/service created
- [ ] Schedule set (recommended: every 6 hours)
- [ ] Command set: `python fetch_all_data.py`
- [ ] Cron job has executed at least once
- [ ] `teams_config.json` is being updated
- [ ] Logs show successful data fetching

## Frontend Deployment

- [ ] Frontend service created (Vercel/Netlify)
- [ ] Root directory set to `frontend/`
- [ ] Build command: `npm run build`
- [ ] Output directory: `dist`
- [ ] Environment variable set:
  - [ ] `VITE_API_URL` = your backend URL
- [ ] Frontend builds successfully
- [ ] Frontend is accessible

## Testing

- [ ] Backend health check: `curl https://your-backend.com/api/health`
- [ ] Frontend loads in browser
- [ ] Dashboard displays data
- [ ] API calls work (check browser console)
- [ ] No CORS errors
- [ ] Auto-refresh works (wait 60 seconds)

## Monitoring

- [ ] Logs are accessible
- [ ] Error notifications set up (optional)
- [ ] Uptime monitoring configured (optional)
- [ ] Data freshness checked (last update timestamp)

## Post-Deployment

- [ ] Share URL with users
- [ ] Document any custom configurations
- [ ] Set up alerts for failures (optional)
- [ ] Test after 6 hours to verify auto-update works

## Troubleshooting

If something isn't working:

1. **Check logs** - Most platforms show logs in dashboard
2. **Verify environment variables** - Make sure all are set correctly
3. **Test endpoints manually** - Use curl or Postman
4. **Check CORS** - Backend should allow frontend origin
5. **Verify cron schedule** - Check platform's cron documentation

## Success Criteria

✅ Dashboard is accessible from internet
✅ Data updates automatically every 6 hours
✅ No manual intervention needed
✅ All API endpoints working
✅ Frontend displays data correctly

---

**Once all items are checked, your deployment is complete!** 🎉

