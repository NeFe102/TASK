#!/usr/bin/env python3
"""Generate the HYPE medium/long-term research PDF."""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    KeepTogether,
    ListFlowable,
    ListItem,
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
ASSET_DIR = OUT_DIR / "assets"
PDF_PATH = OUT_DIR / "HYPE中长期分析_到200美元困难度与币本位合约选择_2026-09-19.pdf"

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
FONT_NAME = "WQYMicroHei"

NAVY = colors.HexColor("#0B1F33")
TEAL = colors.HexColor("#0E8F8A")
TEAL_DARK = colors.HexColor("#0A6B67")
AMBER = colors.HexColor("#C45C26")
RED = colors.HexColor("#B42318")
GREEN = colors.HexColor("#1F7A4D")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#D6DEE8")
BG_SOFT = colors.HexColor("#F4F8F8")
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
    base = getSampleStyleSheet()
    styles = {
        "cover_kicker": ParagraphStyle(
            "cover_kicker",
            fontName=FONT_NAME,
            fontSize=10,
            textColor=TEAL_DARK,
            alignment=TA_LEFT,
            leading=16,
            wordWrap="CJK",
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName=FONT_NAME,
            fontSize=22,
            textColor=NAVY,
            leading=32,
            alignment=TA_LEFT,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontName=FONT_NAME,
            fontSize=11.5,
            textColor=SLATE,
            leading=18,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName=FONT_NAME,
            fontSize=16,
            textColor=NAVY,
            leading=24,
            spaceBefore=14,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName=FONT_NAME,
            fontSize=13,
            textColor=TEAL_DARK,
            leading=20,
            spaceBefore=11,
            spaceAfter=6,
            wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "h3",
            fontName=FONT_NAME,
            fontSize=11.5,
            textColor=NAVY,
            leading=18,
            spaceBefore=8,
            spaceAfter=4,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "body",
            fontName=FONT_NAME,
            fontSize=10,
            textColor=SLATE,
            leading=16.5,
            alignment=TA_LEFT,
            spaceAfter=7,
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName=FONT_NAME,
            fontSize=10,
            textColor=SLATE,
            leading=16,
            leftIndent=2,
            spaceAfter=3,
            wordWrap="CJK",
        ),
        "caption": ParagraphStyle(
            "caption",
            fontName=FONT_NAME,
            fontSize=8.5,
            textColor=MUTED,
            leading=13,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=10,
            wordWrap="CJK",
        ),
        "note": ParagraphStyle(
            "note",
            fontName=FONT_NAME,
            fontSize=9,
            textColor=SLATE,
            leading=14.5,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName=FONT_NAME,
            fontSize=8,
            textColor=MUTED,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "toc": ParagraphStyle(
            "toc",
            fontName=FONT_NAME,
            fontSize=11,
            textColor=SLATE,
            leading=20,
            wordWrap="CJK",
        ),
        "quote": ParagraphStyle(
            "quote",
            fontName=FONT_NAME,
            fontSize=10.5,
            textColor=NAVY,
            leading=17,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=4,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "small": ParagraphStyle(
            "small",
            fontName=FONT_NAME,
            fontSize=8.5,
            textColor=MUTED,
            leading=13,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "th": ParagraphStyle(
            "th",
            fontName=FONT_NAME,
            fontSize=8.4,
            textColor=WHITE,
            leading=12,
            alignment=TA_CENTER,
            wordWrap="CJK",
        ),
        "td": ParagraphStyle(
            "td",
            fontName=FONT_NAME,
            fontSize=8.3,
            textColor=SLATE,
            leading=12.2,
            alignment=TA_CENTER,
            wordWrap="CJK",
        ),
        "td_left": ParagraphStyle(
            "td_left",
            fontName=FONT_NAME,
            fontSize=8.3,
            textColor=SLATE,
            leading=12.2,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "callout_title": ParagraphStyle(
            "callout_title",
            fontName=FONT_NAME,
            fontSize=10.5,
            textColor=NAVY,
            leading=16,
            spaceAfter=4,
            wordWrap="CJK",
        ),
    }
    return styles


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def hr():
    return HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=2, spaceAfter=8)


def callout(title: str, body: str, styles, bg=BG_SOFT, border=TEAL):
    data = [
        [p(f"<b>{title}</b>", styles["callout_title"])],
        [p(body, styles["note"])],
    ]
    t = Table(data, colWidths=[170 * mm])
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
            st = styles["td_left"] if i in left_cols else styles["td"]
            cells.append(p(str(val), st))
        body.append(cells)
    t = Table([head] + body, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
    ]
    for i in range(1, len(body) + 1):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0, i), (-1, i), BG_SOFT))
    t.setStyle(TableStyle(cmds))
    return t


def bullets(items, styles):
    flow = []
    for item in items:
        flow.append(p(f"• {item}", styles["bullet"]))
    return flow


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 11 * mm, w, 11 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, h - 12.1 * mm, w, 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont(FONT_NAME, 8)
    canvas.drawString(16 * mm, h - 7.2 * mm, "HYPE 中长期研究备忘  |  非投资建议")
    canvas.drawRightString(w - 16 * mm, h - 7.2 * mm, "快照日期 2026-09-19")
    canvas.setFillColor(colors.HexColor("#F1F5F9"))
    canvas.rect(0, 0, w, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_NAME, 8)
    canvas.drawString(16 * mm, 5 * mm, "公开信息交叉验证  ·  情景分析而非预测")
    canvas.drawRightString(w - 16 * mm, 5 * mm, f"{doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    header_footer(canvas, doc)


def apply_ticks(ax, prop: font_manager.FontProperties) -> None:
    for label in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
        label.set_fontproperties(prop)


def make_charts(prop: font_manager.FontProperties) -> dict[str, Path]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    paths = {}

    # Chart 1: implied MC at $200. 流通量单位为「亿枚」，市值单位为「亿美元」。
    fig, ax = plt.subplots(figsize=(8.2, 3.6), dpi=160)
    supplies = [2.22, 3.00, 4.00, 5.00, 9.62, 10.00]
    labels = ["2.22亿\n当前流通", "3.00亿", "4.00亿", "5.00亿", "9.62亿\n总供应", "10.00亿\n全稀释"]
    mcaps = [s * 200 for s in supplies]
    colors_bar = ["#0E8F8A", "#2A9D8F", "#4C6B8A", "#C45C26", "#B42318", "#7F1D1D"]
    bars = ax.bar(labels, mcaps, color=colors_bar, width=0.62)
    ax.axhline(205.65, color="#64748B", ls="--", lw=1, label="当前流通市值约 205.65 亿美元")
    ax.set_ylabel("达到 200 美元时的流通市值（亿美元）", fontproperties=prop)
    ax.set_title("同一价格 200 美元，在不同流通盘下意味着完全不同的市值", fontproperties=prop)
    ax.yaxis.grid(True, ls=":", alpha=0.5)
    ax.set_axisbelow(True)
    for b, v in zip(bars, mcaps):
        ax.text(b.get_x() + b.get_width() / 2, v + 40, f"{v:.0f}", ha="center", va="bottom", fontsize=8, fontproperties=prop)
    ax.legend(prop=prop, fontsize=8, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    apply_ticks(ax, prop)
    p1 = ASSET_DIR / "chart_mc_at_200.png"
    fig.tight_layout(pad=0.6)
    fig.savefig(p1, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    paths["mc"] = p1

    # Chart 2: comparables
    fig, ax = plt.subplots(figsize=(8.2, 3.5), dpi=160)
    names = ["HYPE\n流通市值", "HYPE\n全稀释估值", "HYPE到200\n若流通不变", "HYPE到200\n全稀释", "BNB\n约80-100", "SOL\n约40-55"]
    vals = [205.7, 889.6, 444, 2000, 900, 500]
    c = ["#0E8F8A", "#C45C26", "#4C6B8A", "#B42318", "#64748B", "#94A3B8"]
    ax.barh(names[::-1], vals[::-1], color=c[::-1], height=0.62)
    ax.set_xlabel("约当市值 / 估值（亿美元，量级示意）", fontproperties=prop)
    ax.set_title("200 美元对应的估值台阶：流通口径可想象，全稀释口径极难", fontproperties=prop)
    ax.xaxis.grid(True, ls=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    apply_ticks(ax, prop)
    fig.tight_layout()
    p2 = ASSET_DIR / "chart_comps.png"
    fig.savefig(p2, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    paths["comps"] = p2

    # Chart 3: scenario prices
    fig, ax = plt.subplots(figsize=(8.2, 3.5), dpi=160)
    scenarios = ["熊市\n份额回吐", "基准\n震荡消化", "偏多\n份额+回购", "强牛\nL1溢价", "极端\n叙事共振"]
    lows = [32, 55, 85, 130, 180]
    highs = [58, 110, 150, 220, 280]
    mids = [42, 80, 115, 170, 230]
    xs = range(len(scenarios))
    ax.vlines(xs, lows, highs, color="#0B1F33", lw=2)
    ax.scatter(xs, mids, s=42, color="#0E8F8A", zorder=3)
    ax.axhline(93.2, color="#C45C26", ls="--", lw=1, label="快照价约 93.2")
    ax.axhline(200, color="#B42318", ls=":", lw=1.2, label="目标 200")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(scenarios, fontproperties=prop)
    ax.set_ylabel("中长期价格带（美元）", fontproperties=prop)
    ax.set_title("主观情景带：200 美元落在强牛到极端叙事区间，不是基准路径", fontproperties=prop)
    ax.legend(prop=prop, fontsize=8, frameon=False, loc="upper left")
    ax.yaxis.grid(True, ls=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    apply_ticks(ax, prop)
    fig.tight_layout()
    p3 = ASSET_DIR / "chart_scenarios.png"
    fig.savefig(p3, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    paths["scen"] = p3

    # Chart 4: X 轴向右表示回撤加深。
    fig, ax = plt.subplots(figsize=(8.0, 3.5), dpi=160)
    dump = [5, 10, 15, 20, 25, 30]
    lev = 8
    u_remain = [max(0, 100 * (1 - d / 100 * lev)) for d in dump]
    coin_remain = [max(0, 100 * (1 - (1 + lev) * (d / 100))) for d in dump]
    ax.plot(dump, u_remain, marker="o", color="#0E8F8A", lw=2, label="U本位 8倍：保证金美元价值相对稳定")
    ax.plot(dump, coin_remain, marker="s", color="#B42318", lw=2, label="币本位 8倍：币价跌叠加仓位亏，净值下降更快")
    ax.axhline(0, color="#94A3B8", lw=0.8)
    ax.set_xlabel("开仓后继续回撤幅度（%）", fontproperties=prop)
    ax.set_ylabel("账户权益剩余（相对初始美元，%）", fontproperties=prop)
    ax.set_title("同为 8 倍做多：回调未结束时，币本位权益下降更快、更先归零", fontproperties=prop)
    ax.legend(prop=prop, fontsize=8, frameon=False)
    ax.yaxis.grid(True, ls=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlim(4, 31)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    apply_ticks(ax, prop)
    p4 = ASSET_DIR / "chart_margin.png"
    fig.tight_layout(pad=0.6)
    fig.savefig(p4, bbox_inches="tight", pad_inches=0.22, facecolor="white")
    plt.close(fig)
    paths["margin"] = p4

    return paths


def img(path: Path, width=158 * mm):
    probe = Image(str(path))
    ratio = probe.imageHeight / float(probe.imageWidth)
    im = Image(str(path), width=width, height=width * ratio)
    im.hAlign = "CENTER"
    return im


def figure(path: Path, caption: str, styles):
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
        title="HYPE中长期分析：到200美元的困难度、平台前景与币本位/U本位选择",
        author="独立研究备忘",
        subject="Hyperliquid / HYPE research note",
    )

    story = []

    story.append(p("独立研究备忘  ·  公开信息交叉验证  ·  2026年9月19日快照", styles["cover_kicker"]))
    story.append(Spacer(1, 2 * mm))
    story.append(
        p("HYPE 中长期价格与平台前景全景分析", styles["cover_title"])
    )
    story.append(
        p(
            "到 200 美元有多难、平台还能走多远，以及下次回调开多时币本位是不是比 U 本位更好。",
            styles["cover_sub"],
        )
    )
    story.append(
        p(
            "按你的思路展开，并补上截图和公开数据里容易漏掉的变量。",
            styles["cover_sub"],
        )
    )
    story.append(Spacer(1, 8 * mm))
    meta = [
        ["分析对象", "HYPE / Hyperliquid L1 + 链上订单簿 DEX"],
        ["价格快照", "约 93.21–93.25 美元，当日创 94.54 美元历史新高"],
        ["流通口径", "约 2.22 亿枚，市值约 205.65 亿美元，排名约第 15"],
        ["全稀释口径", "上限 10 亿枚，FDV 约 889.62 亿美元，市值/FDV 约 22.24%"],
        ["核心结论", "平台前景偏强，但 200 美元不是基准路径；回调开多默认更适合 U 本位"],
    ]
    meta_table = Table(
        [[p(f"<b>{a}</b>", styles["td_left"]), p(b, styles["td_left"])] for a, b in meta],
        colWidths=[32 * mm, 138 * mm],
    )
    meta_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BG_SOFT),
                ("BACKGROUND", (1, 0), (1, -1), WHITE),
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
    story.append(Spacer(1, 8 * mm))
    story.append(
        callout(
            "阅读前必须知道",
            "本文是研究备忘，不是投资建议、不是买卖推荐、也不是对未来价格的保证。加密资产和永续合约波动极大，杠杆可以亏光本金。文中概率、情景带、难易判断都是基于公开信息和截图快照的主观框架，用来把问题想清楚，不能当预测单用。数据会变，解锁会变，监管会变。任何下单前都需要用交易所实时数据自行复核。",
            styles,
            bg=BG_WARN,
            border=AMBER,
        )
    )
    story.append(Spacer(1, 6 * mm))
    story.append(
        callout(
            "本报告回答三件事",
            "第一，结合 Hyperliquid 的产品独特性与公开数据，判断 HYPE 中长期到 200 美元有多难。第二，分开看平台前景和代币价格，避免把「交易所变强」直接翻译成「币价翻倍」。第三，下次回调开多时，币本位合约是不是比 U 本位更好；结论取决于目标函数，但默认答案是 U 本位。",
            styles,
        )
    )

    story.append(PageBreak())
    story.append(p("目录与分析路径", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "你的原始问题可以拆成四层：平台凭什么独特、代币中长期到 200 有多难、平台本身还能走多远、下次回调开多时合约品种怎么选。下面按这个顺序写，并在每一层补你截图里没有直接给出、但会改变结论的变量。",
            styles["body"],
        )
    )
    toc_items = [
        "一、数据快照：把截图翻译成可计算的事实",
        "二、平台独特性：HYPE 不是普通「交易所代币」",
        "三、代币结构：流通、解锁、未追踪供应与回购销毁",
        "四、到 200 美元：算术、估值台阶、情景与困难度",
        "五、平台发展前景：增长引擎、竞争、监管与生态",
        "六、你可能没注意到的十组关键变量",
        "七、下次回调开多：币本位是不是比 U 本位更好",
        "八、若仍要交易：结构建议而非点位建议",
        "九、总结",
        "附录：主要来源与口径说明",
    ]
    for i, item in enumerate(toc_items, 1):
        story.append(p(item, styles["toc"]))
    story.append(Spacer(1, 4 * mm))
    story.append(
        callout(
            "一句话预览",
            "Hyperliquid 的产品与代币机制在加密里属于第一档；但你提问时价格已经贴着历史新高，200 美元在「流通盘继续被压住」时只是大约 2.1 倍，在「10 亿枚都被市场按全稀释定价」时则是约 2000 亿美元市值。前者困难、并非荒谬；后者极难。回调还没发生时，用币本位高倍做多，是把「还没走完的下跌」和「抵押品同步变便宜」叠在一起。",
            styles,
        )
    )

    # Section 1
    story.append(p("一、数据快照：把截图翻译成可计算的事实", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "以下数字以你提供的交易所页面为准（约 2026-09-19 01:07–01:08）。公开网站上的流通、已解锁、已领取口径并不完全一致，后文会单独解释这个「口径迷雾」，因为它会直接改变对 200 美元难度的判断。",
            styles["body"],
        )
    )
    story.append(p("1.1 价格与市值", styles["h2"]))
    story.append(
        styled_table(
            ["项目", "截图读数", "含义"],
            [
                ["最新价", "约 93.21 / 93.25 美元", "分析基准价取 93.2"],
                ["24h 最高 / 最低", "94.536 / 91.284", "当日波动收窄在高位"],
                ["历史最高", "94.54（2026-09-19）", "提问时已在历史新高附近"],
                ["历史最低", "0.011812（2024-10-26）", "TGE 前后的极低流动性印记"],
                ["发行日 / 发行价", "2024-11-29 / 26.405 美元", "相对发行价约 +2.5 倍"],
                ["排名", "约 No.15 / 行情页 No.14", "已是大型加密资产"],
                ["流通市值", "205.65 亿美元", "2.22 亿枚 × 约 93 美元"],
                ["流通量", "2.22 亿 HYPE", "约占总上限 22.2%"],
                ["总供应量", "9.62 亿 HYPE", "与上限 10 亿之间的差额含销毁/未计入"],
                ["最大供应量", "10.00 亿 HYPE", "硬上限"],
                ["全流通市值 FDV", "889.62 亿美元", "若按上限 10 亿计价"],
                ["市值 / FDV", "22.24%", "未来供给膨胀空间很大"],
                ["24h 成交", "约 68.31 万枚 / 6367 万 USDT", "该所永续口径，约 0.64 亿美元"],
            ],
            [38 * mm, 52 * mm, 80 * mm],
            styles,
        )
    )
    story.append(p("表 1　交易所概览页关键数据（用户截图）", styles["caption"]))

    story.append(p("1.2 解锁进度条", styles["h2"]))
    story.append(
        styled_table(
            ["状态", "数量", "占比", "阅读方式"],
            [
                ["已解锁", "3.74 亿", "37.41%", "不等于已经进流通盘"],
                ["待解锁", "20.00 万", "0.02%", "下一次明确事件"],
                ["未解锁", "1.73 亿", "17.37%", "仍在锁定期"],
                ["未追踪", "4.51 亿", "45.19%", "最大的供应迷雾"],
                ["下次解锁", "2026-09-21", "20 万枚 / 约 1779 万美元", "对盘面几乎可以忽略"],
                ["代币配置", "10.00 亿", "100%", "创世分配 31% 已在饼图标出"],
            ],
            [32 * mm, 32 * mm, 28 * mm, 78 * mm],
            styles,
        )
    )
    story.append(p("表 2　代币经济页（用户截图）", styles["caption"]))
    story.append(
        p(
            "下次解锁只有 20 万枚、一家、0.02%。若把「9 月 21 日会大砸盘」当成主风险，方向就偏了。真正需要盯的是：未追踪的 4.51 亿、已解锁但未进入流通的部分、核心贡献者每月可以领但经常少领的额度、以及创世后仍未释放的社区排放。",
            styles["body"],
        )
    )

    story.append(p("1.3 日线图给出的结构信息", styles["h2"]))
    story.append(
        p(
            "日线从 2026 年 1 月附近约 20 美元抬到 9 月约 93 美元，是一轮趋势级上涨，不是几天的脉冲。EMA20 约 82.41、EMA60 约 74.15，价格在均线上方且贴近新高。MACD 仍在零轴上，但高位放量创历史新高，属于「趋势强、赔率变差」的典型位置：中长期叙事可以继续讨论，短线追多的风险收益比已经不好。",
            styles["body"],
        )
    )
    story.append(
        p(
            "若后面出现你说的「回调再开多」，更合理的观察带不是心理整数，而是：先看能否站稳 90；再看 82 附近的 20 日均线是否被趋势交易者当成第一支撑；再看 74 附近的 60 日均线是否变成趋势是否还在的分界。跌破后者，讨论的就不再是「浅回调加仓」，而是趋势级别的修正。这些是结构观察，不是承诺会在这些位置止跌。",
            styles["body"],
        )
    )

    # Section 2
    story.append(p("二、平台独特性：HYPE 不是普通「交易所代币」", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "项目简介写得很清楚：Hyperliquid 是从零优化的高性能 L1，目标是完全链上的开放金融系统；旗舰应用是全链订单簿永续交易所。这句话里有三层别人很难复制的东西。",
            styles["body"],
        )
    )
    story.append(p("2.1 产品形态：链上 CLOB，而不是 AMM 永续", styles["h2"]))
    story.append(
        p(
            "多数 perp DEX 用 AMM、合成池或链下撮合。Hyperliquid 把撮合、保证金、清算都放进自研 L1（HyperBFT），官方称单块最终性、区块延迟小于 1 秒、HyperCore 可支持约 20 万笔订单/秒。对交易者这意味着：体验接近中心化交易所，但结算在链上可核验。这是它能从「积分农场」里活下来、并把未平仓合约份额做得比成交份额更高的根。",
            styles["body"],
        )
    )
    story.append(p("2.2 架构：交易所即公链，公链反哺交易所", styles["h2"]))
    story.append(
        p(
            "HyperCore 负责原生订单簿，HyperEVM 提供以太坊兼容智能合约。HYPE 既是 gas、又是质押、又是 HIP-3/HIP-4 部署门槛、又是手续费回购的标的。BNB 是「交易所 + 公链」的中心化版本；HYPE 想做的是同一结构的链上版本。市场给它的溢价，有一部分已经是在赌这个「L1 溢价」，而不只是 perp DEX 股份。",
            styles["body"],
        )
    )
    story.append(p("2.3 代币机制：费用几乎不进团队口袋", styles["h2"]))
    story.append(
        p(
            "文档口径是：现货与永续手续费主要流向社区（HLP、Assistance Fund、部署者），Assistance Fund 把费用自动换成 HYPE 并销毁。多份 2026 年中的研究把回购比例放在约 97%–99%。The DeFi Report 在 2026 年 7 月的季报里甚至写：过去 90 天验证者增发约 240 万枚，回购约 250 万枚，净增发为负。同时没有传统 VC 大额解锁。这在加密代币里非常少见，也是价格能在「基本面季节性走弱」时仍然强的重要原因。",
            styles["body"],
        )
    )
    story.append(p("2.4 增长方式：把交易所「出租」出去", styles["h2"]))
    story.append(
        p(
            "HIP-3 允许满足 50 万 HYPE 质押门槛的构建者自建永续市场，股票、商品、指数、盘前公司都可以上。HIP-4 则把预测市场/结果合约接到同一套订单簿。平台从「自己开几个币对」变成「金融操作系统」。这扩大了总盘子，也带来后文要说的收入分成和单点依赖问题。",
            styles["body"],
        )
    )
    story.append(p("2.5 团队背景为什么重要", styles["h2"]))
    story.append(
        p(
            "联合创始人 Jeff Yan 有 Hudson River Trading 高频交易背景，后又做市；iliensinc 公开资料称哈佛背景。高频/做市出身做订单簿，比「发代币再找产品」更对口。这解释了为什么对手用补贴能抢走一段时间成交额，却很难在未平仓合约和黏性资金上把 Hyperliquid 搬走。但团队匿名程度仍高于传统金融，治理与验证者结构也并不充分去中心化，后文会写。",
            styles["body"],
        )
    )

    story.append(
        callout(
            "独特性成立，不等于价格可以线性外推",
            "独特性解释的是「为什么 HYPE 能从一堆 perp 代币里走出来，并且在 2026 年仍能创出新高」。它不自动证明 93 美元之上还有一个轻松的 200。越靠近大型资产定价，市场越会用市值、FDV、市销率、回购收益率来约束想象力。",
            styles,
            bg=BG_SOFT,
            border=TEAL,
        )
    )

    # Section 3
    story.append(p("三、代币结构：流通、解锁、未追踪供应与回购销毁", styles["h1"]))
    story.append(hr())
    story.append(p("3.1 官方分配（公开资料综合）", styles["h2"]))
    story.append(
        styled_table(
            ["类别", "占比", "要点"],
            [
                ["未来排放与社区奖励", "约 38.89%", "最大未解之谜：是否、何时、如何进入市场"],
                ["创世分配 / 空投", "31.00%", "TGE 释放，构成当前流通主体"],
                ["核心贡献者", "23.80%", "有锁定期；实际领取长期低于理论线性额度"],
                ["基金会预算", "6.00%", "偏长期线性"],
                ["社区赠款", "0.30%", "规模小"],
                ["HIP-2 流动性", "约 0.01%", "可忽略"],
            ],
            [48 * mm, 32 * mm, 90 * mm],
            styles,
        )
    )
    story.append(p("表 3　HYPE 分配结构", styles["caption"]))

    story.append(p("3.2 三个不能混用的供应数字", styles["h2"]))
    story.append(
        p(
            "这是很多人（包括不少解锁日历网站）会算错的地方。至少要同时看三套数：",
            styles["body"],
        )
    )
    story.extend(
        bullets(
            [
                "流通量（约 2.22 亿）：真正在市场上转的。你的市值 205.65 亿美元用的是它。",
                "已解锁 / 已归属（截图 3.74 亿，部分网站到 4.6–4.7 亿）：法律或合约上可以领，但大量仍躺在归属钱包、基金会或未领取地址里。",
                "上限 10 亿 / 总供应 9.62 亿：FDV 用的是这一层。889 亿美元的「全稀释」已经接近公开可比时段里 BNB 的量级。",
            ],
            styles,
        )
    )
    story.append(
        p(
            "Tokenomist 在 2026 年 4 月的专题把问题说得很白：白皮书线性模型给核心贡献者约每月 992 万枚「理论上限」，基金会实际公告领取可能只有几十万枚，差几十倍。两边都「对」——一个是授权上限，一个是当月执行。对价格真正有冲击的是执行，不是日历上的红字。",
            styles["body"],
        )
    )
    story.append(
        callout(
            "这是双刃剑，不是单边利好",
            "团队少领、晚领，是过去一年供应压力被高估的主因，也是 HYPE 能维持高估值的支柱之一。但「可领而不领」意味着随时可以加速。市场给的是信誉溢价。一旦某个月领取明显抬升、或者 38.89% 社区排放被用来做新一轮增长战争，溢价会压缩得很快。",
            styles,
            bg=BG_WARN,
            border=AMBER,
        )
    )

    story.append(p("3.3 回购能对冲多少抛压", styles["h2"]))
    story.append(
        p(
            "2026 年中公开数据大致是：30 日费用约 0.6–0.8 亿美元量级，大部分进回购；累计 Assistance Fund 买回过约 4450 万枚的量级；但也有报道指出，季度回购金额从 2025 年三季度近 2.9 亿美元降到 2026 年二季度约 1.49 亿美元。成交可以创新高，利润却可以下降——因为 HIP-3 把最高约一半费用分给构建者，同时费率与做市竞争在加重。",
            styles["body"],
        )
    )
    story.append(
        p(
            "用粗算：若回购维持每年 6–8 亿美元，相对当前 205 亿美元流通市值，回购收益率大约 3%–4%；相对 890 亿美元 FDV，只有约 0.7%–0.9%。这个收益率能提供「有人在买」的支撑，远远不够单独把价格抬到 200。到 200 必须靠：交易量台阶上移、费用率不完全被打穿、流通继续被压住、以及市场愿意给交易所+L1 复合溢价。",
            styles["body"],
        )
    )

    # Section 4
    story.append(p("四、到 200 美元：算术、估值台阶、情景与困难度", styles["h1"]))
    story.append(hr())
    story.append(p("4.1 先做算术，再谈故事", styles["h2"]))
    story.append(
        p(
            "从 93.2 到 200，价格倍数只有约 2.15 倍。看起来不远。真正远的是市值口径。",
            styles["body"],
        )
    )
    story.append(
        styled_table(
            ["假设流通量", "200 美元对应市值", "相对当前流通市值", "难度直觉"],
            [
                ["2.22 亿（近似当前）", "444 亿美元", "约 2.16 倍", "难，但若牛市+流通继续被压住，并非科幻"],
                ["3.00 亿", "600 亿美元", "约 2.9 倍", "需要基本面与风险偏好同时配合"],
                ["4.00 亿", "800 亿美元", "约 3.9 倍", "接近公开可比里 BNB 的流通市值带"],
                ["5.00 亿", "1000 亿美元", "约 4.9 倍", "大型资产顶级估值"],
                ["9.62–10 亿（全稀释）", "1924–2000 亿美元", "约 9.4–9.7 倍", "极难，相当于一线公链/交易所代币之上再跳台阶"],
            ],
            [42 * mm, 42 * mm, 42 * mm, 44 * mm],
            styles,
        )
    )
    story.append(p("表 4　200 美元在不同流通口径下的市值含义（按 93.2 与 205.65 亿美元倒推）", styles["caption"]))
    story.append(figure(charts["mc"], "图 1　同一目标价，流通盘每放大一截，需要的市值上台阶", styles))
    story.append(figure(charts["comps"], "图 2　估值台阶示意。BNB、SOL 为 2026 年公开报道的量级区间，不是实时行情。", styles))

    story.append(p("4.2 市场到底在给什么溢价", styles["h2"]))
    story.append(
        p(
            "The DeFi Report 在 2026 年 7 月（当时价格约 67 美元、未到你这张快照的 93）已经警告：费用和活跃度仍偏熊市，但全稀释市销率接近高位（他们给出约 78 倍 FD P/S，流通口径约 18 倍），回购收益率相对峰值下降。之后价格又从约 67 涨到约 93，估值更贵了。这意味着：HYPE 已经被当成「稀缺优质资产」交易，不是「没人要的低估代币」。越贵，对执行的容错越低。",
            styles["body"],
        )
    )
    story.append(
        p(
            "一个有用的对照：Robinhood 这类持牌经纪商的市销率通常远低于加密全稀释倍数；Pump 一类高费用协议的市销率可以更低。市场愿意给 HYPE 高倍数，是因为它同时像交易所股份、L1 gas、回购机器。一旦其中一角被证伪——比如 HyperEVM 长期不起来、或手续费被 0 费率对手打穿——倍数会先掉，价格不必等基本面崩。",
            styles["body"],
        )
    )

    story.append(p("4.3 通往 200 的三条路径，难度完全不同", styles["h2"]))
    story.append(p("路径 A：紧流通路径（相对最不荒谬）", styles["h3"]))
    story.append(
        p(
            "团队继续少领，社区排放不大规模砸出，回购与质押锁定继续工作，流通仍在 2.2–3.0 亿。此时 200 美元对应 440–600 亿美元流通市值。加密若进入风险偏好回升、同时 Hyperliquid 还能从 CEX 永续里再挖几个点的份额，这一档在中期（大约 12–24 个月量级）是「困难但可讨论」的。它依赖一个脆弱前提：供应纪律不翻车。",
            styles["body"],
        )
    )
    story.append(p("路径 B：基本面扩张路径（更健康，也更慢）", styles["h3"]))
    story.append(
        p(
            "费用重新上台阶，不是只靠涨价。粗算：若市场用 25 倍市销给全稀释定价，2000 亿美元 FDV 需要约 80 亿美元年费用；即使用流通市值 444 亿美元和 20 倍市销，也需要约 22 亿美元年费用。而 2026 年中公开的运行速率更接近每年数亿到十亿美元以下。也就是说，健康地走到 200，大概需要费用再上一个数量级，或市场继续给极端溢价。前者要时间，后者脆。",
            styles["body"],
        )
    )
    story.append(p("路径 C：叙事共振路径（最快，也最容易回吐）", styles["h3"]))
    story.append(
        p(
            "美国合规接入、HIP-3 美股/商品成为主流入口、HIP-4 切走预测市场份额、HyperEVM 出现爆款、比特币牛市带动山寨贝塔——几件事叠在一起时，价格可以先于基本面到 200。这在加密里发生过。问题是：你提问时已经在历史新高，这笔「提前计价」的一部分可能已经走完。叙事路径的回撤也会最深。",
            styles["body"],
        )
    )

    story.append(p("4.4 情景带与困难度（主观框架）", styles["h2"]))
    story.append(figure(charts["scen"], "图 3　中长期情景带。中间点是示意中枢，不是目标价。", styles))
    story.append(
        styled_table(
            ["情景", "价格带（示意）", "需要发生什么", "对 200 美元"],
            [
                ["熊市 / 份额回吐", "约 30–60", "监管冲击、对手补贴再起、领取加速、加密整体收缩", "基本关闭"],
                ["基准 / 高位消化", "约 55–110", "平台仍领先，但估值消化新高，供应缓慢增加", "12 个月内很难"],
                ["偏多", "约 85–150", "回购维持、HIP-3 健康扩张、流通仍紧", "靠近下沿，未站稳"],
                ["强牛", "约 130–220", "加密牛市 + 份额再上台阶 + 供应纪律", "可能触及，难以当作中枢"],
                ["极端叙事", "约 180–280+", "L1 溢价 + 美国市场 + 费用数量级上升", "能到，但不应用它做仓位中枢"],
            ],
            [32 * mm, 32 * mm, 68 * mm, 38 * mm],
            styles,
        )
    )
    story.append(p("表 5　主观情景。用于思考，不用于下单。", styles["caption"]))
    story.append(
        p(
            "困难度结论可以写得直白一些：",
            styles["body"],
        )
    )
    story.extend(
        bullets(
            [
                "短线（数周到数月）：在历史新高附近把 200 当目标，难度很高。先要经历你自己说的回调与消化。",
                "中期（约 6–18 个月）：若走「紧流通 + 牛市贝塔」，200 是偏乐观的上沿，不是基准。主观上把它当成低概率事件更诚实——大约是「需要几件好事同时发生」。",
                "长期（约 18–36 个月）：如果 Hyperliquid 真的从 perp DEX 变成链上金融操作系统，200 不再需要奇迹，但仍需要供应不被放出来、以及费用不能长期走下坡。",
                "按全稀释 10 亿枚计的 2000 亿美元：在可见中期应视为极高难度。那已经不是「再翻一倍」的交易，而是改写整个加密市值结构。",
            ],
            styles,
        )
    )

    # Section 5
    story.append(p("五、平台发展前景：增长引擎、竞争、监管与生态", styles["h1"]))
    story.append(hr())
    story.append(p("5.1 已经验证的", styles["h2"]))
    story.extend(
        bullets(
            [
                "产品市场契合真实存在：不是先发代币再找用户。公开统计里，Hyperliquid 在 perp DEX 成交份额常见于约 36%–44%，未平仓合约份额更高，2026 年中有过约 60%–78% 的 DEX OI 占比、全球永续 OI 约 9%–16% 的报道。",
                "资金黏性优于激励型对手：Aster、Lighter 都出现过补贴驱动的份额脉冲，随后回落。Hyperliquid 的份额能回来，说明订单簿深度和清算体验是核心资产。",
                "HIP-3 把 TAM 从加密永续扩到股票、商品、盘前资产。2026 年中 RWA 永续可占成交约三分之一。平台叙事从「去中心化币安永续」变成「链上一切可交易」。",
                "费用回购 + 无 VC 大解锁，是代币层面少见的对齐。",
            ],
            styles,
        )
    )
    story.append(p("5.2 前景里的增长引擎", styles["h2"]))
    story.append(p("引擎一：继续从 CEX 永续里抢份额", styles["h3"]))
    story.append(
        p(
            "即便在 DEX 称王，全球永续成交份额仍大约只有几个点（公开报道约 6% 量级）。这是最大的空白。只要链上体验继续接近 CEX，长期份额仍有空间。但也要承认：Coinbase、Robinhood、Kraken 持牌永续在合规用户里更顺，Lighter 与 Robinhood 订单流的结合说明传统入口不一定经过 Hyperliquid。",
            styles["body"],
        )
    )
    story.append(p("引擎二：HIP-3 交易所即服务", styles["h3"]))
    story.append(
        p(
            "构建者拿最高约 50% 费用，换来新市场和新用户。对平台是「做大蛋糕、让出一刀」。对 HYPE 持有人：成交涨、单笔留存下降。2026 年已出现「量增利减」的讨论。前景取决于新市场是不是增量用户，而不是把原有 BTC/ETH 流量改道。",
            styles["body"],
        )
    )
    story.append(p("引擎三：HIP-4 预测市场", styles["h3"]))
    story.append(
        p(
            "2026 年 5 月主网上线，对标 Polymarket 与 Kalshi 的第三条路：用同一套高性能订单簿做结果合约，结算走验证者与链内规则。Galaxy 等研究把它视为「交易一切」的拼图。目前费用常为测试期零费率，对 HYPE 价值的贡献还小，但对叙事和用户停留时间有意义。",
            styles["body"],
        )
    )
    story.append(p("引擎四：HyperEVM 能否长出非交易应用", styles["h3"]))
    story.append(
        p(
            "这是「L1 溢价」能不能坐实的关键。2026 年二季度前后，HyperEVM 90 日 REV 大约只有 235 万美元量级，日活约 1 万地址，和交易所基本面完全不在一个量级。稳定币供应倒是上得很快（有报道 Q2 约 58 亿美元、环比大增），说明钱愿意停在链上，但还没变成丰富的应用费。前景上：这是最大的期权，也是最大的「可能永远行权失败」的期权。",
            styles["body"],
        )
    )
    story.append(p("引擎五：美国与持牌通道", styles["h3"]))
    story.append(
        p(
            "公开报道提到特朗普曾表示 CFTC 在探讨以合规方式引入 Hyperliquid；另有 Bloomberg 称 Hyperliquid Labs 与 Kraken 母公司/Bitnomial 有过结构讨论。这是双刃剑：打开美国零售与机构，可能改变体量；但合规往往意味着 KYC、产品裁剪、杠杆下降。美国用户本来就被前端限制，监管真正打击的是「无许可杠杆期货」这一层，不是代币能不能在券商上交易。",
            styles["body"],
        )
    )

    story.append(p("5.3 竞争格局：领先，但护城河会被持续测试", styles["h2"]))
    story.append(
        p(
            "Lighter 用零费率、ZK 可验证和传统入口抢零售；Aster 证明了激励可以把成交份额在数周内打到极端；dYdX 仍在找第二曲线；CEX 自己也在上链或上持牌永续。Hyperliquid 的护城河是深度、清算、生态惯性、HIP-3 先发。它不是不可挑战的。手续费并不最低，杠杆也不是最高。长期赢的方式只能是：继续做最像「真正交易所」的链上场所，而不是比谁更补贴。",
            styles["body"],
        )
    )
    story.append(p("5.4 平台前景的总判断", styles["h2"]))
    story.append(
        p(
            "对平台本身，中长期前景是偏强的：它已经赢下了链上永续的第一轮，并且在把边界扩到 RWA 和预测市场。更大的不确定性不在「会不会立刻死掉」，而在「赢了品类之后，利润和代币能不能同比例赢」。量可以继续创新高，费用与回购可以不同步，HyperEVM 可以长期不爆发，监管可以把最高杠杆的那群用户切走一块。所以：平台前景强于代币自动到 200 的前景。这两者必须分开看。",
            styles["body"],
        )
    )

    # Section 6
    story.append(p("六、你可能没注意到的十组关键变量", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "截图已经覆盖了简介、市值、解锁条和日线。下面这些不会写在「项目报告」里，却同样能决定中长期价格和开多品种。",
            styles["body"],
        )
    )

    extras = [
        (
            "1. 「未追踪」45.19% 才是供应主线",
            "下次 20 万枚解锁不是事件。未追踪的 4.51 亿大致对应未来排放、未按交易所模型归类的钱包、以及口径差。中长期价格模型必须给这部分一个假设，不能当 0。",
        ),
        (
            "2. 已解锁 ≠ 已流通",
            "3.74 亿已解锁对上 2.22 亿流通，中间有一块「随时可卖但还没卖」。它现在是潜在抛压，也是潜在利好（说明持有人愿意继续锁）。一旦这块加速进场，市值/FDV 会被迫重估。",
        ),
        (
            "3. HIP-3 的 Trade.xyz 单点依赖",
            "构建者市场一度高度集中，Trade.xyz 在 HIP-3 成交和 OI 上出现过 90%–99% 量级的占比。这是生态繁荣，也是对手方与运营集中度风险。一个头部构建者出问题，RWA 叙事会一起抖。",
        ),
        (
            "4. 量增利减已经发生过",
            "OI 和成交可以创新高，季度协议利润和回购额可以下降。买 HYPE 本质是买「费用流的剩余索取权」。只看成交排行会高估代币。",
        ),
        (
            "5. 验证者与治理并不充分分散",
            "有统计称前十大验证者中基金会实体合计可占质押约一半。对性能导向的链这很常见，但对「去中心化交易所」叙事和监管定性都敏感。质押还有约 2% 量级的奖励，来自未来排放，会轻微稀释。",
        ),
        (
            "6. HyperEVM 目前几乎还不值「L1 溢价」",
            "稳定币多、应用费少，是「钱来了、还没被用起来」。溢价可以提前给，也可以提前收回。",
        ),
        (
            "7. 监管针对的是杠杆期货，不是市值排名",
            "即使 HYPE 能在美国以现货或持牌期货被交易，也不等于 Hyperliquid 前端可以继续对美国用户提供高杠杆永续。合规做大与无许可费用，可能互相挤占。",
        ),
        (
            "8. 价格里嵌着自己的永续赌场",
            "HYPE 本身就是平台上最活跃的交易对之一。新高附近的回调，往往先由资金费率、多头拥挤和强平驱动，而不是由基本面新闻驱动。中长期持有和高杠杆交易同一标的很难兼容。",
        ),
        (
            "9. 无 VC 不是绝对美德",
            "没有早期投资人解锁，减少了「机构倒货日历」。但也减少了传统做市、研究覆盖和合规市场里的长期出资人。流动性在极端行情里会更依赖零售和链上 LP。",
        ),
        (
            "10. 用 HYPE 做保证金等于给波动加杠杆",
            "在 Hyperliquid 或中心化交易所里，只要保证金是 HYPE，下跌就会同时打仓位和抵押品。这和「币本位合约」是同一类风险，不限于某一家交易所的反向合约。",
        ),
    ]
    for title, body in extras:
        story.append(p(title, styles["h3"]))
        story.append(p(body, styles["body"]))

    story.append(
        callout(
            "额外还容易忽略的操作细节",
            "资金费率在山寨强趋势里常常是多头付空头，会慢性侵蚀做多收益；全仓把现货和合约风险焊死；币本位盈利是币、亏损也是币，税务与记账更乱；HIP-3 市场的预言机与清算规则由部署者设置，极端行情的跳空与自动减仓和主簿不完全一样；援助基金销毁会降低总供应，但速度远慢于价格想象。",
            styles,
        )
    )

    # Section 7
    story.append(p("七、下次回调开多：币本位是不是比 U 本位更好", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "先给结论，再给理由。结论取决于你的目标函数，不取决于「哪个看起来更懂」。",
            styles["body"],
        )
    )
    story.append(
        callout(
            "直接回答你的问题",
            "若目标是「回调后做多、用可控的美元风险去捕捉反弹」，U 本位通常更好。若目标是「我已经有 HYPE、坚决不换成稳定币、只想在确认止跌后用低杠杆把币的数量做大」，币本位才有资格进入讨论。大多数人以为自己是第二种，下单时其实是第一种。在历史新高之后的第一次深回调里，选错品种的代价是：U 本位亏钱，币本位可能把现货库存一起亏掉。",
            styles,
            bg=BG_DANGER,
            border=RED,
        )
    )

    story.append(p("7.1 两种合约到底差在哪", styles["h2"]))
    story.append(
        styled_table(
            ["维度", "U 本位（如 HYPEUSDT）", "币本位（如 HYPEUSD 反向）"],
            [
                ["保证金", "USDT/USDC，美元稳定", "HYPE 本身，价格下跌时抵押品变便宜"],
                ["盈亏结算", "稳定币，美元线性", "HYPE，币数量变化"],
                ["上涨时", "赚美元；若仍想囤币，需再买回", "赚更多 HYPE，囤币目标更直接"],
                ["下跌时", "只亏仓位；抵押品价值稳", "仓位亏 + 抵押品贬值，清算更陡"],
                ["深度与滑点", "通常远好于币本位", "往往更薄，大单更伤"],
                ["资金费率", "独立报价，需当时比较", "同样独立；不能默认谁更便宜"],
                ["记账与风控", "美元盈亏清晰", "要用币和美元两套账"],
                ["机会成本", "占用稳定币", "占用的 HYPE 不能同时去质押吃折扣"],
            ],
            [32 * mm, 69 * mm, 69 * mm],
            styles,
        )
    )
    story.append(p("表 6　品种差异。具体杠杆、维持保证金、资金费以你下单的交易所规则为准。", styles["caption"]))

    story.append(p("7.2 为什么「回调开多」尤其不适合高倍币本位", styles["h2"]))
    story.append(
        p(
            "「下次回调开多」这句话里藏着时间顺序：价格先跌，你再买。人很难买在最低点。更常见的是跌了一截就进场，然后还有第二截。U 本位里，第二截只打击仓位。币本位里，第二截同时打击仓位和保证金市值。",
            styles["body"],
        )
    )
    story.append(figure(charts["margin"], "图 4　8 倍做多的示意权益曲线。币本位在下跌中的清算阈值更近。未含手续费、资金费与维持保证金细节。", styles))
    story.append(
        p(
            "粗算直觉：隔离保证金下，U 本位 n 倍多头大约在下跌约 1/n 附近开始危险；币本位多头大约在下跌约 1/(1+n) 附近就可能把权益打穿。8 倍大约是 12.5% 对上约 11%；看起来只差一点，但因为抵押品本身在跌，真实缓冲更薄，插针时更没时间加保证金。若用全仓，现货 HYPE 会成为燃料，一次深针就能把现货库存烧掉。",
            styles["body"],
        )
    )

    story.append(p("7.3 什么时候币本位反而合理", styles["h2"]))
    story.extend(
        bullets(
            [
                "现货库存已经是主仓，稳定币只是零用金，你不愿意在回调时卖币。",
                "回调已经出现止跌结构（例如站回 20 日均线、或日线不再破前低），而不是还在瀑布里抄底。",
                "杠杆很低，例如 2–3 倍思维，而不是 8–20 倍。币本位的意义是轻微放大币的数量，不是赌方向。",
                "目标函数明确是「未来想持有更多 HYPE」，不是「想把账户等值美元做大再看」。",
                "你比较过当时的资金费率、点差、深度，币本位没有明显更贵。",
            ],
            styles,
        )
    )
    story.append(
        p(
            "即使以上都满足，还有一个常常更优的结构：现货在回调中分批买，合约端只用小仓位 U 本位。这样既保留囤币，又把爆仓隔离在稳定币账户里。想要币本位「赚币」的效果，用现货就能做到，不必把库存抵押进去。",
            styles["body"],
        )
    )

    story.append(p("7.4 用一组数字把「赚币幻觉」算清楚", styles["h2"]))
    story.append(
        p(
            "假设回调后在 75 美元开多，后来到 200 美元。忽略费用和资金费。",
            styles["body"],
        )
    )
    story.append(
        styled_table(
            ["方式", "结果直觉", "谁更合适"],
            [
                ["只用现货", "币数不变，美元约 2.67 倍", "中长期仓的底仓"],
                ["U 本位 3x（稳定币保证金）", "美元盈亏约 3 倍于现货涨幅；币数不自动增加", "交易账户、要清晰风控"],
                ["币本位 3x", "成功则 HYPE 数量增加；失败则库存加速减少", "只适合低杠杆、止跌后、以币为本位的人"],
                ["现货底仓 + 小额 U 本位", "底仓不被清算，卫星仓用美元计风险", "多数情景下更干净"],
            ],
            [48 * mm, 72 * mm, 50 * mm],
            styles,
            left_cols=(0, 1, 2),
        )
    )
    story.append(p("表 7　同一段 75→200 的工具比较（示意）", styles["caption"]))
    story.append(
        p(
            "还有反向凸性：币本位多头在大涨时，同样美元名义的盈利折算成币会变少（价格越高，同样一笔美元盈利换到的币越少）。真正「靠合约囤到很多币」往往发生在你低位、低杠杆、且没有被洗出去的时候。从 93 追到 200，再用高倍币本位，数学上并不美。",
            styles["body"],
        )
    )

    story.append(p("7.5 结合当前盘面的选择", styles["h2"]))
    story.extend(
        bullets(
            [
                "提问时已经在 94.54 历史新高附近。回调尚未发生。现在讨论的是未来的入场品种，不是现在追多。",
                "第一次回调若只是到 82 附近，幅度约 12%，8 倍币本位可能已经在清算边缘。同样幅度对 3 倍 U 本位仍有缓冲。",
                "若回调走到 74 附近（约 -20%），高倍仓无论 U 还是币都很难活；低倍 U 本位至少不必叠加抵押品崩塌。",
                "强趋势里资金费率常年偏正，多头有持有成本。持有越久越要算这笔账。币本位若费率更高、深度更差，就更不该选。",
                "若你的主仓已经在现货，下次回调的「开多」完全可以是加现货，而不是再开合约。合约只解决杠杆和方向，不解决长期持有。",
            ],
            styles,
        )
    )

    # Section 8
    story.append(p("八、若仍要交易：结构建议而非点位建议", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "下面不是喊单。它只是把「你的思路」落成可以执行的约束，减少品种选错和仓位过载。",
            styles["body"],
        )
    )
    story.extend(
        bullets(
            [
                "把账户拆开：现货库存账户、稳定币交易账户。不要用全仓把两者焊死。",
                "现货负责中长期平台赌注；合约只做有失效条件的波段。200 美元这种目标更适合现货思维，不适合高杠杆思维。",
                "回调开多用 U 本位做默认。币本位仅作为「低杠杆、止跌确认后、明确要增币」的例外。",
                "杠杆用「还能不能承受再跌一截」反推，而不是用「到 200 能赚多少」反推。后者一定会把杠杆开到危险区。",
                "事先写清失效条件：例如日线收在 60 日均线之下、或团队单月领取显著抬升、或 HIP-3 头部构建者出风险。触发就降杠杆，而不是加杠杆摊平。",
                "为供应事件单独留一份观察清单：每月领取公告、未追踪供应是否开始归类、回购额是否继续下滑、基金会验证者占比。",
                "不要把平台前景自动翻译成仓位大小。前景强，只说明值得跟踪；价格已经反映很多前景。",
            ],
            styles,
        )
    )

    # Section 9
    story.append(p("九、总结", styles["h1"]))
    story.append(hr())
    story.append(p("关于平台", styles["h2"]))
    story.append(
        p(
            "Hyperliquid 是目前链上永续里最接近「真交易所」的系统：自研 L1、全链订单簿、费用回购、无传统 VC 大解锁、HIP-3 把市场扩展到 RWA、HIP-4 再接预测市场。中长期平台前景偏强，竞争和监管会反复来，但第一轮品类战争它已经赢了。更大的问题是赢了之后利润率和代币稀缺性还能不能一起赢。",
            styles["body"],
        )
    )
    story.append(p("关于到 200 美元", styles["h2"]))
    story.append(
        p(
            "价格倍数只有约 2.15 倍，估值倍数要看口径。流通继续被压在约 2.2–3 亿时，200 美元对应约 440–600 亿美元市值，属于「强牛 + 供应纪律」下的困难目标，不是基准情形。若市场改用 10 亿枚全稀释来定价，200 美元就是约 2000 亿美元，中期极难。提问时已经在历史新高，短线把 200 当下一步，难度高于中长期把 200 当乐观上沿。",
            styles["body"],
        )
    )
    story.append(p("关于你可能漏看的", styles["h2"]))
    story.append(
        p(
            "不要被 9 月 21 日 20 万枚解锁吸引注意力。要盯未追踪的 4.51 亿、已解锁未流通的缺口、团队随时可加速的领取权、HIP-3 收入分流与 Trade.xyz 集中度、HyperEVM 仍然很弱的应用费、验证者集中、监管对无许可杠杆的压力，以及 HYPE 永续上的拥挤杠杆。平台可以继续好，代币也可以因为估值和供应重定价而长期横盘。",
            styles["body"],
        )
    )
    story.append(p("关于币本位还是 U 本位", styles["h2"]))
    story.append(
        p(
            "下次回调开多，默认选 U 本位。币本位只有在「以增币为目标、低杠杆、确认止跌、且不把全部库存拿去当保证金」时才更好。回调过程中币本位是双杀；你要的是回调之后的反弹，不是回调过程中的殉葬。若真正看好中长期平台，更干净的结构是：现货做底仓，U 本位做可抛弃的卫星仓，而不是把 HYPE 抵押进高倍反向合约。",
            styles["body"],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        callout(
            "最后一句",
            "独特性支持「值得认真对待」，不支持「从历史新高直线走到 200」。把平台前景、代币供应、估值口径、合约品种四件事拆开看，比在一个 K 线上寻找答案更接近事实。",
            styles,
            bg=BG_SOFT,
            border=TEAL_DARK,
        )
    )

    story.append(p("附录：主要来源与口径说明", styles["h1"]))
    story.append(hr())
    story.append(
        p(
            "价格、流通、FDV、解锁条、均线与成交来自你提供的交易所截图（约 2026-09-19）。机制与产品描述参考 Hyperliquid 文档（HyperCore / HyperEVM / HIP-3 / HIP-4 / Staking / Fees）。供应与领取差异参考 Tokenomist 对「理论解锁 vs 实际领取」的跟踪。成交、OI、费用、回购、HIP-3 与 HyperEVM 数据参考 DefiLlama 口径的二手汇编（CoinLaw、The DeFi Report、CoinDesk、HTX Insights 等 2026 年中报道）。竞争与监管参考 perp DEX 份额综述及 BlockFirms / Bloomberg 转述的美国合规讨论。BNB、SOL 市值仅作量级对照。",
            styles["body"],
        )
    )
    story.append(
        p(
            "同一指标在不同网站会不一致：流通量、已解锁、已领取、FDV 分母（总供应还是最大供应）尤其混乱。本文以你的截图为交易决策快照，用公开研究解释机制，不试图伪造一个「唯一正确」的链上数字。所有情景带、困难度、品种选择都是分析框架，会随新数据失效。",
            styles["body"],
        )
    )
    story.append(Spacer(1, 6 * mm))
    story.append(
        p(
            "文档生成日期：2026-09-19。本文不构成投资、法律或税务建议。杠杆交易可能导致超过本金的损失。",
            styles["small"],
        )
    )

    def first_page(canvas, doc):
        cover_page(canvas, doc)

    doc.build(story, onFirstPage=first_page, onLaterPages=header_footer)
    print(f"Wrote {PDF_PATH}")
    return PDF_PATH


if __name__ == "__main__":
    build()
