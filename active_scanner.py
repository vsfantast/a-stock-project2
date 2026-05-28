#!/usr/bin/env python3
"""主动机会扫描 — 持仓监控 + 候选池追踪 + 异动检测 + 自动推送"""
import requests, json, os, sys
from datetime import datetime, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
PROJECT = "a-stock-bot"
ALERT_FILE = "/home/ubuntu/a-stock-project/.scanner_alerts.json"

# ====== 配置区 ======
# 持仓股
POSITIONS = {
    "600549": {"name": "厦门钨业", "cost": 53.087, "shares": 100,
               "stop": 50.50, "target": 58.00, "ma5_alert": True},
    "002340": {"name": "格林美", "cost": 8.229, "shares": 200,
               "stop": 7.52, "target": 9.80, "ma5_alert": True},
}

# 候选池
CANDIDATES = {
    "000969": {"name": "安泰科技", "buy_low": 22.40, "buy_high": 22.80, "watch": True},
    "002185": {"name": "华天科技", "buy_low": 15.50, "buy_high": 16.00, "watch": True},
}

# ====== 工具函数 ======

def load_alerts():
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE) as f:
            return json.load(f)
    return {}

def save_alerts(a):
    with open(ALERT_FILE, "w") as f:
        json.dump(a, f)

def send_alert(msg):
    """发送告警到飞书/企微"""
    os.system(f'cc-connect send -p {PROJECT} --message "{msg}" > /dev/null 2>&1')

def is_trading_time():
    now = datetime.now()
    if now.weekday() >= 5:  # 周末
        return False
    t = now.time()
    return time(9, 25) <= t <= time(15, 5)

def get_quote(code):
    """拉取腾讯实时行情"""
    pfx = "sh" if code.startswith(("6","9")) else "sz"
    try:
        r = requests.get(f"https://qt.gtimg.cn/q={pfx}{code}", headers={"User-Agent": UA}, timeout=10)
        p = r.text.split("~")
        if len(p) > 40:
            return {
                "price": float(p[3]) if p[3] else 0,
                "change_pct": float(p[32]) if p[32] else 0,
                "high": float(p[33]) if p[33] else 0,
                "low": float(p[34]) if p[34] else 0,
                "turnover": float(p[38]) if p[38] else 0,
                "vol_ratio": float(p[47]) if p[47] else 0,
                "prev_close": float(p[4]) if p[4] else 0,
            }
    except:
        pass
    return None

def get_kline_ma(code, days=20):
    """拉K线计算MA"""
    pfx = "sh" if code.startswith(("6","9")) else "sz"
    try:
        url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={pfx}{code},day,,,{days+5},qfq"
        r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
        klines = r.json().get("data", {}).get(f"{pfx}{code}", {}).get("qfqday", [])
        if klines:
            closes = [float(k[2]) for k in klines[-days:]]
            ma5 = sum(closes[-5:]) / 5 if len(closes) >= 5 else 0
            ma10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else 0
            return {"ma5": ma5, "ma10": ma10, "closes": closes[-5:]}
    except:
        pass
    return None

def should_alert(key, alert_type, alerts):
    """防重复告警：同样信号30分钟内不重复"""
    now = datetime.now().isoformat()
    ak = f"{key}:{alert_type}"
    if ak in alerts:
        last = datetime.fromisoformat(alerts[ak])
        if (datetime.now() - last).seconds < 1800:  # 30分钟
            return False
    alerts[ak] = now
    return True

# ====== 扫描逻辑 ======

def scan_positions(alerts):
    """扫描持仓股"""
    msgs = []
    for code, cfg in POSITIONS.items():
        q = get_quote(code)
        if not q:
            continue
        price = q["price"]
        name = cfg["name"]
        profit = (price - cfg["cost"]) * cfg["shares"]
        profit_pct = (price / cfg["cost"] - 1) * 100

        # 1. 止损预警
        if price <= cfg["stop"] * 1.03:  # 距离止损3%以内
            if should_alert(code, "stop_close", alerts):
                msgs.append(f"🚨 {name} 逼近止损！现价{price} 止损{cfg['stop']} 距止损{(price-cfg['stop'])/cfg['stop']*100:.1f}%")

        # 2. 止盈触发
        if price >= cfg["target"]:
            if should_alert(code, "target_hit", alerts):
                msgs.append(f"🎯 {name} 触及止盈！现价{price} (+{profit_pct:.1f}%) 盈利{profit:.0f}元")

        # 3. 大幅波动（>3%）
        if abs(q["change_pct"]) >= 3:
            if should_alert(code, "big_move", alerts):
                direction = "📈" if q["change_pct"] > 0 else "📉"
                msgs.append(f"{direction} {name} {q['change_pct']:+.1f}% 现价{price}")

        # 4. 放量（量比>3）
        if q["vol_ratio"] >= 3:
            if should_alert(code, "volume_spike", alerts):
                msgs.append(f"📊 {name} 突然放量！量比{q['vol_ratio']:.0f} 换手{q['turnover']}%")

        # 5. V型反转（低开>2%但现转正）
        if q["prev_close"] > 0 and q["low"] <= q["prev_close"] * 0.98 and q["change_pct"] > 0:
            if should_alert(code, "v_reversal", alerts):
                msgs.append(f"✅ {name} V型反转！低{((q['low']/q['prev_close']-1)*100):.1f}%→现+{q['change_pct']:.1f}%")

    return msgs

def scan_candidates(alerts):
    """扫描候选池"""
    msgs = []
    for code, cfg in CANDIDATES.items():
        if not cfg.get("watch"):
            continue
        q = get_quote(code)
        if not q:
            continue
        price = q["price"]
        name = cfg["name"]
        buy_low = cfg["buy_low"]
        buy_high = cfg["buy_high"]

        # 进入买入区间
        if buy_low <= price <= buy_high:
            if should_alert(code, "in_zone", alerts):
                msgs.append(f"💰 {name}({code}) 进入买入区！现价{price} 目标区间{buy_low}-{buy_high}")

        # 接近买入区间（上方5%以内）
        elif price <= buy_high * 1.05 and price > buy_high:
            if should_alert(code, "near_zone", alerts):
                msgs.append(f"👀 {name}({code}) 接近买入区 现价{price} 还需跌{(price-buy_high)/buy_high*100:.1f}%")

        # 大幅回调中（正在逼近目标）
        elif price <= buy_high * 1.10 and q["change_pct"] < -1:
            if should_alert(code, "dropping", alerts):
                msgs.append(f"⬇️ {name}({code}) 回调中 {q['change_pct']:+.1f}% 现价{price} 目标{buy_high}")

    return msgs

def scan_sectors():
    """扫描板块异动"""
    msgs = []
    # 拉行业板块TOP3涨幅
    try:
        url = "https://push2.eastmoney.com/api/qt/clist/get"
        params = {"pn": "1", "pz": "3", "po": "1", "np": "1", "fltt": "2", "invt": "2",
                  "fs": "m:90+t:2", "fields": "f2,f3,f4,f14"}
        r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=10)
        top3 = r.json().get("data", {}).get("diff", [])
        # 如果有板块涨超5%，提示
        for item in top3:
            chg = float(item.get("f3", 0))
            if chg >= 5:
                msgs.append(f"🔥 板块暴动：{item['f14']} +{chg}%")
    except:
        pass
    return msgs

# ====== 主流程 ======

def main():
    if not is_trading_time():
        return

    alerts = load_alerts()
    all_msgs = []

    # 1. 扫描持仓
    all_msgs += scan_positions(alerts)

    # 2. 扫描候选池
    all_msgs += scan_candidates(alerts)

    # 3. 板块异动（每个小时跑一次）
    now = datetime.now()
    if now.minute < 10:  # 整点附近
        all_msgs += scan_sectors()

    save_alerts(alerts)

    if all_msgs:
        for msg in all_msgs[:5]:  # 最多发5条，避免轰炸
            print(f"[{now.strftime('%H:%M')}] {msg}")
            send_alert(msg)


if __name__ == "__main__":
    main()
    print(f"[{datetime.now().strftime('%H:%M')}] 扫描完成")
