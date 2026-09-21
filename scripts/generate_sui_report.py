#!/usr/bin/env python3
"""Generate the SUI spot-hold and $2-target research PDF."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
)

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports"
ASSET_DIR = OUT_DIR / "assets" / "sui"
PDF_PATH = OUT_DIR / "SUI现货持有与中长期到2美元困难度_2026-09-21.pdf"

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
FONT_NAME = "WQYMicroHei"

NAVY = colors.HexColor("#0B1F33")
TEAL = colors.HexColor("#1B6CA8")
TEAL_DARK = colors.HexColor("#155A8A")
AMBER = colors.HexColor("#C45C26")
RED = colors.HexColor("#B42318")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#D6DEE8")
BG_SOFT = colors.HexColor("#F3F7FB")
BG_WARN = colors.HexColor("#FFF6ED")
BG_DANGER = colors.HexColor("#FDECEC")
WHITE = colors.white


def register_fonts() -> font_manager.FontProperties:
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH, subfontIndex=0))
    prop = font_manager.FontProperties(fname=FONT_PATH)
    plt.rcParams["font.family"] = prop.get_name()
    plt.rcParams["axes.unicode_minus"] = False
    return prop


def make_styles():
    getSampleStyleSheet()
    common = dict(fontName=FONT_NAME, wordWrap="CJK")
    return {
        "cover_kicker": ParagraphStyle("cover_kicker", **common, fontSize=10, textColor=TEAL_DARK, leading=16),
        "cover_title": ParagraphStyle("cover_title", **common, fontSize=22, textColor=NAVY, leading=32, spaceAfter=8),
        "cover_sub": ParagraphStyle("cover_sub", **common, fontSize=11.5, textColor=SLATE, leading=18),
        "h1": ParagraphStyle("h1", **common, fontSize=16, textColor=NAVY, leading=24, spaceBefore=14, spaceAfter=8),
        "h2": ParagraphStyle("h2", **common, fontSize=13, textColor=TEAL_DARK, leading=20, spaceBefore=11, spaceAfter=6),
        "h3": ParagraphStyle("h3", **common, fontSize=11.5, textColor=NAVY, leading=18, spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("body", **common, fontSize=10, textColor=SLATE, leading=16.5, alignment=TA_LEFT, spaceAfter=7),
        "bullet": ParagraphStyle("bullet", **common, fontSize=10, textColor=SLATE, leading=16, leftIndent=2, spaceAfter=3),
        "caption": ParagraphStyle("caption", **common, fontSize=8.5, textColor=MUTED, leading=13, alignment=TA_CENTER, spaceBefore=2, spaceAfter=10),
        "note": ParagraphStyle("note", **common, fontSize=9, textColor=SLATE, leading=14.5, alignment=TA_LEFT),
        "toc": ParagraphStyle("toc", **common, fontSize=11, textColor=SLATE, leading=20),
        "small": ParagraphStyle("small", **common, fontSize=8.5, textColor=MUTED, leading=13),
        "th": ParagraphStyle("th", **common, fontSize=8.4, textColor=WHITE, leading=12, alignment=TA_CENTER),
        "td": ParagraphStyle("td", **common, fontSize=8.3, textColor=SLATE, leading=12.2, alignment=TA_CENTER),
        "td_left": ParagraphStyle("td_left", **common, fontSize=8.3, textColor=SLATE, leading=12.2, alignment=TA_LEFT),
        "callout_title": ParagraphStyle("callout_title", **common, fontSize=10.5, textColor=NAVY, leading=16, spaceAfter=4),
    }


def p(text, style):
    return Paragraph(text, style)


def hr():
    return HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=2, spaceAfter=8)


def callout(title, body, styles, bg=BG_SOFT, border=TEAL):
    t = Table(
        [[p(f"<b>{title}</b>", styles["callout_title"])], [p(body, styles["note"])]],
        colWidths=[170 * mm],
    )
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.8, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (0, 0), 8),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def styled_table(headers, rows, col_widths, styles, left_cols=(0,)):
    head = [p(h, styles["th"]) for h in headers]
    body = []
    for row in rows:
        cells = []
        for i, val in enumerate(row):
            cells.append(p(str(val), styles["td_left"] if i in left_cols else styles["td"]))
        body.append(cells)
    t = Table([head] + body, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(body) + 1):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), BG_SOFT))
    t.setStyle(TableStyle(cmds))
    return t


def bullets(items, styles):
    return [p(f"• {item}", styles["bullet"]) for item in items]


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 11 * mm, w, 11 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, h - 12.1 * mm, w, 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont(FONT_NAME, 8)
    canvas.drawString(16 * mm, h - 7.2 * mm, "SUI 现货与中长期研究备忘  |  非投资建议")
    canvas.drawRightString(w - 16 * mm, h - 7.2 * mm, "快照日期 2026-09-21")
    canvas.setFillColor(colors.HexColor("#F1F5F9"))
    canvas.rect(0, 0, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_NAME, 8)
    canvas.drawString(16 * mm, 5 * mm, "公开信息交叉验证  ·  情景分析而非预测")
    canvas.drawRightString(w - 16 * mm, 5 * mm, f"{doc.page}")
    canvas.restoreState()


def apply_ticks(ax, prop):
    for label in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        label.set_fontproperties(prop)


def make_charts(prop):
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    paths = {}

    fig, ax = plt.subplots(figsize=(8.0, 3.5), dpi=160)
    supplies = [40.97, 45.00, 50.00, 60.00, 100.00]
    labels = ["40.97亿\n当前流通", "45亿", "50亿", "60亿", "100亿\n全稀释"]
    mcaps = [s * 2 for s in supplies]  # 亿枚 * 2美元 = 亿美元
    colors_bar = ["#1B6CA8", "#3D8FBF", "#4C6B8A", "#C45C26", "#B42318"]
    bars = ax.bar(labels, mcaps, color=colors_bar, width=0.62)
    ax.axhline(42.10, color="#64748B", ls="--", lw=1, label="当前流通市值约 42.10 亿美元")
    ax.set_ylabel("达到 2 美元时的流通市值（亿美元）", fontproperties=prop)
    ax.set_title("同一目标价 2 美元，流通盘放大后需要的市值仍在中型公链区间", fontproperties=prop)
    ax.yaxis.grid(True, ls=":", alpha=0.5)
    ax.set_axisbelow(True)
    for b, v in zip(bars, mcaps):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}", ha="center", va="bottom", fontsize=8, fontproperties=prop)
    ax.legend(prop=prop, fontsize=8, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    apply_ticks(ax, prop)
    p1 = ASSET_DIR / "chart_mc_at_2.png"
    fig.tight_layout(pad=0.6)
    fig.savefig(p1, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    paths["mc"] = p1

    fig, ax = plt.subplots(figsize=(8.0, 3.4), dpi=160)
    names = ["当前价", "目标 2 美元", "历史最高 5.37", "当前流通市值", "2美元流通市值", "2美元全稀释"]
    # mixed units - better split. Use price on left chart conceptually as levels
    levels = ["当前\n1.02", "目标\n2.00", "历史最高\n5.37"]
    vals = [1.0227, 2.00, 5.3681]
    c = ["#1B6CA8", "#C45C26", "#94A3B8"]
    ax.bar(levels, vals, color=c, width=0.5)
    ax.set_ylabel("美元", fontproperties=prop)
    ax.set_title("2 美元是回收到历史高点的 37%，不是新高幻想", fontproperties=prop)
    ax.yaxis.grid(True, ls=":", alpha=0.5)
    ax.set_axisbelow(True)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.08, f"{v:.2f}", ha="center", fontsize=8, fontproperties=prop)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    apply_ticks(ax, prop)
    p2 = ASSET_DIR / "chart_price_levels.png"
    fig.tight_layout(pad=0.6)
    fig.savefig(p2, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    paths["levels"] = p2

    fig, ax = plt.subplots(figsize=(8.0, 3.5), dpi=160)
    scenarios = ["熊市\n持续稀释", "基准\n震荡修复", "偏多\n生态回暖", "强牛\nL1轮动", "极端\n再挑战前高"]
    lows = [0.35, 0.70, 1.10, 1.60, 2.80]
    highs = [0.75, 1.50, 2.40, 3.50, 5.50]
    mids = [0.50, 1.10, 1.70, 2.40, 4.00]
    xs = range(len(scenarios))
    ax.vlines(xs, lows, highs, color="#0B1F33", lw=2)
    ax.scatter(xs, mids, s=42, color="#1B6CA8", zorder=3)
    ax.axhline(1.02, color="#C45C26", ls="--", lw=1, label="快照价约 1.02")
    ax.axhline(2.00, color="#B42318", ls=":", lw=1.2, label="目标 2.00")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(scenarios, fontproperties=prop)
    ax.set_ylabel("中长期价格带（美元）", fontproperties=prop)
    ax.set_title("主观情景带：2 美元落在偏多到强牛区间，基准也能碰到上沿", fontproperties=prop)
    ax.legend(prop=prop, fontsize=8, frameon=False, loc="upper left")
    ax.yaxis.grid(True, ls=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    apply_ticks(ax, prop)
    p3 = ASSET_DIR / "chart_scenarios.png"
    fig.tight_layout(pad=0.6)
    fig.savefig(p3, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    paths["scen"] = p3

    fig, ax = plt.subplots(figsize=(8.0, 3.4), dpi=160)
    names = ["SUI\n流通市值", "SUI到2\n流通不变", "SUI到2\n全稀释", "SUI历史高点\n当时市值量级", "SOL\n约40-55"]
    vals = [42.1, 81.9, 200, 170, 500]
    c = ["#1B6CA8", "#3D8FBF", "#C45C26", "#94A3B8", "#64748B"]
    ax.barh(names[::-1], vals[::-1], color=c[::-1], height=0.58)
    ax.set_xlabel("约当市值（亿美元，量级示意）", fontproperties=prop)
    ax.set_title("2 美元对应的市值：中型公链可想象，远未到一线公链台阶", fontproperties=prop)
    ax.xaxis.grid(True, ls=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    apply_ticks(ax, prop)
    p4 = ASSET_DIR / "chart_comps.png"
    fig.tight_layout(pad=0.6)
    fig.savefig(p4, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    paths["comps"] = p4
    return paths


def img(path, width=158 * mm):
    probe = Image(str(path))
    ratio = probe.imageHeight / float(probe.imageWidth)
    im = Image(str(path), width=width, height=width * ratio)
    im.hAlign = "CENTER"
    return im


def figure(path, caption, styles):
    return KeepTogether([img(path), p(caption, styles["caption"])])


def build():
    prop = register_fonts()
    styles = make_styles()
    charts = make_charts(prop)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="SUI现货持有与中长期到2美元困难度",
        author="独立研究备忘",
    )
    story = []

    story.append(p("独立研究备忘  ·  公开信息交叉验证  ·  2026年9月21日快照", styles["cover_kicker"]))
    story.append(Spacer(1, 2 * mm))
    story.append(p("SUI 能不能持有现货，中长期到 2 美元有多难", styles["cover_title"]))
    story.append(p("结合交易所截图与全网公开信息：把现货持有逻辑和 2 美元目标拆开看，并补上解锁、生态、竞争和事故史。", styles["cover_sub"]))
    story.append(Spacer(1, 7 * mm))
    meta = [
        ["分析对象", "SUI / Sui Network 公链原生代币"],
        ["价格快照", "约 1.0227 美元，当日约 +14.02%"],
        ["流通口径", "约 41.0 亿枚，市值约 42.10 亿美元，市值排名约第 24"],
        ["全稀释口径", "上限 100 亿枚，FDV 约 102.77 亿美元，流通率约 40.96%"],
        ["核心结论", "现货可以持有，但不要追这根大阳线；2 美元难度中等偏低，是回收不是新高"],
    ]
    meta_table = Table(
        [[p(f"<b>{a}</b>", styles["td_left"]), p(b, styles["td_left"])] for a, b in meta],
        colWidths=[32 * mm, 138 * mm],
    )
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BG_SOFT),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 7 * mm))
    story.append(
        callout(
            "阅读前必须知道",
            "本文是研究备忘，不是投资建议。加密资产可以腰斩再腰斩。文中「可以持有」「难度中等」都是基于公开信息和这张截图的主观框架，用来想清楚仓位结构，不能当买卖指令。当日已涨约 14%，任何现货决定都要先处理「现在追不追」这个问题。",
            styles,
            bg=BG_WARN,
            border=AMBER,
        )
    )
    story.append(Spacer(1, 5 * mm))
    story.append(
        callout(
            "三句话先给答案",
            "第一，中长期看 2 美元，现货比合约更合适。第二，2 美元不是天价：它只是历史最高 5.37 美元的约 37%，流通市值大约从 42 亿到 82 亿美元。第三，真正的阻力不是算术，而是每月解锁、TVL 已从高点腰斩、以及 Solana 对公链注意力的虹吸。热度排名第 7、市值排名第 24、单日大涨，短线拥挤，现货只能分批，不能一把买完。",
            styles,
        )
    )

    story.append(PageBreak())
    story.append(p("目录", styles["h1"]))
    story.append(hr())
    for item in [
        "一、截图快照：先把数字翻译对",
        "二、Sui 是什么：值不值得当公链底仓",
        "三、代币结构：VC 解锁才是现货持有的主成本",
        "四、到 2 美元：算术简单，路径不简单",
        "五、现货能不能拿：结论、条件、不该拿的人",
        "六、容易漏看的风险",
        "七、总结",
        "附录：来源与口径",
    ]:
        story.append(p(item, styles["toc"]))

    story.append(p("一、截图快照：先把数字翻译对", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "快照来自你提供的 SUIUSDT 永续概况页（约 19:47）。价格用 1.0227 美元做基准。注意：页面是永续合约，但你问的是现货持有。两者标的相同，工具完全不同。",
            styles["body"],
        )
    )
    story.append(
        styled_table(
            ["项目", "截图读数", "阅读方式"],
            [
                ["最新价 / 涨幅", "1.0227 / +14.02%", "大阳线后提问，先处理追高问题"],
                ["热度排名", "No.7", "交易端关注度远高于市值地位"],
                ["市值排名", "No.24", "仍是中型加密资产，不是一线公链"],
                ["流通市值", "42.10 亿美元", "40.97 亿枚 × 约 1.02 美元"],
                ["流通量 / 流通率", "40.965 亿枚 / 40.96%", "六成供应还在后面"],
                ["添加自选比例", "11.67%", "该所用户里关注度不低"],
                ["历史最高", "5.3681（2025-01-07）", "现价约为前高的 19%"],
                ["历史最低", "0.10（2023-05-03）", "主网上线前后的低流动性印记"],
                ["发行日", "2023-05-03", "主网约三年半"],
                ["成交额 / 市值", "0.0158", "该所口径换手一般，不是极端赌博盘"],
                ["最大供应 / FDV", "100 亿枚 / 102.77 亿美元", "全稀释仍是中型公链量级"],
                ["下次解锁", "2026-09-22，约 37.81 万枚", "约 39 万美元，对盘面可忽略"],
            ],
            [42 * mm, 52 * mm, 76 * mm],
            styles,
        )
    )
    story.append(p("表 1　交易所概况页关键数据（用户截图）", styles["caption"]))
    story.append(
        p(
            "两处不要误读。第一，9 月 22 日解锁只有约 37.81 万枚、占市值约 0.01%，不是抛压事件。SUI 的供应压力是「每个月都在出货」的细水长流，不是某一天的红字。第二，热度第 7 对上市值第 24，再叠当日 +14%，更像短线拥挤，而不是基本面一夜变好。现货仓可以规划，不该在这根蜡烛的最高点把子弹打完。",
            styles["body"],
        )
    )

    story.append(p("二、Sui 是什么：值不值得当公链底仓", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "Sui 是 Mysten Labs 做的高性能一层网络。核心团队来自 Meta 的 Diem / Novi。主网 2023 年 5 月上线。它不是「再发一条 EVM 链」，而是对象模型 + Move 语言：互不冲突的交易可以并行，简单转账甚至可以绕过完整共识。2024 年 Mysticeti 共识把最终性压到约 400 毫秒量级。代币用途是 gas、质押、治理，以及存储基金（存数据付费、删数据可退）。",
            styles["body"],
        )
    )
    story.append(p("2.1 已经验证的", styles["h2"]))
    story.extend(
        bullets(
            [
                "架构有辨识度：对象模型、Move 资源安全、zkLogin、DeepBook 共享订单簿、Walrus 存储，不是纯叙事空壳。",
                "团队和融资背景强：a16z、Binance Labs、Lightspeed、Circle 等出现过。这解释了机构产品和 ETF / ETN 讨论为什么会来，也解释了为什么解锁压力会长期存在。",
                "生态不是零：借贷（NAVI、Suilend）、永续（Bluefin）、DEX、游戏和消费应用都有真实用户。DeepBook 累计链上成交有超过 170 亿美元的公开口径。",
                "机构通道在铺：欧洲有过 VanEck 等 ETN；美国侧 21Shares、Franklin Templeton、Canary 等出现过现货 ETF 相关文件；Grayscale 有过 SUI Trust。通道不等于价格马上翻倍。",
            ],
            styles,
        )
    )
    story.append(p("2.2 还没验证的", styles["h2"]))
    story.extend(
        bullets(
            [
                "它还不是「下一个 Solana」。公开对照里，Solana 的 TVL、稳定币流转、开发者基数和注意力仍高一个数量级。Sui 更像「有机会的第二梯队高性能公链」。",
                "链上费用很低。DefiLlama 快照里 24 小时链费用只有数千美元量级。SUI 不是费用回购机器，持有逻辑是「公链期权 + 质押」，不是「协议现金牛」。",
                "TVL 从 2025 年高峰约 20–26 亿美元量级回落到 2026 年 9 月不同口径的约 4.7–12 亿美元。生态还在，热度退了。",
                "BTCFi（Hashi 等）和稳定币支付是期权，不是已经计入的利润。主网验证之前，不能拿来给 2 美元做刚兑。",
            ],
            styles,
        )
    )
    story.append(
        callout(
            "和 HYPE 的关键差别",
            "HYPE 是已经打赢品类的交易所代币，贵在估值，难在再翻倍。SUI 是还没打赢一线公链座位的 L1 代币，便宜在已经从 5.37 跌到约 1.02，难在解锁和注意力。问「现货能不能拿」，SUI 比高位的 HYPE 更适合用现货思考；问「会不会创新高」，SUI 的 2 美元远比 HYPE 的 200 美元老实。",
            styles,
        )
    )

    story.append(p("三、代币结构：VC 解锁才是现货持有的主成本", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "上限 100 亿枚，硬顶。当前流通约 41.0 亿枚，约 41%。Tokenomist 在 2026-09-21 的口径与你的截图几乎一致。剩下约 59 亿枚按计划释放到约 2030 年。官方早期分配常见写法是：社区储备约 50%、早期贡献者约 20%、融资轮约 14%、Mysten 金库约 10%、社区认购约 6%。不同网站把「社区储备 / 质押补贴 / 2030 年后释放」拆法不同，会看到「2030 年后 52%」这种大类，本质是：很大一块并没有按月均匀砸进现货盘，但也没有消失。",
            styles["body"],
        )
    )
    story.append(
        styled_table(
            ["观察点", "含义", "对现货持有"],
            [
                ["流通率约 41%", "六成未进盘", "中长期有稀释，仓位不能按「盘已出尽」来加"],
                ["月度解锁仍在", "常见单月约市值 0.3%–1%", "反弹会被供给吸收，适合分批而不是梭哈"],
                ["9 月 22 日约 38 万枚", "事件型抛压接近零", "不要把它当买卖信号"],
                ["VC / 团队有份额", "和 HYPE 的无 VC 结构相反", "解锁周的抛压是结构，不是情绪"],
                ["质押吸收一部分", "公开口径早期 2026 年名义收益中个位数，净收益常见约 3%–5%", "现货最好去质押，抵消部分稀释"],
                ["存储基金可锁住部分 SUI", "活动上升有轻微通缩效应", "目前费用太低，不能指望它单独把价格抬到 2"],
            ],
            [42 * mm, 58 * mm, 70 * mm],
            styles,
        )
    )
    story.append(p("表 2　供应结构对现货仓的含义", styles["caption"]))
    story.append(
        p(
            "粗算：若未来 12–18 个月流通从 41 亿枚增加到 45–50 亿枚，价格要维持 2 美元，市值就要从约 82 亿走到 90–100 亿美元。稀释不会杀死 2 美元目标，但会把「轻松翻倍」变成「市值还要再多涨一截」。这是现货能拿、却必须控制仓位的核心原因。",
            styles["body"],
        )
    )

    story.append(p("四、到 2 美元：算术简单，路径不简单", styles["h1"]))
    story.append(hr())
    story.append(p("4.1 算术", styles["h2"]))
    story.append(
        styled_table(
            ["假设流通", "2 美元对应市值", "相对当前约 42 亿", "直觉"],
            [
                ["41.0 亿（近似当前）", "82 亿美元", "约 1.95 倍", "中型公链，历史给过更高"],
                ["45 亿", "90 亿美元", "约 2.1 倍", "正常解锁路径"],
                ["50 亿", "100 亿美元", "约 2.4 倍", "仍远小于一线公链"],
                ["100 亿（全稀释）", "200 亿美元", "约 4.8 倍", "要到接近全流通才难"],
            ],
            [42 * mm, 42 * mm, 42 * mm, 44 * mm],
            styles,
        )
    )
    story.append(p("表 3　2 美元在不同流通口径下的市值", styles["caption"]))
    story.append(figure(charts["mc"], "图 1　2 美元对应的市值台阶。流通放大后仍在 80–200 亿美元带。", styles))
    story.append(figure(charts["levels"], "图 2　价格坐标：2 美元远低于 2025 年 1 月的 5.37 美元前高。", styles))
    story.append(figure(charts["comps"], "图 3　市值对照。历史高点市值随当时流通变化，这里只作量级示意。", styles))

    story.append(p("4.2 为什么说难度「中等偏低」", styles["h2"]))
    story.extend(
        bullets(
            [
                "市场已经给过更高：2025 年 1 月见过 5.37 美元。2 美元是回到前高的 37%，属于回收带，不是要它改写加密市值结构。",
                "公开研究里，不少 2026 年末基准情景本来就写在 1.50–2.50 美元附近。说明 2 美元是市场讨论里的中枢附近，不是极端牛案。",
                "对 BTC / SOL 的贝塔很大。若下一轮风险资产回暖，第二梯队公链里 SUI 通常会有一席。它不需要「独自创造牛市」。",
                "反过来：它必须穿过解锁、穿过「不是 Solana」的折价、穿过 TVL 已经退潮的现实。所以也不是「买了就会到」。",
            ],
            styles,
        )
    )
    story.append(p("4.3 情景带（主观）", styles["h2"]))
    story.append(figure(charts["scen"], "图 4　中长期情景带。中间点是示意中枢，不是目标价。", styles))
    story.append(
        styled_table(
            ["情景", "价格带", "2 美元在不在里面", "主要条件"],
            [
                ["熊市 / 持续稀释", "约 0.35–0.75", "不在", "风险资产收缩，解锁砸穿买盘，TVL 再下台阶"],
                ["基准 / 震荡修复", "约 0.70–1.50", "上沿附近，不稳", "生态存活，解锁被消化，没有新叙事"],
                ["偏多 / 生态回暖", "约 1.10–2.40", "在，当作可达上沿", "稳定币和 DeFi 回升，公链轮动"],
                ["强牛 / L1 轮动", "约 1.60–3.50", "作为中途站", "加密牛市 + ETF / 机构资金"],
                ["极端 / 再挑战前高", "约 2.80–5.50+", "轻松超过", "Sui 被重新定价为一线公链，概率低"],
            ],
            [40 * mm, 32 * mm, 42 * mm, 56 * mm],
            styles,
        )
    )
    story.append(p("表 4　主观情景。用于思考，不用于下单。", styles["caption"]))
    story.append(
        p(
            "困难度可以写直白：未来 6 个月要到 2，需要行情配合，难度中等；12–24 个月若加密不是单边熊，2 美元是合理瞄准的回收位，难度中等偏低；用它当「一定到」的承诺则不诚实。相对你之前问的 HYPE 到 200，SUI 到 2 明显更容易。",
            styles["body"],
        )
    )

    story.append(p("五、现货能不能拿：结论、条件、不该拿的人", styles["h1"]))
    story.append(hr())
    story.append(
        callout(
            "直接回答",
            "可以持有现货，但只能作为卫星仓、分批、可质押、能扛 40%–60% 回撤的那种持有。不适合在这根 +14% 的阳线里一次性买满。若你的目标就是中长期看 2 美元，现货优于永续：2 美元是月份到年份的路径，中间会被解锁反复洗，杠杆很难活着到达。",
            styles,
            bg=BG_SOFT,
            border=TEAL,
        )
    )
    story.append(p("5.1 为什么现货说得通", styles["h2"]))
    story.extend(
        bullets(
            [
                "标的是公链代币，不是几天的主题。2 美元需要时间，现货的时间成本低于资金费和爆仓。",
                "价格已经从 5.37 回撤约 81%。下跌本身不是买入理由，但它意味着 2 美元不再要求新的估值体系。",
                "可以质押，大约中个位数年化（净收益常见更低），部分对冲每月解锁。合约做不到这一点。",
                "上限硬顶 100 亿，比无限增发的公链代币更干净。稀释有日历，可以规划。",
            ],
            styles,
        )
    )
    story.append(p("5.2 必须满足的持有条件", styles["h2"]))
    story.extend(
        bullets(
            [
                "仓位当卫星，不当全部风险资产。SUI 对 BTC 弹性大，它不会在比特币不好时独自走出独立牛。",
                "分批：热度第 7 + 单日 +14%，第一笔不该是全部。更合理的是把计划仓位拆成若干周，跌了加、涨了等。",
                "现货去质押，不要把现货再拿去开高倍合约。那是把「能拿住」变成「拿不住」。",
                "先写失效条件：例如稳定跌破 0.70 且生态 TVL 再下台阶、团队或基金会明显异常抛售、主网反复长时间停机。触发就减，而不是加杠杆摊平。",
                "接受路径会很难看：到 2 美元的路上完全可以先回 0.8。现货仓必须按「先回撤再回收」来配资金。",
            ],
            styles,
        )
    )
    story.append(p("5.3 谁不该拿现货", styles["h2"]))
    story.extend(
        bullets(
            [
                "指望几周内翻倍、不能看回撤的人。这种人用现货也会在第一轮解锁阴跌里卖掉。",
                "已经在永续里高倍做多同一标的的人。再叠加现货，风险是重复的。",
                "把 SUI 当成「无解锁优质筹码」的人。它有 VC、有团队、有基金会，和 HYPE 不是一类代币。",
                "资金期限短于 6 个月的人。6 个月内 2 美元要靠行情送礼，不是基本面必然。",
            ],
            styles,
        )
    )
    story.append(
        callout(
            "操作结构（不是点位建议）",
            "若决定拿：用稳定币分批买现货，转到链上质押；合约只在你明确做波段时单独开一个小账户。不要用全仓把现货和合约焊死。2 美元是减仓或重新评估的观察位，不是「到了再翻一倍」的自动加油门。",
            styles,
            bg=BG_WARN,
            border=AMBER,
        )
    )

    story.append(p("六、容易漏看的风险", styles["h1"]))
    story.append(hr())
    extras = [
        (
            "1. 2025 年 5 月 Cetus 被盗约 2.2–2.6 亿美元",
            "当时是头部 DEX。验证者后来用协议升级冻结并回收部分资金。对用户是救援，对去中心化叙事是伤疤：关键时刻，基金会和验证者可以改状态。现货持有人要接受「这条链在极端情况下更像由核心团队协调的高性能网络」。",
        ),
        (
            "2. 2026 年 5 月末连续三次主网停机",
            "官方归因于 v1.72 升级与 gas 逻辑、随机数持久化的连锁 bug。资金没有因此丢失，但 SUI 当周有过明显下跌。高性能链用停机换修复，不是第一次也不会是最后一次。",
        ),
        (
            "3. Move 语言防不了应用层漏洞",
            "Cetus 说明：语言层面少一类错误，不代表 DEX 数学库不会被打穿。生态 TVL 重建需要时间，也需要用户重新信任。",
        ),
        (
            "4. 与 Solana、Aptos、以太坊 L2 抢同一批注意力",
            "技术可以并列第一梯队，市值不一定。SUI 到 2 美元可以靠贝塔完成；要稳定停在 2 以上，需要生态份额不再被抽走。",
        ),
        (
            "5. 费用太薄，买不回多少抛压",
            "和 HYPE 那种费用回购不同，SUI 的买盘主要来自新资金、质押锁定和叙事。解锁月份如果没有风险偏好，现货会阴跌。",
        ),
        (
            "6. 「2030 年后释放」大类并不透明",
            "五十个百分点量级被归到远期，是缓解近两年抛压的设计，也可能在未来变成第二波供应。中长期仓要把它放进模型，不能当永久锁仓。",
        ),
        (
            "7. 监管与上市产品是双刃剑",
            "ETF / 信托能带来合规买盘，也可能在文件延迟、审查或个别市场（例如曾有过的韩国相关争议报道）时变成利空。不要把「有人提交文件」读成「已经批准」。",
        ),
        (
            "8. 当日结构本身就是风险",
            "热度明显高于市值地位，又碰上 14% 的阳线。短线最常见的结局是：先把情绪交易者卷进来，再在解锁或 BTC 回调里把他们洗出去。现货分批就是为了不当这个对手盘。",
        ),
    ]
    for title, body in extras:
        story.append(p(title, styles["h3"]))
        story.append(p(body, styles["body"]))

    story.append(p("七、总结", styles["h1"]))
    story.append(hr())
    story.append(p("能不能持有现货", styles["h2"]))
    story.append(
        p(
            "能，而且如果你的问题是中长期看 2 美元，现货是比合约更匹配的工具。前提是：卫星仓、分批、质押、能接受先跌后涨，并且不把 SUI 误认成无解锁的现金牛。今天这根大阳线，只说明市场在交易它，不说明现在是最佳一次性买点。",
            styles["body"],
        )
    )
    story.append(p("到 2 美元难不难", styles["h2"]))
    story.append(
        p(
            "算术不难：大约两倍，流通市值到约 82 亿美元，仍是中型公链。历史给过 5.37 美元，所以 2 美元是回收。难的是路径：月度解锁、TVL 已退潮、Solana 虹吸、停机和黑客记忆都还在。主观上，把它当成 12–24 个月里「偏多情景可以碰到、基准情景在上沿、熊市情景够不着」的目标，比当成必达价更诚实。它比 HYPE 到 200 容易得多，但仍然会被宏观一票否决。",
            styles["body"],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        callout(
            "最后一句",
            "SUI 值得用现货认真对待，不值得用情绪和杠杆去追一根 +14% 的 K 线。2 美元是合理的中期观察位，不是承诺。",
            styles,
            bg=BG_SOFT,
            border=TEAL_DARK,
        )
    )

    story.append(p("附录：来源与口径", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "价格、市值、流通、FDV、解锁条来自你提供的交易所截图（约 2026-09-21）。机制与分配参考 Sui / Mysten 文档及 2026 年综述（BitMEX 指南、Tokenomist、Tokenomics.com）。TVL、费用参考 DefiLlama 及 Gate 等二手汇编（不同口径 4.7–12 亿美元）。Cetus 事件参考 CoinDesk 与 Sui 官方投票说明。2026 年 5 月停机参考 Sui 官方复盘与 CoinDesk。机构产品与预测区间参考公开新闻和研究，只作对照，不构成本文的点位。情景带是主观框架，会随新数据失效。",
            styles["body"],
        )
    )
    story.append(p("文档生成日期：2026-09-21。不构成投资、法律或税务建议。", styles["small"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    ascii_copy = OUT_DIR / "SUI.pdf"
    ascii_copy.write_bytes(PDF_PATH.read_bytes())
    print(f"Wrote {PDF_PATH}")
    print(f"Wrote {ascii_copy}")
    return PDF_PATH


if __name__ == "__main__":
    build()
