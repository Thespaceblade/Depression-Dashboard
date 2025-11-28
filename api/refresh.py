"""
Vercel serverless function for /api/refresh
Note: In serverless, we can't easily update files, so this just triggers a fetch
For actual updates, use the cron job
"""
from http.server import BaseHTTPRequestHandler
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _utils import json_response, error_response

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request"""
        try:
            # In serverless, we can't easily update files
            # This endpoint just returns a message
            # Actual updates should be done via cron job
            response = json_response({
                "success": True,
                "message": "Refresh triggered. Data will be updated by scheduled cron job.",
                "timestamp": datetime.now().isoformat(),
                "note": "In serverless environment, use cron job for automatic updates"
            })
            
            self.send_response(response['statusCode'])
            for key, value in response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response['body'].encode())
            
        except Exception as e:
            response = error_response(e, 500)
            self.send_response(response['statusCode'])
            for key, value in response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response['body'].encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()



