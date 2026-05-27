#!/usr/bin/env python3
"""东财数据接收器 — 接收Mac推送的东财数据，存入本地缓存"""
import json, os, sys, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from urllib.parse import parse_qs

CACHE_DIR = "/home/ubuntu/.eastmoney_cache"
AUTH_TOKEN = "a-stock-2026"
os.makedirs(CACHE_DIR, exist_ok=True)

class Receiver(BaseHTTPRequestHandler):
    def do_POST(self):
        # 简易鉴权
        token = self.headers.get('X-Auth-Token', '')
        if token != AUTH_TOKEN:
            self.send_error(403); return
        
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length))
        
        endpoint = data.get('endpoint', 'unknown')
        payload = data.get('payload', {})
        ts = datetime.now().isoformat()
        
        # 存缓存
        cache_file = os.path.join(CACHE_DIR, f"{endpoint}.json")
        with open(cache_file, 'w') as f:
            json.dump({"updated": ts, "data": payload}, f, ensure_ascii=False)
        
        self.send_response(200); self.end_headers()
        self.wfile.write(b'OK')
    
    def log_message(self, format, *args):
        pass  # 静默

def serve(port=8777):
    server = HTTPServer(('0.0.0.0', port), Receiver)
    print(f"东财接收器已启动: port {port}")
    server.serve_forever()

if __name__ == "__main__":
    serve()
