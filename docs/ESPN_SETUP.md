# ESPN Fantasy Football Setup Guide

This guide will walk you through setting up automatic fantasy team data fetching from ESPN Fantasy Football.

## Quick Start

1. **Get your League ID**
   - Go to your ESPN Fantasy Football league page
   - Look at the URL: `https://fantasy.espn.com/football/league?leagueId=123456`
   - Copy the number after `leagueId=` (that's your league ID)

2. **Get your Team Name or Team ID** (optional)
   - Your team name is usually visible on your team page
   - Or leave it blank and we'll find it automatically

3. **Determine if you need authentication**
   - **Public League**: No authentication needed! Just use league_id and year
   - **Private League**: You'll need cookies (see below)

4. **Update your config file**
   - Open `teams_config.json`
   - Find the `fantasy_team` section
   - Add an `espn` section with your credentials

## Configuration Examples

### Public League (No Authentication)

```json
"fantasy_team": {
  "name": "Jason's Fantasy Squad",
  "expected_performance": 7,
  "jasons_expectations": 8,
  "espn": {
    "league_id": 123456,
    "year": 2024,
    "team_name": "Jason's Fantasy Squad"
  }
}
```

### Private League (With Authentication)

```json
"fantasy_team": {
  "name": "Jason's Fantasy Squad",
  "expected_performance": 7,
  "jasons_expectations": 8,
  "espn": {
    "league_id": 123456,
    "year": 2024,
    "team_name": "Jason's Fantasy Squad",
    "espn_s2": "AEBi...your_long_cookie_string...",
    "swid": "{12345678-1234-1234-1234-123456789ABC}"
  }
}
```

## Getting ESPN Cookies (For Private Leagues Only)

If your league is private, you'll need to get your ESPN authentication cookies:

1. **Open your browser's Developer Tools**
   - Chrome/Edge: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
   - Firefox: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
   - Safari: Enable Developer menu first (Preferences > Advanced > Show Develop menu)

2. **Go to the Cookies section**
   - Chrome/Edge: Application tab > Cookies > `https://fantasy.espn.com`
   - Firefox: Storage tab > Cookies > `https://fantasy.espn.com`
   - Safari: Storage tab > Cookies > `fantasy.espn.com`

3. **Find and copy these cookies:**
   - **espn_s2**: A long string (usually starts with `AEBi...`)
   - **SWID**: Usually starts with `{` and contains a GUID like `{12345678-1234-1234-1234-123456789ABC}`

4. **Paste them into your config file**

## Testing Your Setup

Once you've configured ESPN in your config file, test it:

```bash
# Show setup instructions
python3 depression_calculator.py --espn-help

# Refresh fantasy data from ESPN
python3 depression_calculator.py --refresh-fantasy

# Run the calculator (will auto-fetch from ESPN)
python3 depression_calculator.py
```

## Troubleshooting

### "Failed to connect to ESPN Fantasy League"
- Check that your `league_id` is correct
- Make sure the `year` matches the current season
- If it's a private league, make sure you've added `espn_s2` and `swid` cookies

### "Team not found in league"
- Check that your `team_name` matches your team name in ESPN (case-insensitive)
- Or try using `team_id` instead (you can find this in the URL when viewing your team)

### "Falling back to manual config data"
- The API fetch failed, but the calculator will still work with your manual data
- Check your internet connection
- Verify your credentials are correct

### Using Manual Data Instead
If you prefer to manually update your fantasy team record:

```bash
# Disable ESPN API
python3 depression_calculator.py --no-espn

# Or manually update in the config file and don't include the "espn" section
```

## What Gets Fetched Automatically

When using ESPN API, the following data is automatically fetched:
- ✅ Team name
- ✅ Wins/Losses/Ties record
- ✅ Recent game results (last 5 weeks)
- ✅ Current week matchup information

You still need to manually set:
- Expected performance (1-10 scale)
- Jason's expectations (1-10 scale)

These are personal preferences and can't be determined from the API.

## Security Note

⚠️ **Important**: Your `espn_s2` and `swid` cookies are sensitive credentials. They give access to your ESPN account.

- **Don't commit them to git** - Add `teams_config.json` to `.gitignore` if it contains cookies
- **Don't share them** - Anyone with these cookies can access your fantasy league
- **They expire** - You may need to refresh them periodically

## Example: Complete Config

```json
{
  "fantasy_team": {
    "name": "Jason's Fantasy Squad",
    "expected_performance": 7,
    "jasons_expectations": 8,
    "espn": {
      "league_id": 123456,
      "year": 2024,
      "team_name": "Jason's Fantasy Squad"
    }
  }
}
```

The `record` and `recent_streak` fields will be automatically populated from ESPN when you run the calculator!

