#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成拓普集团(601689)深度分析报告PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.platypus.flowables import KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os

# ── Paths ──────────────────────────────────────────────────
OUTPUT = os.path.expanduser("~/Documents/项目/拓普集团601689_深度分析报告.pdf")

# ── Fonts ───────────────────────────────────────────────────
try:
    pdfmetrics.registerFont(TTFont('STHeiti', '/System/Library/Fonts/STHeiti Medium.ttc'))
    CN_FONT = 'STHeiti'
except:
    try:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        CN_FONT = 'STSong-Light'
    except:
        CN_FONT = 'Helvetica'

FONT_BOLD = CN_FONT

# ── Colors ──────────────────────────────────────────────────
C_PRIMARY   = HexColor('#1a365d')   # dark navy
C_SECONDARY = HexColor('#2b6cb0')   # blue
C_ACCENT    = HexColor('#c53030')   # red
C_GREEN     = HexColor('#276749')   # green
C_WARN      = HexColor('#dd6b20')   # orange warning
C_BG_LIGHT  = HexColor('#f7fafc')   # light bg
C_BG_HEADER = HexColor('#1a365d')   # header bg
C_BORDER    = HexColor('#e2e8f0')   # border
C_GREY      = HexColor('#718096')

# ── Styles ──────────────────────────────────────────────────
styles = getSampleStyleSheet()

body_style = ParagraphStyle('CNBody',
    fontName=CN_FONT, fontSize=10, leading=16,
    spaceAfter=6, textColor=black, alignment=TA_JUSTIFY)

title_style = ParagraphStyle('CNTitle',
    fontName=CN_FONT, fontSize=24, leading=30,
    spaceAfter=6, textColor=C_PRIMARY, alignment=TA_CENTER)

subtitle_style = ParagraphStyle('CNSubtitle',
    fontName=CN_FONT, fontSize=12, leading=16,
    spaceAfter=12, textColor=C_GREY, alignment=TA_CENTER)

h1_style = ParagraphStyle('CNH1',
    fontName=CN_FONT, fontSize=16, leading=22,
    spaceBefore=16, spaceAfter=8, textColor=C_PRIMARY)

h2_style = ParagraphStyle('CNH2',
    fontName=CN_FONT, fontSize=13, leading=18,
    spaceBefore=12, spaceAfter=6, textColor=C_SECONDARY)

h3_style = ParagraphStyle('CNH3',
    fontName=CN_FONT, fontSize=11, leading=15,
    spaceBefore=8, spaceAfter=4, textColor=black)

small_style = ParagraphStyle('CNSmall',
    fontName=CN_FONT, fontSize=8, leading=12,
    textColor=C_GREY, alignment=TA_CENTER)

warn_style = ParagraphStyle('CNWarn',
    fontName=CN_FONT, fontSize=10, leading=16,
    spaceAfter=6, textColor=C_ACCENT)

green_style = ParagraphStyle('CNGreen',
    fontName=CN_FONT, fontSize=10, leading=16,
    spaceAfter=6, textColor=C_GREEN)

quote_style = ParagraphStyle('CNQuote',
    fontName=CN_FONT, fontSize=10, leading=17,
    spaceAfter=10, textColor=C_PRIMARY, alignment=TA_CENTER,
    leftIndent=30, rightIndent=30)


# ── Helpers ─────────────────────────────────────────────────
def h1(text):
    return Paragraph(text, h1_style)

def h2(text):
    return Paragraph(text, h2_style)

def h3(text):
    return Paragraph(text, h3_style)

def body(text):
    return Paragraph(text, body_style)

def warn(text):
    return Paragraph(text, warn_style)

def green(text):
    return Paragraph(text, green_style)

def quote(text):
    return Paragraph(text, quote_style)

def spacer(h=6):
    return Spacer(1, h)

def hr():
    return HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceBefore=8, spaceAfter=8)

def make_table(headers, rows, col_widths=None):
    """Create a styled table with header row"""
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), C_BG_HEADER),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), CN_FONT),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('LEADING', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, C_BG_LIGHT]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


# ── Build Document ──────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=22*mm, rightMargin=22*mm,
    topMargin=20*mm, bottomMargin=20*mm,
    title='拓普集团(601689)深度分析报告',
    author='巴菲特神谕分析师'
)

story = []

# ═══════════════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════════════
story.append(spacer(40))
story.append(Paragraph("拓普集团（601689.SH）", title_style))
story.append(spacer(8))
story.append(Paragraph("巴菲特神谕 · 深度分析报告", subtitle_style))
story.append(spacer(8))
story.append(Paragraph("2026年5月18日 | 基于巴菲特投资框架的全面评估", small_style))
story.append(spacer(30))
story.append(hr())
story.append(spacer(16))

# Executive Summary
story.append(h1("🔮 巴菲特的裁决"))
story.append(spacer(6))
story.append(body(
    "拓普集团是中国汽车零部件行业中最优秀的平台型供应商之一，在NVH减震器和轻量化底盘领域拥有实质性护城河，"
    "并通过深度绑定特斯拉及其他头部新能源车企获得持续增长动力。但当前约<b>¥1,241亿市值、动态PE高达56倍</b>，"
    "市场已经为'特斯拉生态链核心标的'这个叙事支付了极高的溢价。<b>以巴菲特的标准来看，当前价格没有任何安全边际。</b>"
))
story.append(hr())
story.append(spacer(10))

# ═══════════════════════════════════════════════════════════
# Module 1: Company Overview
# ═══════════════════════════════════════════════════════════
story.append(h1("模块1：公司概览与背景"))

story.append(make_table(
    ['项目', '详情'],
    [
        ['证券代码', '601689.SH（上海证券交易所）'],
        ['当前股价', '¥71.42（2026年5月18日收盘）'],
        ['总市值', '¥1,241.16亿'],
        ['流通市值', '¥1,241.16亿'],
        ['总股本', '约17.38亿股'],
        ['所属行业', '汽车零部件 — 底盘及NVH系统'],
        ['成立时间', '2001年（2015年A股上市）'],
        ['注册地', '浙江省宁波市'],
        ['创始人/实控人', '邬建树（持股约60%+）'],
    ],
    col_widths=[100, 400]
))
story.append(spacer(8))

story.append(h2("发展历程"))
story.append(body(
    "拓普集团起步于橡胶减震器制造，历经二十余年发展，已从单一NVH（噪声、振动、声振粗糙度）零部件供应商，"
    "演变为覆盖<b>减震器 + 内饰功能件 + 轻量化底盘 + 热管理系统 + 智能驾驶执行器</b>五大板块的Tier 0.5平台型供应商。"
    "关键跃迁发生在2019-2020年——深度切入特斯拉上海超级工厂供应链，实现了收入体量与资本市场关注度的质的飞跃。"
))

story.append(h2("股权结构"))
story.append(body(
    "创始人邬建树通过迈科国际控股持有公司约60%以上股份，股权集中度极高，控制权稳定。"
    "沪港通北向资金持续持有，反映外资对该标的的关注。限售股解禁压力整体较小，股权结构清晰。"
))

story.append(h2("一句话描述这家公司"))
story.append(quote(
    '"一家为新能源汽车（尤其是特斯拉）提供底盘+NVH+内饰+热管理一站式解决方案的平台型零部件供应商。"'
))

# ═══════════════════════════════════════════════════════════
# Module 2: Management
# ═══════════════════════════════════════════════════════════
story.append(h1("模块2：管理层评估"))

story.append(h2("核心人物：邬建树（创始人 / 董事长）"))
story.append(body(
    "邬建树是中国汽车零部件行业中极为低调的'匠人型'创始人。他很少出现在媒体聚光灯下，但在产业链内部享有极高声誉。"
    "他的管理风格更接近巴菲特欣赏的'主人翁型经理人'——以老板心态经营企业、长期主义导向、专注于制造工艺和技术积累。"
))

story.append(make_table(
    ['评估维度', '评级', '详细评价'],
    [
        ['资本配置能力', '⭐⭐⭐', '收购审慎，注重垂直整合；研发投入持续加大'],
        ['坦诚程度', '⭐⭐⭐', '公司交流相对朴实，不过度包装'],
        ['利益绑定', '⭐⭐⭐⭐', '创始人持股约60%+，与中小股东利益高度一致'],
        ['历史兑现', '⭐⭐⭐', '战略执行连贯，从NVH到底盘到热管理路径清晰'],
    ],
    col_widths=[90, 60, 370]
))
story.append(spacer(6))
story.append(body(
    "<b>结论：</b>邬建树是一位'骑手'质量较高的管理者。他不是夸夸其谈的CEO，更像深耕制造业的工程师型企业家。"
    "这一点在巴菲特的框架中是加分项。"
))

# ═══════════════════════════════════════════════════════════
# Module 3: Business Model
# ═══════════════════════════════════════════════════════════
story.append(h1("模块3：商业模式深度解析"))

story.append(make_table(
    ['业务板块', '估计占比', '核心客户', '行业地位'],
    [
        ['轻量化底盘系统', '~35%', '特斯拉、吉利、比亚迪', '国内前三'],
        ['NVH减震器', '~25%', '主流OEM全覆盖', '国内龙头'],
        ['内饰功能件', '~20%', '特斯拉、自主品牌', 'Tier 1'],
        ['热管理系统', '~15%', '特斯拉、新势力', '快速成长'],
        ['智能驾驶执行器', '~5%', '早期阶段', '布局期'],
    ],
    col_widths=[110, 60, 130, 80]
))
story.append(spacer(8))

story.append(h2("单位经济分析"))
story.append(body(
    "毛利率 <b>19.26%</b>（2026Q1），处于汽车零部件制造业的合理中等偏低水平。"
    "净利率 <b>8.35%</b>（2026Q1），在同业中属中等。商业模式特征为<b>高固定成本、高资本开支、规模效应驱动</b>——"
    "这意味着产能利用率对利润率的弹性很大，但同时也意味着下行周期中利润可能加速收缩。"
))

# ═══════════════════════════════════════════════════════════
# Module 4: Moat
# ═══════════════════════════════════════════════════════════
story.append(h1("模块4：经济护城河分析"))

story.append(make_table(
    ['护城河类型', '评级', '证据与判断'],
    [
        ['网络效应', '无', '零部件不是平台型产品，用户增加不直接提升产品价值'],
        ['转换成本', '窄→宽', '进入OEM供应链需2-4年认证周期；Tier 0.5平台化后切换成本极高'],
        ['成本优势', '窄', '规模效应+垂直整合；但铝/橡胶等原材料价格周期影响显著'],
        ['无形资产', '窄', '技术专利积累+客户认证壁垒，但品牌在消费端无影响力'],
        ['有效规模', '窄', '底盘零部件市场容量大，可容纳多个玩家'],
    ],
    col_widths=[90, 60, 370]
))
story.append(spacer(8))

story.append(body(
    "<b>护城河总评：窄护城河，正在加宽中。</b>最核心的护城河来源是<b>转换成本+先发优势</b>的组合。"
    "一旦通过2-4年的认证周期进入核心OEM的Tier 0.5平台，就很难被轻易替换。"
    "但这条护城河不是牢不可破的——如果竞争对手在技术和成本上大幅超越，OEM仍会转向。"
))
story.append(warn(
    "<b>关键问题：</b>10年后护城河会更宽还是更窄？→ 取决于：(1) 能否在热管理和智能驾驶执行器上复制底盘的成功；"
    "(2) 客户集中度风险能否有效分散。目前概率中等偏上。"
))

# ═══════════════════════════════════════════════════════════
# Module 5: Financial Analysis
# ═══════════════════════════════════════════════════════════
story.append(h1("模块5：财务深度分析"))

story.append(h2("5.1 2026年Q1核心数据"))

story.append(make_table(
    ['财务指标', '2026Q1数值', '同比变化', '趋势信号'],
    [
        ['营业收入', '¥66.28亿', '+14.92%', '✅ 稳健增长'],
        ['归母净利润', '¥5.52亿', '-2.42%', '🔴 预警！'],
        ['扣非净利润', '¥4.73亿', '-2.77%', '🔴 预警！'],
        ['毛利率', '19.26%', '小幅下降', '⚠️ 承压'],
        ['净利率', '8.35%', '下降', '⚠️ 承压'],
        ['EPS（基本）', '¥0.32', '—', '—'],
        ['ROE（季度）', '2.27%', '年化约9%', '⚠️ 偏低'],
    ],
    col_widths=[100, 110, 110, 100]
))
story.append(spacer(8))

story.append(h2("5.2 核心估值与财务比率"))
story.append(make_table(
    ['指标', '数值', '行业参考', '评估'],
    [
        ['动态PE', '56.23x', '25-35x', '🔴 极贵'],
        ['PE TTM', '~63x', '25-35x', '🔴 极贵'],
        ['PB', '5.05x', '2-4x', '🟡 偏贵'],
        ['PS', '~4.5x', '1.5-3x', '🟡 偏贵'],
        ['ROE（年化）', '~9%', '>15%', '⚠️ 偏低'],
        ['资产负债率', '40.77%', '<60%', '✅ 健康'],
        ['流动比率', '1.32', '>1.5', '⚠️ 尚可'],
        ['速动比率', '1.05', '>1.0', '⚠️ 偏紧'],
    ],
    col_widths=[100, 100, 90, 100]
))
story.append(spacer(8))

story.append(h2("5.3 杜邦分析（年化估算）"))
story.append(body(
    "<b>ROE ≈ 净利率 × 资产周转率 × 杠杆倍数</b><br/>"
    "9% ≈ 8.35% × 0.65 × 1.69"
))
story.append(body(
    "ROE偏低的核心原因是<b>净利率不高</b>（制造业通病，OEM议价权强）和<b>资产周转率一般</b>（典型重资产模式）。"
    "ROE若要提升至15%+，要么净利率大幅改善（不太现实），要么通过更大规模的产能释放提高周转率。"
))

story.append(h2("5.4 资产负债健康度"))
story.append(green("✅ 资产负债率仅40.77%，在重资产制造业中属稳健水平"))
story.append(green("✅ 流动比率1.32，短期偿债风险可控"))
story.append(warn("⚠️ 速动比率1.05，流动资产中存货占比较高，变现能力需关注"))

story.append(h2("5.5 所有者盈余计算（巴菲特方法）"))
story.append(make_table(
    ['项目', '季度金额', '年化估算'],
    [
        ['归母净利润', '¥5.52亿', '¥22.08亿'],
        ['+ 折旧与摊销（估）', '¥1.5亿', '¥6.0亿'],
        ['- 维护性资本开支（估）', '¥0.8亿', '¥3.2亿'],
        ['= 所有者盈余', '<b>¥6.22亿</b>', '<b>¥24.88亿</b>'],
    ],
    col_widths=[160, 120, 120]
))
story.append(spacer(6))
story.append(warn(
    "<b>所有者盈余收益率 = 24.88亿 / 1241亿 ≈ 2.0%</b> —— 远低于巴菲特偏好的10%+门槛，"
    "也低于当前中国10年期国债收益率（约1.7%）+ 风险溢价的合理要求。"
))

story.append(h2("5.6 ⚠️ 核心预警信号"))
story.append(warn(
    "<b>增收不增利！</b>——2026年Q1营收同比增长14.92%，但净利润同比下降2.42%。"
    "这是本报告最重要的财务红灯。可能原因：原材料成本上升、OEM降价压力传导、新业务初期毛利偏低。"
    "如果这个趋势在Q2延续，当前估值将面临重大压力。"
))

# ═══════════════════════════════════════════════════════════
# Module 7: Valuation
# ═══════════════════════════════════════════════════════════
story.append(h1("模块7：多模型估值"))

story.append(h2("7.1 相对估值"))
story.append(make_table(
    ['估值指标', '拓普集团', '行业均值', '自身5年均值', '偏离度'],
    [
        ['PE（动态）', '56.23x', '25-35x', '35-45x', '偏高30-60%'],
        ['PB', '5.05x', '2-4x', '3-5x', '偏高'],
        ['PS', '~4.5x', '1.5-3x', '2-4x', '偏高'],
    ],
    col_widths=[90, 80, 80, 80, 80]
))
story.append(spacer(8))

story.append(h2("7.2 DCF估值（三种情景）"))
story.append(make_table(
    ['情景', '增速假设', '永续增长率', '合理市值', '对应股价'],
    [
        ['乐观', '20%/5年 → 15%/5年', '3%', '¥1,500亿', '¥86'],
        ['基准', '15%/5年 → 10%/5年', '2%', '¥1,050亿', '¥60'],
        ['悲观', '10%/5年 → 5%/5年', '1.5%', '¥780亿', '¥45'],
    ],
    col_widths=[50, 140, 70, 80, 70]
))
story.append(spacer(8))

story.append(h2("7.3 反向DCF——市场在说什么？"))
story.append(body(
    "当前¥1,241亿市值<b>隐含的未来5年净利润复合增长率约为18-20%</b>。"
    "考虑到2026年Q1净利润已经同比下滑2.4%，这个隐含增长率的要求相当苛刻。"
    "市场先生目前处于<b>过度乐观</b>的状态。"
))

story.append(h2("7.4 估值汇总"))
story.append(make_table(
    ['估值方法', '合理价值区间（元/股）', '适用性'],
    [
        ['相对估值法（30-40x PE）', '¥52 - 70', '主要参考'],
        ['DCF基准情景', '¥60', '主要参考'],
        ['所有者盈余法', '¥30 - 40', '巴菲特标准（严格）'],
        ['反向DCF检验', '当前价隐含18-20%增长', '参考'],
        ['<b>综合合理区间</b>', '<b>¥50 - 68</b>', ''],
    ],
    col_widths=[160, 140, 110]
))
story.append(spacer(6))
story.append(warn(
    "<b>当前价格¥71.42 > 合理区间上沿¥68。安全边际为负。</b>"
))

# ═══════════════════════════════════════════════════════════
# Module 8: Competition
# ═══════════════════════════════════════════════════════════
story.append(h1("模块8：竞争与行业分析"))

story.append(h2("主要竞争对手"))
story.append(make_table(
    ['竞争对手', '代码', '竞争领域', '对比拓普的差异'],
    [
        ['中鼎股份', '000887', '橡胶件/NVH', '传统对手，拓普在新能源领域领先'],
        ['伯特利', '603596', '线控制动', '更专注于制动，拓普平台化更广'],
        ['三花智控', '002050', '热管理', '热管理专家，拓普是后来者'],
        ['旭升集团', '603305', '铝合金零部件', '同为特斯拉供应商，体量较小'],
    ],
    col_widths=[80, 70, 90, 200]
))
story.append(spacer(8))

story.append(h2("波特五力速览"))
story.append(make_table(
    ['竞争力量', '强度', '核心判断'],
    [
        ['供应商议价力', '中', '铝/橡胶大宗商品，价格周期波动大'],
        ['买方议价力', '<b>强</b>', 'OEM客户集中；特斯拉/比亚迪谈判力强大'],
        ['新进入者威胁', '低', '2-4年认证周期+高资本门槛'],
        ['替代品威胁', '低', '底盘零部件短期内没有替代方案'],
        ['行业内竞争', '中高', '多家同质化供应商争夺份额'],
    ],
    col_widths=[100, 60, 280]
))

story.append(h2("差异化优势评估"))
story.append(body(
    "拓普的核心差异化在于<b>平台化（Tier 0.5）供应模式</b>——同时为OEM提供多个子系统，"
    "减少其供应链管理复杂度。这种模式一旦形成，客户粘性很强。但三花、旭升等竞争对手也在走类似路线，"
    "先发优势窗口正在收窄。"
))

# ═══════════════════════════════════════════════════════════
# Module 9: Technical Analysis
# ═══════════════════════════════════════════════════════════
story.append(h1("模块9：技术面与K线分析"))
story.append(Paragraph("（巴菲特本人不使用技术分析，本节仅供交易型投资者参考）", small_style))
story.append(spacer(6))

story.append(h2("近期走势（2026年5月）"))
story.append(make_table(
    ['日期', '开盘', '最高', '最低', '收盘', '成交量(手)', '信号'],
    [
        ['5/06', '60.68', '62.87', '60.50', '62.04', '436,908', '起涨'],
        ['5/07', '62.45', '64.64', '61.68', '64.47', '496,047', '连阳'],
        ['5/08', '64.20', '68.83', '63.88', '66.89', '721,031', '放量突破'],
        ['5/11', '67.60', '67.93', '65.99', '66.96', '486,960', '整固'],
        ['5/12', '67.50', '68.36', '66.22', '67.05', '385,132', '缩量'],
        ['5/13', '66.33', '67.29', '65.34', '67.09', '369,700', '缩量'],
        ['5/14', '67.55', '67.80', '65.03', '65.08', '368,949', '缩量调整'],
        ['5/15', '65.08', '71.59', '64.70', '69.93', '<b>945,204</b>', '🔥 爆量拉升'],
        ['5/18', '70.00', '72.88', '69.49', '<b>71.42</b>', '774,581', '高开震荡'],
    ],
    col_widths=[42, 52, 52, 52, 52, 65, 65]
))
story.append(spacer(8))

story.append(h2("技术信号汇总"))
story.append(green("✅ <b>趋势：</b>短期强势多头，从60.68到71.42（±2周+17.7%）"))
story.append(green("✅ <b>量价配合：</b>5/15放量至94.5万手（平时2倍），机构资金入场迹象明显"))
story.append(body("📌 <b>关键阻力位：</b>72.88（今日高点）/ 76.92（52周高点）"))
story.append(body("📌 <b>关键支撑位：</b>69.49（今日低点）/ 65.00区域 / 62.00区间"))
story.append(warn("⚠️ <b>超买风险：</b>连续两周急涨17%+，RSI大概率进入超买区域（>70），短期获利回吐压力大"))
story.append(warn("⚠️ <b>总体判断：</b>短期趋势强劲但已超买；中长期仍处于52周中位区域，方向不明"))

# ═══════════════════════════════════════════════════════════
# Module 10: Catalysts
# ═══════════════════════════════════════════════════════════
story.append(h1("模块10：增长催化剂与前景展望"))

story.append(h2("顺风"))
story.append(green("✅ 中国新能源车渗透率仍有提升空间，2025年已超50%，向60-70%推进"))
story.append(green("✅ 特斯拉Cybertruck量产/下一代平台带来新增量机会"))
story.append(green("✅ 智能驾驶执行器（线控制动/转向）是下一波核心增长点"))
story.append(green("✅ 海外产能布局（墨西哥/欧洲工厂）打开全球化空间"))

story.append(h2("逆风"))
story.append(warn("⚠️ 整车降价压力持续向上游传导——'增收不增利'的根源"))
story.append(warn("⚠️ 原材料（铝/橡胶）价格波动影响毛利率"))
story.append(warn("⚠️ 地缘政治不确定性（中美关税、供应链重构风险）"))

story.append(h2("催化剂日历"))
story.append(make_table(
    ['时间', '事件', '重要性', '关注要点'],
    [
        ['2026年7月初', '特斯拉Q2交付数据', '⭐⭐⭐⭐⭐', '直接传导至拓普订单预期'],
        ['2026年8月底', '拓普2026年中报', '⭐⭐⭐⭐⭐', '利润率是否企稳是关键'],
        ['持续', '热管理/执行器新订单', '⭐⭐⭐⭐', '新业务拓展验证成长逻辑'],
        ['持续', '大宗商品价格走势', '⭐⭐⭐', '铝价影响毛利率'],
    ],
    col_widths=[90, 120, 70, 150]
))

# ═══════════════════════════════════════════════════════════
# Module 11: Risks
# ═══════════════════════════════════════════════════════════
story.append(h1("模块11：风险矩阵"))

story.append(make_table(
    ['风险类别', '评级(1-5)', '具体描述'],
    [
        ['估值风险', '🔴 5 - 关键', '56x动态PE，任何业绩miss都可能触发戴维斯双杀'],
        ['客户集中度', '🔴 4', '特斯拉占比估计仍在30-40%，单客户风险突出'],
        ['利润率侵蚀', '🔴 4', 'Q1净利润同比下降，增收不增利，趋势令人担忧'],
        ['竞争加剧', '🟡 3', '其他供应商也在走平台化路线，护城河并非不可逾越'],
        ['原材料波动', '🟡 3', '铝/橡胶价格直接影响毛利率'],
        ['地缘政治', '🟡 3', '中美关系影响特斯拉供应链逻辑'],
        ['宏观周期', '🟡 3', '汽车是周期性行业，经济下行时首当其冲'],
        ['技术替代', '🟢 2', '底盘零部件10年内被替代的概率较低'],
    ],
    col_widths=[90, 70, 290]
))
story.append(spacer(8))

story.append(h2("黑天鹅情景"))
story.append(warn(
    "<b>最坏情况推演：</b>特斯拉在中国市场份额大幅下滑 + 原材料价格暴涨 + 整车厂强制降价 → "
    "营收下滑叠加利润率崩塌 → 戴维斯双杀（业绩×估值同步收缩）→ 股价可能跌至<b>¥35-40区域（较当前-50%）</b>。"
    "这并非完全不可想象——2022-2024年特斯拉股价波动期间，拓普的波动幅度往往更大。"
))

# ═══════════════════════════════════════════════════════════
# Module 12: Buffett Scorecard
# ═══════════════════════════════════════════════════════════
story.append(h1("模块12：巴菲特计分卡"))

story.append(make_table(
    ['评估标准', '得分', '证据摘要'],
    [
        ['业务是否易于理解', '2/3', '汽车零件制造，不算复杂；但技术迭代较快'],
        ['经营历史是否一致', '2/3', '战略连贯，稳步扩张，路径清晰'],
        ['长期前景是否良好', '2/3', '新能源车+智能化是长赛道'],
        ['管理层坦诚与理性', '3/3', '邬建树务实低调，不炒作概念'],
        ['主人翁经营心态', '3/3', '创始人持股60%+，高度利益绑定'],
        ['高ROE + 低负债', '1/3', 'ROE仅~9%，负债率40%尚可'],
        ['强劲自由现金流', '1/3', '扩张期资本开支大，FCF偏弱'],
        ['宽广经济护城河', '2/3', '窄护城河，有加宽趋势'],
        ['保守会计处理', '2/3', '制造业，会计操纵风险较低'],
        ['存在安全边际', '<b>0/3</b>', '当前价¥71.42 > 合理估值上沿¥68'],
        ['定价能力（抗通胀）', '1/3', 'OEM议价权弱，成本转嫁能力有限'],
        ['低资本再投入需求', '1/3', '重资产模式，持续需要大额资本支出'],
        ['<b>总分</b>', '<b>20/36</b>', '<b>C级 — 一般</b>'],
    ],
    col_widths=[120, 50, 280]
))
story.append(spacer(8))

story.append(make_table(
    ['等级', '分数区间', '含义'],
    [
        ['A级', '30-36分', '杰出公司——巴菲特会认真考虑'],
        ['B级', '24-29分', '优秀公司——值得深入研究'],
        ['<b>C级</b>', '<b>18-23分</b>', '<b>一般——不适合巴菲特式价值投资</b>'],
        ['D级', '12-17分', '令人担忧——回避'],
        ['F级', '<12分', '垃圾——坚决回避'],
    ],
    col_widths=[50, 80, 220]
))

# ═══════════════════════════════════════════════════════════
# Final Decision
# ═══════════════════════════════════════════════════════════
story.append(h1("🎯 最终投资决策"))

story.append(make_table(
    ['决策维度', '结论'],
    [
        ['综合评级', '<b>⚠️ 持有/观望（不建议新建仓位）</b>'],
        ['12个月目标价（基准）', '¥60 - 68'],
        ['当前价格', '<b>¥71.42</b>'],
        ['潜在空间', '下行约10-15%至合理区间'],
        ['建议仓位占比', '0%（等待更好入场时机）'],
    ],
    col_widths=[140, 310]
))
story.append(spacer(8))

story.append(h2("分批建仓策略（如决定买入）"))
story.append(make_table(
    ['批次', '买入价位', '仓位占比', '逻辑'],
    [
        ['首仓', '¥62 - 65', '30%', '回到支撑位 + 估值进入合理区间上沿'],
        ['二仓', '¥55 - 60', '30%', 'DCF基准估值区 + 安全边际出现'],
        ['三仓', '¥48 - 52', '40%', '悲观情景估值 + 显著安全边际'],
    ],
    col_widths=[50, 80, 70, 250]
))
story.append(spacer(8))

story.append(h2("卖出/减仓信号"))
story.append(make_table(
    ['信号类型', '触发条件', '操作'],
    [
        ['🛑 止损', '跌破¥58（较当前-19%）', '无条件清仓'],
        ['🟡 减仓', 'PE超过65x / 连续两季净利润下滑', '减至半仓'],
        ['🟢 止盈', '¥85 - 90区间', '分批兑现'],
        ['🔴 清仓', '失去特斯拉核心供应商地位', '立即清仓'],
    ],
    col_widths=[80, 200, 150]
))
story.append(spacer(8))

story.append(h2("核心监控指标"))
story.append(body("1. <b>毛利率趋势</b> — 能否稳定在19%以上是利润率能否企稳的领先指标"))
story.append(body("2. <b>净利润增速</b> — 必须转正并与营收增速匹配，否则估值逻辑崩塌"))
story.append(body("3. <b>特斯拉交付量</b> — 最大客户的基本面晴雨表"))
story.append(body("4. <b>客户多元化进展</b> — 非特斯拉客户收入占比的边际变化"))
story.append(body("5. <b>新业务利润贡献</b> — 热管理/智能驾驶执行器的收入和利润率"))

story.append(h2("下一个催化剂日期"))
story.append(body("📅 <b>2026年7月初</b> — 特斯拉Q2交付数据（对拓普有直接传导效应）"))
story.append(body("📅 <b>2026年8月底</b> — 拓普集团2026年中报（最关键的业绩检验窗口）"))
story.append(body("📅 <b>持续关注</b> — 大宗商品（铝）价格走势、中美贸易政策变化"))

# ═══════════════════════════════════════════════════════════
# Buffett Final Word
# ═══════════════════════════════════════════════════════════
story.append(spacer(20))
story.append(hr())
story.append(spacer(12))
story.append(h1("🗣️ 巴菲特最可能说的话"))
story.append(spacer(8))
story.append(quote(
    '"拓普是一家好公司，由一位务实的创始人经营，在一个有前景的行业里。但好公司不等于好投资。<br/><br/>'
    '以56倍市盈率买一家净利率只有8%、利润还在下滑的公司，这不是投资，这是投机。<br/><br/>'
    '我会把它放在我的观察清单上，然后等市场先生变得恐慌时再打电话给我。"'
))
story.append(spacer(12))
story.append(hr())

# ═══════════════════════════════════════════════════════════
# Disclaimer
# ═══════════════════════════════════════════════════════════
story.append(spacer(16))
story.append(Paragraph("⚠️ 免责声明", h3_style))
story.append(body(
    "本分析仅供教育和研究用途，不构成投资建议。'巴菲特'视角是一个受沃伦·巴菲特公开表述的投资原则启发的分析框架——"
    "它并不代表沃伦·巴菲特本人对任何具体公司的观点。报告中使用的部分数据为估算值，可能与实际存在偏差。"
    "所有投资都有风险，过往表现不代表未来收益，请在做出投资决策前咨询合格的财务顾问。"
))
story.append(spacer(6))
story.append(Paragraph("报告生成时间：2026年5月18日 | 数据来源：东方财富、腾讯证券 | 分析框架：巴菲特神谕分析师", small_style))

# ── Generate PDF ──────────────────────────────────────────
doc.build(story)
print(f"✅ PDF已生成: {OUTPUT}")
print(f"文件大小: {os.path.getsize(OUTPUT) / 1024:.1f} KB")
