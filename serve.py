#!/usr/bin/env python3
# Simple file server to serve index.html with CORS

import http.server
import socketserver
import os
from pathlib import Path

PORT = 5173
DIR = Path(__file__).parent

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def translate_path(self, path):
        # Serve index.html for root path
        if path == '/':
            path = '/index.html'
        return super().translate_path(path)

os.chdir(DIR)
with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    print(f"Server running at http://127.0.0.1:{PORT}")
    print(f"Serving files from: {DIR}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()
