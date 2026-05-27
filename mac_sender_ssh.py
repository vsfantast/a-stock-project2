#!/usr/bin/env python3
"""Mac→HK 东财数据推送 (SSH端口443，零额外端口)"""
import subprocess, time, json, ssl
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.request import urlopen, Request

HOST = 'ubuntu@43.128.20.163'
PORT = '443'

def fetch(url):
    try:
        r = urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=10)
        return r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return json.dumps({'error':str(e)})

while True:
    try:
        data = {}
        data['industry'] = fetch('https://push2.eastmoney.com/api/qt/clist/get?fid=f3&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:2&fields=f2,f3,f14,f62,f104')
        data['concept']  = fetch('https://push2.eastmoney.com/api/qt/clist/get?fid=f3&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:3&fields=f2,f3,f14,f62')
        data['updated']  = time.strftime('%Y-%m-%d %H:%M:%S')

        j = json.dumps(data, ensure_ascii=False)
        r = subprocess.run(['ssh','-p',PORT,'-o','StrictHostKeyChecking=no',
            '-o','ConnectTimeout=10',HOST,'cat > /tmp/eastmoney_live.json'],
            input=j, capture_output=True, text=True, timeout=15)

        if r.returncode == 0:
            print(f"[{data['updated']}] 推送 OK")
        else:
            print(f"失败: {r.stderr.strip()}")
    except Exception as e:
        print(f"错误: {e}")

    time.sleep(60)
