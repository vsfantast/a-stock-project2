#!/usr/bin/env python3
"""Mac端：每分钟抓取东财数据，推送到HK服务器"""
import json, time, ssl

# 自己签的不验证
ssl._create_default_https_context = ssl._create_unverified_context

SERVER = "http://43.128.20.163:8777"
TOKEN = "a-stock-2026"

from http.client import HTTPSConnection, HTTPConnection
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json

def fetch(url):
    """从国内直连东财"""
    try:
        r = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=10)
        return r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f'{{"error":"{e}"}}'

def push(endpoint, raw_text):
    """推送到HK服务器"""
    try:
        import urllib.request
        data = json.dumps({"endpoint": endpoint, "payload": raw_text}).encode()
        req = Request(SERVER, data=data, headers={
            'Content-Type': 'application/json',
            'X-Auth-Token': TOKEN,
        })
        urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"推送失败: {e}")
        return False

# ====== 抓取任务 ======

def fetch_industry_top5():
    """行业板块TOP5"""
    url = "https://push2.eastmoney.com/api/qt/clist/get?fid=f3&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:2&fields=f2,f3,f14,f62,f104,f128"
    return fetch(url)

def fetch_concept_top5():
    """概念板块TOP5"""
    url = "https://push2.eastmoney.com/api/qt/clist/get?fid=f3&po=1&pz=5&pn=1&np=1&fltt=2&invt=2&fs=m:90+t:3&fields=f2,f3,f14,f62"
    return fetch(url)

def fetch_fund_flow(code, market=0):
    """个股资金流 (0=深圳, 1=上海)"""
    url = f"https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={market}.{code}&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57&lmt=5&klt=101"
    return fetch(url)

def fetch_margin(code):
    """融资融券"""
    mkt = '1' if code.startswith(('6','9')) else '0'
    secucode = f"{code}.{'SH' if code.startswith('6') else 'SZ'}"
    url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPTA_WEB_RZRQ_GGMX&filter=(SCODE=%22{code}%22)&pageSize=5&sortColumns=DATE&sortTypes=-1&source=WEB&client=WEB"
    return fetch(url)

def fetch_dragon(code, date="2026-05-27"):
    """龙虎榜"""
    url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_DAILYBILLBOARD_DETAILSNEW&filter=(TRADE_DATE%3E=%272026-05-01%27)(SECURITY_CODE=%22{code}%22)&pageSize=5&sortColumns=TRADE_DATE&sortTypes=-1&source=WEB&client=WEB"
    return fetch(url)

# ====== 主循环 ======

if __name__ == "__main__":
    print("东财数据推送器启动...")

    # 你的持仓 + 候选
    WATCHLIST = ["000555", "600549", "000969", "002185", "603005"]

    while True:
        try:
            # 1. 行业+概念板块
            push("industry_top5", fetch_industry_top5())
            push("concept_top5", fetch_concept_top5())

            # 2. 每支持仓的资金流
            for code in WATCHLIST[:2]:  # 只推持仓，减少负担
                mkt = 1 if code.startswith(('6','9')) else 0
                push(f"fund_{code}", fetch_fund_flow(code, mkt))

            print(f"[OK] 推送完成")
        except Exception as e:
            print(f"[ERR] {e}")

        time.sleep(60)  # 每分钟
