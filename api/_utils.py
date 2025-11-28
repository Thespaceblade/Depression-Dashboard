"""
Shared utilities for Vercel serverless functions
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from depression_calculator import DepressionCalculator

def get_calculator():
    """Get calculator instance (creates new one each time since serverless is stateless)"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "teams_config.json")
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



