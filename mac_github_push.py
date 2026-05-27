#!/usr/bin/env python3
"""Mac端：抓东财 → GitHub API写文件 → HK curl直读 (零端口零隧道)"""
import time, json, ssl, base64
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.request import urlopen, Request

TOKEN = "你的GitHub_Token_放这里"
API = "https://api.github.com/repos/vsfantast/a-stock-project2/contents/eastmoney_live.json"
RAW = "https://raw.githubusercontent.com/vsfantast/a-stock-project2/main/eastmoney_live.json"

def fetch(url):
    r = urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=10)
    return r.read().decode('utf-8', errors='ignore')

def push_to_github(content):
    # 先获取现有文件的SHA
    try:
        r = urlopen(Request(API, headers={'Authorization':f'Bearer {TOKEN}','User-Agent':'python'}), timeout=10)
        sha = json.loads(r.read()).get('sha','')
    except:
        sha = ''

    # PUT更新
    body = json.dumps({
        'message': 'eastmoney update',
        'content': base64.b64encode(content.encode()).decode(),
        'branch': 'main',
        **({'sha': sha} if sha else {})
    }).encode()

    req = Request(API, data=body, method='PUT',
        headers={'Authorization':f'Bearer {TOKEN}','Content-Type':'application/json','User-Agent':'python'})
    r = urlopen(req, timeout=15)
    return r.status == 200 or r.status == 201

while True:
    try:
        data = {}
        data['industry'] = fetch('https://push2.eastmoney.com/api/qt/clist/get?fid=f3&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:2&fields=f2,f3,f14,f62,f104')
        data['concept'] = fetch('https://push2.eastmoney.com/api/qt/clist/get?fid=f3&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:3&fields=f2,f3,f14,f62')
        data['updated'] = time.strftime('%Y-%m-%d %H:%M:%S')

        ok = push_to_github(json.dumps(data, ensure_ascii=False))
        print(f"[{data['updated']}] {'OK' if ok else 'FAIL'}")
    except Exception as e:
        print(f"错误: {e}")

    time.sleep(60)
