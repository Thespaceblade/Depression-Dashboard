"""
Shared utilities for Vercel serverless functions
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.depression_calculator import DepressionCalculator

def get_calculator():
    """Get calculator instance (creates new one each time since serverless is stateless)"""
    # In Vercel, includeFiles copies matched files into the function bundle.
    # Prefer src/data/teams_config.json — it is covered by includeFiles "src/**"
    # without needing brace-globs that previously broke Preview deploys (#13/#17).

    current_file = os.path.abspath(__file__)  # /var/task/api/_utils.py (or similar)
    api_dir = os.path.dirname(current_file)   # /var/task/api
    project_root = os.path.dirname(api_dir)    # /var/task

    possible_paths = [
        # Packaged via includeFiles src/**
        os.path.join(project_root, "src", "data", "teams_config.json"),
        # Root copy (local / if explicitly included)
        os.path.join(project_root, "teams_config.json"),
        "teams_config.json",
        os.path.join("src", "data", "teams_config.json"),
        os.path.join(api_dir, "teams_config.json"),
    ]

    config_path = None
    for path in possible_paths:
        if os.path.exists(path):
            config_path = path
            print(f"✅ Found teams_config.json at: {config_path}")
            break

    if not config_path:
        config_path = possible_paths[0]
        print(f"⚠️ teams_config.json not found. Tried paths:")
        for path in possible_paths:
            print(f"  - {path} (exists: {os.path.exists(path)})")
        print(f"Current __file__: {current_file}")
        print(f"Current working directory: {os.getcwd()}")
        try:
            if os.path.exists(project_root):
                print(f"Project root contents: {os.listdir(project_root)[:10]}")
            src_data = os.path.join(project_root, "src", "data")
            if os.path.exists(src_data):
                print(f"src/data contents: {os.listdir(src_data)[:20]}")
        except Exception:
            pass

    return DepressionCalculator(config_path)

def json_response(data, status_code=200):
    """Create JSON response for Vercel"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(data)
    }

def error_response(error, status_code=500, details=None):
    """Create error response"""
    data = {
        'success': False,
        'error': str(error)
    }
    if details:
        data['details'] = details
    return json_response(data, status_code)


def _team_payload(team, team_result):
    """Build API team dict including mood-impact sort key."""
    MIN_RAW, MAX_RAW = -50.0, 100.0
    raw = float(team_result.get("score") or 0)
    scaled = ((raw - MIN_RAW) / (MAX_RAW - MIN_RAW)) * 100.0
    scaled = max(0.0, min(100.0, scaled))
    weight = team.impact_weight() if hasattr(team, "impact_weight") else float(getattr(team, "interest_level", 1.0) or 1.0)
    mood_impact = abs(scaled - 50.0) * weight
    total_games = team.wins + team.losses + getattr(team, "ties", 0)
    win_percentage = round((team.wins / total_games * 100), 1) if total_games else 0
    return {
        "name": team.name,
        "sport": team.sport,
        "wins": team.wins,
        "losses": team.losses,
        "ties": getattr(team, "ties", 0),
        "record": f"{team.wins}-{team.losses}" + (f"-{team.ties}" if getattr(team, "ties", 0) else ""),
        "win_percentage": win_percentage,
        "recent_streak": team.recent_streak,
        "depression_points": round(raw, 1),
        "scaled_score": round(scaled, 1),
        "mood_impact": round(mood_impact, 2),
        "recency_factor": round(
            float(
                team_result.get("recency_factor")
                if team_result.get("recency_factor") is not None
                else (team.season_recency_factor() if hasattr(team, "season_recency_factor") else 1.0)
            ),
            3,
        ),
        "from_prior_season": getattr(team, "from_prior_season", None),
        "is_offseason": team.is_in_offseason() if hasattr(team, "is_in_offseason") else False,
        "breakdown": team_result.get("breakdown", {}),
        "expected_performance": team.expected_performance,
        "jasons_expectations": team.jasons_expectations,
        "rivals": team.rivals,
        "recent_rivalry_losses": team.recent_rivalry_losses,
        "interest_level": team.interest_level,
        "notes": team.notes,
    }

