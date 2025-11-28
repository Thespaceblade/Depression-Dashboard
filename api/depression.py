"""
Vercel serverless function for /api/depression
"""
import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from depression_calculator import DepressionCalculator

def handler(request):
    """Get current depression score and breakdown"""
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "teams_config.json")
        calc = DepressionCalculator(config_path)
        result = calc.calculate_total_depression()
        emoji, level = calc.get_depression_level(result["total_score"])
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "success": True,
                "score": round(result["total_score"], 1),
                "level": level,
                "emoji": emoji,
                "breakdown": result["breakdown"],
                "timestamp": datetime.now().isoformat()
            })
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": str(e),
                "details": error_details
            })
        }

