# -*- coding: utf-8 -*-
"""
trading-handbook.pdf 插图还原脚本（v2 质量修复版）
用 matplotlib 重新绘制 PDF 中的 9 张教学示意图（TradingView 白底风格）：
- 红 = 下跌 (239,83,80)，青 = 上涨/标注 (38,166,154)
- 输出到 handbook/images/，覆盖同名 PNG，保持 markdown 引用不变

v2 修复：
- fig_p41_x187（Wyckoff）：新增成交量面板（SC 巨量 / ST 缩量 / SOS 放量），
  区间线对齐真实高低点，所有事件标注改用引线指向准确位置
- fig_p23_x139（内包线）：母线高低点虚线修正到真实高低点，标注带引线
- fig_p13_x111（K 线结构）：实体/影线比例均衡，标注全部带引线
- fig_p15_x117（趋势）：HH/HL/LH/LL 标注坐标修正（原为错误值），趋势线连对结构点
- fig_p16_x120（支撑阻力）：支撑线对齐多次测试低点
- fig_p17_x123（锤子线 sweep）：支撑线对齐真实前低
- fig_p23_x138（吞没）：吞没范围竖线修正到两根实体区间

运行：python draw_handbook_figs.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

UP = "#26a69a"      # 上涨/多头
DOWN = "#ef5350"    # 下跌/空头
TEAL = "#26a69a"    # 结构标注线
DARK = "#263238"    # 深色文字
GRAY = "#90a4ae"
ORANGE = "#ff9800"

OUT = os.path.join("handbook", "images")


def candle(ax, x, o, h, l, c, width=0.55, alpha=1.0, zorder=3):
    """画一根 K 线，返回收盘是否上涨"""
    up = c >= o
    color = UP if up else DOWN
    ax.plot([x, x], [l, h], color=color, linewidth=1.1, alpha=alpha, zorder=zorder - 1)
    body_h = abs(c - o)
    if body_h < 1e-6:
        ax.plot([x - width / 2, x + width / 2], [c, c], color=color, linewidth=1.6, zorder=zorder, alpha=alpha)
    else:
        ax.add_patch(Rectangle((x - width / 2, min(o, c)), width, body_h,
                               facecolor=color, edgecolor=color, alpha=alpha, zorder=zorder))
    return up


def hl_line(ax, x0, x1, y, color=TEAL, ls="--", lw=1.2, label=None):
    """水平虚线 + 可选文字标签（标签放线右端上方，避免超出图幅）"""
    ax.plot([x0, x1], [y, y], color=color, ls=ls, lw=lw, zorder=2)
    if label:
        ax.text(x1 - 0.15, y, label, fontsize=10, color=color, va="bottom", ha="right", zorder=5)


def mark(ax, x, y, text, dy=0.0, color=DARK, fs=10, va="bottom", ha="center", box=False):
    """标注点"""
    if box:
        ax.text(x, y + dy, text, fontsize=fs, color=color, va=va, ha=ha, zorder=5,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.8))
    else:
        ax.text(x, y + dy, text, fontsize=fs, color=color, va=va, ha=ha, zorder=5)


def annotate_mark(ax, x, y, text, x_text, y_text, color=DARK, fs=10, va="center", ha="left", box=True):
    """带引线的标注：引线从文字框指向 (x, y) 目标点"""
    ax.annotate(text, xy=(x, y), xytext=(x_text, y_text),
                fontsize=fs, color=color, va=va, ha=ha, zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.0,
                                connectionstyle="arc3,rad=0.12"),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.8) if box else None)


def arrows(ax, x, y0, y1, color=TEAL, lw=1.4):
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw), zorder=4)


def style_ax(ax, xlim=None, ylim=None):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_facecolor("white")


def savefig(fig, name, dpi=160):
    fig.savefig(os.path.join(OUT, name), dpi=dpi, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"已生成 {name}")


# ---------------------------------------------------------------- 图 2-1
def fig_kline_structure():
    """2.1 一根 K 线的结构：实体与影线（放大单根 K 线 + OHLC 标注）"""
    fig, ax = plt.subplots(figsize=(10.5, 6.1))
    style_ax(ax, xlim=(-1.8, 9.5), ylim=(90, 122))
    o, c, h, l = 100.0, 110.0, 115.0, 95.0
    candle(ax, 2.6, o, h, l, c, width=2.0)
    # OHLC 虚线标注（左侧紧凑排列）
    for y, name in [(h, "最高价"), (l, "最低价"), (o, "开盘价"), (c, "收盘价")]:
        ax.plot([-0.8, 2.6], [y, y], color=GRAY, ls=":", lw=1.0, zorder=1)
        ax.text(-1.0, y, f"{name} {y:.0f}", fontsize=10.5, color=DARK, ha="right", va="center", zorder=5)
    # 上影线/下影线/实体：带引线标注
    annotate_mark(ax, 2.6, (h + c) / 2, "上影线：多头上攻后\n被空头压回（拒绝）",
                  4.4, 116.8, color=DARK, fs=11)
    annotate_mark(ax, 2.6, (l + o) / 2, "下影线：空头下压后\n被多头拉回（承接）",
                  4.4, 93.8, color=DARK, fs=11)
    annotate_mark(ax, 2.6, (o + c) / 2, "实体：阳线 = 多头赢\n越长赢得越彻底",
                  4.4, 106.5, color=UP, fs=11)
    savefig(fig, "fig_p13_x111.png")


# ---------------------------------------------------------------- 图 2-2
def fig_trend():
    """2.3 趋势：左上升 HH/HL，右下降 LH/LL（标注指向真实摆动点）"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))
    # 上升趋势：低点 97→103→107→108 抬高，高点 105→106→110→115 抬高
    k1 = [(0, 100, 104, 97, 97), (1, 97, 103, 94, 102), (2, 102, 105, 99, 99),
          (3, 99, 101, 97, 100), (4, 100, 106, 98, 105), (5, 105, 108, 103, 104),
          (6, 104, 106, 102, 105), (7, 105, 110, 104, 109), (8, 109, 111, 107, 108),
          (9, 108, 110, 106, 109), (10, 109, 113, 108, 112), (11, 112, 115, 110, 114)]
    for x, o, h, l, c in k1:
        candle(ax1, x, o, h, l, c)
    hh = [(2, 105), (4, 106), (7, 110), (11, 115)]   # 摆动高点
    hl = [(3, 97), (5, 103), (8, 107), (10, 108)]    # 摆动低点
    for x, y in hh:
        mark(ax1, x, y, "HH", dy=2.6, color=UP, fs=10, va="bottom")
    for x, y in hl:
        mark(ax1, x, y, "HL", dy=-2.6, color=DOWN, fs=10, va="top")
    # 上升趋势线：连接依次抬高的低点
    ax1.plot([3, 5, 8, 10], [97, 103, 107, 108], color=TEAL, ls="--", lw=1.2, zorder=2)
    mark(ax1, 5.5, 115.5, "上升趋势：HH + HL 依次抬高", fs=12, color=UP, box=True)
    style_ax(ax1, xlim=(-0.6, 12.2), ylim=(86, 119))
    # 下降趋势：高点 114→113→110 降低，低点 111→108→103 降低
    k2 = [(0, 114, 116, 111, 111), (1, 111, 114, 109, 113), (2, 113, 115, 111, 112),
          (3, 112, 114, 109, 110), (4, 110, 113, 108, 112), (5, 112, 113, 109, 109),
          (6, 109, 111, 106, 107), (7, 107, 110, 105, 109), (8, 109, 110, 106, 106),
          (9, 106, 109, 103, 104), (10, 104, 107, 102, 106), (11, 106, 108, 103, 103)]
    for x, o, h, l, c in k2:
        candle(ax2, x, o, h, l, c)
    lh = [(1, 114), (5, 113), (8, 110)]   # 摆动高点
    ll = [(0, 111), (4, 108), (9, 103)]   # 摆动低点
    for x, y in lh:
        mark(ax2, x, y, "LH", dy=2.6, color=UP, fs=10, va="bottom")
    for x, y in ll:
        mark(ax2, x, y, "LL", dy=-2.6, color=DOWN, fs=10, va="top")
    # 下降趋势线：连接依次降低的高点
    ax2.plot([1, 5, 8], [114, 113, 110], color=TEAL, ls="--", lw=1.2, zorder=2)
    mark(ax2, 5.5, 115.5, "下降趋势：LH + LL 依次降低", fs=12, color=DOWN, box=True)
    style_ax(ax2, xlim=(-0.6, 12.2), ylim=(86, 119))
    savefig(fig, "fig_p15_x117.png")


# ---------------------------------------------------------------- 图 2-3
def fig_support_resistance():
    """2.4 支撑与阻力：多次测试、突破、回踩角色互换"""
    fig, ax = plt.subplots(figsize=(13, 6.3))
    style_ax(ax, xlim=(-0.8, 16.2), ylim=(88, 112))
    # 区间 94.5~100.5：低点多次触 94.5，高点多次触 100.5；k10 放量突破后回踩
    k = [(0, 99, 102, 97, 98), (1, 98, 100, 94.5, 95.5), (2, 96, 99, 95, 97),
         (3, 97, 101, 96, 98), (4, 98, 100, 94.5, 95.5), (5, 96, 99, 95, 97),
         (6, 98, 101, 97, 98), (7, 98, 100.5, 94.5, 95.5), (8, 96, 99, 94.5, 96),
         (9, 97, 101, 96, 99), (10, 99, 104, 98, 102),  # 放量突破
         (11, 102, 105, 100, 103), (12, 103, 106, 101.5, 104),  # 回踩不破
         (13, 104, 107, 102.5, 105), (14, 105, 108, 103.5, 106)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    support, resist = 94.5, 100.5
    hl_line(ax, -0.6, 8.6, resist, label="阻力（多次测试）")
    hl_line(ax, -0.6, 13.0, support, label="支撑（多次测试）")
    hl_line(ax, 9.0, 14.4, resist, color=TEAL, ls="-.")
    annotate_mark(ax, 10, 104.2, "放量突破", 9.6, 108.2, color=UP, fs=10.5, ha="left")
    annotate_mark(ax, 12, 101.8, "回踩不破\n支撑→阻力", 12.8, 97.2, color=ORANGE, fs=10.5, ha="left")
    savefig(fig, "fig_p16_x120.png")


# ---------------------------------------------------------------- 图 2-4
def fig_hammer_sweep():
    """2.6 实战演练：回调到支撑 → 跌破（sweep）→ 锤子线拉回"""
    fig, ax = plt.subplots(figsize=(13, 6.3))
    style_ax(ax, xlim=(-0.8, 17.5), ylim=(88, 114))
    k = [(0, 97, 100, 94, 95), (1, 95, 99, 93, 97), (2, 97, 101, 95, 96),
         (3, 96, 100, 94, 98), (4, 98, 103, 96, 100), (5, 100, 104, 98, 99),
         (6, 99, 102, 96, 97), (7, 97, 100, 95, 98), (8, 98, 101, 96, 97),
         (9, 97, 100, 95, 98), (10, 98, 101, 96, 97), (11, 97, 100, 95, 99),
         (12, 99, 101, 96, 96.5),   # 回踩支撑
         (13, 96.5, 100, 95.2, 99.5),  # 跌破支撑后锤子线拉回（sweep）
         (14, 99.5, 102, 98, 100), (15, 100, 104, 99, 102), (16, 102, 105, 101, 103)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    support = 96.0
    hl_line(ax, -0.6, 13.2, support, label="支撑（前低 / HL 区，多次测试）")
    annotate_mark(ax, 12, 96.3, "回踩支撑\n（第 4 次测试）", 10.6, 91.6, color=DARK, fs=10, ha="left")
    annotate_mark(ax, 13, 95.6, "跌破支撑扫止损\n锤子线快速拉回 = sweep", 13.9, 90.8, color=UP, fs=10.5, ha="left")
    arrows(ax, 13.3, 96.8, 99.2, color=UP)
    annotate_mark(ax, 15, 102.6, "顺势做多：目标前高", 15.6, 107.4, color=UP, fs=10.5, ha="left")
    savefig(fig, "fig_p17_x123.png")


# ---------------------------------------------------------------- 图 3-1
def fig_false_breakout():
    """3.1 假突破：冲破前高后收回，扫掉追突破者止损"""
    fig, ax = plt.subplots(figsize=(12.5, 6.3))
    style_ax(ax, xlim=(-0.8, 16.5), ylim=(88, 120))
    k = [(0, 98, 102, 94, 94), (1, 94, 101, 92, 99), (2, 99, 103, 97, 98),
         (3, 98, 102, 96, 100), (4, 100, 104, 98, 101), (5, 101, 105, 99, 102),
         (6, 102, 106, 100, 103), (7, 103, 107, 101, 104), (8, 104, 108, 102, 105),
         (9, 105, 113.5, 106.5, 112),  # 冲破前高
         (10, 112, 113, 104, 105),  # 长上影收回（假突破）
         (11, 105, 107, 100, 101), (12, 101, 104, 97, 98), (13, 98, 102, 95, 97),
         (14, 97, 100, 92, 93)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    resist = 108.0
    hl_line(ax, -0.6, 8.6, resist, label="前高（阻力）")
    hl_line(ax, 9.0, 10.4, resist, color=GRAY, ls=":")
    annotate_mark(ax, 9, 113.6, "冲破前高\n追突破者进场", 8.2, 118.2, color=UP, fs=10, ha="left")
    annotate_mark(ax, 10, 108.9, "收回前高下方（长上影）\n假突破成立 → 做空", 11.0, 116.0, color=DOWN, fs=10, ha="left")
    arrows(ax, 10.6, 105.5, 100.5, color=DOWN)
    annotate_mark(ax, 14, 92.8, "下方止损被扫 →\n成为反向燃料", 14.9, 88.8, color=DOWN, fs=10, ha="left")
    savefig(fig, "fig_p21_x133.png")


# ---------------------------------------------------------------- 图 3-3
def fig_engulfing():
    """3.3 看涨吞没：小阴线被大阳线完全包住（放量）"""
    fig, ax = plt.subplots(figsize=(11, 5.8))
    style_ax(ax, xlim=(-2, 14), ylim=(86, 118))
    k = [(0, 103, 106, 99, 99), (1, 99, 103, 96, 101), (2, 101, 104, 98, 100),
         (3, 100, 103, 97, 99), (4, 99, 102, 96, 97), (5, 97, 100, 94, 96),
         (6, 96, 99, 93, 95), (7, 95, 98, 92, 93), (8, 93, 96, 90, 91),  # 小阴线（犹豫）
         (9, 91, 101.5, 88.5, 100),  # 大阳线吞没
         (10, 100, 103, 98, 101), (11, 101, 104, 99, 102), (12, 102, 107, 101, 105)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    annotate_mark(ax, 8, 93.5, "小阴线（犹豫）", 6.0, 90.0, color=DOWN, fs=10, ha="left")
    annotate_mark(ax, 9, 99.0, "看涨吞没：大阳线实体\n完全包住前一根 + 放量", 10.3, 87.8, color=UP, fs=10, ha="left")
    # 标出吞没范围：两根 K 线的实体区间（小阴线实体 91~93，大阳线实体 91~100）
    ax.plot([8.45, 8.45], [90.5, 101], color=ORANGE, lw=1.2, ls=":", zorder=4)
    ax.plot([9.55, 9.55], [90.5, 101], color=ORANGE, lw=1.2, ls=":", zorder=4)
    ax.plot([8.45, 9.55], [90.5, 90.5], color=ORANGE, lw=1.2, ls=":", zorder=4)
    ax.plot([8.45, 9.55], [101, 101], color=ORANGE, lw=1.2, ls=":", zorder=4)
    annotate_mark(ax, 11.5, 105.8, "继续上涨", 10.2, 110.5, color=UP, fs=10.5, ha="left")
    arrows(ax, 11.3, 103, 105.2, color=UP)
    savefig(fig, "fig_p23_x138.png")


# ---------------------------------------------------------------- 图 3-4
def fig_inside_bar():
    """3.4 内包线：子线完全在母线范围内，等待突破方向"""
    fig, ax = plt.subplots(figsize=(11, 5.8))
    style_ax(ax, xlim=(-2, 14), ylim=(88, 116))
    k = [(0, 97, 101, 93, 93), (1, 93, 99, 90, 97), (2, 97, 101, 95, 96),
         (3, 96, 100, 94, 98), (4, 98, 103, 97, 100), (5, 100, 103, 98, 99),
         (6, 99, 102, 97, 100), (7, 100, 104, 99, 100.5),   # 母线：高 104 / 低 99
         (8, 100.5, 102.5, 99.5, 101.5),  # 子线：高 102.5 / 低 99.5（内包）
         (9, 101.5, 106, 100, 104), (10, 104, 107, 102, 103), (11, 103, 106, 101, 104),
         (12, 104, 108, 103, 106)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, 6.6, 9.3, 104, color=ORANGE, label="母线高点 104")
    hl_line(ax, 6.6, 9.3, 99, color=ORANGE, label="母线低点 99")
    annotate_mark(ax, 8, 102.4, "子线：波动收缩\n完全在母线范围内", 4.3, 111.0, color=DARK, fs=10, ha="left")
    annotate_mark(ax, 9, 105.2, "突破子线高点 → 做多", 9.6, 112.5, color=UP, fs=10.5, ha="left")
    arrows(ax, 9.4, 103.5, 105.2, color=UP)
    savefig(fig, "fig_p23_x139.png")


# ---------------------------------------------------------------- 图 4-1
def fig_pullback_system():
    """4.2 系统一：趋势回调交易 完整一笔（入场/止损/目标标注）"""
    fig, ax = plt.subplots(figsize=(13.5, 6.9))
    style_ax(ax, xlim=(-1, 19), ylim=(98, 134))
    k = [(0, 108, 112, 104, 104), (1, 104, 110, 101, 108), (2, 108, 112, 106, 107),
         (3, 107, 111, 105, 109), (4, 109, 113, 107, 110), (5, 110, 113, 108, 109),
         (6, 109, 112, 107, 110), (7, 110, 115, 109, 113),  # HH
         (8, 113, 115, 110, 111), (9, 111, 113, 108, 110), (10, 110, 112, 107, 108),
         (11, 108, 110, 105, 106), (12, 106, 108, 103, 104),  # 回调到 HL 区
         (13, 104, 108, 101.5, 107),  # 锤子线确认
         (14, 107, 112, 106, 110),  # 入场后上涨
         (15, 110, 114, 109, 112), (16, 112, 115.5, 111, 113),  # 新 HL
         (17, 113, 117, 112, 115), (18, 115, 118.5, 114, 117)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    entry, stop, target = 106.5, 100.5, 114.8
    hl_line(ax, -1, 18.8, stop, color=DOWN, label="止损（HL 下方）")
    hl_line(ax, -1, 18.8, target, color=TEAL, label="目标（前高 / 2R+）")
    annotate_mark(ax, 12, 104.2, "回调到 HL 区", 9.6, 100.6, color=DOWN, fs=10, ha="left")
    annotate_mark(ax, 13, 107.2, "入场：锤子线确认", 11.6, 112.2, color=UP, fs=10.5, ha="left")
    arrows(ax, 14.3, 106.5, 103.5, color=DOWN)
    ax.annotate("", xy=(14.5, target), xytext=(14.5, entry),
                arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.4), zorder=4)
    annotate_mark(ax, 15.2, (entry + target) / 2, "盈亏比 ≥ 2", 16.4, 108.2, color=TEAL, fs=10, ha="left")
    # 趋势结构线：连接 HH
    ax.plot([7, 11, 16], [114, 109, 114.5], color=TEAL, ls="--", lw=1.0, zorder=2)
    savefig(fig, "fig_p28_x150.png")


# ---------------------------------------------------------------- 图 5-1
def fig_wyckoff():
    """5.10 Wyckoff 吸筹：PS→SC→AR→ST→Spring→SOS→LPS（含成交量面板）"""
    fig, (ax, axv) = plt.subplots(2, 1, figsize=(14, 7.6), sharex=True,
                                  gridspec_kw={"height_ratios": [3.1, 1], "hspace": 0.06})
    style_ax(ax, xlim=(-1, 17.5), ylim=(92.5, 113))
    # 价格 K 线：下跌 → PS → SC(巨量长下影) → AR → ST(缩量不破) → 区间 → Spring → SOS → LPS
    k = [(0, 110, 112, 107, 108), (1, 108, 110, 105, 106), (2, 106, 108, 103, 104),
         (3, 104, 106, 101, 102), (4, 102, 105, 99, 100),   # PS：下跌放缓，量开始放大
         (5, 100, 103, 94.5, 96),   # SC：恐慌抛售，巨量长下影
         (6, 96, 99.5, 95, 98),     # AR：自动反弹
         (7, 98, 100, 96.5, 97),
         (8, 97, 99, 94.8, 96),     # ST：二次测试，缩量不破 SC 低点
         (9, 96, 98, 95, 96.5), (10, 96.5, 98.5, 95.2, 97), (11, 97, 99, 95.5, 96.5),
         (12, 96.5, 98.5, 95.3, 97.5),  # 区间震荡（吸筹）
         (13, 97, 98.5, 94.2, 97.5),     # Spring：跌破下沿扫止损后拉回，量放大
         (14, 97.5, 101, 96.5, 100.5),   # SOS：放量突破区间上沿
         (15, 100.5, 102, 99, 99.5),     # LPS：回踩上沿不破，缩量
         (16, 99.5, 102.5, 99, 101)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    lo, hi = 95.0, 99.5
    hl_line(ax, 5.5, 14.4, hi, color=GRAY, label="区间上沿（AR 高点）")
    hl_line(ax, 5.5, 14.4, lo, color=GRAY, label="区间下沿（SC 低点上方）")
    # 事件标注（带引线，避免重叠）
    annotate_mark(ax, 4, 105.0, "PS\n初现支撑", 2.0, 110.8, color=DARK, fs=9.5, ha="left")
    annotate_mark(ax, 5, 95.5, "SC 卖出高潮\n巨量 + 长下影", 0.6, 100.2, color=DOWN, fs=9.5, ha="left")
    annotate_mark(ax, 6, 99.2, "AR\n自动反弹", 5.0, 110.8, color=UP, fs=9.5, ha="left")
    annotate_mark(ax, 8, 95.5, "ST 二次测试\n缩量不破", 8.6, 100.4, color=ORANGE, fs=9.5, ha="left")
    annotate_mark(ax, 13, 95.0, "Spring 弹簧\n跌破下沿扫止损后拉回", 13.0, 100.6, color=ORANGE, fs=9.5, ha="left")
    annotate_mark(ax, 14, 100.8, "SOS 强势信号\n放量突破", 13.2, 109.0, color=UP, fs=9.5, ha="left")
    annotate_mark(ax, 15, 100.0, "LPS\n最后支撑点", 15.4, 109.0, color=UP, fs=9.5, ha="left")
    mark(ax, 8.2, 107.5, "吸筹区间：机构低位收集筹码", fs=12, color=UP, box=True)
    # 成交量面板：SC 巨量、ST 缩量、SOS 放量、LPS 缩量
    vols = [22, 20, 18, 16, 24, 45, 30, 22, 14, 18, 17, 16, 15, 35, 52, 22, 26]
    for (x, o, h, l, c), v in zip(k, vols):
        up = c >= o
        color = UP if up else DOWN
        axv.bar(x, v, width=0.55, color=color, alpha=0.75, zorder=3)
    style_ax(axv, ylim=(0, 60))
    for s in axv.spines.values():
        s.set_visible(True)
    axv.spines["left"].set_visible(False)
    axv.spines["top"].set_visible(False)
    axv.spines["right"].set_visible(False)
    axv.set_yticks([])
    axv.annotate("SC 巨量", xy=(5, 45), xytext=(2.6, 50),
                 fontsize=9, color=DOWN, va="bottom",
                 arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    axv.annotate("ST 缩量", xy=(8, 14), xytext=(6.4, 24),
                 fontsize=9, color=ORANGE, va="bottom",
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    axv.annotate("SOS 放量", xy=(14, 52), xytext=(12.2, 56),
                 fontsize=9, color=UP, va="bottom",
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    savefig(fig, "fig_p41_x187.png")


# ---------------------------------------------------------------- 新增：4.5 状态机

def draw_box(ax, x, y, w, h, text, ec=TEAL, fs=11, tc=DARK):
    """流程图方框"""
    ax.add_patch(Rectangle((x, y), w, h, facecolor="white", edgecolor=ec, lw=1.6, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, fontsize=fs, ha="center", va="center",
            color=tc, zorder=4, linespacing=1.5)


def flow_arrow(ax, x0, y0, x1, y1, color=DARK, ls="-", rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5, ls=ls,
                                connectionstyle=f"arc3,rad={rad}"), zorder=2)


def fig_state_machine():
    """4.5 状态机：结构判定 → 三系统切换（新增代码图，替换 ASCII）"""
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    style_ax(ax, xlim=(0, 13.2), ylim=(0, 6.6))
    # 左列：结构判定
    draw_box(ax, 0.3, 3.0, 2.1, 1.1, "结构判定\nHH+HL / LH+LL / 区间", ec=DARK)
    # 中列：三种状态
    draw_box(ax, 4.0, 5.2, 2.2, 1.0, "上升趋势", ec=UP)
    draw_box(ax, 4.0, 3.0, 2.2, 1.0, "下降趋势", ec=DOWN)
    draw_box(ax, 4.0, 0.5, 2.2, 1.0, "区间", ec=ORANGE)
    # 区间分支
    draw_box(ax, 7.8, 1.7, 2.0, 0.9, "边界未破", ec=ORANGE, fs=10.5)
    draw_box(ax, 7.8, 0.3, 2.0, 0.9, "边界被破", ec=ORANGE, fs=10.5)
    # 右列：系统
    draw_box(ax, 10.5, 5.2, 2.5, 1.0, "系统一\n顺势回调做多", ec=UP, fs=10.5)
    draw_box(ax, 10.5, 3.0, 2.5, 1.0, "系统一（镜像）\n下降趋势做空", ec=DOWN, fs=10.5)
    draw_box(ax, 10.5, 1.7, 2.5, 0.9, "系统二\n区间边界反向", ec=ORANGE, fs=10.5)
    draw_box(ax, 10.5, 0.3, 2.5, 0.9, "系统三\n突破跟随", ec=ORANGE, fs=10.5)
    # 连线
    flow_arrow(ax, 2.4, 4.05, 4.0, 5.7, rad=0.18)   # 结构判定 → 上升
    flow_arrow(ax, 2.4, 3.55, 4.0, 3.5)             # 结构判定 → 下降
    flow_arrow(ax, 2.4, 3.0, 4.0, 1.0, rad=-0.18)   # 结构判定 → 区间
    flow_arrow(ax, 6.2, 5.7, 10.5, 5.7)             # 上升 → 系统一
    flow_arrow(ax, 6.2, 3.5, 10.5, 3.5)             # 下降 → 系统一镜像
    flow_arrow(ax, 6.2, 1.3, 7.8, 1.3, rad=-0.25)   # 区间 → 边界未破
    flow_arrow(ax, 6.2, 0.7, 7.8, 0.4, rad=0.25)    # 区间 → 边界被破
    flow_arrow(ax, 9.8, 2.15, 10.5, 2.15)           # 边界未破 → 系统二
    flow_arrow(ax, 9.8, 0.75, 10.5, 0.75)           # 边界被破 → 系统三
    flow_arrow(ax, 12.2, 1.2, 12.2, 4.6, color=GRAY, ls="--", rad=0.3)  # 系统三 → 系统一（回注）
    mark(ax, 11.9, 2.9, "回到系统一", fs=9.5, color=GRAY, va="bottom", ha="right")
    savefig(fig, "fig_p4_state_machine.png")


# ---------------------------------------------------------------- 新增：5.2 流动性池

def fig_liquidity_pool():
    """5.2 流动性池：前高上方 BSL、前低下方 SSL"""
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    style_ax(ax, xlim=(-0.8, 12.5), ylim=(89, 115))
    k = [(0, 98, 101, 96, 97), (1, 97, 100, 95, 99), (2, 99, 103, 98, 101),
         (3, 101, 104, 99, 102), (4, 102, 103, 99, 100), (5, 100, 102, 97, 98),
         (6, 98, 101, 96, 99), (7, 99, 102, 98, 100), (8, 100, 104, 99, 102),
         (9, 102, 106, 101, 104)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hi, lo = 103.5, 96.0
    # 流动性池色块
    ax.add_patch(Rectangle((-0.55, hi), 10.1, 5.5, facecolor=UP, alpha=0.12, zorder=1))
    ax.add_patch(Rectangle((-0.55, lo - 5.5), 10.1, 5.5, facecolor=DOWN, alpha=0.12, zorder=1))
    hl_line(ax, -0.6, 9.5, hi, color=UP, label="前高（被测试 3 次）")
    hl_line(ax, -0.6, 8.0, lo, color=DOWN, label="前低（被测试 2 次）")
    annotate_mark(ax, 8.5, 105.5, "BSL 买方流动性\n（空头止损 + 追多止损）", 9.3, 111.5, color=UP, fs=10.5, ha="left")
    annotate_mark(ax, 8.5, 94.0, "SSL 卖方流动性\n（多头止损 + 追空止损）", 9.3, 90.5, color=DOWN, fs=10.5, ha="left")
    savefig(fig, "fig_p5_liquidity.png")


# ---------------------------------------------------------------- 新增：5.3 sweep

def fig_sweep():
    """5.3 sweep：插破前高扫 BSL 后快速收回，真方向向下"""
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    style_ax(ax, xlim=(-0.8, 13.5), ylim=(88, 116))
    k = [(0, 98, 102, 94, 94), (1, 94, 101, 92, 99), (2, 99, 103, 97, 98),
         (3, 98, 102, 96, 100), (4, 100, 104, 98, 101), (5, 101, 105, 99, 102),
         (6, 102, 106, 100, 103), (7, 103, 107, 101, 104), (8, 104, 108, 102, 105),
         (9, 105, 114, 106.5, 112),   # 插破前高（长上影）
         (10, 112, 112.5, 104, 105),  # 快速收回前高下方
         (11, 105, 107, 101, 102), (12, 102, 104, 98, 99)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    resist = 108.0
    ax.add_patch(Rectangle((-0.55, resist), 9.7, 5.5, facecolor=UP, alpha=0.12, zorder=1))
    hl_line(ax, -0.6, 9.6, resist, color=UP, label="前高 = BSL 池子")
    annotate_mark(ax, 9, 113.5, "插破前高\n扫掉 BSL（长上影）", 8.0, 115.2, color=UP, fs=10, ha="left")
    annotate_mark(ax, 10, 109.0, "收盘收回前高下方\n= sweep 确认，真方向向下", 10.6, 114.0, color=DOWN, fs=10, ha="left")
    arrows(ax, 10.7, 105.5, 100.5, color=DOWN)
    annotate_mark(ax, 12, 98.8, "跟随做空", 11.6, 91.8, color=DOWN, fs=10.5, ha="left")
    savefig(fig, "fig_p5_sweep.png")


# ---------------------------------------------------------------- 新增：5.4 BOS / CHoCH

def fig_bos_choch():
    """5.4 BOS：破前高延续；CHoCH：破 HL 转势警告"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(-0.8, 16.5), ylim=(92, 118))
    k = [(0, 98, 101, 96, 97), (1, 97, 100, 94, 99), (2, 99, 103, 98, 101),
         (3, 101, 104, 99, 102), (4, 102, 105, 100, 103), (5, 103, 106, 101, 104),
         (6, 104, 107, 102, 105), (7, 105, 108, 103, 106),   # 前高 108
         (8, 106, 109, 104, 107), (9, 107, 110, 105, 108),   # HL 104
         (10, 108, 112, 106, 110),  # BOS：破前高 108
         (11, 110, 111, 106, 107), (12, 107, 109, 104, 105),
         (13, 105, 107, 101.5, 102.5),  # CHoCH：破 HL 104
         (14, 102.5, 104, 99, 100), (15, 100, 102, 97, 98)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    prev_high, prev_hl = 108.0, 104.0
    hl_line(ax, 0.5, 9.5, prev_high, color=GRAY, ls=":", label="前高")
    hl_line(ax, 2.0, 12.8, prev_hl, color=GRAY, ls=":", label="前 HL")
    mark(ax, 7, 105.5, "HH", dy=2.2, color=UP, fs=9.5, va="bottom")
    mark(ax, 8, 102.5, "HL", dy=-2.2, color=UP, fs=9.5, va="top")
    annotate_mark(ax, 10, 112.2, "BOS：破前高\n趋势延续确认", 10.0, 117.2, color=UP, fs=10, ha="left")
    annotate_mark(ax, 13, 102.0, "CHoCH：破 HL\n多头结构被破坏，转势警告", 13.4, 108.0, color=DOWN, fs=10, ha="left")
    savefig(fig, "fig_p5_bos_choch.png")


# ---------------------------------------------------------------- 新增：5.5 订单块

def fig_order_block():
    """5.5 订单块：拉升前最后一根反向 K 线 = 看涨 OB，回踩入场"""
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    style_ax(ax, xlim=(-0.8, 13.5), ylim=(90, 118))
    k = [(0, 100, 103, 97, 98), (1, 98, 101, 95, 96), (2, 96, 99, 93, 94),   # 下跌
         (3, 94, 97, 92, 95), (4, 95, 98, 93, 94),                            # 最后一根小阴线（OB）
         (5, 94, 103, 93.5, 101.5),  # 大阳线拉升（displacement）
         (6, 101.5, 107, 100, 105), (7, 105, 109, 103, 106),  # 继续拉升
         (8, 106, 107, 100, 101),    # 回调进入 OB 区域
         (9, 101, 105, 99.5, 103), (10, 103, 108, 102, 106)]  # 从 OB 启动上涨
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ob_lo, ob_hi = 93.5, 95.0
    ax.add_patch(Rectangle((3.4, ob_lo), 1.8, ob_hi - ob_lo, facecolor=ORANGE, alpha=0.35, zorder=2))
    ax.add_patch(Rectangle((7.6, ob_lo), 2.6, ob_hi - ob_lo, facecolor=ORANGE, alpha=0.15, zorder=1))
    hl_line(ax, 3.5, 10.1, ob_hi, color=ORANGE, ls=":", label="OB 区域")
    hl_line(ax, 3.5, 10.1, ob_lo, color=ORANGE, ls=":")
    annotate_mark(ax, 4, 96.2, "最后一根反向 K 线\n= 看涨 OB", 2.2, 105.2, color=ORANGE, fs=10, ha="left")
    annotate_mark(ax, 5, 103.0, "拉升（displacement）", 5.6, 114.5, color=UP, fs=10, ha="left")
    annotate_mark(ax, 8, 99.0, "回调进入 OB 区域\n= 入场区（配合锤子/内包）", 8.9, 94.5, color=DARK, fs=10, ha="left")
    savefig(fig, "fig_p5_ob.png")


# ---------------------------------------------------------------- 新增：5.6 FVG

def fig_fvg():
    """5.6 FVG：K1 高点 < K3 低点 → 中间的空隙即缺口"""
    fig, ax = plt.subplots(figsize=(10, 5.8))
    style_ax(ax, xlim=(-1.2, 4.2), ylim=(96, 114))
    k = [(0, 100, 103, 99, 102), (1, 102, 105, 101, 104), (2, 105, 110, 106, 109)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c, width=0.7)
    # FVG 色块：K1 高 103 与 K3 低 106 之间的空隙
    ax.add_patch(Rectangle((-0.32, 103), 2.64, 3.0, facecolor=ORANGE, alpha=0.35, zorder=2))
    hl_line(ax, -0.5, 0.4, 103, color=GRAY, ls=":", label="K1 高点 103")
    hl_line(ax, 1.6, 2.5, 106, color=GRAY, ls=":", label="K3 低点 106")
    mark(ax, 0, 102, "K1", dy=-2.5, fs=12, color=DARK, va="top")
    mark(ax, 1, 101, "K2", dy=-2.5, fs=12, color=DARK, va="top")
    mark(ax, 2, 106, "K3", dy=-2.5, fs=12, color=DARK, va="top")
    annotate_mark(ax, 1, 104.5, "FVG：K1 与 K3 之间的空隙\n（看涨缺口，倾向回补）", 1.9, 110.8, color=ORANGE, fs=11, ha="left")
    savefig(fig, "fig_p5_fvg.png")


# ---------------------------------------------------------------- v3：1.1 扩散曲线
def fig_diffusion():
    """1.1 扩散理论：左 S 形价格周期 + 五类参与者位置；右高斯分布 2.5/13.5/34/34/16"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.8))
    # 左：S 形价格周期（累积→上升→派发→下降）
    x1 = np.linspace(0, 5, 300)
    y1 = 88 + 24 / (1 + np.exp(-(x1 - 2.5) * 1.6))
    x2 = np.linspace(5, 10, 300)
    y2 = 112 - 24 / (1 + np.exp(-(x2 - 7.5) * 1.6))
    ax1.plot(np.append(x1, x2), np.append(y1, y2), color=TEAL, lw=2.2, zorder=3)
    # 五类参与者在周期上的位置
    pts = [(0.15, 88, "创新者\n2.5%\n(内部人)", UP), (1.35, 92.6, "早期参与者\n13.5%\n(消息灵通)", UP),
           (3.2, 106, "早期人群 34%\n(趋势早期入场)", ORANGE), (4.9, 111.8, "晚期人群 34%\n(末段接盘)", DOWN),
           (6.9, 105.5, "迟缓者 16%\n(最后接棒)", DOWN)]
    for x, y, t, c in pts:
        ax1.plot(x, y, "o", ms=7, color=c, zorder=5)
        ax1.annotate(t, xy=(x, y), xytext=(x + 0.15, y - 3.2), fontsize=8.5, color=DARK,
                     arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9), va="top", ha="left")
    mark(ax1, 4.4, 96.5, "累积", fs=11, color=UP)
    mark(ax1, 2.6, 88.5, "上升趋势", fs=11, color=UP)
    mark(ax1, 7.0, 116.2, "派发", fs=11, color=DOWN)
    mark(ax1, 8.8, 93.5, "下降趋势", fs=11, color=DOWN)
    mark(ax1, 4.6, 84.5, "S 形曲线 = 价格周期（参与者依次入场）", fs=10.5, color=DARK, box=True)
    style_ax(ax1, xlim=(-0.3, 10.6), ylim=(82, 120))
    # 右：高斯分布五段
    xs = np.linspace(-3.6, 3.6, 500)
    g = np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi)
    segs = [(-3.6, -1.96, UP, "创新者 2.5%"), (-1.96, -0.99, UP, "早期 13.5%"),
            (-0.99, 0.99, ORANGE, "早期人群 34%"), (0.99, 1.96, DOWN, "晚期人群 34%"),
            (1.96, 3.6, DOWN, "迟缓者 16%")]
    for a, b, c, t in segs:
        m = (xs >= a) & (xs <= b)
        ax2.fill_between(xs[m], 0, g[m], color=c, alpha=0.35, zorder=2)
    ax2.plot(xs, g, color=DARK, lw=1.6, zorder=3)
    for a, t in [(-1.96, "-1.96"), (-0.99, "-0.99"), (0.99, "0.99"), (1.96, "1.96")]:
        ax2.plot([a, a], [0, np.exp(-a ** 2 / 2) / np.sqrt(2 * np.pi)], color=GRAY, ls=":", lw=1.0)
        ax2.text(a, -0.045, t, fontsize=8, color=GRAY, ha="center")
    mark(ax2, 0, 0.47, "高斯曲线 = 成交量/情绪分布", fs=10.5, color=DARK, box=True)
    style_ax(ax2, xlim=(-3.8, 3.8), ylim=(-0.06, 0.52))
    savefig(fig, "fig_p1_diffusion.png")


# ---------------------------------------------------------------- v3：2.9 洛氏 1-2-3
def fig_123_ross():
    """2.9 洛氏 1-2-3：左低位（做多）1/2/3 点 + 突破 2 点入场；右高位（做空）镜像"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.8))
    # 左：低位 1-2-3（做多）
    k1 = [(0, 106, 108, 103, 104), (1, 104, 106, 101, 102), (2, 102, 104, 99, 100),
          (3, 100, 102, 97, 98), (4, 98, 103, 97, 102), (5, 102, 105, 101, 104),
          (6, 104, 105, 100, 101), (7, 101, 103, 99, 102), (8, 102, 106, 101, 105.5),
          (9, 105.5, 109, 104, 108)]
    for x, o, h, l, c in k1:
        candle(ax1, x, o, h, l, c)
    mark(ax1, 3, 97, "1 点", dy=-2.6, color=DOWN, fs=10.5, va="top")
    mark(ax1, 5, 105, "2 点", dy=2.4, color=UP, fs=10.5, va="bottom")
    mark(ax1, 7, 99, "3 点\n(更高低点)", dy=-2.6, color=UP, fs=9.5, va="top")
    hl_line(ax1, 0.6, 9.4, 105, color=TEAL, ls="--", label="突破 2 点 → 入场")
    annotate_mark(ax1, 8, 106.2, "低位 1-2-3 突破\n多空较量结束", 6.8, 111.6, color=UP, fs=10, ha="left")
    style_ax(ax1, xlim=(-0.6, 10.6), ylim=(92, 114))
    # 右：高位 1-2-3（做空）
    k2 = [(0, 106, 110, 105, 109), (1, 109, 112, 108, 111), (2, 111, 114, 110, 113),
          (3, 113, 116, 112, 115), (4, 115, 115, 110, 111), (5, 111, 112, 107, 108),
          (6, 108, 111, 108, 110), (7, 110, 112, 109, 110), (8, 110, 110, 106, 107),
          (9, 107, 108, 103, 104)]
    for x, o, h, l, c in k2:
        candle(ax2, x, o, h, l, c)
    mark(ax2, 3, 116, "1 点", dy=2.4, color=UP, fs=10.5, va="bottom")
    mark(ax2, 5, 107, "2 点", dy=-2.6, color=DOWN, fs=10.5, va="top")
    mark(ax2, 7, 109, "3 点\n(更低高点)", dy=-2.6, color=DOWN, fs=9.5, va="top")
    hl_line(ax2, 0.6, 9.4, 107, color=TEAL, ls="--", label="跌破 2 点 → 入场")
    annotate_mark(ax2, 8, 105.2, "高位 1-2-3 跌破\n空方获胜", 5.6, 110.5, color=DOWN, fs=10, ha="left")
    style_ax(ax2, xlim=(-0.6, 10.6), ylim=(98, 120))
    savefig(fig, "fig_p2_123.png")


# ---------------------------------------------------------------- v3：2.9 洛氏霍克 Rh
def fig_ross_hook():
    """2.9 Rh：1-2-3 突破后第一根不创新高的 K 线，回调到 Rh 入场（奇克入市法）"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(-0.8, 13.5), ylim=(92, 115))
    k = [(0, 104, 107, 102, 103), (1, 103, 105, 100, 101), (2, 101, 103, 98, 99),
         (3, 99, 101, 96, 97), (4, 97, 102, 96, 101), (5, 101, 104, 100, 103),
         (6, 103, 103.5, 100, 101), (7, 101, 103, 99, 102), (8, 102, 105, 101, 104.5),
         (9, 104.5, 105, 102, 103), (10, 103, 104, 100, 101), (11, 101, 105.5, 100, 104.5),
         (12, 104.5, 108, 103, 107)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    mark(ax, 3, 97, "1", dy=-2.4, color=DOWN, fs=10.5, va="top")
    mark(ax, 5, 104, "2", dy=2.2, color=UP, fs=10.5, va="bottom")
    mark(ax, 7, 99, "3", dy=-2.4, color=UP, fs=10.5, va="top")
    hl_line(ax, 0.6, 8.4, 104, color=GRAY, ls=":", label="2 点（突破）")
    hl_line(ax, 8.8, 12.4, 102, color=ORANGE, ls="--", label="Rh（突破后第一根不创新高的 K 线）")
    annotate_mark(ax, 9, 105.0, "Rh：2 点突破后第一根\n不创新高的 K 线", 6.2, 110.2, color=ORANGE, fs=9.5, ha="left")
    annotate_mark(ax, 11, 104.5, "回调到 Rh 附近限价入场\n（奇克入市法：提前入市）", 9.6, 93.6, color=UP, fs=9.5, ha="left")
    annotate_mark(ax, 10, 100.0, "止损 Rh 下方", 11.9, 97.2, color=DOWN, fs=9.5, ha="left")
    arrows(ax, 11.6, 103.5, 107.2, color=UP)
    savefig(fig, "fig_p2_ross_hook.png")


# ---------------------------------------------------------------- v3：3.11 最终旗形
def fig_final_flag():
    """3.11 模式二：趋势末端旗形突破失败 → 反转（概率约 40%）"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(-0.8, 15.5), ylim=(94, 118))
    k = [(0, 100, 103, 98, 99), (1, 99, 103, 98, 102), (2, 102, 106, 101, 105),
         (3, 105, 109, 104, 108), (4, 108, 109, 105, 106), (5, 106, 110, 105, 109),
         (6, 109, 113, 108, 112), (7, 112, 113, 109, 110), (8, 110, 114, 109, 113),
         (9, 113, 114, 110, 111), (10, 111, 113, 109, 110), (11, 110, 116.5, 109, 113),
         (12, 113, 114, 107, 108), (13, 108, 109, 104, 105), (14, 105, 106, 100, 101)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.add_patch(Rectangle((8.4, 108.5), 2.6, 5.0, facecolor=ORANGE, alpha=0.25, zorder=1))
    hl_line(ax, 8.5, 11.2, 113.5, color=ORANGE, ls=":", label="旗形上沿")
    annotate_mark(ax, 9, 112.0, "最终旗形\n(趋势末端盘整)", 6.6, 115.8, color=ORANGE, fs=9.5, ha="left")
    annotate_mark(ax, 11, 116.0, "突破失败\n长上影收回", 11.6, 116.8, color=DOWN, fs=10, ha="left")
    annotate_mark(ax, 12, 107.2, "旗形破位 → 反向\n反转概率约 40%", 9.8, 100.2, color=DOWN, fs=9.5, ha="left")
    arrows(ax, 12.7, 108.5, 103.0, color=DOWN)
    savefig(fig, "fig_p3_final_flag.png")


# ---------------------------------------------------------------- v3：3.11/4.21 楔形三推 P3
def fig_wedge_p3():
    """3.11 模式五 + 4.21 模型二：上升楔形三推 P1/P2/P3，P3 挂限价空，破位 75%"""
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    style_ax(ax, xlim=(-0.8, 11.5), ylim=(92, 112))
    k = [(0, 100, 102, 98, 99), (1, 99, 103.5, 98, 102.5), (2, 102.5, 103.5, 100, 101),
         (3, 101, 105.5, 100, 104.5), (4, 104.5, 105.5, 102, 103), (5, 103, 107.5, 102.5, 107),
         (6, 107, 107.5, 103.5, 104), (7, 104, 105, 101, 102), (8, 102, 103, 98, 99),
         (9, 99, 100, 95, 96)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    # 楔形上下沿（收敛）
    ax.plot([0.6, 5.4], [99, 107.4], color=GRAY, ls="--", lw=1.2)   # 上沿（推高点连线）
    ax.plot([0.6, 5.4], [97.5, 103.2], color=ORANGE, ls="--", lw=1.2)  # 下沿（回调低点连线）
    mark(ax, 1, 103.5, "P1", dy=2.0, color=DARK, fs=10.5, va="bottom")
    mark(ax, 3, 105.5, "P2", dy=2.0, color=DARK, fs=10.5, va="bottom")
    mark(ax, 5, 107.5, "P3", dy=2.0, color=ORANGE, fs=11, va="bottom")
    annotate_mark(ax, 5.8, 106.6, "P3 挂限价空\n(4.21 模型二)", 6.6, 110.8, color=ORANGE, fs=9.5, ha="left")
    annotate_mark(ax, 8, 98.6, "跌破楔形下沿\n破位概率约 75%", 7.0, 93.8, color=DOWN, fs=9.5, ha="left")
    annotate_mark(ax, 2.4, 96.6, "楔形：三推收敛\n(3-5 条腿后更接近反转)", 0.9, 92.6, color=DARK, fs=9.5, ha="left")
    savefig(fig, "fig_p3_wedge_p3.png")


# ---------------------------------------------------------------- v3：3.11 测量移动
def fig_measured_move():
    """3.11 模式七：测量移动 Leg1 = Leg2，目标可提前投射"""
    fig, ax = plt.subplots(figsize=(12, 5.9))
    style_ax(ax, xlim=(-0.8, 8.8), ylim=(96, 118))
    k = [(0, 100, 103, 99, 102), (1, 102, 105, 101, 104), (2, 104, 108, 103, 107),
         (3, 107, 107.5, 104, 105), (4, 105, 109, 104, 108), (5, 108, 111, 107, 110),
         (6, 110, 114, 109, 113), (7, 113, 115, 111, 112)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    # Leg1 / Leg2 区间
    ax.add_patch(Rectangle((-0.55, 100), 3.1, 8.0, facecolor=UP, alpha=0.10, zorder=1))
    ax.add_patch(Rectangle((3.8, 105), 3.3, 9.0, facecolor=UP, alpha=0.10, zorder=1))
    hl_line(ax, 0.2, 8.6, 108, color=GRAY, ls=":", label="Leg 1 终点 108")
    hl_line(ax, 3.6, 8.6, 114, color=TEAL, ls="--", label="目标：Leg 2 ≈ Leg 1（114）")
    annotate_mark(ax, 1.2, 100.6, "Leg 1\n(长度 ≈ 8)", 0.6, 104.6, color=UP, fs=10, ha="left")
    annotate_mark(ax, 4.6, 105.6, "Leg 2 ≈ Leg 1\n(测量移动)", 3.9, 109.0, color=UP, fs=10, ha="left")
    annotate_mark(ax, 3, 104.2, "回调", 2.0, 96.8, color=DOWN, fs=9.5, ha="left")
    annotate_mark(ax, 6.2, 114.2, "目标可提前算：\nLeg1 长度投射", 4.2, 117.2, color=TEAL, fs=9.5, ha="left")
    savefig(fig, "fig_p3_measured_move.png")


# ---------------------------------------------------------------- v3：3.11 开盘反转
def fig_opening_reversal():
    """3.11 模式九：开盘假突破前高（磁力位）→ 60-90 分钟窗口内反转"""
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    style_ax(ax, xlim=(-0.8, 9.8), ylim=(94, 116))
    k = [(0, 104, 106, 102, 103), (1, 103, 107, 102, 105), (2, 105, 110, 104, 108),
         (3, 108, 112.5, 107, 110.5), (4, 110.5, 110.8, 104.5, 106), (5, 106, 107, 102, 103),
         (6, 103, 104, 99, 100), (7, 100, 101, 96, 97)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, -0.6, 3.4, 110, color=GRAY, ls="--", label="前高（磁力位）")
    ax.plot([3.0, 3.0], [94.5, 115.5], color=ORANGE, ls=":", lw=1.4)
    ax.plot([5.6, 5.6], [94.5, 115.5], color=ORANGE, ls=":", lw=1.4)
    mark(ax, 4.3, 95.8, "开盘反转窗口（60-90 分钟）", fs=10, color=ORANGE, va="bottom")
    annotate_mark(ax, 3, 112.0, "开盘冲高\n假突破前高", 1.6, 114.8, color=UP, fs=10, ha="left")
    annotate_mark(ax, 4, 105.2, "收盘收回 → 开盘反转\n做空（失败率 > 70% 后反向）", 4.8, 110.5, color=DOWN, fs=9.5, ha="left")
    arrows(ax, 4.7, 106.5, 100.5, color=DOWN)
    savefig(fig, "fig_p3_opening_reversal.png")


# ---------------------------------------------------------------- v3：4.20 二次突破确认
def fig_breakout_confirm():
    """4.20 模型二：第一次突破失败（洗掉弱手）→ 3 根 K 线内二次突破 → 实体收盘入场"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(-0.8, 10.5), ylim=(94, 116))
    k = [(0, 100, 103, 98, 99), (1, 99, 102, 97, 100), (2, 100, 104, 99, 102),
         (3, 102, 105.5, 101, 104), (4, 104, 104.5, 100, 101), (5, 101, 104, 100, 103),
         (6, 103, 106.5, 102, 106), (7, 106, 109, 105, 108), (8, 108, 111, 107, 110)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, -0.6, 3.2, 104, color=GRAY, ls="--", label="关键位（区间上沿）")
    hl_line(ax, 3.6, 6.4, 104, color=GRAY, ls=":")
    annotate_mark(ax, 3, 105.2, "第一次突破\n(影线插破)", 1.4, 110.6, color=DOWN, fs=9.5, ha="left")
    annotate_mark(ax, 4, 100.6, "突破失败\n(洗掉追突破的弱手)", 2.8, 95.6, color=DOWN, fs=9.5, ha="left")
    annotate_mark(ax, 6, 106.8, "3 根 K 线内二次突破\n实体收盘 → 入场（极值外 1 tick）", 4.6, 112.6, color=UP, fs=9.5, ha="left")
    arrows(ax, 6.7, 105.5, 109.5, color=UP)
    savefig(fig, "fig_p4_breakout_confirm.png")


# ---------------------------------------------------------------- v3：4.21 限价单（区间 1:1）
def fig_limit_order_zone():
    """4.21 模型一：区间前高挂限价空 / 前低挂限价多，固定 1:1 盈亏比"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(-0.8, 13.5), ylim=(88, 112))
    k = [(0, 100, 104, 98, 99), (1, 99, 102, 96, 97), (2, 97, 101, 95, 99),
         (3, 99, 103, 97, 100), (4, 100, 103, 97, 98), (5, 98, 101, 95, 96),
         (6, 96, 100, 94, 98), (7, 98, 102, 96, 99), (8, 99, 103, 97, 100),
         (9, 100, 102, 96, 97), (10, 97, 100, 95, 98), (11, 98, 102, 97, 100),
         (12, 100, 104, 99, 102)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hi, lo, mid = 103.0, 95.0, 99.0
    hl_line(ax, -0.6, 12.4, hi, color=DOWN, label="前高：挂限价空（1:1）")
    hl_line(ax, -0.6, 12.4, lo, color=UP, label="前低：挂限价多（1:1）")
    hl_line(ax, -0.6, 12.4, mid, color=GRAY, ls=":", label="区间中线")
    annotate_mark(ax, 3, 103.6, "到价自动成交\n止损边界外，目标中线/1:1", 3.6, 108.4, color=DOWN, fs=9.5, ha="left")
    annotate_mark(ax, 9, 95.6, "限价单：等市场来找你\n永不滑点（第 1.3）", 5.4, 91.0, color=UP, fs=9.5, ha="left")
    mark(ax, 6.0, 104.4, "窄区间：固定 1:1 盈亏比，不贪", fs=10.5, color=DARK, box=True)
    savefig(fig, "fig_p4_limit_order_zone.png")


# ---------------------------------------------------------------- v3：4.22 always-in 第三根未遂
def fig_always_in():
    """4.22 打法二：强突破后逆势尝试，第二根逆势 K 收盘反手，第三根未遂反转 80% 失败"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(-0.8, 13.5), ylim=(90, 116))
    k = [(0, 98, 102, 96, 97), (1, 97, 100, 94, 95), (2, 95, 99, 93, 97),
         (3, 97, 101, 96, 98), (4, 98, 102, 97, 99), (5, 99, 103, 98, 100),
         (6, 100, 104, 99, 101), (7, 101, 105, 100, 102), (8, 102, 107, 101, 105),
         (9, 105, 109, 104, 106), (10, 106, 108, 103, 104), (11, 104, 106.5, 102.5, 105.5),
         (12, 105.5, 110, 105, 108), (13, 108, 112, 107, 110)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, 7.8, 13.4, 107, color=UP, ls="--", label="强突破（放量大实体）")
    annotate_mark(ax, 10, 103.4, "逆 1 失败\n(第一次逆势)", 8.6, 94.4, color=DOWN, fs=9.5, ha="left")
    annotate_mark(ax, 11, 106.6, "逆 2 收盘 → 反手做多\n(第二根逆势 K 收盘建仓)", 8.0, 110.8, color=UP, fs=9.5, ha="left")
    annotate_mark(ax, 12, 109.8, "第三根仍未遂\n反转 80% 失败 → 只用前两次", 9.2, 113.2, color=UP, fs=9.5, ha="left")
    savefig(fig, "fig_p4_always_in.png")


# ---------------------------------------------------------------- v3：5.13/5.14 摆动范围 + 溢价折价
def fig_swing_range():
    """5.13/5.14 摆动范围：当前范围 vs 左侧范围（突破方向判定）；中点分溢价/折价区"""
    fig, ax = plt.subplots(figsize=(13, 6.4))
    style_ax(ax, xlim=(-0.8, 14.5), ylim=(88, 118))
    k = [(0, 96, 99, 94, 95), (1, 95, 99, 93, 97), (2, 97, 101, 95, 98),
         (3, 98, 102, 96, 99), (4, 99, 103, 97, 100), (5, 100, 104, 98, 101),
         (6, 101, 105, 99, 102), (7, 102, 106, 100, 103), (8, 103, 104, 100, 101),
         (9, 101, 103, 99, 102), (10, 102, 105, 101, 104), (11, 104, 107, 103, 106),
         (12, 106, 110, 105, 108), (13, 108, 112, 107, 110)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    left_lo, left_hi = 96.0, 103.0
    cur_lo, cur_hi = 99.0, 106.0
    ax.add_patch(Rectangle((-0.55, left_lo), 8.3, left_hi - left_lo, facecolor=GRAY, alpha=0.12, zorder=1))
    ax.add_patch(Rectangle((7.6, cur_lo), 6.4, cur_hi - cur_lo, facecolor=UP, alpha=0.10, zorder=1))
    hl_line(ax, -0.6, 8.2, left_hi, color=GRAY, label="左侧摆动范围高点")
    hl_line(ax, -0.6, 13.9, cur_lo, color=GRAY, ls=":", label="当前摆动范围低点")
    hl_line(ax, 7.8, 13.9, cur_hi, color=UP, label="当前摆动范围高点")
    mid = (cur_lo + cur_hi) / 2
    hl_line(ax, 7.8, 13.9, mid, color=ORANGE, ls="--", label="中点：上=溢价区 / 下=折价区")
    annotate_mark(ax, 11, 106.4, "突破左侧范围高点\n= 向上突破确认", 10.2, 111.8, color=UP, fs=9.5, ha="left")
    annotate_mark(ax, 10.4, 100.8, "回调进折价区\n= 做多机会", 8.9, 94.6, color=UP, fs=9.5, ha="left")
    savefig(fig, "fig_p5_swing_range.png")


# ---------------------------------------------------------------- v3：5.15 供需区
def fig_supply_demand():
    """5.15 供需区：强下跌后大实体反弹 = 需求区，回踩需求区做多"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(-0.8, 13.5), ylim=(90, 116))
    k = [(0, 108, 110, 105, 106), (1, 106, 108, 103, 104), (2, 104, 106, 101, 102),
         (3, 102, 104, 99, 100), (4, 100, 102, 97, 98), (5, 98, 100, 95, 96),
         (6, 96, 98, 94, 95), (7, 95, 104, 94.5, 103), (8, 103, 108, 102, 106),
         (9, 106, 110, 105, 108), (10, 108, 109, 103, 104), (11, 104, 108, 103, 106),
         (12, 106, 111, 105, 109)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    dem_lo, dem_hi = 94.5, 96.0
    ax.add_patch(Rectangle((6.4, dem_lo), 4.2, dem_hi - dem_lo, facecolor=ORANGE, alpha=0.35, zorder=2))
    hl_line(ax, 6.5, 10.5, dem_hi, color=ORANGE, ls=":", label="需求区（反弹前最后一根阴线区域）")
    hl_line(ax, 6.5, 10.5, dem_lo, color=ORANGE, ls=":")
    annotate_mark(ax, 7, 104.2, "需求区：强下跌后\n大实体反弹（失衡）", 3.2, 108.2, color=ORANGE, fs=9.5, ha="left")
    annotate_mark(ax, 10, 103.4, "回踩需求区 → 做多\n(配合锤子/内包确认)", 7.4, 95.8, color=UP, fs=9.5, ha="left")
    savefig(fig, "fig_p5_supply_demand.png")


# ---------------------------------------------------------------- v3：5.16 S2B / B2S
def fig_s2b_b2s():
    """5.16 S2B：先卖推低突破前低（扫 SSL）→ 反向拉升突破前高（做多）；B2S 为镜像"""
    fig, ax = plt.subplots(figsize=(13, 6.4))
    style_ax(ax, xlim=(-0.8, 14.5), ylim=(88, 116))
    k = [(0, 102, 105, 100, 101), (1, 101, 104, 99, 102), (2, 102, 106, 101, 104),
         (3, 104, 107, 102, 105), (4, 105, 108, 103, 106), (5, 106, 107, 103, 104),
         (6, 104, 105, 101, 102), (7, 102, 103, 98, 99), (8, 99, 100, 95, 96),
         (9, 96, 101, 95.5, 100), (10, 100, 104, 99, 103), (11, 103, 107, 102, 106),
         (12, 106, 110, 105, 109), (13, 109, 112, 108, 111)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, 3.6, 8.2, 108, color=GRAY, ls=":", label="前高 108")
    hl_line(ax, 5.6, 8.6, 98, color=DOWN, ls="--", label="前低 98（SSL）")
    hl_line(ax, 8.8, 13.9, 108, color=TEAL, ls="--", label="突破前高 → 做多（S2B 完成）")
    annotate_mark(ax, 8, 95.4, "S：先卖推低\n插破前低扫 SSL", 5.2, 91.2, color=DOWN, fs=9.5, ha="left")
    annotate_mark(ax, 9, 100.4, "快速收回\n(不再跌)", 8.0, 104.0, color=ORANGE, fs=9.5, ha="left")
    annotate_mark(ax, 12, 110.2, "B：反向拉升\n突破前高 → 入场", 10.2, 114.8, color=UP, fs=9.5, ha="left")
    mark(ax, 2.2, 110.8, "B2S = 镜像：先买推高突破前高扫 BSL，再跌破前低做空", fs=9.5, color=GRAY, va="bottom")
    savefig(fig, "fig_p5_s2b_b2s.png")


# ---------------------------------------------------------------- v3：5.17 流动性诱导
def fig_liquidity_induce():
    """5.17 流动性诱导：亚盘横盘高低点被伦敦/纽约开盘掠夺；内部流动性嵌套"""
    fig, ax = plt.subplots(figsize=(13.5, 6.4))
    style_ax(ax, xlim=(-0.8, 15.5), ylim=(90, 118))
    k = [(0, 100, 102, 98, 99), (1, 99, 101, 97, 98), (2, 98, 100.5, 97, 99.5),
         (3, 99.5, 100.5, 98, 99), (4, 99, 101, 97.5, 100), (5, 100, 100.5, 98, 98.5),
         (6, 98.5, 104.5, 98, 103), (7, 103, 103.5, 99, 100), (8, 100, 102, 99, 101),
         (9, 101, 104, 100, 103), (10, 103, 107, 102, 106), (11, 106, 110, 105, 108),
         (12, 108, 112, 107, 110), (13, 110, 113, 109, 111), (14, 111, 115, 110, 113)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    asia_hi, asia_lo = 100.5, 97.0
    hl_line(ax, -0.6, 6.2, asia_hi, color=GRAY, label="亚盘高点（内部流动性）")
    hl_line(ax, -0.6, 6.2, asia_lo, color=GRAY, label="亚盘低点")
    ax.add_patch(Rectangle((-0.55, asia_lo), 6.4, asia_hi - asia_lo, facecolor=GRAY, alpha=0.12, zorder=1))
    annotate_mark(ax, 2, 100.8, "亚洲时段横盘\n高低点 = 内部流动性池\n(散户止损聚集处)", 0.5, 109.5, color=DARK, fs=9.5, ha="left")
    annotate_mark(ax, 6, 104.0, "伦敦/纽约开盘掠夺：\n插破亚盘高点扫 BSL", 6.8, 112.2, color=UP, fs=9.5, ha="left")
    annotate_mark(ax, 7, 99.4, "快速收回后\n真实方向向上", 6.4, 93.0, color=UP, fs=9.5, ha="left")
    annotate_mark(ax, 9, 103.4, "外侧更大结构 = 外部流动性\n(层层嵌套，一处接一处扫)", 9.2, 108.2, color=ORANGE, fs=9.5, ha="left")
    savefig(fig, "fig_p5_liquidity_induce.png")


# ---------------------------------------------------------------- v3：8.10 拍卖四环节
def fig_auction_cycle():
    """8.10 拍卖理论：趋势→停止→震荡→转换 四环节循环（平衡/失衡标注）"""
    fig, ax = plt.subplots(figsize=(12, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.4))
    draw_box(ax, 5.2, 5.6, 2.9, 1.2, "① 趋势阶段\n失衡：单向运动", ec=DOWN, fs=10.5)
    draw_box(ax, 9.6, 5.6, 2.9, 1.2, "② 停止阶段\n大量反向交易", ec=ORANGE, fs=10.5)
    draw_box(ax, 9.6, 1.6, 2.9, 1.2, "③ 震荡阶段\n平衡：新价值区\n(累积/派发)", ec=ORANGE, fs=10.5)
    draw_box(ax, 5.2, 1.6, 2.9, 1.2, "④ 转换阶段\n再失衡：离开区间\n(反转或延续)", ec=UP, fs=10.5)
    flow_arrow(ax, 8.1, 6.2, 9.6, 6.2)
    flow_arrow(ax, 11.05, 5.6, 11.05, 2.8)
    flow_arrow(ax, 9.6, 2.2, 8.1, 2.2)
    flow_arrow(ax, 5.2, 2.8, 5.2, 5.6, rad=0.35)
    mark(ax, 6.7, 4.1, "平衡 → 失衡 → 平衡 循环\n(任意时间级别可观察)\n= 第 4.6 状态机的理论依据",
         fs=10.5, color=DARK, box=True, ha="center")
    mark(ax, 3.0, 6.4, "接受/拒绝判定\n新价位停留久+量堆积 = 接受", fs=9.5, color=GRAY)
    savefig(fig, "fig_p8_auction_cycle.png")


# ---------------------------------------------------------------- v3：6.12 洛氏 3 手合约
def fig_three_contracts():
    """6.12 洛氏 3 手合约：1 手抵费用平仓 → 2 手赚成本平仓 → 3 手保本后奔跑"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(-0.8, 12.5), ylim=(96, 116))
    k = [(0, 102, 104, 100, 101), (1, 101, 103, 98, 99), (2, 99, 102, 97, 100),
         (3, 100, 105, 99, 104), (4, 104, 108, 103, 107), (5, 107, 108, 105, 106),
         (6, 106, 109, 105, 108), (7, 108, 112, 107, 111), (8, 111, 115, 110, 114),
         (9, 114, 116, 112, 113), (10, 113, 115, 111, 114)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    entry = 101.5
    hl_line(ax, -0.6, 12.4, entry, color=GRAY, ls=":", label="入场价 = 盈亏平衡点")
    hl_line(ax, 4.3, 12.4, 105.5, color=UP, ls="--", label="1 手止盈位（抵费用）")
    hl_line(ax, 6.3, 12.4, 108.5, color=UP, ls="--", label="2 手止盈位（赚成本）")
    annotate_mark(ax, 3, 105.0, "入场 3 手", 2.0, 110.0, color=DARK, fs=10, ha="left")
    annotate_mark(ax, 5.6, 108.0, "第 1 手：平仓抵补佣金/费用\n第 2 手：平仓赚等额盈利\n(对直接成本 100% 回报)", 3.4, 113.8, color=UP, fs=9, ha="left")
    annotate_mark(ax, 7.5, 107.6, "第 3 手止损移到盈亏平衡\n(跟踪止损，不许亏超平衡点)", 7.6, 98.6, color=ORANGE, fs=9, ha="left")
    annotate_mark(ax, 9, 115.5, "第 3 手奔跑：10 次里 7-8 次\n保本离场，2-3 次大回报", 8.6, 116.4, color=UP, fs=9, ha="left")
    savefig(fig, "fig_p6_three_contracts.png")


# ---------------------------------------------------------------- v4：6.4 盈亏平衡胜率曲线
def fig_be_curve():
    """6.4 盈亏平衡胜率曲线：RR 越高，需要的最低胜率越低"""
    fig, ax = plt.subplots(figsize=(11, 6.2))
    rr = np.linspace(0.5, 4.0, 200)
    be = 1 / (1 + rr) * 100
    ax.plot(rr, be, color=DARK, lw=2.2)
    ax.fill_between(rr, be, 105, color=UP, alpha=0.08)
    ax.fill_between(rr, 0, be, color=DOWN, alpha=0.08)
    for x, y, lab in [(1, 50, "RR 1:1 → 需 >50%"), (2, 33.3, "RR 2:1 → 需 >33.3%"), (3, 25, "RR 3:1 → 需 >25%")]:
        ax.plot([x], [y], "o", color=ORANGE, ms=8, zorder=5)
        ax.annotate(lab, xy=(x, y), xytext=(x + 0.12, y + 6), fontsize=10.5, color=ORANGE,
                    arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    ax.text(3.35, 96, "盈利区", fontsize=12, color=UP, ha="center")
    ax.text(3.35, 7, "亏损区", fontsize=12, color=DOWN, ha="center")
    ax.set_xlabel("风险回报比 RR（目标 ÷ 止损）", fontsize=11)
    ax.set_ylabel("所需最低胜率 %", fontsize=11)
    ax.set_xticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
    ax.set_yticks([0, 20, 25, 33.3, 40, 50, 66.7, 80, 100])
    ax.set_ylim(0, 105)
    ax.grid(alpha=0.3)
    ax.set_title("盈亏平衡：RR 越高，对胜率的要求越低（“截断亏损、让利润奔跑”的数学依据）",
                 fontsize=12, color=DARK)
    savefig(fig, "fig_p6_be_curve.png")


# ---------------------------------------------------------------- v3：6.2 止损-仓位跷跷板
def fig_stop_size():
    """6.2 止损距离与仓位跷跷板：止损翻倍，仓位减半（Al Brooks 比例）"""
    fig, ax = plt.subplots(figsize=(11, 5.2))
    stops = ["20 点止损", "40 点止损", "80 点止损"]
    sizes = [100, 50, 25]
    bars = ax.bar(stops, sizes, width=0.45, color=[UP, ORANGE, DOWN], alpha=0.85)
    for b, s in zip(bars, sizes):
        ax.text(b.get_x() + b.get_width() / 2, s + 2, f"{s}%", ha="center",
                fontsize=13, color=DARK, fontweight="bold")
    ax.set_ylim(0, 118)
    ax.set_ylabel("相对仓位（基准 20 点 = 100%）", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    ax.set_title("止损距离 × 仓位 = 恒定风险：止损翻倍 → 仓位减半", fontsize=12, color=DARK)
    ax.text(0.5, 112, "目标：每笔总风险保持一致（先定止损，再反推仓位）", fontsize=10, color=GRAY)
    savefig(fig, "fig_p6_stop_size.png")


# ---------------------------------------------------------------- v3：7.1 连亏概率
def fig_drawdown_prob():
    """7.1 概率思维：40% 胜率系统连亏 n 笔的概率——连亏是正常分布"""
    fig, ax = plt.subplots(figsize=(11, 5.8))
    n = np.arange(1, 11)
    p = 0.6 ** n * 100
    colors = [ORANGE if i in (5, 8) else TEAL for i in n]
    bars = ax.bar(n, p, width=0.6, color=colors, alpha=0.85)
    for b, v in zip(bars, p):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center", fontsize=9.5, color=DARK)
    ax.annotate("连亏 5 笔：7.8%\n100 笔内几乎必然出现一次", xy=(5, 7.8), xytext=(6.2, 32),
                fontsize=10.5, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
    ax.annotate("连亏 8 笔：1.7%（也别慌）", xy=(8, 1.7), xytext=(6.2, 15),
                fontsize=10.5, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
    ax.set_xlabel("连续亏损笔数", fontsize=11)
    ax.set_ylabel("出现概率 %（40% 胜率系统）", fontsize=11)
    ax.set_xticks(n)
    ax.set_ylim(0, 68)
    ax.grid(axis="y", alpha=0.3)
    ax.set_title("连亏是概率的必然，不是系统坏了——仓位要设计成“扛得住连亏”", fontsize=12, color=DARK)
    savefig(fig, "fig_p7_drawdown_prob.png")


# ---------------------------------------------------------------- v3：8.7 验证闭环
def fig_verify_loop():
    """8.7 上真钱的门槛：验证闭环——回测→模拟→小资金→实盘复盘→回到回测"""
    fig, ax = plt.subplots(figsize=(12, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.4))
    draw_box(ax, 1.6, 5.6, 3.0, 1.3, "① 回测 100+ 笔\n期望值 > 0？\nSQN > 2？", ec=TEAL, fs=10.5)
    draw_box(ax, 8.8, 5.6, 3.0, 1.3, "② 模拟盘 100 笔\n执行率 > 90%？", ec=TEAL, fs=10.5)
    draw_box(ax, 8.8, 1.6, 3.0, 1.3, "③ 最小资金实盘\n验证情绪与执行", ec=ORANGE, fs=10.5)
    draw_box(ax, 1.6, 1.6, 3.0, 1.3, "④ 复盘 + 日志\n重算真实期望值", ec=ORANGE, fs=10.5)
    flow_arrow(ax, 4.6, 6.25, 8.8, 6.25)
    flow_arrow(ax, 10.3, 5.6, 10.3, 2.9)
    flow_arrow(ax, 8.8, 2.25, 4.6, 2.25)
    flow_arrow(ax, 1.6, 2.9, 1.6, 5.6, rad=0.35)
    mark(ax, 5.2, 4.1, "任一环节不达标 → 回到 ①\n“没有达到门槛前，永远在练，不上真钱”", fs=10, color=DARK, box=True)
    savefig(fig, "fig_p8_verify_loop.png")


# ---------------------------------------------------------------- v3：8.9 R 分布与 SQN
def fig_r_dist():
    """8.9 SQN：R 倍数分布直方图——大多数 -1R，少数大 R 撑起整体期望"""
    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    np.random.seed(7)
    r_vals = np.concatenate([
        np.random.normal(-1.0, 0.15, 60),   # 亏损集中在 -1R（止损严格执行）
        np.random.normal(1.0, 0.2, 25),     # 盈利 ~1R
        np.random.normal(2.3, 0.3, 12),     # 大盈利 ~2-3R
        np.random.normal(4.0, 0.5, 3)])     # 少数 3-5R
    ax.hist(r_vals, bins=24, color=TEAL, alpha=0.75, edgecolor="white")
    ax.axvline(0, color=DARK, lw=1.2)
    mean_r = r_vals.mean()
    ax.axvline(mean_r, color=ORANGE, lw=2.0, ls="--")
    ax.text(mean_r + 0.12, 9, f"平均 R = {mean_r:.2f}\n（SQN 的分子）", fontsize=10.5, color=ORANGE, va="top")
    ax.text(-1.55, 9.5, "60% 的交易亏 -1R\n（亏损被严格截断）", fontsize=10, color=DOWN, va="top")
    ax.text(2.5, 8.5, "少数 +3~5R 大单\n（让利润奔跑）", fontsize=10, color=UP, va="top")
    ax.set_xlabel("单笔盈亏（单位 R）", fontsize=11)
    ax.set_ylabel("交易笔数", fontsize=11)
    ax.set_xlim(-2.5, 5.5)
    ax.grid(axis="y", alpha=0.3)
    ax.set_title("R 分布：SQN = 平均 R ÷ R 标准差 × √笔数 —— 靠分布特征打分，不靠单笔",
                 fontsize=12, color=DARK)
    savefig(fig, "fig_p8_r_dist.png")


# ---------------------------------------------------------------- v4：9.1 考核三段式流程
def fig_prop_flow():
    """9.1 Prop 考核三段式：Phase 1 → Phase 2 → Funded，各带盈利目标与回撤约束"""
    fig, ax = plt.subplots(figsize=(12.5, 5.8))
    style_ax(ax, xlim=(0, 13.6), ylim=(0, 6.6))
    draw_box(ax, 0.9, 3.0, 3.4, 2.2, "Phase 1 挑战\n盈利目标 8-10%\n日回撤 ≤5%\n总回撤 ≤8-10%", ec=DOWN, fs=10.5)
    draw_box(ax, 5.4, 3.0, 3.4, 2.2, "Phase 2 验证\n盈利目标 ≈5%\n规则相同\n验证不是运气", ec=ORANGE, fs=10.5)
    draw_box(ax, 9.9, 3.0, 3.4, 2.2, "Funded 实盘\n分成 80-90%\n回撤线仍在\n出金 14-30 天", ec=UP, fs=10.5)
    flow_arrow(ax, 4.3, 4.1, 5.4, 4.1)
    flow_arrow(ax, 8.8, 4.1, 9.9, 4.1)
    mark(ax, 4.85, 5.6, "主要淘汰关：目标最高、\n最容易重仓冲刺撞线", fs=9.5, color=DOWN)
    mark(ax, 11.6, 1.4, "不是终点：=“第二场考核”，\n纪律不变，奖励从过线变现金流", fs=9.5, color=UP)
    mark(ax, 6.8, 6.2, "三段式考核：先定品种再选平台，读全规则（周末/新闻/一致性）", fs=11, color=DARK, box=True)
    savefig(fig, "fig_p9_prop_flow.png")


# ---------------------------------------------------------------- v4：9.3 轻仓 vs 重仓
def fig_risk_curve():
    """9.3 达标节奏数学：0.5% 风险稳步达标 vs 2% 风险重仓撞线出局"""
    fig, ax = plt.subplots(figsize=(12, 6.0))
    np.random.seed(11)
    n = np.arange(0, 81)  # 80 笔
    # 轻仓：单笔风险 0.5%，期望 +0.1%/笔，波动小
    light = np.cumsum(np.random.normal(0.1, 0.5, len(n)))
    # 重仓：单笔风险 2%，期望 +0.4%/笔，波动大
    heavy = np.cumsum(np.random.normal(0.4, 2.0, len(n)))
    ax.plot(n, light, color=UP, lw=2.2, label="轻仓：0.5% 风险，80 笔稳步 +8%")
    ax.plot(n, heavy, color=DOWN, lw=2.2, label="重仓：2% 风险，20 笔撞 -10% 总回撤线")
    ax.axhline(8, color=UP, ls=":", lw=1.2)
    ax.axhline(-10, color=DOWN, ls=":", lw=1.2)
    ax.text(2, 8.6, "Phase 1 目标 +8%", fontsize=10, color=UP)
    ax.text(2, -11.6, "总回撤线 -10%", fontsize=10, color=DOWN)
    # 重仓撞线点（第一次跌破 -10）
    hit = np.where(heavy < -10)[0]
    if len(hit):
        ax.plot(hit[0], heavy[hit[0]], "x", color=DOWN, ms=12, mew=2.5)
        ax.annotate("第 %d 笔撞线出局\n（连亏 3 笔概率 21.6%，长期必遇）" % hit[0],
                    xy=(hit[0], heavy[hit[0]]), xytext=(hit[0] - 28, -22),
                    fontsize=10, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))
    ax.set_xlabel("交易笔数", fontsize=11)
    ax.set_ylabel("账户累计收益 %", fontsize=11)
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_title("重仓把 1.5 个月压缩成 1-2 周，代价是把淘汰概率从低拉到必然——“慢就是快”",
                 fontsize=12, color=DARK)
    savefig(fig, "fig_p9_risk_curve.png")


# ---------------------------------------------------------------- v4：10.1 期权到期损益
def fig_call_put():
    """10.1 期权不对称性：买入 Call / 买入 Put 到期损益图（最大亏损 = 权利金）"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.4))
    s = np.linspace(4950, 5150, 200)  # 标的价格
    strike, prem = 5050, 30
    # 买入 Call：盈亏 = max(S-K,0) - 权利金
    pnl_call = np.maximum(s - strike, 0) - prem
    ax1.plot(s, pnl_call, color=UP, lw=2.4)
    ax1.axhline(0, color=GRAY, lw=0.8)
    ax1.axvline(strike, color=GRAY, ls=":", lw=1.0)
    ax1.axvline(strike + prem, color=ORANGE, ls="--", lw=1.2)
    ax1.text(strike + 3, -46, "行权价 5050", fontsize=9, color=GRAY)
    ax1.text(strike + prem + 3, -46, "盈亏平衡 5080", fontsize=9, color=ORANGE)
    ax1.annotate("最大亏损 = 权利金 30 点\n（亏损有限）", xy=(5000, -30), xytext=(4960, -75),
                 fontsize=9.5, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax1.annotate("盈利无限（理论上行不封顶）", xy=(5130, 50), xytext=(5075, 65),
                 fontsize=9.5, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax1.set_title("买入 Call（看涨）到期损益", fontsize=12, color=DARK)
    ax1.set_xlabel("到期时 ES 价格")
    ax1.set_ylabel("盈亏（点）")
    ax1.set_ylim(-85, 85)
    ax1.grid(alpha=0.3)
    # 买入 Put：盈亏 = max(K-S,0) - 权利金
    pnl_put = np.maximum(strike - s, 0) - prem
    ax2.plot(s, pnl_put, color=DOWN, lw=2.4)
    ax2.axhline(0, color=GRAY, lw=0.8)
    ax2.axvline(strike, color=GRAY, ls=":", lw=1.0)
    ax2.axvline(strike - prem, color=ORANGE, ls="--", lw=1.2)
    ax2.text(strike + 3, -46, "行权价 5050", fontsize=9, color=GRAY)
    ax2.text(4965, -46, "盈亏平衡 5020", fontsize=9, color=ORANGE)
    ax2.annotate("最大亏损 = 权利金 30 点", xy=(5080, -30), xytext=(5030, -75),
                 fontsize=9.5, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax2.annotate("下跌越多赚越多\n（最大盈利 = K - 权利金）", xy=(4970, 50), xytext=(4985, 65),
                 fontsize=9.5, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax2.set_title("买入 Put（看跌）到期损益", fontsize=12, color=DARK)
    ax2.set_xlabel("到期时 ES 价格")
    ax2.set_ylim(-85, 85)
    ax2.grid(alpha=0.3)
    fig.suptitle("买方不对称性：亏损封顶、盈利敞开——但“不仅要方向对，还要对得足够多”",
                 fontsize=12.5, color=DARK, y=1.0)
    savefig(fig, "fig_p10_call_put.png")


# ---------------------------------------------------------------- v4：10.2 Theta 衰减
def fig_theta_decay():
    """10.2 时间价值衰减：越接近到期蒸发越快（最后 2-3 周加速）"""
    fig, ax = plt.subplots(figsize=(11, 5.8))
    t = np.linspace(0, 60, 300)  # 距到期天数
    # 时间价值近似：厚→薄，加速衰减
    tv = 20 * (t / 60) ** 1.6 + 1.0
    ax.plot(t, tv, color=TEAL, lw=2.4)
    ax.fill_between(t, 0, tv, color=TEAL, alpha=0.12)
    ax.axvspan(0, 14, color=ORANGE, alpha=0.15)
    ax.text(7, 18.2, "最后 2-3 周：Theta 咬得最狠\n（时间价值加速蒸发）", fontsize=10.5, color=ORANGE, ha="center")
    ax.annotate("距到期 60 天：\n时间价值厚", xy=(60, tv[-1]), xytext=(46, 16),
                fontsize=10, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))
    ax.annotate("到期日：\n只剩内在价值", xy=(0, 1.0), xytext=(10, 3.5),
                fontsize=10, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))
    ax.set_xlabel("距到期日（天）", fontsize=11)
    ax.set_ylabel("时间价值（点）", fontsize=11)
    ax.set_xlim(0, 62)
    ax.set_ylim(0, 21)
    ax.invert_xaxis()
    ax.grid(alpha=0.3)
    ax.set_title("时间价值衰减曲线：买期权做方向，必须同时选对“到期日”", fontsize=12, color=DARK)
    savefig(fig, "fig_p10_theta.png")


# ---------------------------------------------------------------- 图 1-2（太妃 L01A）
def fig_p1_equilibrium():
    """1.1 均衡价位理论：市场目的=找到公平价格、促成最多成交；<20%时刻处于突破"""
    fig, ax = plt.subplots(figsize=(13, 6.3))
    style_ax(ax, xlim=(-1, 27), ylim=(94, 114))
    # 大部分时间在均衡带 99.5~103 内震荡，两次急速突破后回归
    k = [(0, 101, 102.6, 99.6, 100.4), (1, 100.4, 102, 98.8, 99.6), (2, 99.6, 101.4, 98.6, 100.8),
         (3, 100.8, 102.8, 99.8, 101.6), (4, 101.6, 103, 100.2, 101), (5, 101, 102.4, 99.4, 100.2),
         (6, 100.2, 101.8, 99, 100.6), (7, 100.6, 102.4, 99.8, 101.8), (8, 101.8, 107.5, 101.4, 106.2),  # 突破1
         (9, 106.2, 109, 105, 107.6), (10, 107.6, 109.8, 105.8, 106.8), (11, 106.8, 108.2, 105.2, 106),
         (12, 106, 107.4, 104, 105.2), (13, 105.2, 106.4, 103.2, 104.2), (14, 104.2, 105.2, 102.4, 103.2),
         (15, 103.2, 104.6, 102, 103.6), (16, 103.6, 105, 102.6, 104.2), (17, 104.2, 105.6, 103, 104),
         (18, 104, 105.4, 102.4, 103.2), (19, 103.2, 104.4, 101.6, 102.4), (20, 102.4, 103.6, 101, 102),
         (21, 102, 103.2, 100.6, 101.6), (22, 101.6, 102.8, 100.4, 101.2), (23, 101.2, 102.4, 99.8, 100.8),
         (24, 100.8, 102, 99.4, 100.4), (25, 100.4, 101.6, 98.8, 99.6), (26, 99.6, 101, 98.2, 99.8)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    # 均衡带：浅青底 + 上下边界虚线
    ax.axhspan(99.5, 103, color=TEAL, alpha=0.07, zorder=0)
    hl_line(ax, -0.8, 26.5, 103, color=TEAL, lw=1.0)
    hl_line(ax, -0.8, 26.5, 99.5, color=TEAL, lw=1.0)
    mark(ax, 12.8, 103.6, "均衡价位带：市场想待在这里，创造最多成交", color=TEAL, fs=11)
    # 两次突破段高亮
    ax.axvspan(8.2, 11.8, color=ORANGE, alpha=0.15, zorder=0)
    ax.axvspan(18.2, 20.8, color=ORANGE, alpha=0.15, zorder=0)
    annotate_mark(ax, 9, 107.6, "突破（急速运动）\n上涨 = 原价觅不到卖家\n100→150→200→250 逐级成交", 1.5, 110.5, color=ORANGE, fs=10.5)
    annotate_mark(ax, 19.4, 101.8, "突破（急速运动）\n< 20% 的时间处于这种状态", 12.5, 108.8, color=ORANGE, fs=10.5)
    mark(ax, 23.6, 96.6, "> 80% 的时间\n价格在均衡位附近上下探测", color=DARK, fs=10.5, box=True, va="top")
    ax.set_title("市场的目的不是制造趋势，而是找到公平价格、促成最多成交——均衡是常态，突破是例外", fontsize=12.5, color=DARK)
    savefig(fig, "fig_p1_equilibrium.png")


# ---------------------------------------------------------------- 图 1-3（1.5 杠杆）
def fig_p1_leverage():
    """1.5 杠杆放大的是仓位误差：同样的判断错误，不同杠杆下账户损伤天差地别"""
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    style_ax(ax, xlim=(0, 2.1), ylim=(-120, 8))
    x = np.linspace(0, 2.0, 80)
    for lev, c, lab in [(30, TEAL, "1:30 杠杆"), (100, ORANGE, "1:100 杠杆"), (500, DOWN, "1:500 杠杆")]:
        y = -x * lev * 2  # 价格每反向 1%，本金损伤 = 杠杆 × 1%（示意系数）
        ax.plot(x, y, color=c, lw=2.2, label=lab)
    ax.axhline(-100, color=DARK, ls="--", lw=1.4)
    mark(ax, 0.05, -103, "爆仓线 -100%", color=DARK, fs=10.5, ha="left", va="bottom")
    ax.axvline(0.5, color=GRAY, ls=":", lw=1.2)
    mark(ax, 0.5, 3, "价格反向 0.5%", color=GRAY, fs=10, ha="center", va="bottom")
    annotate_mark(ax, 0.5, -30, "账户 −30%（小伤）", 0.9, -52, color=TEAL, fs=10)
    annotate_mark(ax, 0.5, -100, "账户 −100%（爆仓）", 0.9, -108, color=ORANGE, fs=10)
    annotate_mark(ax, 0.5, -108, "账户 −500%（远远爆仓）", 1.35, -90, color=DOWN, fs=10)
    ax.legend(loc="lower left", fontsize=10, frameon=False)
    ax.set_title("杠杆不改变你的胜率，它放大的是你的仓位误差", fontsize=13, color=DARK)
    savefig(fig, "fig_p1_leverage.png")


# ---------------------------------------------------------------- 图 1-4（1.7 全球时段）
def fig_p1_sessions():
    """1.7 全球时段：悉尼/东京/伦敦/纽约与黄金重叠窗口（北京时间横轴）"""
    fig, ax = plt.subplots(figsize=(13, 5.6))
    style_ax(ax, xlim=(0, 24), ylim=(-1.2, 5.4))
    ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
    ax.set_xticklabels(["0:00", "4:00", "8:00", "12:00", "16:00", "20:00", "24:00"], fontsize=9, color=DARK)
    ax.tick_params(axis="x", length=0)
    # 时段横条：y 从下往上 0~3
    bars = [("悉尼", 6, 14, GRAY, 0), ("东京", 8, 14.5, TEAL, 1), ("伦敦", 15, 24, ORANGE, 2),
            ("纽约", 20, 24, DOWN, 3), ("纽约", 0, 4, DOWN, 3)]
    for name, s, e, c, y in bars:
        ax.barh(y, e - s, left=s, height=0.62, color=c, alpha=0.85, edgecolor="white", zorder=3)
        ax.text((s + e) / 2, y, name, ha="center", va="center", fontsize=10, color="white", zorder=4)
    # 黄金窗口高亮
    ax.axvspan(20, 24, color="#ffeb3b", alpha=0.35, zorder=0)
    mark(ax, 22, 4.4, "黄金窗口：伦敦 + 纽约重叠（北京 20:00-24:00）", color=ORANGE, fs=11.5, box=True)
    mark(ax, 11.5, 4.4, "亚盘：流动性薄，信号质量低", color=GRAY, fs=10.5)
    ax.set_title("全球交易时段（北京时间）：流动性随时段变化，黄金窗口只有 4 小时", fontsize=12.5, color=DARK)
    savefig(fig, "fig_p1_sessions.png")


# ---------------------------------------------------------------- 图 3-9（太妃 L03A）
def fig_p3_breakout_four():
    """3.10 突破的四种结果（L03A）：成功 / 回调 / 失败 / 反转；所有影线都是失败的突破"""
    fig, axes = plt.subplots(2, 2, figsize=(13, 8.6))
    # 每格：阻力线 100，突破点 x=5
    def _panel(ax, k, title, sub, tc):
        for x, o, h, l, c in k:
            candle(ax, x, o, h, l, c)
        hl_line(ax, -0.4, 8.6, 100, color=GRAY, lw=1.0)
        mark(ax, 4.1, 100.8, "阻力", color=GRAY, fs=9)
        mark(ax, 4.1, 100, title, dy=5.2 if tc != DOWN else -4.2, color=tc, fs=12, box=True)
        mark(ax, 4.1, 100, sub, dy=-4.8 if tc != DOWN else 5.4, color=DARK, fs=9.5)
        style_ax(ax, xlim=(-0.5, 9.3), ylim=(94, 111))
    _panel(axes[0][0], [(0, 98.5, 100, 97, 99), (1, 99, 100.4, 97.8, 98.8), (2, 98.8, 99.8, 97.6, 98.4),
                        (3, 98.4, 99.6, 97.4, 98.2), (4, 98.2, 99.4, 97.2, 98),
                        (5, 98, 104.5, 97.8, 103.2), (6, 103.2, 107, 102.4, 106), (7, 106, 109, 105.2, 108)],
           "① 突破成功", "趋势 K 线穿透阻力\n后续跟进 K 线延续", UP)
    _panel(axes[0][1], [(0, 98.5, 100, 97, 99), (1, 99, 100.4, 97.8, 98.8), (2, 98.8, 99.8, 97.6, 98.4),
                        (3, 98.4, 99.6, 97.4, 98.2), (4, 98.2, 99.4, 97.2, 98),
                        (5, 98, 103.8, 97.8, 102.6), (6, 102.6, 104.5, 100.2, 103.4), (7, 103.4, 105.5, 102.6, 104.8)],
           "② 突破回调（停顿）", "顺势力量暂时休息\n（双重底牛旗）", UP)
    _panel(axes[1][0], [(0, 98.5, 100, 97, 99), (1, 99, 100.4, 97.8, 98.8), (2, 98.8, 99.8, 97.6, 98.4),
                        (3, 98.4, 99.6, 97.4, 98.2), (4, 98.2, 99.4, 97.2, 98),
                        (5, 98, 102.8, 97.8, 101.6), (6, 101.6, 102.2, 98.8, 99.6), (7, 99.6, 100.4, 97.8, 98.6)],
           "③ 突破失败", "突破 K 线收回区间\n它就是一根影线", DOWN)
    _panel(axes[1][1], [(0, 98.5, 100, 97, 99), (1, 99, 100.4, 97.8, 98.8), (2, 98.8, 99.8, 97.6, 98.4),
                        (3, 98.4, 99.6, 97.4, 98.2), (4, 98.2, 99.4, 97.2, 98),
                        (5, 98, 102.6, 97.8, 101.2), (6, 101.2, 101.8, 95.5, 96.4), (7, 96.4, 97.4, 94, 95)],
           "④ 反转（空头突破成功）", "多头突破失败 = 空头突破成功\n若实现，逆势方转为顺势方", DOWN)
    fig.suptitle("突破的四种结果：成功的突破 = 趋势 K 线穿透支撑/阻力；所有影线都是失败的突破", fontsize=13, color=DARK, y=0.99)
    savefig(fig, "fig_p3_breakout_four.png")


# ---------------------------------------------------------------- 图 3-10（太妃 L04A）
def fig_p3_testing():
    """3.10 突破后必有测试（L04A）：价格折返突破点，四批人共同决策"""
    fig, ax = plt.subplots(figsize=(13, 6.6))
    style_ax(ax, xlim=(-1, 17.5), ylim=(94, 115))
    k = [(0, 98.5, 100, 97, 99), (1, 99, 100.4, 97.8, 98.8), (2, 98.8, 99.8, 97.6, 98.4),
         (3, 98.4, 99.6, 97.4, 98.2), (4, 98.2, 99.4, 97.2, 98), (5, 98, 104.5, 97.8, 103.2),  # 突破
         (6, 103.2, 107, 102.4, 105.6), (7, 105.6, 107.5, 103.5, 105),  # 冲高
         (8, 105, 106, 101.5, 102.6), (9, 102.6, 103.6, 100.4, 101.6),  # 折返
         (10, 101.6, 102.6, 99.8, 100.6), (11, 100.6, 101.8, 99.4, 100.4),  # 测试突破点
         (12, 100.4, 103, 99.8, 102.2), (13, 102.2, 105.5, 101.8, 104.6)]  # 测试成功，延续
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, -0.8, 12.2, 100, color=GRAY, lw=1.0)
    mark(ax, 5, 100, "突破点", dy=2.0, color=GRAY, fs=9.5)
    ax.axvspan(8.2, 11.8, color=ORANGE, alpha=0.16, zorder=0)
    annotate_mark(ax, 10, 100, "测试：价格折返突破点\n四批人共同决策，票多的赢", 2.2, 105, color=ORANGE, fs=11)
    # 四批人
    mark(ax, 15.2, 112.8, "空仓的多头：还敢重新做多吗？", color=UP, fs=10, ha="center")
    mark(ax, 15.2, 110.6, "持仓的多头：敢持有、敢加仓吗？", color=UP, fs=10, ha="center")
    mark(ax, 15.2, 108.4, "空仓的空头：敢趁机做空吗？", color=DOWN, fs=10, ha="center")
    mark(ax, 15.2, 106.2, "持仓的空头：有不亏的机会就跑吗？", color=DOWN, fs=10, ha="center")
    mark(ax, 15.2, 103.6, "票多的赢，票少的输", color=DARK, fs=11.5, box=True, ha="center")
    ax.plot([13.6, 14.6], [104, 105.5], color=UP, lw=1.6, ls="--")
    ax.plot([13.6, 14.6], [103.5, 101], color=DOWN, lw=1.6, ls="--")
    mark(ax, 14.6, 106.3, "测试成功：延续", color=UP, fs=10.5, ha="left")
    mark(ax, 14.6, 100, "测试失败：反转", color=DOWN, fs=10.5, ha="left")
    ax.set_title("突破发生后必有测试：市场对失衡的自我调节——测试决定突破能否延续行情", fontsize=12.5, color=DARK)
    savefig(fig, "fig_p3_testing.png")


# ---------------------------------------------------------------- 图 4-6（太妃 L17A）
def fig_p4_pullback_seq():
    """4.2 首次回调序列（L17A）：趋势从发起到结束，是顺势方动能衰退、逆势方愈发进取的进程"""
    fig, ax = plt.subplots(figsize=(13.5, 6.4))
    style_ax(ax, xlim=(-1, 24.5), ylim=(94, 116))
    # K线：强势阳线→实体变短→十字星→阴线→高1→高2→高3→20gap→破均线→区间
    k = [(0, 98.5, 100, 97, 99), (1, 99, 102, 98, 101), (2, 101, 104, 100, 103),
         (3, 103, 106.5, 102, 105.5), (4, 105.5, 108, 104.5, 107), (5, 107, 109.5, 105.5, 106.5),
         (6, 106.5, 108.5, 105, 107), (7, 107, 108.8, 105.8, 106.6), (8, 106.6, 107.8, 105.4, 106.2),
         (9, 106.2, 107, 104.6, 105.2), (10, 105.2, 106.4, 103.8, 104.6), (11, 104.6, 106.8, 104, 106),
         (12, 106, 107.4, 104.6, 105.4), (13, 105.4, 106.6, 103.6, 104.4), (14, 104.4, 106, 103, 105.2),
         (15, 105.2, 106.4, 103.8, 104.4), (16, 104.4, 105.2, 102.6, 103.4), (17, 103.4, 104.4, 102, 103),
         (18, 103, 103.8, 101.4, 102.2), (19, 102.2, 103.2, 100.6, 101.4), (20, 101.4, 102.2, 99.8, 100.6),
         (21, 100.6, 101.6, 99.2, 100.2), (22, 100.2, 101, 98.8, 99.4), (23, 99.4, 100.2, 98.2, 98.8)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    # 均线：先升后平缓回落（EMA20 简化曲线）
    mx = np.linspace(0, 23, 200)
    my = 99 + 8.5 * np.exp(-((mx - 4.5) ** 2) / 30) - 0.09 * np.maximum(mx - 9, 0)
    ax.plot(mx, my, color=ORANGE, lw=2.0, zorder=2, label="EMA20")
    # 阶段标注（顶部编号）
    stages = [(2, "① 强势阳线\n实体大影线短"), (5, "② 实体变短\n上影线变长"), (8, "③ 重叠增多\n④ 十字星"),
              (10, "⑤ 高1\n一推回调"), (14, "⑥ 高2\n二推回调"), (17, "⑦ 高3\n三推（楔形）"),
              (19, "⑧ 20 gap\n触及均线"), (21, "⑨ 收盘破均线"), (22.6, "⑩ 整根K线\n在均线下方")]
    for x, t in stages:
        ax.text(x, 115.2, t, fontsize=8.8, color=DARK, ha="center", va="top", zorder=5)
    # 三阶段底色
    ax.axvspan(-0.8, 8.5, color=UP, alpha=0.06, zorder=0)
    ax.axvspan(8.5, 17.5, color=ORANGE, alpha=0.06, zorder=0)
    ax.axvspan(17.5, 24.5, color=DOWN, alpha=0.06, zorder=0)
    mark(ax, 3.8, 95.8, "初期：回调弱而浅\n（旗形延续）", color=UP, fs=10, ha="center", va="bottom")
    mark(ax, 13, 95.8, "中期：回调加深\n（高1→高2→高3）", color=ORANGE, fs=10, ha="center", va="bottom")
    mark(ax, 21, 95.8, "末期：破均线、入区间\n（首次反转尝试倾向失败，\n原趋势极值倾向被测试）", color=DOWN, fs=10, ha="center", va="bottom")
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    ax.set_title("首次回调序列：趋势的生命周期 = 顺势方动能衰退、逆势方愈发进取的阶梯", fontsize=12.5, color=DARK)
    savefig(fig, "fig_p4_pullback_seq.png")


# ---------------------------------------------------------------- 图 7-2（太妃 L12）
def fig_p7_style():
    """7.7 波段 vs 刮头皮（L12）：为什么没有高胜率+高盈亏比——对手都是精明的"""
    fig, ax = plt.subplots(figsize=(11.5, 6.6))
    style_ax(ax, xlim=(0.4, 3.2), ylim=(20, 95))
    # 期望 0.2 的胜率-盈亏比曲线：win = 1.2/(RR+1)
    rr = np.linspace(0.5, 3.0, 120)
    win = 1.2 / (rr + 1) * 100
    ax.plot(rr, win, color=DARK, lw=2.2, zorder=3)
    ax.scatter([1, 2], [60, 40], s=140, zorder=5, color=[UP, ORANGE])
    annotate_mark(ax, 1, 60, "刮头皮：1R × 60% 胜率\n期望 = 1×0.6 − 1×0.4 = 0.2", 1.55, 72, color=UP, fs=10.5)
    annotate_mark(ax, 2, 40, "波段：2R × 40% 胜率\n期望 = 2×0.4 − 1×0.6 = 0.2", 2.45, 55, color=ORANGE, fs=10.5)
    ax.axvline(1, color=UP, ls=":", lw=1.0)
    ax.axvline(2, color=ORANGE, ls=":", lw=1.0)
    mark(ax, 0.7, 88, "高胜率、低盈亏比\n（刮头皮地带）", color=UP, fs=10)
    mark(ax, 2.75, 88, "低胜率、高盈亏比\n（波段地带）", color=ORANGE, fs=10)
    mark(ax, 2.75, 32, "期望值相同的点\n时常相互成交", color=GRAY, fs=9.5)
    ax.set_xticks([0.5, 1, 1.5, 2, 2.5, 3])
    ax.set_xticklabels(["0.5", "1", "1.5", "2", "2.5", "3"], fontsize=9, color=DARK)
    ax.set_yticks([30, 40, 50, 60, 70, 80, 90])
    ax.set_yticklabels(["30%", "40%", "50%", "60%", "70%", "80%", "90%"], fontsize=9, color=DARK)
    ax.set_xlabel("盈亏比（R 倍）", fontsize=11, color=DARK)
    ax.set_ylabel("胜率", fontsize=11, color=DARK)
    ax.grid(alpha=0.25)
    mark(ax, 1.8, 24, "波段：不介意止损，痛恨错失大波段（持有 10-30 根 K 线）\n刮头皮：不喜欢亏损，不介意踏空利润（持有 1-5 根 K 线）\n哪个是你更愿意忍受的？——这就是你选择风格的依据", color=DARK, fs=10, box=True, va="bottom")
    ax.set_title("为什么不存在“高胜率 + 高盈亏比”？——对手都是精明的，你占据一头就失去另一头", fontsize=12.5, color=DARK)
    savefig(fig, "fig_p7_style.png")


# ---------------------------------------------------------------- 图 7-3（7.2 损失厌恶）
def fig_p7_loss_aversion():
    """7.2 损失厌恶：Kahneman 价值函数，亏损的痛约为盈利快乐的两倍"""
    fig, ax = plt.subplots(figsize=(11, 6.2))
    style_ax(ax, xlim=(-230, 230), ylim=(-24, 16))
    xg = np.linspace(0, 200, 100)
    xl = np.linspace(-200, 0, 100)
    ax.plot(xg, 10 * (xg / 200) ** 0.6, color=UP, lw=2.6, zorder=3)          # 收益：凹
    ax.plot(xl, -22 * (-xl / 200) ** 0.6, color=DOWN, lw=2.6, zorder=3)      # 损失：凸且陡
    ax.axhline(0, color=GRAY, lw=1.0)
    ax.axvline(0, color=GRAY, lw=1.0)
    mark(ax, 0, 0.5, "参考点（现状）", color=GRAY, fs=9.5, ha="center")
    # 对比：+200 的快乐 vs −100 的痛苦
    ax.plot([100, 100], [0, -17.7], color=DOWN, ls=":", lw=1.2)
    ax.plot([200, 200], [0, 10], color=UP, ls=":", lw=1.2)
    mark(ax, 200, 10.8, "赚 200 的快乐\n（10 单位）", color=UP, fs=10, ha="center")
    mark(ax, 100, -18.6, "亏 100 的痛苦\n（−17.7 单位）", color=DOWN, fs=10, ha="center")
    annotate_mark(ax, 130, -18.6, "亏 100 的痛苦 ≈ 赚 200 的快乐", 40, -21.5, color=DARK, fs=11)
    mark(ax, 160, -4.5, "亏损区：凸函数\n→ 死扛不止损（风险寻求）", color=DOWN, fs=10)
    mark(ax, -160, 12, "盈利区：凹函数\n→ 赚一点就跑（风险回避）", color=UP, fs=10)
    ax.set_title("损失厌恶（Kahneman & Tversky, 1979）：失去的痛，约为得到的快乐的两倍", fontsize=12.5, color=DARK)
    savefig(fig, "fig_p7_loss_aversion.png")


# ---------------------------------------------------------------- 图 7-4（7.1 心理三阶段）
def fig_p7_three_stages():
    """7.1 心理成熟三阶段：结果导向 → 规则导向 → 概率导向"""
    fig, ax = plt.subplots(figsize=(13.5, 6.2))
    style_ax(ax, xlim=(0, 13.8), ylim=(0, 6.8))
    cols = [
        (0.4, DARK, "阶段 1：结果导向（新手）", "关注：这笔赚没赚\n赚了=天才，亏了=系统骗人\n情绪随单笔盈亏起伏"),
        (4.9, ORANGE, "阶段 2：规则导向（进阶）", "关注：有没有按规则做\n开始执行规则\n但情绪仍随盈亏起伏"),
        (9.4, UP, "阶段 3：概率导向（成熟）", "关注：是否一致执行了\n正期望值系统\n看 100 笔的分布，不是这一笔"),
    ]
    for x, c, title, body in cols:
        draw_box(ax, x, 3.6, 4.0, 1.6, title, ec=c, fs=12.5, tc=c)
        draw_box(ax, x, 0.9, 4.0, 2.0, body, ec=GRAY, fs=10.5)
    flow_arrow(ax, 4.55, 4.4, 4.85, 4.4, color=DARK)
    flow_arrow(ax, 9.05, 4.4, 9.35, 4.4, color=DARK)
    mark(ax, 6.9, 0.35, "评价标准从“赚没赚”换成“有没有一致执行”，心态问题就解决了一大半", color=DARK, fs=11.5, box=True, va="bottom")
    mark(ax, 6.9, 6.35, "好交易 = 按计划执行的亏损单；坏交易 = 侥幸赚钱的违规单", color=DARK, fs=11.5, box=True, va="top")
    ax.set_title("心理成熟的三个阶段：从看单笔结果，到看一致执行", fontsize=12.5, color=DARK)
    savefig(fig, "fig_p7_three_stages.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    fig_kline_structure()
    fig_trend()
    fig_support_resistance()
    fig_hammer_sweep()
    fig_false_breakout()
    fig_engulfing()
    fig_inside_bar()
    fig_pullback_system()
    fig_wyckoff()
    fig_state_machine()
    fig_liquidity_pool()
    fig_sweep()
    fig_bos_choch()
    fig_order_block()
    fig_fvg()
    # ---------- v3 新增（洛氏/威科夫2.0/雷神/南桥素材） ----------
    fig_diffusion()
    fig_123_ross()
    fig_ross_hook()
    fig_final_flag()
    fig_wedge_p3()
    fig_measured_move()
    fig_opening_reversal()
    fig_breakout_confirm()
    fig_limit_order_zone()
    fig_always_in()
    fig_swing_range()
    fig_supply_demand()
    fig_s2b_b2s()
    fig_liquidity_induce()
    fig_auction_cycle()
    fig_three_contracts()
    # ---------- v4 新增（6/7/8 章无图章节） ----------
    fig_be_curve()
    fig_stop_size()
    fig_drawdown_prob()
    fig_verify_loop()
    fig_r_dist()
    # ---------- v4 新增（9/10 章无图章节） ----------
    fig_prop_flow()
    fig_risk_curve()
    fig_call_put()
    fig_theta_decay()
    # ---------- v5 新增（第1/3/4/7章补图 + 太妃PPT概念） ----------
    fig_p1_equilibrium()
    fig_p1_leverage()
    fig_p1_sessions()
    fig_p3_breakout_four()
    fig_p3_testing()
    fig_p4_pullback_seq()
    fig_p7_style()
    fig_p7_loss_aversion()
    fig_p7_three_stages()
    # ---------- v6 新增（第2章 K线信号字典 + 铁丝网，PA_Agent 提示词库） ----------
    fig_p2_signal_bars()
    fig_p2_barbwire()
    fig_p2_checklist()
    fig_p3_wedge_contrast()
    fig_p3_h1h2()
    fig_p4_mm_four()
    fig_p4_channel_types()
    fig_p4_ff_20gb()
    fig_p4_state_tree()
    print("全部完成")


# ---------------------------------------------------------------- 图 2-2（PA_Agent 文件16 K线信号字典）
def fig_p2_signal_bars():
    """2.1 K 线信号字典：信号棒→入场棒→确认棒、内包/外包、ioi、2BR、MDB"""
    fig, axes = plt.subplots(2, 2, figsize=(13, 8.6))
    # (a) 信号棒→入场棒→确认棒
    ax = axes[0][0]
    for x, o, h, l, c in [(0, 98, 105.8, 97.2, 105.2), (1, 104.2, 107.2, 103.4, 106.8), (2, 106.2, 109.2, 105.4, 108.6)]:
        candle(ax, x, o, h, l, c)
    hl_line(ax, -0.4, 0.45, 105.8, color=UP, ls=":", lw=1.2)
    hl_line(ax, -0.4, 3.3, 106.8, color=GRAY, ls=":", lw=1.0)
    mark(ax, 0, 110.5, "①信号棒", color=DARK, fs=10.5, box=True)
    mark(ax, 0, 110.5, "收盘近高点、实体大\n不超过平均 1.5 倍", dy=-1.9, color=DARK, fs=8.5)
    mark(ax, 1, 112.6, "②入场棒：突破信号棒高点触发", color=UP, fs=10, box=True)
    mark(ax, 2, 115, "③确认棒：继续创新高", color=UP, fs=10, box=True)
    mark(ax, 1.65, 107.9, "突破触发", color=GRAY, fs=8.5)
    style_ax(ax, xlim=(-0.6, 3.4), ylim=(95.5, 116.5))
    ax.set_title("(a) 一次入场三段式：信号→入场→确认", fontsize=11, color=DARK)
    # (b) 内包 vs 外包
    ax = axes[0][1]
    candle(ax, 0, 100, 105, 99, 104)
    candle(ax, 1, 102.6, 104, 101.6, 103.4)
    mark(ax, 1, 105.6, "IB 内包：收缩\n单根不单独交易", color=GRAY, fs=9.5, box=True)
    candle(ax, 3.6, 100, 105, 99, 104)
    candle(ax, 4.6, 103.2, 107.2, 97.8, 106.4)
    mark(ax, 4.6, 108.6, "OB 外包：扩张\n不是突破信号", color=ORANGE, fs=9.5, box=True)
    style_ax(ax, xlim=(-0.6, 5.8), ylim=(95.5, 112))
    ax.set_title("(b) 内包棒（波动收缩）vs 外包棒（波动扩张）", fontsize=11, color=DARK)
    # (c) ioi 模式
    ax = axes[1][0]
    candle(ax, 0, 100, 105, 99, 104)
    candle(ax, 1, 102.6, 104, 101.6, 103.4)
    candle(ax, 2, 102, 107.6, 100.4, 106.8)
    candle(ax, 3, 105.6, 106.9, 104.5, 106.2)
    mark(ax, 1, 108.8, "① 内包：犹豫", color=GRAY, fs=9.5)
    mark(ax, 2, 111, "② 外包：选择方向（突破）", color=UP, fs=9.5)
    mark(ax, 3, 108.8, "③ 内包：蓄力", color=GRAY, fs=9.5)
    mark(ax, 1.9, 96.5, "ioi = 突破模式：等第三根内包后的触发，方向由背景决定", color=DARK, fs=9.5, box=True, va="top")
    style_ax(ax, xlim=(-0.6, 4.3), ylim=(94.5, 113))
    ax.set_title("(c) ioi 组合：内包→外包→内包", fontsize=11, color=DARK)
    # (d) 2BR + MDB
    ax = axes[1][1]
    candle(ax, 0, 105, 106.8, 103.2, 104.4)
    candle(ax, 1, 104.4, 108, 103.8, 107.6)
    mark(ax, 0.5, 109.6, "2BR 双棒反转：第二根实体≥第一根50%\n胜率仅 50-55%，须在关键位读", color=DOWN, fs=9.5, box=True)
    candle(ax, 3.4, 103.6, 105.6, 103, 105.2)
    candle(ax, 4.4, 103.8, 106.4, 103, 106)
    hl_line(ax, 3.2, 4.8, 103, color=UP, ls=":", lw=1.2)
    mark(ax, 3.9, 108.4, "MDB 微双底：两根棒低点差<2跳\n卖方两次突破失败", color=UP, fs=9.5, box=True)
    style_ax(ax, xlim=(-0.6, 5.6), ylim=(101, 112))
    ax.set_title("(d) 2BR 双棒反转 与 MDB 微双底", fontsize=11, color=DARK)
    fig.suptitle("K 线信号字典：先上下文，再形态；没有跟随的信号不能当成高概率机会", fontsize=13, color=DARK, y=0.99)
    savefig(fig, "fig_p2_signal_bars.png")


# ---------------------------------------------------------------- 图 2-8（PA_Agent 文件21 铁丝网）
def fig_p2_barbwire():
    """2.8 铁丝网 Barbwire：紧凑重叠、绕 EMA 穿梭——大部分信号忽略"""
    fig, ax = plt.subplots(figsize=(13, 6.3))
    style_ax(ax, xlim=(-1, 17), ylim=(96.2, 104.4))
    # EMA20 平坦线
    ax.plot([-1, 17], [100, 100], color=ORANGE, lw=1.8, zorder=1)
    mark(ax, 15.8, 100.35, "EMA20（平坦纠缠）", color=ORANGE, fs=9.5)
    # 铁丝网K线：绕100穿梭、小实体、重叠、十字星
    k = [(0, 99.8, 100.9, 99.3, 100.6), (1, 100.5, 101.1, 99.7, 100.2), (2, 100.1, 100.7, 99.4, 99.9),
         (3, 99.8, 100.5, 99.2, 100.3), (4, 100.2, 100.9, 99.6, 99.8), (5, 99.7, 100.4, 99.3, 100.1),
         (6, 100, 100.6, 99.4, 99.7), (7, 99.6, 100.2, 99.1, 100), (8, 99.9, 100.6, 99.3, 99.6),
         (9, 99.6, 100.1, 99, 99.9), (10, 99.8, 100.4, 99.2, 99.7), (11, 99.6, 100.2, 99.1, 100.1),
         (12, 100, 100.8, 99.5, 100.4), (13, 100.3, 101, 99.7, 100), (14, 99.9, 100.5, 99.4, 100.2)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c, width=0.52)
    # 区间上下沿
    hl_line(ax, -0.8, 15.6, 101.0, color=GRAY, ls=":", lw=1.1)
    hl_line(ax, -0.8, 15.6, 99.0, color=GRAY, ls=":", lw=1.1)
    ax.annotate("", xy=(15.6, 99.0), xytext=(15.6, 101.0),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.3), zorder=2)
    mark(ax, 15.55, 100, "区间宽度 ÷ 平均波段高度 < 25%\n（紧凑度）", dy=0, color=GRAY, fs=9, ha="right")
    mark(ax, 7.5, 103.6, "铁丝网 Barbwire：紧凑重叠、绕 EMA 穿梭\n十字星/内包棒频繁但方向不明", color=DOWN, fs=11.5, box=True)
    mark(ax, 7.5, 96.9, "大部分信号忽略；最危险 = 高点上方买、低点下方卖的普通突破（大概率假突破）", color=DOWN, fs=10.5, box=True, va="top")
    mark(ax, 16.4, 102.6, "自检咒语：\n紧凑横向整理？\n来回穿梭？\n边界几乎重叠？", color=DARK, fs=9.5, box=True, ha="left")
    mark(ax, 3, 97.6, "机会在铁丝网之后：突破失败（失败的失败）\n极值附近短 K 线刮头皮（仅边界）\n铁丝网后尖峰级突破 + 跟随", color=UP, fs=9.5, box=True, va="top", ha="left")
    savefig(fig, "fig_p2_barbwire.png")


# ---------------------------------------------------------------- 图 2-9（PA_Agent 逐棒检查单）
def fig_p2_checklist():
    """2.9 逐棒检查单：五步流程 + 六条口诀"""
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.8))
    # 左：每根 K 线收盘后的五步流程
    ax = axes[0]
    steps = ["① 分类：趋势棒/十字星/内包/外包？",
             "② 角色：结构/信号/入场/确认棒？",
             "③ 上下文：趋势/通道/区间/突破后/反转？",
             "④ 跟随：后 1-2 根同向推进？",
             "⑤ 更新计划：顺势/等二次/等测试/放弃/不做"]
    ys = [8.35, 6.65, 4.95, 3.25, 1.55]
    for i, (t, y) in enumerate(zip(steps, ys)):
        draw_box(ax, 0.8, y, 8.2, 1.25, t, ec=DARK, fs=10.5)
        if i < 4:
            flow_arrow(ax, 4.9, y, 4.9, ys[i + 1] + 1.25, color=TEAL)
    mark(ax, 4.9, 9.75, "每根 K 线收盘后（10 秒内跑完）", color=TEAL, fs=11, box=True)
    style_ax(ax, xlim=(0, 10), ylim=(0, 10.8))
    ax.set_title("① 五步固定流程", fontsize=11.5, color=DARK)
    # 右：六条口诀
    ax = axes[1]
    tips = [("① 先上下文，再形态", 0.4, 7.9), ("② 先信号质量，再入场计划", 5.2, 7.9),
            ("③ 先二次入场，再评估反转", 0.4, 5.7), ("④ 先跟随，再确认可交易", 5.2, 5.7),
            ("⑤ 先惯性，再逆势", 0.4, 3.5), ("⑥ 看不懂，就等下一根", 5.2, 3.5)]
    for t, x, y in tips:
        draw_box(ax, x, y, 4.4, 1.6, t, ec=TEAL, fs=11)
    mark(ax, 4.9, 1.5, "没有跟随的信号，不能当成高概率机会", color=DARK, fs=10, box=True)
    style_ax(ax, xlim=(0, 10), ylim=(0, 10.8))
    ax.set_title("② 六条口诀（每次看图默念）", fontsize=11.5, color=DARK)
    fig.suptitle("逐棒检查单（Al Brooks）：先上下文再形态、先信号质量再计划、先二次入场再反转、先跟随再确认、先惯性再逆势、看不懂就等下一根", fontsize=12, color=DARK, y=0.99)
    savefig(fig, "fig_p2_checklist.png")


# ---------------------------------------------------------------- 图 4-10（PA_Agent 市场诊断框架 状态判定树）
def fig_p4_state_tree():
    """4.6 状态判定树：通道与区间的唯一入口"""
    fig, ax = plt.subplots(figsize=(15.5, 8.2))
    draw_box(ax, 5.2, 7.6, 4.6, 1.4, "是否存在有序波段序列？\n（≥2 组 HH+HL / LL+LH）", ec=DARK, fs=11)
    draw_box(ax, 1.0, 5.0, 4.8, 1.4, "序列 ≥3 组且可画\n平行趋势线？", ec=TEAL, fs=11)
    draw_box(ax, 9.2, 5.0, 4.8, 1.4, "清晰上下边界？\n（各 ≥2 次测试）", ec=TEAL, fs=11)
    draw_box(ax, 0.4, 2.4, 4.6, 1.7, "按最近回撤分类：\n<30% 窄 / 30-50% 常规\n50-78.6% 宽通道（4.21）", ec=UP, fs=10)
    draw_box(ax, 5.6, 2.4, 4.6, 1.7, "trending_tr\n趋势型区间（仅 2 组）\n同框架、置信度更低", ec=GRAY, fs=10)
    draw_box(ax, 9.2, 2.4, 4.6, 1.7, "trading_range\n普通交易区间\n（区间策略，4.3）", ec=DOWN, fs=10)
    draw_box(ax, 14.4, 2.4, 3.9, 1.7, "extreme_tr\n极端区间\n期望值为负，不做", ec=GRAY, fs=10)
    flow_arrow(ax, 6.0, 7.6, 3.2, 6.4, color=DARK, rad=-0.15)
    flow_arrow(ax, 9.0, 7.6, 11.4, 6.4, color=DARK, rad=0.15)
    flow_arrow(ax, 3.4, 5.0, 3.4, 4.1, color=TEAL)
    flow_arrow(ax, 5.8, 5.0, 7.8, 4.1, color=TEAL, rad=-0.2)
    flow_arrow(ax, 11.5, 5.0, 11.5, 4.1, color=TEAL)
    flow_arrow(ax, 13.8, 5.0, 15.6, 4.1, color=TEAL, rad=0.25)
    mark(ax, 4.3, 7.25, "是", color=DARK, fs=10)
    mark(ax, 10.6, 7.25, "否", color=DARK, fs=10)
    mark(ax, 3.9, 4.62, "是", color=TEAL, fs=10)
    mark(ax, 6.9, 4.62, "否", color=TEAL, fs=10)
    mark(ax, 11.9, 4.62, "是", color=TEAL, fs=10)
    mark(ax, 14.9, 4.62, "否", color=TEAL, fs=10)
    mark(ax, 7.6, 0.35, "最新波段出现 LL（涨）/ HH（跌）→ 立即重估是否转区间；状态转换期降级处理（弱信号不做，目标保守）", color=DARK, fs=10, box=True)
    style_ax(ax, xlim=(0, 18.6), ylim=(0, 9.5))
    ax.set_title("状态判定树：通道与区间的唯一入口——每一步都有硬条件，斜率/视觉宽度只作辅助", fontsize=12.5, color=DARK)
    savefig(fig, "fig_p4_state_tree.png")


# ---------------------------------------------------------------- 图 3-11（PA_Agent 文件14 楔形回撤 vs 楔形反转）
def fig_p3_wedge_contrast():
    """3.8 楔形回撤 vs 楔形反转：顺大势楔形=入场机会，趋势末端楔形=反转预警"""
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.4))
    # 左：上升趋势中的下降楔形回撤（顺大势）
    ax = axes[0]
    k = [(0, 96, 99, 95, 98.4), (1, 98.4, 101, 97.6, 100.4), (2, 100.4, 103, 99.6, 102.2), (3, 102.2, 104, 101.2, 103.4),
         (4, 103.4, 104.2, 101.4, 102.2), (5, 102.2, 103, 100.6, 101.4), (6, 101.4, 102.2, 100, 100.8),  # 推1
         (7, 100.8, 101.8, 99.6, 100.4), (8, 100.4, 101.4, 99.2, 100), (9, 100, 101, 98.6, 99.4),  # 推2
         (10, 99.4, 100.2, 98.2, 99), (11, 99, 100, 98, 98.8), (12, 98.8, 99.6, 97.6, 98.4),  # 推3（最低）
         (13, 98.4, 101.2, 98, 100.6), (14, 100.6, 103.4, 100, 102.8), (15, 102.8, 105.4, 102.2, 105)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.plot([4.6, 11.6], [104.2, 99.8], color=GRAY, ls="--", lw=1.2)
    ax.plot([3.8, 11.8], [103.4, 98.6], color=GRAY, ls=":", lw=1.2)
    mark(ax, 8, 101.2, "下降楔形回撤（10-20棒）\n与主趋势相反 → 顺大势入场机会", color=DOWN, fs=10, box=True)
    mark(ax, 14.2, 107.2, "楔形突破后\n回到原趋势方向", color=UP, fs=10.5, box=True)
    mark(ax, 13, 99.9, "突破线", color=GRAY, fs=8.5)
    style_ax(ax, xlim=(-0.6, 16), ylim=(95, 108.5))
    ax.set_title("① 楔形回撤（Wedge Pullback）：顺势架构 → 突破时顺势入场", fontsize=11.5, color=DARK)
    # 右：上升趋势末端的上升楔形（趋势末端）
    ax = axes[1]
    k = [(0, 96, 99, 95, 98.4), (1, 98.4, 101, 97.6, 100.4), (2, 100.4, 103, 99.6, 102.2), (3, 102.2, 104, 101.2, 103.4),
         (4, 103.4, 105, 102.6, 104.4), (5, 104.4, 106, 103.8, 105.4), (6, 105.4, 106.8, 104.6, 106.2),  # 推1
         (7, 106.2, 107.6, 105.4, 107), (8, 107, 108.4, 106.2, 107.8), (9, 107.8, 109, 106.8, 108.4),  # 推2
         (10, 108.4, 109.6, 107.6, 109), (11, 109, 110.2, 108.2, 109.6), (12, 109.6, 110.6, 108.8, 110),  # 推3
         (13, 110, 111, 108.4, 109.2), (14, 109.2, 110, 106.8, 107.6), (15, 107.6, 108.6, 104.6, 105.4)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.plot([4.6, 11.6], [104.2, 110.2], color=GRAY, ls="--", lw=1.2)
    ax.plot([4.2, 11.4], [103.6, 108.8], color=GRAY, ls=":", lw=1.2)
    mark(ax, 8, 111.6, "上升楔形（≥20棒）\n与主趋势相同 → 反转预警", color=DOWN, fs=10, box=True)
    mark(ax, 14.2, 103, "跌破楔形下边界\n趋势反转", color=DOWN, fs=10.5, box=True)
    mark(ax, 13, 108.6, "破位线", color=GRAY, fs=8.5)
    style_ax(ax, xlim=(-0.6, 16), ylim=(95, 113.5))
    ax.set_title("② 楔形反转（Wedge Reversal）：末端架构 → 破位后警惕反转", fontsize=11.5, color=DARK)
    fig.suptitle("楔形回撤 vs 楔形反转：判断口诀——楔形方向与主趋势相反=回撤，相同=反转（35-40% 楔形会逆突破，须等确认）", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p3_wedge_contrast.png")


# ---------------------------------------------------------------- 图 3-12（PA_Agent 文件19 H1/H2 计数速查）
def fig_p3_h1h2():
    """3.11 H1/H2 计数：强趋势 H1 可用，宽通道/反转/边界必须等 H2"""
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.4))
    # 左：强上升趋势中的 H1 / H2 顺势入场
    ax = axes[0]
    k = [(0, 100, 104, 99, 103.4), (1, 103.4, 106, 102.6, 105.4), (2, 105.4, 108, 104.8, 107.4),
         (3, 107.4, 110, 106.8, 109.4), (4, 109.4, 110.6, 108.2, 108.8), (5, 108.8, 109.4, 107.4, 108.0),  # 第一腿
         (6, 108.0, 110.2, 107.8, 109.8), (7, 109.8, 111.6, 109.4, 111.2), (8, 111.2, 113.0, 110.8, 112.4),
         (9, 112.4, 113.6, 111.6, 112.2), (10, 112.2, 112.8, 110.8, 111.4),  # 第二腿
         (11, 111.4, 113.4, 111.0, 113.0), (12, 113.0, 115.2, 112.6, 114.8), (13, 114.8, 116.4, 114.2, 116.0)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, 4.4, 6.5, 109.4, color=TEAL, lw=1.0)   # 前棒高点：H1 触发线
    hl_line(ax, 9.4, 11.5, 112.8, color=TEAL, lw=1.0)  # 前棒高点：H2 触发线
    annotate_mark(ax, 6, 110.8, "H1 入场：第一腿回撤后\n突破前一棒高点（109.4）", 0.8, 112.6, color=UP, fs=10)
    annotate_mark(ax, 11, 114.2, "H2 入场：第二腿回撤后\n再突破前一棒高点（112.8）", 6.6, 117.8, color=UP, fs=10)
    mark(ax, 5.0, 105.8, "第一腿回撤", color=DOWN, fs=9)
    mark(ax, 9.9, 109.0, "第二腿回撤", color=DOWN, fs=9)
    mark(ax, 3.0, 95.6, "强上升趋势（HH+HL）\n回撤浅（1-2 棒）→ H1 即可入场", color=DARK, fs=9.5, box=True)
    style_ax(ax, xlim=(-0.6, 15.6), ylim=(94, 121))
    ax.set_title("① 强趋势中：H1/H2 都是顺势入场点", fontsize=11.5, color=DARK)
    # 右：宽通道/区间边界中 H1 失败，必须等 H2
    ax = axes[1]
    k = [(0, 96, 99, 95, 98.4), (1, 98.4, 101, 97.6, 100.4), (2, 100.4, 102, 99.6, 101.4),
         (3, 101.4, 102.4, 100.4, 101.2), (4, 101.2, 103.0, 100.8, 102.4),  # H1：突破前棒高点
         (5, 102.4, 102.8, 100.8, 101.4), (6, 101.4, 102.2, 100.2, 100.8), (7, 100.8, 101.8, 99.6, 100.4),
         (8, 100.4, 102.4, 100.0, 101.8), (9, 101.8, 103.8, 101.4, 103.2),  # H2：突破前棒高点
         (10, 103.2, 104.8, 102.8, 104.4), (11, 104.4, 105.6, 103.8, 105.2)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, 3.4, 5.5, 102.4, color=GRAY, lw=1.0)   # H1 触发线：102.4
    hl_line(ax, 8.4, 10.5, 102.4, color=TEAL, lw=1.0)  # H2 触发线：同一价位
    annotate_mark(ax, 4, 103.8, "H1 失败：突破前棒高点\n但无跟随，立刻回落", 0.6, 106.8, color=DOWN, fs=10)
    annotate_mark(ax, 9, 104.6, "H2 入场：第二次测试\n更可靠（二次入场）", 6.4, 108.2, color=UP, fs=10)
    mark(ax, 6.0, 94.4, "宽通道/区间边界：突破前棒高点\n常失败 → 必须等 H2 二次入场", color=DARK, fs=9.5, box=True)
    style_ax(ax, xlim=(-0.6, 12.6), ylim=(93, 111))
    ax.set_title("② 宽通道/区间边界：H1 多失败，必须等 H2", fontsize=11.5, color=DARK)
    fig.suptitle("H1/H2 计数：以“突破前一棒高点”的入场棒为准——强趋势 H1 可用，宽通道/反转/边界必须等 H2，第三次回调（High 3）即楔形", fontsize=12, color=DARK, y=0.99)
    savefig(fig, "fig_p3_h1h2.png")


# ---------------------------------------------------------------- 图 4-7（PA_Agent 文件23 四类 Measured Move）
def fig_p4_mm_four():
    """4.12 四类 Measured Move：区间高度/通道宽度/楔形高度/尖峰腿等距投射"""
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.2))
    # ① 区间高度翻测：突破点 + 区间高 H（约 60% 到达）
    ax = axes[0][0]
    k = [(0, 98, 100.5, 97.5, 100), (1, 100, 101, 98.5, 99.5), (2, 99.5, 102, 99, 101.5), (3, 101.5, 102, 99, 99.8),
         (4, 99.8, 101.8, 98.6, 101.2), (5, 101.2, 102, 98.8, 99.6), (6, 99.6, 103.2, 99.2, 102.8),  # 突破
         (7, 102.8, 105.2, 102.4, 104.8)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.add_patch(Rectangle((0.5, 98), 5.2, 3.7, fill=False, ec=GRAY, lw=1.2, ls="--", zorder=1))
    ax.annotate("", xy=(6.1, 101.7), xytext=(6.1, 98),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.4), zorder=5)
    hl_line(ax, 6.6, 8, 105.4, color=TEAL, lw=1.2)
    mark(ax, 6.15, 99.9, "区间高 H", color=GRAY, fs=9)
    mark(ax, 2.8, 96.6, "区间（上下沿各测 2 次+）", color=DARK, fs=9, box=True)
    annotate_mark(ax, 7, 105.6, "目标 = 突破点 + H\n约 60% 到达", 4.6, 107.6, color=UP, fs=9.5)
    style_ax(ax, xlim=(-0.6, 9), ylim=(95, 110))
    ax.set_title("① 区间高度翻测（约 60%）：目标 = 突破点 + 区间高 H", fontsize=10.5, color=DARK)
    # ② 通道宽度翻测：破位点 − 通道宽 W
    ax = axes[0][1]
    k = [(0, 94.8, 96.3, 94.3, 96), (1, 96, 97.6, 95.6, 97.3), (2, 97.3, 98.9, 96.9, 98.6), (3, 98.6, 100.2, 98.2, 99.9),
         (4, 99.9, 101.5, 99.5, 101.2), (5, 101.2, 102.8, 100.8, 102.5), (6, 102.5, 104.1, 102.1, 103.8),
         (7, 103.8, 105.4, 103.4, 105.1), (8, 105.1, 105.6, 102.8, 103.4),  # 跌破下轨
         (9, 103.4, 103.8, 101.9, 102.2)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.plot([0, 9], [96.5, 107.3], color=GRAY, ls="--", lw=1.2)
    ax.plot([0, 9], [94.5, 105.3], color=GRAY, ls=":", lw=1.2)
    ax.annotate("", xy=(9.5, 106.3), xytext=(9.5, 104.3),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.4), zorder=5)
    hl_line(ax, 8.6, 9.8, 102.1, color=TEAL, lw=1.2)
    mark(ax, 9.7, 105.3, "通道宽 W", color=GRAY, fs=9)
    annotate_mark(ax, 8, 103.6, "跌破下轨\n目标 = 破位点 − W", 5.2, 101.4, color=DOWN, fs=9.5)
    mark(ax, 4, 93.6, "平行通道（上下轨平行）", color=DARK, fs=9, box=True)
    style_ax(ax, xlim=(-0.6, 10.6), ylim=(93, 109.5))
    ax.set_title("② 通道宽度翻测：目标 = 破位点 − 通道宽 W", fontsize=10.5, color=DARK)
    # ③ 楔形高度翻测：破位点 − 楔形高 H
    ax = axes[1][0]
    k = [(0, 99.5, 100.5, 99, 100.2), (1, 100.2, 101.2, 99.8, 100.9), (2, 100.9, 102, 100.5, 101.7),
         (3, 101.7, 102.5, 101.3, 102.2), (4, 102.2, 103.2, 101.8, 102.9), (5, 102.9, 103.8, 102.5, 103.5),
         (6, 103.5, 104.5, 103.1, 104.2), (7, 104.2, 105, 103.8, 104.7), (8, 104.7, 104.9, 101.8, 102.2)]  # 大阴破位
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.plot([0, 7], [99, 103.8], color=GRAY, ls="--", lw=1.2)
    ax.plot([0, 7], [100.2, 104.7], color=GRAY, ls=":", lw=1.2)
    ax.annotate("", xy=(7.6, 103.5), xytext=(7.6, 99.2),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.4), zorder=5)
    hl_line(ax, 8.6, 9.6, 98.2, color=TEAL, lw=1.2)
    mark(ax, 7.8, 101.4, "楔形高 H", color=GRAY, fs=9)
    annotate_mark(ax, 8, 102.6, "破下边界\n目标 = 破位点 − H", 5.4, 99.4, color=DOWN, fs=9.5)
    mark(ax, 4, 97.2, "上升楔形三推（起点→极点）", color=DARK, fs=9, box=True)
    style_ax(ax, xlim=(-0.6, 10.6), ylim=(96, 108))
    ax.set_title("③ 楔形高度翻测：目标 = 破位点 − 楔形高 H（反转方向）", fontsize=10.5, color=DARK)
    # ④ 尖峰 leg 翻测：回撤低点 + L（70%+）
    ax = axes[1][1]
    k = [(0, 97, 98, 96.5, 97.7), (1, 97.7, 99.5, 97.3, 99.2), (2, 99.2, 101, 98.8, 100.7), (3, 100.7, 102.5, 100.3, 102.2),
         (4, 102.2, 103.5, 101.8, 103.2), (5, 103.2, 103.4, 101, 101.6), (6, 101.6, 102.2, 100.4, 101),  # 回撤
         (7, 101, 103, 100.6, 102.6), (8, 102.6, 104.6, 102.2, 104.2), (9, 104.2, 107.4, 103.8, 107)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.annotate("", xy=(0.9, 103.3), xytext=(0.9, 96.7),
                arrowprops=dict(arrowstyle="<->", color=GRAY, lw=1.4), zorder=5)
    hl_line(ax, 9.3, 10.3, 107.4, color=TEAL, lw=1.2)
    mark(ax, 1.1, 100, "尖峰腿长 L", color=GRAY, fs=9)
    annotate_mark(ax, 6, 100.8, "回撤低点", 3.4, 97.6, color=DOWN, fs=9.5)
    annotate_mark(ax, 9, 107.6, "目标 = 回撤低点 + L\n约 70%+ 到达（最可靠）", 6.2, 109.6, color=UP, fs=9.5)
    mark(ax, 2.6, 95.6, "强趋势 leg / 尖峰：起点→终点", color=DARK, fs=9, box=True)
    style_ax(ax, xlim=(-0.6, 11), ylim=(94.5, 111.5))
    ax.set_title("④ 尖峰 leg 翻测（70%+）：目标 = 回撤低点 + L", fontsize=10.5, color=DARK)
    fig.suptitle("四类 Measured Move：目标是算出来的——等距投射（区间高度 / 通道宽度 / 楔形高度 / 尖峰腿），MM 多作 TP2", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p4_mm_four.png")


# ---------------------------------------------------------------- 图 4-8（PA_Agent 文件13 通道量化分类）
def fig_p4_channel_types():
    """4.21 通道量化分类：窄/宽/微型——主判据=最近回撤百分比"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5.6))
    # ① 窄通道：回撤 < 30%，只做顺势
    ax = axes[0]
    k = [(0, 96, 98, 95.8, 97.8), (1, 97.8, 99.8, 97.6, 99.6), (2, 99.6, 101.6, 99.4, 101.4),
         (3, 101.4, 103, 101.2, 102.8), (4, 102.8, 104.6, 102.6, 104.4), (5, 104.4, 105.8, 104, 105.4),
         (6, 105.4, 106.6, 105, 106.2), (7, 106.2, 107.4, 105.8, 107), (8, 107, 108, 106.4, 107.6),
         (9, 107.6, 108.6, 107, 108.2)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.plot([0, 9], [95.8, 107], color=GRAY, ls="--", lw=1.2)
    ax.plot([0, 9], [98, 108.6], color=GRAY, ls=":", lw=1.2)
    mark(ax, 4.5, 94.3, "窄通道：回撤 < 30%，几乎无重叠\n连续趋势棒（>65%），持续 5-20 棒", color=DARK, fs=9, box=True)
    annotate_mark(ax, 9, 109.2, "只做顺势\n第一个逆势突破通常失败", 5.8, 111.2, color=UP, fs=9.5)
    style_ax(ax, xlim=(-0.6, 10.6), ylim=(93.5, 113))
    ax.set_title("① 窄/紧凑通道：回撤 < 30%（本质=尖峰）", fontsize=10.5, color=DARK)
    # ② 宽通道/台阶：回撤 50-78.6%，突破后必有测试
    ax = axes[1]
    k = [(0, 96, 97.5, 95.5, 97), (1, 97, 99, 96.5, 98.6), (2, 98.6, 100.5, 98.2, 100.2),  # 台阶1
         (3, 100.2, 100.8, 98.3, 98.9), (4, 98.9, 99.5, 97.5, 98.1),  # 回撤约 60%
         (5, 98.1, 101, 97.9, 100.8), (6, 100.8, 103.2, 100.6, 103),  # 台阶2
         (7, 103, 103.6, 101.6, 102.2), (8, 102.2, 103, 101.4, 101.9),  # 回撤约 67%
         (9, 101.9, 104, 101.7, 103.8)]  # 台阶3
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    hl_line(ax, 2.4, 4.4, 100.5, color=GRAY, lw=1.0)
    hl_line(ax, 6.4, 8.4, 103.2, color=GRAY, lw=1.0)
    mark(ax, 1.2, 94.2, "台阶1", color=DARK, fs=9)
    mark(ax, 5.4, 94.2, "台阶2", color=DARK, fs=9)
    mark(ax, 9.2, 94.2, "台阶3", color=DARK, fs=9)
    mark(ax, 3.9, 99.9, "回撤 50-78.6%\n（到前高附近）", color=DOWN, fs=8.5)
    annotate_mark(ax, 9, 105, "突破后必有测试\n测试成功=顺势入场", 6.6, 106.6, color=UP, fs=9)
    mark(ax, 2.0, 92.6, "宽通道 = 倾斜交易区间\n仅顺主方向，禁逆势刮头皮", color=DARK, fs=9, box=True)
    style_ax(ax, xlim=(-0.6, 10.6), ylim=(92, 108.5))
    ax.set_title("② 宽通道/台阶：回撤 50-78.6%（锯齿形）", fontsize=10.5, color=DARK)
    # ③ 微型通道：2-10 棒，突破必失败 → 顺势入场
    ax = axes[2]
    k = [(0, 96, 97.2, 95.8, 97), (1, 97, 98.2, 96.8, 98), (2, 98, 99.2, 97.8, 99), (3, 99, 100.2, 98.8, 100),
         (4, 100, 101.2, 99.8, 101),  # 微型通道（5 棒，几乎无回撤）
         (5, 101, 101.4, 99, 99.6),  # 大阴跌破下轨（突破）
         (6, 99.6, 100.4, 99.2, 100.2), (7, 100.2, 101.8, 100, 101.6), (8, 101.6, 103.2, 101.4, 103)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.plot([0, 4], [95.8, 99.8], color=GRAY, ls="--", lw=1.2)
    ax.plot([0, 4], [97.2, 101.2], color=GRAY, ls=":", lw=1.2)
    annotate_mark(ax, 5, 99.8, "突破失败：跌破下轨\n后收回通道内", 1.6, 97.6, color=DOWN, fs=9)
    annotate_mark(ax, 8, 103.8, "顺势入场：回到通道内\n继续原方向", 5.4, 105.4, color=UP, fs=9)
    mark(ax, 2, 94.6, "2-10 棒微型通道\n（几乎无回撤）", color=DARK, fs=9, box=True)
    style_ax(ax, xlim=(-0.6, 9.6), ylim=(93.5, 107.5))
    ax.set_title("③ 微型通道（2-10 棒）：突破通常失败", fontsize=10.5, color=DARK)
    fig.suptitle("通道量化分类：主判据 = 最近回撤百分比（窄 <30% / 常规 30-50% / 宽 50-78.6%）——窄通道只做顺势，宽通道等突破测试，微型通道等突破失败", fontsize=12, color=DARK, y=0.99)
    savefig(fig, "fig_p4_channel_types.png")


# ---------------------------------------------------------------- 图 4-9（PA_Agent 文件20/24 20GB + 最终旗形）
def fig_p4_ff_20gb():
    """4.22 20GB 第一次触 EMA 顺势刮头皮 + 最终旗形突破失败反转"""
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2))
    # 左：20GB——连续约 20 根未触 EMA，第一次回触顺势刮头皮
    ax = axes[0]
    k = [(0, 96.6, 98, 96.4, 97.8), (1, 97.8, 99, 97.6, 98.8), (2, 98.8, 100, 98.6, 99.8), (3, 99.8, 101, 99.6, 100.8),
         (4, 100.8, 102, 100.6, 101.8), (5, 101.8, 102.8, 101.4, 102.6), (6, 102.6, 103.6, 102.2, 103.4),
         (7, 103.4, 104.4, 103, 104.2), (8, 104.2, 104.8, 103.6, 104), (9, 104, 104.6, 102.6, 103.2)]  # 回触 EMA
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.plot([0, 9.5], [95.5, 103.4], color=TEAL, ls="--", lw=1.6)
    mark(ax, 8.4, 105.6, "EMA20（均线）", color=TEAL, fs=9)
    mark(ax, 4.5, 94.8, "连续约 20 根未触 EMA20\n= 趋势极强（均值回归风险上升）", color=DARK, fs=9, box=True)
    annotate_mark(ax, 9, 103, "第一次回触 EMA\n顺势刮头皮", 5.8, 97.2, color=UP, fs=9.5)
    mark(ax, 0.3, 92.6, "两次失败规则：失败两次后不第三次，重新判定市场状态", color=GRAY, fs=8.5)
    style_ax(ax, xlim=(-0.6, 10.6), ylim=(91.5, 107.5))
    ax.set_title("① 20GB：二十根均线缺口——第一次回触顺势刮头皮", fontsize=11, color=DARK)
    # 右：最终旗形——趋势末端整理区突破失败反转
    ax = axes[1]
    k = [(0, 96, 98, 95.6, 97.6), (1, 97.6, 99.6, 97.2, 99.2), (2, 99.2, 101.2, 98.8, 100.8), (3, 100.8, 102.6, 100.4, 102.2),
         (4, 102.2, 103, 101.2, 102.4), (5, 102.4, 103.2, 101.6, 102.2), (6, 102.2, 103, 101.4, 102.8),  # FF 整理区
         (7, 102.8, 103.4, 101.8, 102.2), (8, 102.2, 103, 101.6, 102.8), (9, 102.8, 103.6, 102, 102.4),
         (10, 102.4, 103.2, 101.8, 102.6), (11, 102.6, 104.6, 102.4, 104.2),  # 突破上边界
         (12, 104.2, 104.6, 102, 102.6), (13, 102.6, 103, 100.8, 101.2)]  # 无跟随 → 反转
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.add_patch(Rectangle((3.6, 101.3), 7, 2.35, fill=False, ec=GRAY, lw=1.2, ls="--", zorder=1))
    annotate_mark(ax, 11, 104.8, "突破上边界\n但无跟随", 8.6, 106.6, color=DOWN, fs=9.5)
    annotate_mark(ax, 13, 100.4, "失败 FF = 高价值\n反转 setup（FFES）", 8.4, 98.2, color=DOWN, fs=9.5)
    mark(ax, 7, 104.9, "最终旗形：趋势末端\n10-20+ 棒水平整理", color=DARK, fs=9, box=True)
    mark(ax, 1.6, 94.6, "主趋势（已持续较久）", color=DARK, fs=9)
    style_ax(ax, xlim=(-0.6, 14.6), ylim=(93.5, 108.5))
    ax.set_title("② 最终旗形：趋势末端整理，突破常失败并反转", fontsize=11, color=DARK)
    fig.suptitle("20GB 与最终旗形：二十根不触均线=趋势极强（第一次回触顺势刮头皮，预期测试原趋势极点）；趋势末端旗形突破常失败——失败 FF 是高价值反转", fontsize=12, color=DARK, y=0.99)
    savefig(fig, "fig_p4_ff_20gb.png")


if __name__ == "__main__":
    main()
