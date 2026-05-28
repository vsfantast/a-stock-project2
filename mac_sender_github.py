#!/usr/bin/env python3
"""Mac端：抓东财数据 → 飞书Webhook推送到HK Claude所在群"""
import json, time, ssl
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.request import urlopen, Request

WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/f281cf20-e638-494c-b1d7-29742c3fa8b2"

def fetch(url):
    return urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=10).read().decode('utf-8',errors='ignore')

while True:
    try:
        ind = json.loads(fetch('https://push2.eastmoney.com/api/qt/clist/get?fid=f3&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:2&fields=f2,f3,f14,f62'))
        con = json.loads(fetch('https://push2.eastmoney.com/api/qt/clist/get?fid=f3&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:3&fields=f2,f3,f14,f62'))
        
        lines = ["[东财实时数据]", f"更新时间:{time.strftime('%H:%M:%S')}", ""]
        lines.append("行业TOP5:")
        for i in ind['data']['diff'][:5]:
            lines.append(f"  {i['f14']} +{i['f3']}%")
        lines.append("")
        lines.append("概念TOP5:")
        for i in con['data']['diff'][:5]:
            lines.append(f"  {i['f14']} +{i['f3']}%")
        
        msg = '\n'.join(lines)
        urlopen(Request(WEBHOOK, data=json.dumps({'msg_type':'text','content':{'text':msg}}).encode(),
            headers={'Content-Type':'application/json'}), timeout=10)
        print(f"[{time.strftime('%H:%M:%S')}] OK")
    except Exception as e:
        print(f"ERR: {e}")
    time.sleep(60)
