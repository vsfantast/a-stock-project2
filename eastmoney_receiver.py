#!/usr/bin/env python3
"""东财数据接收器"""
import json, os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from urllib.parse import parse_qs

AUTH_TOKEN = "a-stock-2026"

class R(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.headers.get('X-Auth-Token','') != AUTH_TOKEN:
            self.send_error(403); return
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            data['_received'] = datetime.now().isoformat()
            os.makedirs('/home/ubuntu/.eastmoney_cache', exist_ok=True)
            with open('/home/ubuntu/.eastmoney_cache/latest.json','w') as f:
                json.dump(data, f, ensure_ascii=False)
            self.send_response(200); self.send_header('Content-Type','text/plain'); self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, *args): pass

if __name__ == "__main__":
    HTTPServer(('127.0.0.1', 8778), R).serve_forever()
    print("Receiver on 8778")
