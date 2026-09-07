"""
Vercel serverless function for /api/upcoming-events
"""
from http.server import BaseHTTPRequestHandler
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _utils import json_response, error_response


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request"""
        try:
            # Ensure project root is importable for src.*
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)

            from src.upcoming_schedule import fetch_upcoming_events_result

            result = fetch_upcoming_events_result(limit=10, allow_snapshot=True)
            payload = {
                "success": bool(result.get("success", True)),
                "events": result.get("events") or [],
                "count": len(result.get("events") or []),
                "source": result.get("source") or "none",
                "partial": bool(result.get("partial")),
                "timestamp": datetime.now().isoformat(),
            }
            if result.get("warning"):
                payload["warning"] = result["warning"]
            if result.get("errors"):
                payload["errors"] = result["errors"]

            response = json_response(payload)

            self.send_response(response["statusCode"])
            for key, value in response["headers"].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response["body"].encode())

        except Exception as e:
            import traceback

            response = error_response(e, 500, traceback.format_exc())
            self.send_response(response["statusCode"])
            for key, value in response["headers"].items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response["body"].encode())

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
