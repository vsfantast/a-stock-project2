#!/usr/bin/env python3
"""V3.0 初选模块 — 标准化选股第一步
全市场候选池 → 7层过滤 → TOP10 → 输出到 V2.9 深度分析
"""
import requests, json, sys
UA = 'Mozilla/5.0'

# ====== 配置 ======
MAX_PRICE = None  # 自动根据可用资金计算
MIN_TURNOVER = 1.0  # 最小换手率%
MAX_PE = 200  # 最大PE（纯题材过滤）
MIN_RSI = 25  # RSI下限
MAX_RSI = 80  # RSI上限
CASH = 2800  # 可用资金（可手动调整）

# ====== 候选池（按行业维护，定期更新） ======
UNIVERSE = {
    "半导体/封测": [
        ("002185","华天科技"),("002156","通富微电"),("600584","长电科技"),
        ("603005","晶方科技"),("002079","苏州固锝"),
    ],
    "电子元件": [
        ("603678","火炬电子"),("002049","紫光国微"),("600460","士兰微"),
    ],
    "新能源/锂电": [
        ("002460","赣锋锂业"),("002466","天齐锂业"),("002340","格林美"),
        ("002407","多氟多"),("000762","西藏矿业"),
    ],
    "有色金属": [
        ("600549","厦门钨业"),("600111","北方稀土"),("000831","中国稀土"),
        ("000630","铜陵有色"),("000960","锡业股份"),
    ],
    "新材料": [
        ("000969","安泰科技"),("002130","沃尔核材"),("600516","方大炭素"),
    ],
    "化工/玻纤": [
        ("600176","中国巨石"),("002080","中材科技"),("600596","新安股份"),
    ],
    "军工/高端制造": [
        ("000768","中航西飞"),("002013","中航机电"),("600893","航发动力"),
    ],
    "消费/医药": [
        ("000858","五粮液"),("600519","贵州茅台"),("000538","云南白药"),
    ],
}

def get_quote(code):
    pf = "sh" if code.startswith(("6","9")) else "sz"
    r = requests.get(f'https://qt.gtimg.cn/q={pf}{code}', headers={'User-Agent': UA}, timeout=5)
    p = r.text.split('~')
    if len(p) < 40: return None
    return {
        'price': float(p[3]) if p[3] else 0,
        'chg': float(p[32]) if p[32] else 0,
        'turnover': float(p[38]) if p[38] else 0,
        'pe': float(p[39]) if p[39] else 999,
        'mcap': float(p[45]) if p[45] else 0,
    }

def get_kline(code):
    pf = "sh" if code.startswith(("6","9")) else "sz"
    url = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={pf}{code},day,,,30,qfq'
    r = requests.get(url, headers={'User-Agent': UA}, timeout=5)
    klines = r.json().get('data',{}).get(f'{pf}{code}',{}).get('qfqday',[])
    if not klines or len(klines) < 20: return None

    closes = [float(k[2]) for k in klines[-20:]]
    ma5 = sum(closes[-5:])/5; ma10 = sum(closes[-10:])/10; ma20 = sum(closes[-20:])/20
    trend = '多头' if ma5>ma10>ma20 else ('空头' if ma5<ma10<ma20 else '纠缠')

    g,l=[],[]
    for i in range(1,min(15,len(closes))):
        c=closes[-i]-closes[-i-1]
        if c>0:g.append(c)
        else:l.append(abs(c))
    rsi = 100-(100/(1+sum(g)/max(sum(l),0.0001)))

    trs=[]
    for i in range(1,min(15,len(klines))):
        h=float(klines[-i][3]); lo=float(klines[-i][4]); pc=float(klines[-i-1][2])
        trs.append(max(h-lo,abs(h-pc),abs(lo-pc)))
    atr = sum(trs)/len(trs)

    return {'trend':trend,'rsi':rsi,'atr':atr,'atr_pct':atr/closes[-1]*100,'ma5':ma5,'ma10':ma10,'ma20':ma20}

def get_hot_sectors():
    """从东财实时数据获取今日主线板块"""
    try:
        r = requests.get("https://jsonblob.com/api/jsonBlob/019e6c05-9fb5-784c-b0b6-1c2f159a84ee", headers={'User-Agent': UA}, timeout=5)
        d = r.json()
        ind = json.loads(d['industry']) if isinstance(d['industry'],str) else d['industry']
        con = json.loads(d['concept']) if isinstance(d['concept'],str) else d['concept']
        hot = set()
        for item in ind['data']['diff'][:10]:
            if float(item['f3']) > 1:
                hot.add(item['f14'])
        for item in con['data']['diff'][:5]:
            if float(item['f3']) > 1:
                hot.add(item['f14'])
        return hot, d.get('updated','?')
    except:
        return set(), 'N/A'

def screen():
    """7层过滤"""
    hot_sectors, updated = get_hot_sectors()

    results = []
    total = 0
    passed = [0]*8  # 每层通过数

    for sector, stocks in UNIVERSE.items():
        # 检查是否在主线
        in_main = any(h in sector for h in hot_sectors)
        sector_score = 2 if in_main else 0

        for code, name in stocks:
            total += 1
            passed[0] += 1

            # L1: 获取行情
            q = get_quote(code)
            if not q: continue
            passed[1] += 1

            # L2: 价格
            cost = q['price'] * 100
            if cost > CASH * 1.6: continue  # 放宽到1.6倍（含卖出后资金）
            passed[2] += 1

            # L3: 流动性
            if q['turnover'] < MIN_TURNOVER: continue
            passed[3] += 1

            # L4: 非暴跌
            if q['chg'] < -7: continue
            passed[4] += 1

            # L5: PE过滤
            if q['pe'] > MAX_PE and q['pe'] > 0: continue
            passed[5] += 1

            # L6: 趋势+RSI
            k = get_kline(code)
            if not k: continue
            passed[6] += 1

            if k['trend'] == '空头': continue
            if k['rsi'] < MIN_RSI or k['rsi'] > MAX_RSI: continue
            passed[7] += 1

            # === 初选评分 ===
            score = 0
            score += 3 if k['trend'] == '多头' else (1 if k['trend'] == '纠缠' else 0)
            score += 3 if 40 < k['rsi'] < 70 else (2 if 30 < k['rsi'] < 75 else 1)
            score += sector_score
            score += 1 if q['turnover'] > 3 else 0

            results.append({
                'code':code,'name':name,'price':q['price'],'chg':q['chg'],
                'pe':q['pe'],'turnover':q['turnover'],'mcap':q['mcap'],
                'trend':k['trend'],'rsi':k['rsi'],'atr_pct':k['atr_pct'],
                'cost':cost,'sector':sector,'main':in_main,
                'score':score
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results, passed, total, updated, hot_sectors

if __name__ == "__main__":
    results, passed, total, updated, hot = screen()

    print(f"东财更新:{updated}")
    print(f"主线板块:{len(hot)}个")
    print(f"候选池:{total}支 → 通过初选:{len(results)}支")
    print(f"过滤:行情{passed[1]}→价格{passed[2]}→流动{passed[3]}→非跌{passed[4]}→PE{passed[5]}→K线{passed[6]}→趋势RSI{passed[7]}")
    print()

    for i, r in enumerate(results[:10]):
        main_tag = '★' if r['main'] else ' '
        print(f"#{i+1} {r['name']}({r['code']}) {r['price']:.2f}元 {r['chg']:+.1f}% {r['trend']} RSI{r['rsi']:.0f} PE{r['pe']:.0f} {r['sector']} {main_tag} 评分:{r['score']}/9")
