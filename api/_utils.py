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
    # In Vercel, includeFiles copies files to the function's directory
    # The function runs from /var/task/ (or similar), and includeFiles puts files at the project root
    # So from api/_utils.py, we need to go up two levels to get to the project root
    
    # Calculate base paths
    current_file = os.path.abspath(__file__)  # /var/task/api/_utils.py (or similar)
    api_dir = os.path.dirname(current_file)   # /var/task/api
    project_root = os.path.dirname(api_dir)    # /var/task
    
    # Try multiple possible paths for teams_config.json
    possible_paths = [
        # Primary: project root (where includeFiles puts it)
        os.path.join(project_root, "teams_config.json"),
        # Fallback: relative to current working directory
        "teams_config.json",
        # Fallback: relative to api directory (unlikely but try)
        os.path.join(api_dir, "teams_config.json"),
    ]
    
    config_path = None
    for path in possible_paths:
        if os.path.exists(path):
            config_path = path
            print(f"✅ Found teams_config.json at: {config_path}")
            break
    
    if not config_path:
        # If none found, use the primary path and let DepressionCalculator handle the error
        # But log helpful debugging info
        config_path = possible_paths[0]
        print(f"⚠️ teams_config.json not found. Tried paths:")
        for path in possible_paths:
            print(f"  - {path} (exists: {os.path.exists(path)})")
        print(f"Current __file__: {current_file}")
        print(f"Current working directory: {os.getcwd()}")
        try:
            if os.path.exists(project_root):
                print(f"Project root contents: {os.listdir(project_root)[:10]}")
        except:
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





