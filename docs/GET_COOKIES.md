# How to Get Your ESPN Cookies

Your league requires authentication. Follow these steps to get your cookies:

## Quick Steps:

1. **Open your ESPN Fantasy League page**
   - Make sure you're logged in
   - Go to: https://fantasy.espn.com/football/team?leagueId=925989669&teamId=2&seasonId=2025

2. **Open Developer Tools**
   - **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
   - **Firefox**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
   - **Safari**: Enable Developer menu first (Preferences > Advanced > Show Develop menu), then press `Cmd+Option+I`

3. **Navigate to Cookies**
   - **Chrome/Edge**: 
     - Click the "Application" tab
     - In the left sidebar, expand "Cookies"
     - Click on `https://fantasy.espn.com`
   - **Firefox**:
     - Click the "Storage" tab
     - In the left sidebar, expand "Cookies"
     - Click on `https://fantasy.espn.com`
   - **Safari**:
     - Click the "Storage" tab
     - In the left sidebar, expand "Cookies"
     - Click on `fantasy.espn.com`

4. **Find and Copy These Cookies:**
   
   **espn_s2**:
   - Look for a cookie named `espn_s2`
   - It will be a long string (usually starts with `AEBi...` or similar)
   - Copy the entire value
   
   **SWID**:
   - Look for a cookie named `SWID`
   - It usually starts with `{` and contains a GUID like `{12345678-1234-1234-1234-123456789ABC}`
   - Copy the entire value including the curly braces

5. **Add to Config File**
   - Open `teams_config.json`
   - Find the `fantasy_team` > `espn` section
   - Paste your cookies:
     ```json
     "espn": {
       "league_id": 925989669,
       "year": 2025,
       "team_id": 2,
       "espn_s2": "PASTE_YOUR_ESPN_S2_COOKIE_HERE",
       "swid": "PASTE_YOUR_SWID_COOKIE_HERE"
     }
     ```

## Visual Guide:

```
Developer Tools
├── Application (Chrome) / Storage (Firefox)
    └── Cookies
        └── https://fantasy.espn.com
            ├── espn_s2  ← Copy this value
            └── SWID     ← Copy this value
```

## Security Note:

⚠️ **Keep these cookies private!** They give access to your ESPN account.
- Don't commit them to git
- Don't share them with anyone
- They may expire and need to be refreshed periodically

## After Adding Cookies:

Run this command to test:
```bash
python3 -m src.depression_calculator --refresh-fantasy
```

If it works, you'll see:
```
✓ Loaded fantasy team 'Your Team Name' from ESPN API
  Record: X-Y-Z
  Current Week N Matchup: vs Opponent Name
```

