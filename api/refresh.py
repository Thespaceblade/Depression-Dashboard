"""
Vercel serverless function for /api/refresh

On Vercel, team config cannot be rewritten in place. This endpoint is honest about
that: it does not refetch sports APIs into persisted config. Scheduled GitHub
Actions / cron own source updates. Clients may still reload displayed API data.
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
            response = json_response({
                "success": True,
                "refreshed": False,
                "mode": "cron_only",
                "message": "Sports records are not refreshed from this button on Vercel. Source data updates on the scheduled cron/GitHub Action.",
                "timestamp": datetime.now().isoformat(),
                "note": "Reload the dashboard to re-read the current API responses. Persisted config updates come from cron."
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
