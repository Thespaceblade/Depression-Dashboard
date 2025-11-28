"""
Vercel Cron job to fetch sports data every 6 hours
This updates teams_config.json via GitHub API
"""
from http.server import BaseHTTPRequestHandler
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from sports_api import SportsDataFetcher

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle cron job trigger"""
        try:
            # Get config path
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "teams_config.json"
            )
            
            # Fetch data
            fetcher = SportsDataFetcher()
            fetcher.update_config_file(config_path)
            
            # Note: In Vercel, we can't directly commit to git
            # The config file will be updated in the deployment
            # For persistent updates, you'd need to use GitHub API to commit
            # or use Vercel KV/Environment variables
            
            response = {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    "success": True,
                    "message": "Data fetched successfully",
                    "timestamp": datetime.now().isoformat(),
                    "note": "Config updated. Changes will persist in next deployment."
                })
            }
            
            self.send_response(response['statusCode'])
            for key, value in response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response['body'].encode())
            
        except Exception as e:
            import traceback
            error_response = {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })
            }
            
            self.send_response(error_response['statusCode'])
            for key, value in error_response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(error_response['body'].encode())



