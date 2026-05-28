#!/usr/bin/env python3
"""V3.3 交易胜率统计面板"""
import os, re

LOG_DIR = "/home/ubuntu/a-stock-project/交易日志"

def parse_trades():
    trades = []
    if not os.path.exists(LOG_DIR):
        return trades
    for fname in sorted(os.listdir(LOG_DIR)):
        if fname.startswith('.') or '总览' in fname or not fname.endswith('.md'):
            continue
        parts = fname.replace('.md','').split('_')
        if len(parts) < 3: continue
        date, name, direction = parts[0], parts[1], parts[2]
        with open(os.path.join(LOG_DIR, fname)) as f:
            c = f.read()

        # 买入
        if '买入' in direction:
            cost_m = re.search(r'成本.*?(\d+\.?\d*)\s*元', c) or re.search(r'买入成本.*?(\d+\.?\d*)', c)
            shares_m = re.search(r'(\d+)\s*股', c)
            cost = float(cost_m.group(1)) if cost_m else 0
            shares = int(shares_m.group(1)) if shares_m else 0
            trades.append({'date':date,'name':name,'dir':'买入','price':cost,'shares':shares,'pl':0,'status':'holding'})
            continue

        # 卖出 — 匹配 **盈亏**：-222元（-6.4%）
        pl = 0; pl_pct = 0; sell_price = 0
        pl_m = re.search(r'盈亏.*?[：:]\s*([-+]?\d+\.?\d*)\s*元', c)
        if pl_m: pl = float(pl_m.group(1))
        pct_m = re.search(r'[（(]([-+]?\d+\.?\d*)%[）)]', c)
        if pct_m: pl_pct = float(pct_m.group(1))
        price_m = re.search(r'卖出价格[：:].*?(\d+\.?\d*)', c)
        if price_m: sell_price = float(price_m.group(1))
        trades.append({'date':date,'name':name,'dir':'卖出','price':sell_price,'pl':pl,'pl_pct':pl_pct,'status':'closed'})
    return trades

def dashboard():
    trades = parse_trades()
    closed = [t for t in trades if t['status']=='closed']
    holding = [t for t in trades if t['status']=='holding']
    wins = [t for t in closed if t['pl']>0]
    losses = [t for t in closed if t['pl']<0]
    total_pl = sum(t['pl'] for t in closed)
    wr = len(wins)/len(closed)*100 if closed else 0
    avg_w = sum(t['pl'] for t in wins)/len(wins) if wins else 0
    avg_l = sum(t['pl'] for t in losses)/len(losses) if losses else 0

    print("=" * 55)
    print("  交易胜率面板  V3.3")
    print("=" * 55)
    print(f"  已平仓: {len(closed)}笔 | 持仓: {len(holding)}支")
    print(f"  盈利: {len(wins)}笔 | 亏损: {len(losses)}笔")
    print(f"  胜率: {wr:.0f}% | 累计: {total_pl:+.0f}元")
    if avg_w > 0 and abs(avg_l) > 0:
        print(f"  均盈: {avg_w:+.0f}元 | 均亏: {avg_l:+.0f}元 | 盈亏比: {abs(avg_w/avg_l):.1f}:1")
    print()
    print("  明细:")
    for t in trades:
        if t['status']=='holding':
            print(f"    {t['date']} {t['name']} 买入 @{t['price']:.2f} 🔵持有")
        else:
            print(f"    {t['date']} {t['name']} 卖出 @{t['price']:.2f} {t['pl']:+.0f}元({'✅' if t['pl']>0 else '❌'})")

if __name__ == '__main__':
    dashboard()
