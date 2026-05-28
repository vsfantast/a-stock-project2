#!/usr/bin/env python3
"""V3.0 初选模块 — 标准化选股第一步
全市场候选池 → 7层过滤 → TOP10 → 输出到 V2.9 深度分析
"""
import requests, json, sys
UA = 'Mozilla/5.0'

# ====== 配置 ======
MIN_TURNOVER = 1.0  # 最小换手率%
MIN_RSI = 25      # RSI下限
MAX_RSI = 80      # RSI上限

# ====== 市值配置（V3.2） ======
MCAP_LARGE   = 500   # 大盘股（亿）
MCAP_SMALL   = 100   # 小盘股（亿）

# ====== 板块别名映射（V3.2 — 解决东财行业名与候选池名不匹配） ======
SECTOR_ALIASES = {
    "半导体":   "半导体/封测",
    "封测":     "半导体/封测",
    "集成电路": "半导体/封测",
    "芯片":     "半导体/封测",
    "分立器件": "半导体/封测",
    "被动元件": "电子/被动元件",
    "MLCC":    "电子/被动元件",
    "锂":       "新能源/锂电",
    "能源金属": "新能源/锂电",
    "电池":     "新能源/锂电",
    "光伏":     "光伏/储能",
    "储能":     "光伏/储能",
    "钨":       "有色金属",
    "稀土":     "有色金属",
    "铜":       "有色金属",
    "锡":       "有色金属",
    "小金属":   "有色金属",
    "玻纤":     "化工/玻纤",
    "磨具":     "化工/玻纤",
    "有机硅":   "化工/玻纤",
    "新材料":   "新材料",
    "军工":     "军工/高端制造",
    "航空":     "军工/高端制造",
    "机器人":   "机器人/自动化",
    "自动化":   "机器人/自动化",
    "汽车":     "汽车/零部件",
    "医药":     "医药",
    "白酒":     "消费/白酒",
    "电力":     "电力/能源",
    "通信":     "通信/5G",
    "5G":       "通信/5G",
}

def match_sector(eastmoney_sector_name):
    """东财板块名 → 候选池名"""
    for key, target in SECTOR_ALIASES.items():
        if key in eastmoney_sector_name:
            return target
    return None
CASH = 2800  # 可用资金（可手动调整）

# ====== 候选池（V3.1 扩展至 65 支，覆盖 14 个行业） ======
UNIVERSE = {
    "半导体/封测": [
        ("002185","华天科技"),("002156","通富微电"),("600584","长电科技"),
        ("603005","晶方科技"),("002079","苏州固锝"),("600460","士兰微"),
        ("002049","紫光国微"),
    ],
    "电子/被动元件": [
        ("603678","火炬电子"),("000636","风华高科"),("002138","顺络电子"),
    ],
    "新能源/锂电": [
        ("002460","赣锋锂业"),("002466","天齐锂业"),("002340","格林美"),
        ("002407","多氟多"),("000762","西藏矿业"),("002192","融捷股份"),
    ],
    "光伏/储能": [
        ("601012","隆基绿能"),("002459","晶澳科技"),("600438","通威股份"),
        ("002518","科士达"),
    ],
    "有色金属": [
        ("600549","厦门钨业"),("600111","北方稀土"),("000831","中国稀土"),
        ("000630","铜陵有色"),("000960","锡业股份"),("000603","盛达资源"),
    ],
    "新材料": [
        ("000969","安泰科技"),("002130","沃尔核材"),("600516","方大炭素"),
        ("002171","楚江新材"),
    ],
    "化工/玻纤": [
        ("600176","中国巨石"),("002080","中材科技"),("600596","新安股份"),
        ("600309","万华化学"),("000830","鲁西化工"),
    ],
    "军工/高端制造": [
        ("000768","中航西飞"),("002013","中航机电"),("600893","航发动力"),
        ("600760","中航沈飞"),("002025","航天电器"),
    ],
    "机器人/自动化": [
        ("002747","埃斯顿"),("002527","新时达"),("300124","汇川技术"),
    ],
    "汽车/零部件": [
        ("000625","长安汽车"),("601238","广汽集团"),("002594","比亚迪"),
        ("000338","潍柴动力"),
    ],
    "医药": [
        ("000538","云南白药"),("600276","恒瑞医药"),("002001","新和成"),
        ("000963","华东医药"),
    ],
    "消费/白酒": [
        ("000858","五粮液"),("600519","贵州茅台"),("000568","泸州老窖"),
    ],
    "电力/能源": [
        ("600900","长江电力"),("601985","中国核电"),("600011","华能国际"),
    ],
    "通信/5G": [
        ("000063","中兴通讯"),("600498","烽火通信"),("002396","星网锐捷"),
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

# ====== PE 周期股白名单（这些行业高PE ≠ 差） ======
CYCLE_SECTORS = {"有色金属","新能源/锂电","化工/玻纤","新材料","钢铁/煤炭"}

def is_cycle_stock(sector):
    return any(c in sector for c in CYCLE_SECTORS)

def calc_m0(hot_list):
    """M0: 用板块强度估算市场环境"""
    gt5 = sum(1 for _,c in hot_list if c > 5)
    gt3 = sum(1 for _,c in hot_list if c > 3)
    if gt5 >= 3:    return "HOT"
    elif gt3 >= 3:  return "NORMAL"
    elif gt3 >= 1:  return "FAST"
    return "COLD"

def get_m0_weights(mode):
    """M0 动态权重"""
    if mode == "HOT":
        return {"sector":4, "trend":3, "rsi":1}
    elif mode in ("NORMAL","FAST"):
        return {"trend":4, "rsi":3, "sector":1}
    else:
        return {"rsi":5, "trend":2, "sector":1}

def screen():
    hot_sectors, updated = get_hot_sectors()
    # 从hot_sectors提取板块名和涨幅
    hot_list = []
    for s in hot_sectors:
        # hot_sectors is set of strings like "磨具磨料"
        hot_list.append((s, 5.0))  # 东财数据已过滤>1%的板块

    # 重新获取实际涨幅
    try:
        r_raw = requests.get("https://jsonblob.com/api/jsonBlob/019e6c05-9fb5-784c-b0b6-1c2f159a84ee", headers={'User-Agent': UA}, timeout=5)
        d_raw = r_raw.json()
        ind_raw = json.loads(d_raw['industry']) if isinstance(d_raw['industry'],str) else d_raw['industry']
        hot_list = [(i['f14'], float(i['f3'])) for i in ind_raw['data']['diff'][:10]]
        hot_names = {i['f14'] for i in ind_raw['data']['diff'][:10] if float(i['f3']) > 1}
    except:
        hot_names = hot_sectors

    m0 = calc_m0(hot_list)
    w = get_m0_weights(m0)

    results = []
    total = sum(len(v) for v in UNIVERSE.values())
    passed = [total, 0, 0, 0, 0, 0, 0, 0]

    for sector, stocks in UNIVERSE.items():
        # V3.2: 板块双向匹配
        in_main = False
        for h in hot_names:
            matched = match_sector(h)
            if matched and matched == sector:
                in_main = True; break
            if h in sector or any(kw in h for kw in sector.split('/')):
                in_main = True; break

        for code, name in stocks:
            q = get_quote(code)
            if not q: continue; passed[1] += 1

            # L2: 价格 — 1手<=可用资金×1.6
            cost = q['price'] * 100
            if cost > CASH * 1.6: continue; passed[2] += 1

            # L3: 流动性
            if q['turnover'] < MIN_TURNOVER: continue; passed[3] += 1

            # L4: 非暴跌
            if q['chg'] < -7: continue; passed[4] += 1

            # L5: PE — 周期股放宽到500，非周期200
            pe_limit = 500 if is_cycle_stock(sector) else 200
            if 0 < q['pe'] > pe_limit: continue; passed[5] += 1

            # L6: K线
            k = get_kline(code)
            if not k: continue; passed[6] += 1

            # L7: 趋势+RSI（HOT模式放宽RSI上限到90）
            rsi_max = 90 if m0 == "HOT" else (85 if m0 == "NORMAL" else MAX_RSI)
            if k['trend'] == '空头': continue
            if k['rsi'] < MIN_RSI or k['rsi'] > rsi_max: continue
            passed[7] += 1

            # === M0 动态评分 ===
            t_score = 0
            if k['trend'] == '多头': t_score = w['trend']
            elif k['trend'] == '纠缠': t_score = w['trend'] // 2

            r_score = 0
            if m0 == "HOT":
                r_score = 0 if k['rsi'] > 85 else w['rsi']
            elif m0 in ("NORMAL","FAST"):
                r_score = w['rsi'] if 30 < k['rsi'] < 75 else w['rsi']//2
            else:  # COLD
                r_score = w['rsi'] if k['rsi'] < 35 else (w['rsi']//2 if k['rsi'] < 50 else 0)

            s_score = w['sector'] if in_main else 0

            # 市值加分（V3.2）：大盘+1 小盘+1（不同风格各有优势）
            m_score = 1 if q['mcap'] > MCAP_LARGE else (1 if q['mcap'] < MCAP_SMALL else 0)

            score = t_score + r_score + s_score + m_score
            score += 1 if q['turnover'] > 3 else 0  # 活跃加分

            # V3.2: A/B 预分类
            if q['turnover'] > 12 and abs(q['chg']) > 3 and k['rsi'] > 60 and in_main:
                strat = 'A'
            else:
                strat = 'B'

            results.append({
                'code':code,'name':name,'price':q['price'],'chg':q['chg'],
                'pe':q['pe'],'turnover':q['turnover'],'mcap':q['mcap'],
                'trend':k['trend'],'rsi':k['rsi'],'atr_pct':k['atr_pct'],
                'cost':cost,'sector':sector,'main':in_main,
                'score':score, 'm0': m0, 'strat': strat
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results, passed, total, updated, hot_sectors, m0, w

if __name__ == "__main__":
    results, passed, total, updated, hot, m0, w = screen()

    print(f"东财更新:{updated}")
    print(f"M0模式:{m0}  权重:板块{w['sector']}/趋势{w['trend']}/RSI{w['rsi']}")
    print(f"候选池:{total}支 → 通过初选:{len(results)}支")
    print(f"过滤:行情{passed[1]}→价格{passed[2]}→流动{passed[3]}→非跌{passed[4]}→PE{passed[5]}→K线{passed[6]}→趋势RSI{passed[7]}")
    print()

    for i, r in enumerate(results[:10]):
        main_tag = '★' if r['main'] else ' '
        print(f"#{i+1} {r['name']}({r['code']}) {r['price']:.2f}元 {r['chg']:+.1f}% {r['trend']} RSI{r['rsi']:.0f} PE{r['pe']:.0f} [{r['strat']}] {r['sector']} {main_tag} {r['score']}分")
