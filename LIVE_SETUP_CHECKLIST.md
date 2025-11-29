# Live Scores Setup - Quick Checklist

## ✅ Pre-Setup
- [ ] GitHub account ready
- [ ] Code editor open
- [ ] Terminal ready

## 🚂 Part 1: Railway Backend (30 min)
- [ ] Create Railway account (railway.app)
- [ ] Create new project from GitHub
- [ ] Set environment variables (PORT, FLASK_ENV, PYTHONUNBUFFERED)
- [ ] Deploy and get Railway URL
- [ ] Test: `https://your-url.railway.app/api/health`

## 💻 Part 2: Backend Code (45 min)
- [ ] Create `backend/live_updates.py` (copy from guide)
- [ ] Update `backend/app.py` (add imports and endpoint)
- [ ] Test locally: `python backend/app.py`
- [ ] Verify: `curl http://localhost:5001/api/live-games`

## 🎨 Part 3: Frontend Code (30 min)
- [ ] Update `frontend/src/api.ts` (add Railway URL)
- [ ] Update `frontend/src/types/index.ts` (add LiveGame type)
- [ ] Create `frontend/src/components/LiveGameCard.tsx`
- [ ] Update `frontend/src/App.tsx` (add live games state & display)
- [ ] Test locally: `npm run dev`

## 🚀 Part 4: Deploy (20 min)
- [ ] Commit changes: `git add . && git commit -m "Add live scores" && git push`
- [ ] Railway auto-deploys (check logs)
- [ ] Add `VITE_API_URL` to Vercel environment variables
- [ ] Redeploy Vercel frontend
- [ ] Test production site

## ✅ Verification
- [ ] Backend health check works
- [ ] Live games endpoint returns JSON
- [ ] Frontend loads without errors
- [ ] During live game, cards appear and update

## 📝 Your URLs
- Railway Backend: `_____________________________`
- Vercel Frontend: `_____________________________`

---

**Full detailed guide:** See `docs/STEP_BY_STEP_LIVE_SETUP.md`

