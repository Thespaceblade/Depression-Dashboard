"""
Vercel serverless function for /api/depression
"""
from http.server import BaseHTTPRequestHandler
import sys
import os
from datetime import datetime

# Add utils to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _utils import get_calculator, json_response, error_response

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request"""
        try:
            calc = get_calculator()
            result = calc.calculate_total_depression()
            emoji, level = calc.get_depression_level(result["total_score"])
            
            response = json_response({
                "success": True,
                "score": round(result["total_score"], 1),
                "level": level,
                "emoji": emoji,
                "breakdown": result["breakdown"],
                "timestamp": datetime.now().isoformat()
            })
            
            self.send_response(response['statusCode'])
            for key, value in response['headers'].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response['body'].encode())
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            # Log to console for Vercel logs
            print(f"ERROR in /api/depression: {str(e)}")
            print(f"Traceback:\n{error_details}")
            # Include file path info if it's a file error
            if "FileNotFoundError" in str(type(e)) or "No such file" in str(e):
                import os
                print(f"Current working directory: {os.getcwd()}")
                print(f"__file__ location: {__file__}")
                try:
                    parent_dir = os.path.dirname(os.path.dirname(__file__))
                    print(f"Parent directory contents: {os.listdir(parent_dir) if os.path.exists(parent_dir) else 'DOES NOT EXIST'}")
                except:
                    pass
            response = error_response(e, 500, error_details)
            
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
