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


# ---------------------------------------------------------------- v7：8.12 订单流三件套
import random as _random


def fig_p8_orderflow():
    """8.12 订单流三件套：DOM 静态地图 / 逐笔动态新闻 / Delta 记分牌（合成示意）"""
    _random.seed(11)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16.5, 5.8))
    # ---- 面板 1：DOM 盘口（当前挂单分布，静态） ----
    levels = [99.6, 99.7, 99.8, 99.9, 100.0, 100.1, 100.2, 100.3, 100.4, 100.5]
    qty = [16, 24, 450, 28, 35, 12, 15, 22, 30, 400]  # 下 5 档买单，上 5 档卖单
    y = np.arange(len(levels))
    colors = [UP] * 5 + [DOWN] * 5
    ax1.barh(y, qty, color=colors, alpha=0.85, height=0.62, zorder=3)
    ax1.set_yticks(y)
    ax1.set_yticklabels([f"{v:.1f}" for v in levels], fontsize=8.5)
    ax1.axhline(4.5, color=GRAY, ls="--", lw=0.9)
    ax1.text(8, 4.9, "卖盘（报价 100.1~100.5）", fontsize=9, color=DOWN, va="bottom")
    ax1.text(8, 4.15, "买盘（报价 99.6~100.0）", fontsize=9, color=UP, va="top")
    ax1.annotate("买墙 450：\n真实支撑（吃不完）", xy=(450, 2), xytext=(300, 2.6),
                 fontsize=9.5, color=UP, ha="center", va="bottom",
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.1))
    ax1.annotate("卖墙 400：\n幌骗风险——\n可能瞬间撤单", xy=(400, 9), xytext=(240, 7.2),
                 fontsize=9.5, color=DOWN, ha="center", va="bottom",
                 arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.1))
    ax1.annotate("价差 1 tick", xy=(21, 4.5), xytext=(120, 4.9),
                 fontsize=8.5, color=GRAY, ha="center", va="bottom",
                 arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9))
    ax1.set_xlabel("挂单量（手）", fontsize=10)
    ax1.set_ylim(-0.6, 9.6)
    ax1.set_title("① DOM：静态地图\n“现在谁在挂单”", fontsize=11.5, color=DARK)
    ax1.grid(axis="x", alpha=0.25)
    # ---- 面板 2：逐笔 tape（成交流，动态） ----
    n = 26
    t = np.arange(n)
    base = 100.05
    drift = np.array([0, 0.02, -0.01, 0.03, 0.01, -0.02, 0.04, 0.02, 0.0, -0.03,
                      -0.01, 0.02, 0.03, 0.05, 0.02, 0.0, -0.02, 0.01, 0.04, 0.06,
                      0.03, 0.01, -0.02, 0.05, 0.08, 0.10])
    vol = [12, 30, 8, 45, 15, 22, 60, 18, 25, 10, 14, 38, 52, 20, 9, 16, 40, 12,
           28, 70, 24, 15, 18, 46, 80, 55]
    side = [1, -1, 1, -1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1,
            1, -1, -1, 1, -1, 1]
    for i in range(n):
        c = UP if side[i] > 0 else DOWN
        ax2.scatter(t[i], base + drift[i], s=vol[i] * 2.2, c=c, alpha=0.8,
                    marker="^" if side[i] > 0 else "v", zorder=4, linewidths=0)
    ax2.plot(t, base + drift, color=GRAY, lw=1.0, ls=":", zorder=2)
    ax2.axhline(base, color=GRAY, ls="--", lw=0.9)
    ax2.text(-0.8, base - 0.055, "成交价 100.00", fontsize=8.5, color=GRAY)
    ax2.annotate("主动买：市价单吃卖盘\n（点越大量越大）", xy=(24, base + 0.10), xytext=(13.5, base + 0.13),
                 fontsize=9.5, color=UP, ha="center", va="bottom",
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.1))
    ax2.annotate("主动卖：市价单砸买盘", xy=(6, base + 0.04), xytext=(1.2, base + 0.125),
                 fontsize=9.5, color=DOWN, ha="center", va="bottom",
                 arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.1))
    ax2.text(12.6, base - 0.075, "冰山单陷阱：逐笔只见拆出的碎单\n（大单未必是“大单”）", fontsize=9, color=ORANGE,
             ha="center", va="top", bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=ORANGE, lw=0.8))
    ax2.set_xlim(-1.2, 26.5)
    ax2.set_ylim(base - 0.13, base + 0.155)
    ax2.set_xlabel("时间顺序（一笔一标记）", fontsize=10)
    ax2.set_title("② 逐笔 Time & Sales：动态新闻\n“现在谁在成交”", fontsize=11.5, color=DARK)
    ax2.grid(alpha=0.25)
    # ---- 面板 3：Delta 柱（主动买 − 主动卖，累积） ----
    x = np.arange(40)
    # 震荡段(0-12) → 突破但 delta 萎缩(13-18) → 回踩缩量(19-27) → 反弹放量(28-39)
    delta = np.concatenate([
        np.array([8, -12, 15, -20, 6, -8, 10, -5, -14, 9, 7, -11, 4]),
        np.array([18, 14, 9, 5, -2, -6]),
        np.array([-8, -11, -6, -13, -5, -9, -7, -4, -10]),
        np.array([22, 30, 18, 26, 42, 34, 50, 38, 28, 35, 24, 30])])
    ax3.bar(x, delta, color=[UP if d >= 0 else DOWN for d in delta], alpha=0.85, width=0.8)
    ax3.axhline(0, color=GRAY, lw=1.0)
    ax3.axvspan(12.5, 18.5, color=ORANGE, alpha=0.12)
    ax3.axvspan(27.5, 40, color=UP, alpha=0.08)
    ax3.annotate("突破前高，但 delta 不跟进\n（买卖差不放大）→ 假突破", xy=(15, 14), xytext=(15.5, 34),
                 fontsize=9, color=ORANGE, ha="center", va="bottom",
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1))
    ax3.annotate("回踩：负 delta 缩量\n（无人恐慌）", xy=(23, -7), xytext=(23, -34),
                 fontsize=9, color=GRAY, ha="center", va="top",
                 arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
    ax3.annotate("反弹：正 delta 放大\n（真金白银推）→ 趋势健康", xy=(33, 35), xytext=(26.5, 56),
                 fontsize=9, color=UP, ha="center", va="bottom",
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.1))
    ax3.text(6, 44, "震荡：多空拉锯\n净 delta 来回摆", fontsize=9, color=GRAY, ha="center")
    ax3.set_xlabel("时间（按 K 线累计）", fontsize=10)
    ax3.set_ylabel("Delta（主动买 − 主动卖）", fontsize=10)
    ax3.set_xlim(-1, 40)
    ax3.set_ylim(-48, 62)
    ax3.set_title("③ Delta：记分牌\n“净方向压力”", fontsize=11.5, color=DARK)
    ax3.grid(axis="y", alpha=0.25)
    fig.subplots_adjust(wspace=0.24, left=0.055, right=0.975, top=0.78, bottom=0.13)
    fig.suptitle("订单流三件套（合成示意）：DOM 是静态地图、逐笔是动态新闻、Delta 是记分牌\n互证规则：三者共振才信——只有大墙（可能幌骗）或只有 delta（单根噪音）都不下结论",
                 fontsize=12.5, color=DARK)
    savefig(fig, "fig_p8_orderflow.png")


# ---------------------------------------------------------------- v7：5.12 Volume Profile


def fig_p5_volume_profile():
    """5.12 Volume Profile：成交量按价格轴横向分布——POC/VA/HVN/LVN 一图看懂"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 6.3), gridspec_kw={"width_ratios": [1.15, 1]})
    # 左：K 线路径（横盘堆积 → 突破快速通过 → 新高再堆积）
    k = [(0, 99.5, 100.5, 98.5, 100.0), (1, 100.0, 101.0, 99.0, 99.5), (2, 99.5, 100.5, 99.0, 100.0),
         (3, 100.0, 101.5, 99.5, 101.0), (4, 101.0, 101.5, 99.0, 99.5), (5, 99.5, 100.5, 99.0, 100.0),
         (6, 100.0, 101.0, 99.5, 100.5), (7, 100.5, 102.0, 100.0, 101.5), (8, 101.5, 102.0, 99.5, 100.0),
         (9, 100.0, 101.0, 99.0, 99.5), (10, 99.5, 100.5, 99.0, 100.0),
         (11, 100.0, 102.5, 99.5, 102.0), (12, 102.0, 104.5, 101.5, 104.0),
         (13, 104.0, 106.0, 103.5, 105.5), (14, 105.5, 107.5, 105.0, 107.0)]
    for x, o, h, l, c in k:
        candle(ax1, x, o, h, l, c, width=0.6)
    ax1.add_patch(Rectangle((-0.5, 98.2), 11, 4.1, facecolor=GRAY, alpha=0.10, zorder=1))
    ax1.text(5, 103.0, "横盘区间：量在下方堆积（VA）", fontsize=10, color=DARK, ha="center")
    ax1.annotate("突破 VA 上沿 → 按趋势思维", xy=(12, 102.3), xytext=(8.6, 105.6),
                 fontsize=10, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.1))
    ax1.annotate("穿过 LVN 快速通过区：\n成交量稀薄，别挂单等回踩", xy=(12.7, 104.3), xytext=(11.9, 97.3),
                 fontsize=9.5, color=ORANGE, va="top", ha="center",
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1))
    ax1.annotate("新高处新堆积（HVN）\n成为新支撑", xy=(14, 107.3), xytext=(10.8, 109.3),
                 fontsize=9.5, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1))
    ax1.set_xlabel("时间（K 线）", fontsize=10.5)
    ax1.set_ylabel("价格", fontsize=10.5)
    ax1.set_xlim(-0.8, 15.3)
    ax1.set_ylim(96.5, 110.8)
    ax1.grid(alpha=0.3)
    ax1.set_title("价格路径：横盘堆积 → 突破快速通过 → 新高再堆积", fontsize=11.5, color=DARK)
    # 右：Volume Profile 横向直方图（量按价格分布）
    prices = np.arange(98.0, 107.75, 0.5)
    vol = [12, 25, 40, 58, 85, 60, 44, 28, 15, 6, 4, 3, 3, 5, 8, 14, 22, 18, 12, 8]
    yp = np.arange(len(prices))
    colors = []
    for p in prices:
        if 98.5 <= p <= 101.5:
            colors.append(UP)
        elif 102.5 <= p <= 105.0:
            colors.append(ORANGE)
        elif p >= 106.0:
            colors.append(TEAL)
        else:
            colors.append(GRAY)
    ax2.barh(yp, vol, color=colors, alpha=0.85, height=0.72)
    ax2.set_yticks(yp)
    ax2.set_yticklabels([f"{p:.1f}" for p in prices], fontsize=8.5)
    ax2.axhline(yp[4], color=DARK, ls="--", lw=1.2)  # POC = 100.0
    ax2.axhspan(yp[1] - 0.4, yp[7] + 0.4, color=UP, alpha=0.06)  # VA 98.5-101.5
    ax2.annotate("POC 100.0：量最大\n= 市场重心（磁铁 + 支撑阻力）", xy=(85, yp[4]), xytext=(98, yp[4] + 3.4),
                 fontsize=9.5, color=DARK, va="center", ha="left",
                 arrowprops=dict(arrowstyle="->", color=DARK, lw=1.1))
    ax2.annotate("价值区间 VA：70% 成交量\n（VAL 98.5 / VAH 101.5）", xy=(60, yp[7]), xytext=(88, yp[7] + 4.2),
                 fontsize=9.5, color=UP, va="center", ha="left",
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.1))
    ax2.annotate("LVN 低量节点：快速通过区\n（102.5-105.0 量稀薄）", xy=(6, yp[9]), xytext=(20, yp[14]),
                 fontsize=9.5, color=ORANGE, va="center", ha="left",
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1))
    ax2.annotate("HVN 高量节点：\n突破后新堆积 = 新支撑", xy=(18, yp[17]), xytext=(30, yp[17]),
                 fontsize=9.5, color=TEAL, va="center", ha="left",
                 arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1))
    ax2.set_xlim(0, 160)
    ax2.set_ylim(-0.8, len(prices) - 0.2)
    ax2.set_xlabel("成交量（横向分布）", fontsize=10.5)
    ax2.set_title("Volume Profile：量按价格横向分布\n（POC 重心 / VA 价值区 / LVN 快车道 / HVN 支撑阻力）",
                  fontsize=11.5, color=DARK)
    ax2.grid(axis="x", alpha=0.25)
    fig.subplots_adjust(wspace=0.22, left=0.05, right=0.975, top=0.88, bottom=0.1)
    savefig(fig, "fig_p5_volume_profile.png")


# ---------------------------------------------------------------- v7：8.11 足迹图

def fig_p8_footprint():
    """8.11 足迹图：每根 K 线的成交量按价格档拆开（左买右卖），失衡档高亮"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 6.2), gridspec_kw={"width_ratios": [1.18, 1]})
    # 左：足迹图本体（一根大阳 K 线，档位数字 左买右卖）
    style_ax(ax1, xlim=(0, 12.5), ylim=(99.75, 101.25))
    candle(ax1, 6.2, 100.0, 101.0, 99.9, 100.8, width=2.6)
    ax1.plot([6.2, 6.2], [99.9, 101.0], color=GRAY, lw=0.7, alpha=0.5)
    rows = [  # (价格, 买量, 卖量)
        (101.0, 3, 12), (100.8, 8, 4), (100.7, 12, 5), (100.6, 22, 6), (100.5, 15, 8),
        (100.4, 60, 10), (100.3, 18, 20), (100.2, 25, 12), (100.1, 42, 15), (100.0, 30, 18),
        (99.9, 5, 25)]
    for p, b, a in rows:
        ax1.text(5.15, p, str(b), fontsize=8, color=UP, ha="right", va="center")
        ax1.text(7.25, p, str(a), fontsize=8, color=DOWN, ha="left", va="center")
        ax1.text(6.2, p, f"{p:.1f}", fontsize=7.5, color=GRAY, ha="center", va="center")
    ax1.add_patch(Rectangle((4.95, 100.35), 2.5, 0.1, facecolor=ORANGE, alpha=0.28, edgecolor=ORANGE, lw=0.7))
    ax1.annotate("失衡：买 60 vs 卖 10\n单边吃单 → 快速通过区\n价格倾向回填（呼应 5.6 FVG）",
                 xy=(6.2, 100.4), xytext=(8.8, 100.55),
                 fontsize=9.5, color=ORANGE, va="center", ha="left",
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1))
    ax1.annotate("上影档：卖量 12 压顶\n上攻受阻信号", xy=(6.2, 101.0), xytext=(8.4, 101.1),
                 fontsize=9, color=DOWN, va="center", ha="left",
                 arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax1.text(0.2, 101.18, "足迹图：每根 K 线的成交量按价格档拆开\n左 = 主动买量，右 = 主动卖量（合成示意）",
             fontsize=9.5, color=DARK, va="top")
    # 右：三种读法小结
    style_ax(ax2, xlim=(0, 10.5), ylim=(0, 8.2))
    draw_box(ax2, 0.6, 6.1, 9.3, 1.6, "① 失衡：某档量远大于相邻档\n（买/卖严重一边倒）→ 快速通过区，倾向回填", ec=ORANGE, fs=9.5)
    draw_box(ax2, 0.6, 3.8, 9.3, 1.6, "② 变盘模式：趋势中大量成交但价格不继续\n= 努力无结果 → 反转警告（呼应 5.10）", ec=DOWN, fs=9.5)
    draw_box(ax2, 0.6, 1.5, 9.3, 1.6, "③ 延续模式：快速通过时清淡 + 回踩时放量\n→ 趋势健康，继续（呼应 8.4 三件套互证）", ec=UP, fs=9.5)
    mark(ax2, 5.25, 0.55, "与图 8-4 互证：足迹失衡 ≈ 单根 delta 大幅转正；\n变盘 ≈ delta 衰竭——同一个过程的两套读数", fs=9, color=GRAY, ha="center")
    fig.subplots_adjust(wspace=0.14, left=0.045, right=0.98, top=0.9, bottom=0.09)
    fig.suptitle("足迹图：把每根 K 线的量按价格档拆开（左买右卖）——失衡、变盘、延续三种读法",
                 fontsize=12.5, color=DARK)
    savefig(fig, "fig_p8_footprint.png")


# ---------------------------------------------------------------- v7：4.26 ORB 开盘区间突破

def fig_p4_orb():
    """4.26 ORB：开盘区间 + 收盘突破 + 回测不破 + 顺势走高（六要素图形化）"""
    fig, ax = plt.subplots(figsize=(13.5, 6.6))
    k = [(0, 100.5, 101.5, 99.5, 101.0), (1, 101.0, 101.8, 100.2, 100.5), (2, 100.5, 102.0, 100.0, 101.8),
         (3, 101.8, 103.0, 101.5, 102.8), (4, 102.8, 103.5, 102.2, 103.2),
         (5, 103.2, 103.8, 102.1, 102.2), (6, 102.2, 103.5, 102.1, 103.3),
         (7, 103.3, 104.5, 103.0, 104.2), (8, 104.2, 105.0, 103.8, 104.8), (9, 104.8, 106.0, 104.5, 105.8),
         (10, 105.8, 106.5, 105.5, 106.3), (11, 106.3, 107.0, 106.0, 106.8)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c, width=0.6)
    orb_hi, orb_lo = 102.0, 99.5
    ax.add_patch(Rectangle((-0.55, orb_lo), 3.6, orb_hi - orb_lo, facecolor=GRAY, alpha=0.14, zorder=1))
    hl_line(ax, -0.6, 12.4, orb_hi, color=GRAY, ls=":", lw=1.2)
    hl_line(ax, -0.6, 12.4, orb_lo, color=GRAY, ls=":", lw=1.2)
    ax.text(12.2, orb_hi, "ORB 上沿 102.0", fontsize=9.5, color=GRAY, va="bottom", ha="right")
    ax.text(12.2, orb_lo, "ORB 下沿 99.5", fontsize=9.5, color=GRAY, va="bottom", ha="right")
    mark(ax, 1, 103.4, "开盘区间 ORB：\n前 N 根 K 线的高低点\n（N = 5/15/30 分钟）", fs=9.5, color=DARK, va="bottom")
    ax.annotate("收盘突破上沿 → 顺势入场\n（等收盘确认，别追盘中插针）", xy=(3.5, 102.6), xytext=(2.0, 107.6),
                fontsize=9.5, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.1))
    ax.annotate("回测上沿不破 = 高质量二次入场\n（突破→测试结构的时间版本）", xy=(5.5, 102.2), xytext=(6.6, 108.8),
                fontsize=9.5, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1))
    ax.annotate("止损 = 对侧边界外 1 tick\n（≈99.4，窄 ORB 止损紧凑）", xy=(3.5, 99.5), xytext=(7.0, 97.3),
                fontsize=9.5, color=DOWN, va="top", ha="center",
                arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.1))
    ax.annotate("趋势日：移动止损吃全天\n（呼应 4.15）", xy=(10, 106.5), xytext=(8.6, 109.8),
                fontsize=9.5, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1))
    ax.set_xlabel("时间（开盘后 K 线）", fontsize=11)
    ax.set_ylabel("价格", fontsize=11)
    ax.set_xlim(-1.1, 13.2)
    ax.set_ylim(96.2, 111.5)
    ax.grid(alpha=0.3)
    ax.set_title("ORB：开盘区间 = 隔夜信息定价战场——收盘突破、回测不破、趋势日单边（合成示意）",
                 fontsize=12, color=DARK)
    savefig(fig, "fig_p4_orb.png")


# ---------------------------------------------------------------- v7：10.6 期权四策略损益

def fig_opt_strategies():
    """10.6 四策略到期损益：保护性 Put / 备兑 Call / 牛市价差 / 跨式（ES 例子）"""
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.6))
    s = np.linspace(4940, 5210, 300)
    S0, K, K2 = 5050, 5050, 5150
    # ① 保护性 Put：多单 + 买 Put（prem 30）
    pnl = (s - S0) + (np.maximum(K - s, 0) - 30)
    ax = axes[0][0]
    ax.plot(s, s - S0, color=UP, lw=1.4, alpha=0.5, ls="--", label="持有标的")
    ax.plot(s, pnl, color=DARK, lw=2.4, label="+ 保护性 Put")
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.annotate("暴跌时 Put 补损：\n最大回吐锁在保费 30", xy=(4980, -30), xytext=(4948, -85),
                fontsize=9, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax.annotate("上涨照常盈利\n（趋势继续拿）", xy=(5180, 130), xytext=(5100, 175),
                fontsize=9, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax.set_title("① 保护性 Put：给浮盈多单买保险", fontsize=11.5, color=DARK)
    ax.legend(fontsize=8.5, loc="lower right")
    # ② 备兑 Call：多单 + 卖虚值 Call（收 15）
    pnl = (s - S0) - (np.maximum(s - K2, 0) - 15)
    ax = axes[0][1]
    ax.plot(s, s - S0, color=UP, lw=1.4, alpha=0.5, ls="--", label="持有标的")
    ax.plot(s, pnl, color=DARK, lw=2.4, label="+ 卖出虚值 Call")
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.axvline(K2, color=GRAY, ls=":", lw=1.0)
    ax.text(K2 + 3, -90, "行权价 5150", fontsize=8.5, color=GRAY)
    ax.annotate("震荡期白收权利金 15\n（租金）", xy=(5050, 15), xytext=(5070, 60),
                fontsize=9, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax.annotate("大涨被行权：\n盈利封顶 115（少赚不亏）", xy=(5170, 115), xytext=(5100, 150),
                fontsize=9, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    ax.set_title("② 备兑 Call：震荡期收租金", fontsize=11.5, color=DARK)
    ax.legend(fontsize=8.5, loc="lower right")
    # ③ 牛市价差：买 5050 Call(30) + 卖 5150 Call(收15)
    pnl = np.maximum(s - K, 0) - 30 - (np.maximum(s - K2, 0) - 15)
    ax = axes[1][0]
    ax.plot(s, pnl, color=DARK, lw=2.4)
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.axvline(K, color=GRAY, ls=":", lw=1.0)
    ax.axvline(K2, color=GRAY, ls=":", lw=1.0)
    ax.annotate("最大亏损 = 净成本 15\n（下单即物理锁死）", xy=(4980, -15), xytext=(4948, -75),
                fontsize=9, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax.annotate("最大盈利封顶 85\n（我不赌超过 5150 的部分）", xy=(5170, 85), xytext=(5060, 140),
                fontsize=9, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax.set_title("③ 牛市价差：定义风险的方向交易", fontsize=11.5, color=DARK)
    # ④ 跨式：买 Call + 买 Put（各 25）
    pnl = np.maximum(s - K, 0) + np.maximum(K - s, 0) - 50
    ax = axes[1][1]
    ax.plot(s, pnl, color=DARK, lw=2.4)
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.annotate("最大亏损 = 双权利金 50\n（唯一风险是波动不够）", xy=(5050, -50), xytext=(4955, -85),
                fontsize=9, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax.annotate("大波动即盈利\n（涨跌都行）", xy=(5190, 90), xytext=(5100, 175),
                fontsize=9, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax.text(4960, 160, "坑：事件前 IV 已被抬高，\n事件后 IV crush 两边一起贬值", fontsize=9, color=ORANGE, va="top")
    ax.set_title("④ 跨式：赌大波动，不赌方向", fontsize=11.5, color=DARK)
    for ax in axes.flat:
        ax.set_xlabel("到期时 ES 价格")
        ax.set_ylabel("盈亏（点）")
        ax.set_ylim(-110, 210)
        ax.grid(alpha=0.25)
    fig.subplots_adjust(wspace=0.2, hspace=0.3, left=0.055, right=0.98, top=0.9, bottom=0.07)
    fig.suptitle("四种策略 = 四种“你想干什么”：对冲 / 收租 / 方向 / 波动——损益形状一看就懂（ES 例子）",
                 fontsize=12.5, color=DARK)
    savefig(fig, "fig_p10_strategies.png")


# ---------------------------------------------------------------- v7：1.17 资产配置两条腿

def fig_p1_asset_allocation():
    """1.17 资产配置：总资产分两条腿（交易/配置）+ 配置账户 60/40 再平衡"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.6))
    # 左：总资产分层
    segs1 = [(0, 15, UP, "交易账户 15%\n进攻：小资金、高纪律、正期望值\n亏光不影响生活（≤10-20%）"),
             (15, 100, DARK, "配置账户 85%\n防守：指数基金为主、不盯盘\n长期复利 = “输得起”的底气")]
    for x0, x1, c, lab in segs1:
        ax1.barh(0, x1 - x0, left=x0, color=c, height=0.62, alpha=0.9)
        if c == UP:
            ax1.text(x0 + 7.5, 0.12, lab.split("\n")[0], fontsize=11, color="white", ha="center", va="center", fontweight="bold")
            ax1.text(x0 + 7.5, -0.30, "\n".join(lab.split("\n")[1:]), fontsize=8.5, color=DARK, ha="center", va="top")
        else:
            ax1.text(x0 + (x1 - x0) / 2, 0.12, lab.split("\n")[0], fontsize=11, color="white", ha="center", va="center", fontweight="bold")
            ax1.text(x0 + (x1 - x0) / 2, -0.30, "\n".join(lab.split("\n")[1:]), fontsize=8.5, color=DARK, ha="center", va="top")
    ax1.axvline(15, color="white", lw=2.0)
    ax1.set_xlim(-4, 104)
    ax1.set_ylim(-1.1, 1.0)
    ax1.set_xticks([0, 15, 50, 85, 100])
    ax1.set_xticklabels(["0%", "15%", "50%", "85%", "100%"], fontsize=9)
    ax1.set_yticks([])
    ax1.set_xlabel("总资产（百分比）", fontsize=10.5)
    for s in ax1.spines.values():
        s.set_visible(False)
    ax1.set_title("两条腿：交易账户进攻，配置账户防守", fontsize=12, color=DARK)
    # 右：配置账户内部 60/40
    segs2 = [(0, 60, TEAL, "60% 股票指数基金\n（沪深 300 等）\n长期增长引擎"),
             (60, 90, ORANGE, "30% 债券/货币基金\n压舱石\n（回撤缓冲）"),
             (90, 100, GRAY, "10% 现金\n应急缓冲")]
    for x0, x1, c, lab in segs2:
        ax2.barh(0, x1 - x0, left=x0, color=c, height=0.62, alpha=0.9)
        ax2.text(x0 + (x1 - x0) / 2, 0.12, lab.split("\n")[0], fontsize=10, color="white",
                 ha="center", va="center", fontweight="bold")
        ax2.text(x0 + (x1 - x0) / 2, -0.30, "\n".join(lab.split("\n")[1:]), fontsize=8.5,
                 color=DARK, ha="center", va="top")
    ax2.set_xlim(-4, 104)
    ax2.set_ylim(-1.5, 1.35)
    ax2.set_xticks([0, 60, 90, 100])
    ax2.set_xticklabels(["0%", "60%", "90%", "100%"], fontsize=9)
    ax2.set_yticks([])
    ax2.set_xlabel("配置账户内部（百分比）", fontsize=10.5)
    for s in ax2.spines.values():
        s.set_visible(False)
    ax2.annotate("60/40 再平衡：每 1-2 年调回比例\n（卖涨的、买跌的）——强制低买高卖",
                 xy=(30, 0.4), xytext=(12, 1.25),
                 fontsize=9.5, color=DARK, va="center", ha="center",
                 arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
    ax2.set_title("配置账户内部：60/40 再平衡（编者示例比例）", fontsize=12, color=DARK)
    fig.subplots_adjust(wspace=0.3, left=0.04, right=0.985, top=0.85, bottom=0.14)
    fig.suptitle("资产配置：先保证“输得起”，再谈“赢”——交易账户只是资产的一小部分",
                 fontsize=12.5, color=DARK)
    savefig(fig, "fig_p1_asset_allocation.png")


# ---------------------------------------------------------------- v7：3.8 蜡烛组合形态

def fig_p3_combo_bars():
    """3.8 蜡烛组合形态：启明星/黄昏星、红三兵/三乌鸦、平头顶/底（2x3 镜像对照）"""
    fig, axes = plt.subplots(2, 3, figsize=(14.5, 8.8))
    panels = [
        (axes[0][0], "启明星（看涨）",
         [(0, 103, 103.5, 101, 101.2), (1, 101.5, 102.0, 100.8, 101.3), (2, 101.0, 103.5, 100.8, 103.2)],
         [("① 大阴：空头主导", 0, 104.2), ("② 星：犹豫（实体越小越干净）", 1, 98.8), ("③ 大阳吞没过半 → 看涨", 2, 104.2)]),
        (axes[0][1], "黄昏星（看跌）",
         [(0, 101, 103, 100.5, 102.8), (1, 102.5, 103.0, 101.8, 102.2), (2, 102.5, 103.0, 100.5, 100.8)],
         [("① 大阳：多头主导", 0, 103.8), ("② 星：犹豫", 1, 101.8), ("③ 大阴吞没过半 → 看跌", 2, 99.8)]),
        (axes[0][2], "平头顶部（两次拒绝）",
         [(0, 101, 104.5, 100.5, 103.5), (1, 103.2, 104.5, 101.5, 102.0)],
         [("两高点几乎等高\n= 同一价位两次被拒\n阻力确认 → 看跌", 0.5, 105.6)]),
        (axes[1][0], "红三兵（启动）",
         [(0, 100, 101.5, 99.5, 101.2), (1, 101.0, 102.5, 100.8, 102.2), (2, 102.0, 103.5, 101.8, 103.2)],
         [("低位三连阳：每根开盘在前实体、收盘近高\n→ 趋势启动（高位出现警惕最后一冲）", 1, 98.6)]),
        (axes[1][1], "三乌鸦（下跌启动）",
         [(0, 104, 104.2, 102.5, 102.8), (1, 103.0, 103.2, 101.5, 101.8), (2, 102.0, 102.2, 100.5, 100.8)],
         [("镜像：三连阴逐级走低 → 下跌启动", 1, 104.6)]),
        (axes[1][2], "平头底部（支撑确认）",
         [(0, 103, 104.0, 99.5, 100.5), (1, 100.8, 103.0, 99.5, 102.5)],
         [("两低点几乎等高\n= 同一价位两次获撑\n支撑确认 → 看涨", 0.5, 98.9)]),
    ]
    for ax, title, k, annos in panels:
        for x, o, h, l, c in k:
            candle(ax, x, o, h, l, c, width=0.55)
        if title.startswith("平头顶") or title.startswith("平头底"):
            hi = max(h for _, _, h, _, _ in k)
            lo = min(l for _, _, _, l, _ in k)
            hl_line(ax, -0.4, len(k) - 0.6, hi if title.startswith("平头顶") else lo,
                    color=GRAY, ls=":", lw=1.2)
        for txt, x, y in annos:
            mark(ax, x, y, txt, fs=9, color=DARK, ha="center")
        ax.set_xlim(-0.6, len(k) - 0.4)
        ax.set_ylim(97.8, 106.4)
        ax.set_title(title, fontsize=11.5, color=DARK)
        ax.grid(alpha=0.25)
    fig.subplots_adjust(wspace=0.28, hspace=0.42, left=0.04, right=0.985, top=0.88, bottom=0.07)
    fig.suptitle("蜡烛组合形态：多根 K 线“合谋”——启明星/红三兵/平头都要有位置和背景（呼应 4.2 信号质量）",
                 fontsize=12.5, color=DARK)
    savefig(fig, "fig_p3_combo_bars.png")


# ---------------------------------------------------------------- v7：3.9 MTR 统一框架

def fig_p3_mtr():
    """3.9 反转形态统一框架：头肩顶 = HH MTR + LH MTR；双顶熊旗（Ali 细节）；MTR 四组件"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17.5, 6.4), gridspec_kw={"width_ratios": [1.25, 1.25, 1]})
    # 面板 A：头肩顶 = MTR 拼图
    k = [(0, 100, 102, 99.5, 101.5), (1, 101.5, 103, 101, 102.5), (2, 102.5, 104.5, 102, 104),
         (3, 104, 106, 103.5, 105.5), (4, 105.5, 107, 102, 102.5), (5, 102.5, 108, 102, 107.5),
         (6, 107.5, 109, 106, 106.5), (7, 106.5, 110.5, 106, 110), (8, 110, 111, 102.5, 103),
         (9, 103, 104, 102.5, 103.5), (10, 103.5, 106, 103, 105.5), (11, 105.5, 107.5, 105, 106),
         (12, 106, 107, 104.5, 105), (13, 105, 105.5, 101.5, 102)]
    for x, o, h, l, c in k:
        candle(ax1, x, o, h, l, c, width=0.55)
    ax1.plot([4, 10], [102, 102.4], color=GRAY, ls="--", lw=1.3, zorder=2)  # 颈线
    ax1.annotate("左肩：HH MTR\n（多头没能延续）", xy=(5, 108.2), xytext=(1.2, 109.8),
                 fontsize=9, color=TEAL, ha="center", arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.0))
    ax1.annotate("头：更高高点\n（最强冲击）", xy=(8, 111.2), xytext=(7.6, 114.6),
                 fontsize=9, color=DARK, ha="center", arrowprops=dict(arrowstyle="->", color=DARK, lw=1.0))
    ax1.annotate("右肩：LH\n多头没创新高 = 弱势\n（三次冲击一次比一次弱）", xy=(11, 107.7), xytext=(10.4, 114.6),
                 fontsize=9, color=ORANGE, ha="center", arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    ax1.annotate("跌破颈线 + 放量 → 确认\n目标 = 头高投射", xy=(13, 101.6), xytext=(10.6, 99.6),
                 fontsize=9, color=DOWN, va="top", arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax1.set_title("① 头肩顶 = HH MTR + LH MTR\n（所有反转都是双顶/双底变体）", fontsize=11, color=DARK)
    # 面板 B：双顶熊旗（Ali 细节）
    k = [(0, 100, 102, 99.5, 101.5), (1, 101.5, 104, 101, 103.5), (2, 103.5, 106, 103, 105.5),
         (3, 105.5, 109, 105, 108.5), (4, 108.5, 110, 106, 106.5), (5, 106.5, 108, 105.5, 107),
         (6, 107, 109.5, 106, 108.5), (7, 108.5, 110, 107.5, 108), (8, 108, 108.5, 105, 105.5),
         (9, 105.5, 106, 103.5, 104), (10, 104, 106.5, 103.5, 105.5), (11, 105.5, 106, 101, 101.5)]
    for x, o, h, l, c in k:
        candle(ax2, x, o, h, l, c, width=0.55)
    ax2.plot([-0.5, 11.5], [105, 105], color=GRAY, ls="--", lw=1.3, zorder=2)  # 颈线
    ax2.annotate("顶① / 顶② 几乎等高\n（Ali：第二顶 = 相同或更低，不是更高）", xy=(7, 110.2), xytext=(3.2, 112.6),
                 fontsize=9, color=DARK, ha="center", arrowprops=dict(arrowstyle="->", color=DARK, lw=1.0))
    ax2.annotate("跌破前先出现隐含低点 103.5\n→ 颈线破位等低点确认，别提前抢空", xy=(9, 103.9), xytext=(8.2, 99.8),
                 fontsize=9, color=ORANGE, va="top", ha="center",
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    ax2.annotate("反抽颈线后真跌破 → 确认\n（目标 = 顶高投射）", xy=(11, 101.2), xytext=(8.4, 97.0),
                 fontsize=9, color=DOWN, va="top", ha="center",
                 arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax2.set_title("② 双顶熊旗（Ali）：跌破前先有隐含低点", fontsize=11, color=DARK)
    # 面板 C：MTR 四组件
    style_ax(ax3, xlim=(0, 10.5), ylim=(0, 10.4))
    draw_box(ax3, 0.4, 8.3, 9.7, 1.5, "① 原趋势存在\nHTF 清晰 HH+HL / LL+LH 序列", ec=TEAL, fs=9)
    draw_box(ax3, 0.4, 6.0, 9.7, 1.5, "② 趋势线/通道突破\n收盘突破，不是单根毛刺", ec=TEAL, fs=9)
    draw_box(ax3, 0.4, 3.7, 9.7, 1.5, "③ 趋势恢复失败\n无强跟随、未创新高/新低", ec=ORANGE, fs=9)
    draw_box(ax3, 0.4, 1.4, 9.7, 1.5, "④ 前极点测试失败\n无法超越前高/前低 → 双顶底/更低高", ec=ORANGE, fs=9)
    mark(ax3, 5.25, 0.55, "四组件缺一不可——单根反转棒只是“反转尝试”\n完整 MTR 首次成功率 35-40%：优先等 H2/L2 二次入场", fs=8.5, color=GRAY, ha="center")
    ax3.set_title("③ MTR 四组件（缺一不可）", fontsize=11, color=DARK)
    for ax in (ax1, ax2):
        ax.set_xlim(-0.7, len(k) if ax is ax2 else 13.8)
        ax.set_ylim(95.5, 116.5)
        ax.grid(alpha=0.3)
    fig.subplots_adjust(wspace=0.3, left=0.035, right=0.985, top=0.88, bottom=0.08)
    fig.suptitle("反转形态的统一框架（Brooks + Ali）：头肩 = HH MTR + LH MTR，双顶 = 两次冲击同一阻力\nMTR 四组件齐了才是反转，否则只是反转尝试",
                 fontsize=12.5, color=DARK)
    savefig(fig, "fig_p3_mtr.png")


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


# ---------------------------------------------------------------- v4：10.4 希腊字母 Delta/Gamma
import math as _math


def _norm_cdf(x):
    return 0.5 * (1 + _math.erf(x / _math.sqrt(2)))


def _norm_pdf(x):
    return _math.exp(-x * x / 2) / _math.sqrt(2 * _math.pi)


def fig_greek_curves():
    """10.4 希腊字母直觉：Call Delta 的 S 曲线 + Gamma 钟形（平值附近最剧烈）"""
    K, sigma, T = 100.0, 0.30, 30.0 / 365.0
    s = np.linspace(80, 120, 300)
    d1 = (np.log(s / K) + 0.5 * sigma * sigma * T) / (sigma * _math.sqrt(T))
    delta = np.array([_norm_cdf(x) for x in d1])
    gamma = np.array([_norm_pdf(x) for x in d1]) / (s * sigma * _math.sqrt(T))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.4))
    # 左：Delta S 曲线
    ax1.plot(s, delta, color=TEAL, lw=2.4)
    ax1.axhline(0.5, color=GRAY, ls=":", lw=1.0)
    ax1.axvline(K, color=GRAY, ls=":", lw=1.0)
    ax1.annotate("平值：Delta ≈ 0.5\n（约等于持有半单位标的）", xy=(K, 0.5), xytext=(86, 0.62),
                 fontsize=9.5, color=DARK, arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
    ax1.annotate("深度实值：Delta → 1\n（越来越像直接持有标的）", xy=(118, delta[-1]), xytext=(108, 0.82),
                 fontsize=9.5, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.0))
    ax1.annotate("深度虚值：Delta → 0\n（方向几乎不影响它）", xy=(82, delta[0]), xytext=(83, 0.16),
                 fontsize=9.5, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.0))
    ax1.set_title("Delta：我的方向敞口有多大\n——标的每动 1 点，期权动多少", fontsize=12, color=DARK)
    ax1.set_xlabel("标的价格")
    ax1.set_ylabel("Delta")
    ax1.set_xlim(80, 120)
    ax1.set_ylim(0, 1.05)
    ax1.grid(alpha=0.3)
    # 右：Gamma 钟形
    ax2.plot(s, gamma, color=ORANGE, lw=2.4)
    ax2.axvline(K, color=GRAY, ls=":", lw=1.0)
    ax2.annotate("平值附近：Gamma 最大\n——Delta 变化最剧烈：\n方向对赚得快，方向错亏得快", xy=(K, gamma.max()), xytext=(93, gamma.max() * 0.62),
                 fontsize=9.5, color=DARK, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
    ax2.annotate("深实值 / 深虚值：Gamma ≈ 0\n（Delta 几乎不再变化）", xy=(118, gamma[-1]), xytext=(104, gamma.max() * 0.25),
                 fontsize=9.5, color=GRAY, arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
    ax2.set_title("Gamma：Delta 变得有多快\n——敞口变化的加速度", fontsize=12, color=DARK)
    ax2.set_xlabel("标的价格")
    ax2.set_ylabel("Gamma")
    ax2.set_xlim(80, 120)
    ax2.grid(alpha=0.3)
    fig.suptitle("希腊字母的直觉：Delta 回答“方向敞口多大”，Gamma 回答“它变得多快”——两者都在平值附近最敏感",
                 fontsize=12.5, color=DARK, y=1.0)
    savefig(fig, "fig_p10_greek.png")


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


# ---------------------------------------------------------------- v8：6.13 风险预算制分配

def fig_p6_risk_budget():
    """6.13 多策略资金分配：总预算 $750 → 按策略权重切分 + 相关性修正合并 + 期权对冲"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6.2), gridspec_kw={"width_ratios": [1.15, 1]})
    # ---- 面板 A：总预算 → 策略切分 ----
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.add_patch(Rectangle((0.5, 7.5), 9, 1.5, facecolor=DARK, alpha=0.9, zorder=3))
    ax1.text(5, 8.25, "总风险预算 $750 = $50,000 × 1.5%（所有持仓名义风险之和）",
             fontsize=10.5, color="white", ha="center", va="center", zorder=4)
    segs = [(0.5, 3.6, 40, 300, "趋势回调（4.3）", UP),
            (4.2, 2.7, 30, 225, "区间边界（4.4）", ORANGE),
            (7.0, 2.7, 30, 225, "微通道（4.6）", TEAL)]
    for x, w, pct, money, name, color in segs:
        ax1.add_patch(Rectangle((x, 3.4), w, 2.2, facecolor=color, alpha=0.85, zorder=3))
        ax1.text(x + w / 2, 4.85, name, fontsize=10, color="white", ha="center", va="center", zorder=4)
        ax1.text(x + w / 2, 3.95, "%d%%  $%d" % (pct, money), fontsize=9, color="white", ha="center", va="center", zorder=4)
    for cx in (2.3, 5.55, 8.35):
        flow_arrow(ax1, cx, 7.5, cx, 5.6, color=GRAY)
    ax1.add_patch(Rectangle((0.5, 1.0), 9, 1.8, facecolor="white", ec=DARK, lw=0.8, zorder=3))
    ax1.text(5, 1.9, "单笔默认 0.5% = $250；预算制下可能被压小（$225/笔）——这是对的",
             fontsize=9.5, color=DARK, ha="center", va="center", zorder=4)
    ax1.text(5, 1.3, "保护的是“多个系统同向触发”的极端日子（趋势日三系统同向）",
             fontsize=9, color=ORANGE, ha="center", va="center", zorder=4)
    ax1.set_title("① 先封顶总风险，再按策略权重切分（$50,000 账户）", fontsize=12, color=DARK)
    # ---- 面板 B：相关性修正 + 期权对冲 ----
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.text(5, 9.3, "相关性修正：同向高相关合并计算，不简单相加", fontsize=12, color=DARK, ha="center")
    ax2.add_patch(Rectangle((0.5, 7.2), 2.8, 1.4, facecolor=UP, alpha=0.8, zorder=3))
    ax2.text(1.9, 8.15, "EURUSD 多\n0.5%", fontsize=9.5, color="white", ha="center", va="center", zorder=4)
    ax2.add_patch(Rectangle((3.6, 7.2), 2.8, 1.4, facecolor=UP, alpha=0.8, zorder=3))
    ax2.text(5.0, 8.15, "GBPUSD 多\n0.5%", fontsize=9.5, color="white", ha="center", va="center", zorder=4)
    ax2.add_patch(Rectangle((6.7, 7.2), 2.8, 1.4, facecolor=DOWN, alpha=0.8, zorder=3))
    ax2.text(8.1, 8.15, "ES 空\n0.5%", fontsize=9.5, color="white", ha="center", va="center", zorder=4)
    flow_arrow(ax2, 1.9, 7.2, 1.9, 5.0, color=UP, rad=0.15)
    flow_arrow(ax2, 5.0, 7.2, 5.0, 5.0, color=UP, rad=-0.15)
    ax2.add_patch(Rectangle((0.5, 3.6), 5.4, 1.4, facecolor="white", ec=UP, lw=1.2, zorder=3))
    ax2.text(3.2, 4.3, "合并 = 1 笔“美元走弱”\n风险按 1% 算（不是 2 个 0.5%）",
             fontsize=9.5, color=DARK, ha="center", va="center", zorder=4)
    flow_arrow(ax2, 8.1, 7.2, 8.1, 5.0, color=DOWN, rad=0.15)
    ax2.add_patch(Rectangle((6.7, 3.6), 2.8, 1.4, facecolor="white", ec=ORANGE, lw=1.2, zorder=3))
    ax2.text(8.1, 4.3, "不同逻辑\n可同时持", fontsize=9.5, color=DARK, ha="center", va="center", zorder=4)
    ax2.add_patch(Rectangle((0.5, 1.2), 9, 1.7, facecolor="white", ec=GRAY, lw=0.8, zorder=3))
    ax2.text(5, 2.05, "组合层第 4 条安全带：期权对冲（10.6）——保护性 Put 的保费\n计入风险预算，专管持仓过夜的尾部风险（呼应 1.8 黑天鹅）",
             fontsize=9, color=DARK, ha="center", va="center", zorder=4)
    ax2.set_title("② 实际敞口开盘前算清：总敞口 ≤ 1.5% 才允许同时开仓", fontsize=12, color=DARK, y=0.02)
    fig.suptitle("风险预算制（6.13）：封顶 → 切分 → 合并 → 对冲，四步把“多策略”变成“一个受控组合”",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p6_risk_budget.png")


# ---------------------------------------------------------------- v8：9.8 考核进度阶梯

def fig_p9_progress():
    """9.8 完整考核过程：8 周 72 笔阶梯 +10%（红线一次不碰）+ Phase 2 / Funded 摘要"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6.2), gridspec_kw={"width_ratios": [1.5, 1]})
    # ---- 面板 A：Phase 1 阶梯 ----
    x = [0, 2, 4, 6, 8]
    y = [0, 2.5, 5.0, 7.5, 10.0]
    ax1.plot(x, y, drawstyle="steps-post", color=UP, lw=2.6, marker="o", ms=7, zorder=4)
    ax1.axhline(10, color=UP, ls=":", lw=1.2)
    ax1.text(8.35, 10.4, "Phase 1 目标 +10%", fontsize=10, color=UP)
    ax1.axhline(-5, color=ORANGE, ls=":", lw=1.2)
    ax1.text(8.35, -4.6, "日回撤线 -5%", fontsize=9.5, color=ORANGE)
    ax1.axhline(-10, color=DOWN, ls=":", lw=1.2)
    ax1.text(8.35, -9.6, "总回撤线 -10%", fontsize=9.5, color=DOWN)
    for sx, sy in [(2, 2.5), (4, 5.0), (6, 7.5)]:
        ax1.text(sx, sy + 0.55, "18 笔\n+2.5%", fontsize=9, color=DARK, ha="center")
    ax1.annotate("第 8 周：72 笔累计 +10.0%\n→ Phase 1 通过（约 2 个月）",
                 xy=(8, 10), xytext=(4.6, 11.4), fontsize=10, color=UP,
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.2))
    ax1.text(0.1, -12.9, "日回撤从日内高点起算；连亏 2 笔后休息一天——不让亏损段放大（红线一次不碰）",
             fontsize=9, color=GRAY)
    ax1.set_xlim(0, 8.6)
    ax1.set_ylim(-14, 12.6)
    ax1.set_xticks([0, 2, 4, 6, 8])
    ax1.set_xlabel("考核周数", fontsize=11)
    ax1.set_ylabel("账户累计收益 %", fontsize=11)
    ax1.grid(alpha=0.3)
    ax1.set_title("Phase 1：胜率 40% + 盈亏比 2.2 → 每笔期望 +0.14%，72 笔 × 0.14% ≈ 10%",
                  fontsize=11.5, color=DARK)
    # ---- 面板 B：Phase 2 + Funded 摘要 ----
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.add_patch(Rectangle((2.2, 7.0), 7.3, 1.5, facecolor=UP, alpha=0.85, zorder=3))
    ax2.text(5.85, 7.75, "Phase 2：目标 +5%\n同样方法，约 1 个月通过", fontsize=10, color="white", ha="center", va="center", zorder=4)
    ax2.text(0.3, 7.75, "阶段\n目标", fontsize=10, color=DARK, ha="left", va="center")
    ax2.add_patch(Rectangle((2.2, 4.7), 7.3, 1.5, facecolor=ORANGE, alpha=0.85, zorder=3))
    ax2.text(5.85, 5.45, "Funded 首月：+4%\n出金分成 80-90%（周期 14-30 天）", fontsize=10, color="white", ha="center", va="center", zorder=4)
    ax2.add_patch(Rectangle((0.5, 2.0), 9, 1.6, facecolor="white", ec=DARK, lw=0.8, zorder=3))
    ax2.text(5, 2.8, "纪律红线全程生效：单笔 ≤0.5%、总敞口 ≤1.5%、\n日回撤 ≤5%、周末/新闻/一致性规则全部遵守",
             fontsize=9.5, color=DARK, ha="center", va="center", zorder=4)
    ax2.text(5, 0.8, "关键：无重仓、无报复、无违规——“慢就是快”不是口号，是 72 笔的算数",
             fontsize=10, color=DOWN, ha="center", va="center")
    ax2.set_title("Phase 2 + Funded：纪律不变，奖励从过线变现金流", fontsize=12, color=DARK)
    fig.suptitle("一次完整考核（FTMO 式 $100k，9.8）：8 周 72 笔稳稳 +10%，红线一次不碰——达标靠小优势 × 大样本",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p9_progress.png")


# ---------------------------------------------------------------- v8：2.5 量价四规则

def fig_p2_volume_rules():
    """2.5 量价四规则：放量上涨/缩量回调/放量不新高/缩量新高（2×2 对照）"""
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 8.8))
    data = [
        ([(0, 96.6, 97.9, 96.2, 97.7), (1, 97.5, 98.7, 97.1, 98.5), (2, 98.3, 99.7, 98.0, 99.5)],
         [0.8, 1.5, 2.4], "(a) 放量上涨 = 健康", "价格步步新高 + 量同步放大\n真金白银在推，不是虚拉", None, None),
        ([(0, 97.8, 99.1, 97.5, 98.9), (1, 98.9, 99.2, 98.4, 98.6), (2, 98.6, 98.9, 98.1, 98.3)],
         [2.0, 0.9, 0.6], "(b) 缩量回调 = 洗盘", "回调时没什么人真在卖（缩量）\n持仓者没跑，趋势大概率延续", None, None),
        ([(0, 97.6, 98.5, 97.3, 98.3), (1, 98.3, 99.8, 98.1, 99.7), (2, 99.5, 99.75, 98.8, 99.0)],
         [0.9, 2.0, 2.6], "(c) 放量不新高 = 危险", "巨量却没打出新成果（虚线未破）\n多方在耗尽——变天的早期信号", 99.8, "前高"),
        ([(0, 97.6, 98.4, 97.4, 98.2), (1, 98.2, 99.0, 98.0, 98.8), (2, 98.8, 99.9, 98.6, 99.7)],
         [1.8, 0.7, 0.4], "(d) 缩量新高 = 虚弱", "价格新高却没什么人跟（缩量）\n强弩之末，警惕假突破 FBO", 99.7, "新高"),
    ]
    for ax, (bars, vols, title, note, hl, hl_label) in zip(axes.flat, data):
        for x, o, h, l, c in bars:
            up = candle(ax, x, o, h, l, c)
            col = ORANGE if vols[x] >= 2.4 else (UP if up else DOWN)
            if title.startswith("(d)") and vols[x] <= 0.8:
                col = GRAY
            ax.add_patch(Rectangle((x - 0.18, 0.7), 0.36, 0.5 + vols[x] * 1.25,
                                   facecolor=col, alpha=0.7, zorder=3))
        if hl:
            hl_line(ax, -0.6, 2.9, hl, color=GRAY, ls=":", lw=1.3)
            ax.text(2.75, hl + 0.12, hl_label, fontsize=8.5, color=GRAY, ha="right")
        ax.set_title(title, fontsize=12, color=DARK)
        mark(ax, 1.5, 100.45, note, fs=8.5, color=DARK, ha="center")
        ax.set_xlim(-0.7, 3.7)
        ax.set_ylim(0.2, 102.0)
        ax.set_facecolor("white")
        for s in ax.spines.values():
            s.set_visible(False)
    fig.suptitle("量价四规则（2.5）：量是价格的“参与度验证”——放量要配得上价格成果，缩量要看清是洗盘还是没人跟",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p2_volume_rules.png")


# ---------------------------------------------------------------- v9：8.9 绩效归因

def fig_p8_attribution():
    """8.9 绩效归因：左=资金曲线（100 笔，含一段连亏回撤与恢复）；右=setup 归因条形图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6.0), gridspec_kw={"width_ratios": [1.5, 1]})
    # ---- 面板 A：资金曲线（100 笔，确定性序列：0-35 缓涨 → 36-42 连亏急跌 → 恢复缓涨） ----
    t = np.arange(100)
    rets = np.full(100, 0.14)
    rets[:35] += 0.02 * np.sin(np.arange(35) / 8.0)
    rets[35:42] = -0.5
    rets[42:] += 0.25 * np.sin((np.arange(58) + 8) / 6.0)
    eq = np.cumsum(rets)
    x = np.arange(1, 101)
    ax1.plot(x, eq, color=UP, lw=2.0, zorder=4)
    ax1.fill_between(x, eq, 0, color=UP, alpha=0.06, zorder=2)
    # 最大回撤区间标注（36-42 连亏：峰 35 → 谷 42，全局最大回撤）
    peak, valley = eq[34], eq[41]
    ax1.plot([35, 35], [0, peak], color=GRAY, ls=":", lw=1.0, zorder=3)
    ax1.plot([42, 42], [0, valley], color=GRAY, ls=":", lw=1.0, zorder=3)
    ax1.fill_between(x[34:42], eq[34:42], peak, color=DOWN, alpha=0.18, zorder=2)
    ax1.annotate("连亏 6 笔 → 回撤 %.1f%%\n（峰 %.1f%% → 谷 %.1f%%）" % (peak - valley, peak, valley),
                 xy=(38.5, valley + 0.3), xytext=(45, peak - 3.2), fontsize=10, color=DOWN,
                 arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))
    ax1.annotate("恢复：约 2-3 周回到前高——\n回撤能恢复的前提是仓位没爆（6.1）",
                 xy=(53, eq[52] + 0.2), xytext=(58, peak + 4.6), fontsize=9.5, color=DARK,
                 arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
    ax1.text(2, 11.6, "100 笔 × 每笔期望 +0.14%% → 累计约 %+.1f%%\n单笔风险 0.5%%，最大回撤 %.1f%%（理论可控）" % (eq[-1], peak - valley),
             fontsize=9.5, color=GRAY, va="top")
    ax1.set_xlim(0, 101)
    ax1.set_ylim(-3.5, 12.5)
    ax1.set_xlabel("交易笔数（按月复盘，连亏段对照 6.3 理论预期）", fontsize=11)
    ax1.set_ylabel("账户累计收益 %", fontsize=11)
    ax1.grid(alpha=0.3)
    ax1.set_title("资金曲线：稳步向上 + 一次可控回撤——看恢复速度，不看单日波动", fontsize=11.5, color=DARK)
    # ---- 面板 B：setup 归因条形图 ----
    setups = ["突破", "ORB", "区间边界", "趋势回调"]
    total_r = [-1.4, 0.9, 3.1, 8.2]
    counts = [15, 15, 28, 42]
    cols = [DOWN, ORANGE, UP, UP]
    bars = ax2.barh(setups, total_r, color=cols, height=0.55, zorder=3)
    for i, (v, c) in enumerate(zip(total_r, counts)):
        if v > 0:
            ax2.text(v + 0.25, i, "+%.1fR\n(%d 笔)" % (v, c), va="center", ha="left", fontsize=9.5, color=DARK)
        else:
            ax2.text(v - 0.25, i, "%.1fR\n(%d 笔)" % (v, c), va="center", ha="right", fontsize=9.5, color=DOWN)
    ax2.axvline(0, color=DARK, lw=1.0, zorder=2)
    ax2.annotate("负贡献 setup：\n砍掉它，系统质量\n立刻上一个台阶",
                 xy=(-1.4, 0), xytext=(2.6, 0.0), fontsize=10, color=DOWN, va="center",
                 arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))
    ax2.text(0.15, 3.52, "合计 100 笔 +10.8R：\n趋势回调贡献 76% 的利润（呼应 7.1 的 80/20）",
             fontsize=9.5, color=DARK, va="bottom")
    ax2.set_xlim(-3.4, 11.6)
    ax2.set_ylim(-0.7, 4.0)
    ax2.grid(alpha=0.3, axis="x")
    ax2.set_title("按 setup 归因：钱具体是哪个系统赚的", fontsize=11.5, color=DARK)
    fig.suptitle("绩效归因（8.9）：SQN 说“系统整体行不行”，归因说“钱从哪来”——说不清上个月的钱是哪个 setup 赚的，验证就没闭环",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p8_attribution.png")


# ---------------------------------------------------------------- v10：6.7 凯利 / 6.8 破产概率 / 6.9 复利

def fig_p6_kelly():
    """6.7 凯利公式：左=f* vs 胜率（b=1/2/3 曲线族）；右=对数增长率 vs 仓位曲线"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.8))
    # 左：f* = p - (1-p)/b
    p = np.linspace(0.05, 0.65, 200)
    for b, col, lab in [(1, GRAY, "盈亏比 b=1"), (2, UP, "盈亏比 b=2"), (3, ORANGE, "盈亏比 b=3")]:
        f = p - (1 - p) / b
        ax1.plot(p, f, color=col, lw=2.0, label=lab)
    ax1.plot([0.4], [0.1], "o", color=UP, ms=8, zorder=5)
    ax1.annotate("胜率 40%、盈亏比 2\n→ 理论最优 f* = 10%", xy=(0.4, 0.1), xytext=(0.14, 0.30),
                 fontsize=10, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.2))
    ax1.axhline(0.005, color=DOWN, ls=":", lw=1.3)
    ax1.text(0.052, 0.008, "本书单笔风险 0.5%：远低于任何凯利值\n考核期要的是生存，不是增长", fontsize=9.5, color=DOWN)
    ax1.set_xlim(0.05, 0.65)
    ax1.set_ylim(-0.02, 0.62)
    ax1.set_xlabel("胜率 p", fontsize=11)
    ax1.set_ylabel("凯利仓位 f*", fontsize=11)
    ax1.legend(fontsize=9.5, loc="upper left")
    ax1.grid(alpha=0.3)
    ax1.set_title("左：理论最优仓位 f* = p − (1−p)/b——胜率越高、盈亏比越大，上限越高", fontsize=11.5, color=DARK)
    # 右：对数增长率 g(f) = p·ln(1+f·b) + q·ln(1−f)
    f = np.linspace(0.001, 0.35, 300)
    b, p_ = 2.0, 0.4
    g = p_ * np.log(1 + f * b) + (1 - p_) * np.log(1 - f)
    ax2.plot(f, g, color=DARK, lw=2.2)
    ax2.axvline(0.1, color=UP, ls="--", lw=1.2)
    ax2.text(0.103, g.max() * 0.5, "满凯利 f*=10%\n（增长率最高点）", fontsize=9.5, color=UP)
    ax2.axvline(0.05, color=ORANGE, ls="--", lw=1.2)
    ax2.text(0.053, g.max() * 0.78, "半凯利 5%：\n增长损失很小，\n回撤大幅缩小", fontsize=9.5, color=ORANGE)
    ax2.axvline(0.005, color=DOWN, ls=":", lw=1.2)
    ax2.text(0.008, g.max() * 0.12, "本书 0.5%：\n生存优先", fontsize=9.5, color=DOWN)
    ax2.set_xlim(-0.005, 0.36)
    ax2.set_xlabel("实际使用的仓位 f", fontsize=11)
    ax2.set_ylabel("对数增长率 g(f)", fontsize=11)
    ax2.grid(alpha=0.3)
    ax2.set_title("右：增长率曲线——满凯利是尖峰，在 f/2~f/4 处损失极小（用 20% 波动换 80% 增长）", fontsize=11.5, color=DARK)
    fig.suptitle("凯利公式（6.7）：f* 是仓位的理论上限，不是目标——输入不准 + 回撤极深，实用取半凯利或四分之一凯利",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p6_kelly.png")


def fig_p6_ruin():
    """6.8 破产概率：左=100 笔中至少出现一段 k 连亏的概率；右=犯错预算对比"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.6), gridspec_kw={"width_ratios": [1.6, 1]})
    # 左：P(至少一段 k 连亏) = 1 - (1 - q^k)^(N-k+1)，N=100, p=0.4
    N, p_, q = 100, 0.4, 0.6
    ks = np.arange(3, 16)
    probs = [1 - (1 - q ** k) ** (N - k + 1) for k in ks]
    ax1.bar(ks, probs, color=UP, alpha=0.85, width=0.62)
    for k, pr in zip(ks, probs):
        ax1.text(k, pr + 0.02, "%.0f%%" % (pr * 100), ha="center", fontsize=9, color=DARK)
    ax1.annotate("5 连亏 ≈ 100%：几乎必现\n→ 2% 风险（5 次预算）≈ 必爆", xy=(5, probs[2]), xytext=(6.8, 0.52),
                 fontsize=9.5, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.1))
    ax1.annotate("10 连亏仍 ≈ 42%：风险翻 4 倍的人\n平均两轮考核就爆一次", xy=(10, probs[7]), xytext=(11.4, 0.66),
                 fontsize=9.5, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.1))
    ax1.annotate("20 连亏仅 ≈ 0.3%：0.5% 风险\n几乎不可破（4 段 5 连亏叠加）", xy=(15, probs[12]), xytext=(10.2, 0.06),
                 fontsize=9.5, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.1))
    ax1.set_xlim(2.5, 16.5)
    ax1.set_ylim(0, 1.08)
    ax1.set_xlabel("连亏 k 笔（100 笔中至少出现一段）", fontsize=11)
    ax1.set_ylabel("概率", fontsize=11)
    ax1.grid(alpha=0.3, axis="y")
    ax1.set_title("胜率 40% 的系统：连亏长度分布——连亏无法避免，但可以让它“不致命”", fontsize=11.5, color=DARK)
    # 右：犯错预算对比
    ax2.barh(["2% 风险", "0.5% 风险"], [5, 20], color=[DOWN, UP], height=0.5)
    ax2.text(5.4, 0, "5 次\n（2% × 5 = 10% 回撤线）", fontsize=10, color=DOWN, va="center")
    ax2.text(20.5, 1, "20 次\n（0.5% × 20 = 10% 回撤线）", fontsize=10, color=UP, va="center")
    ax2.set_xlim(0, 22.5)
    ax2.set_ylim(-0.6, 1.6)
    ax2.grid(alpha=0.3, axis="x")
    ax2.set_title("犯错预算：风险减半 → 存活率数量级提升", fontsize=11.5, color=DARK)
    fig.suptitle("破产概率（6.8）：风险百分比与存活率是指数关系——0.5% 风险 + 10% 回撤线 = 20 次犯错预算",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p6_ruin.png")


def fig_p6_compound():
    """6.9 复利与规模化：36 个月复利 vs 单利对比"""
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    t = np.arange(0, 37)
    comp = 1.04 ** t
    linear = 1 + 0.04 * t
    ax.plot(t, comp, color=UP, lw=2.4, label="复利：月 +4%（1.04^t）")
    ax.plot(t, linear, color=GRAY, lw=2.0, ls="--", label="单利：月 +4%（1 + 0.04t）")
    ax.fill_between(t, linear, comp, color=UP, alpha=0.08)
    ax.annotate("36 个月：复利 ≈ 4.1 倍 vs 单利 2.4 倍\n差距 1.7 倍全部来自“利滚利”", xy=(36, comp[-1]),
                 xytext=(19, comp[-1] * 0.58), fontsize=10.5, color=UP,
                 arrowprops=dict(arrowstyle="->", color=UP, lw=1.3))
    ax.text(1.5, 4.35, "权益增长后，同样 0.5% 风险对应的\n绝对金额自动变大——仓位自己长大\n（不要手动加风险）", fontsize=10, color=DARK, va="top")
    ax.set_xlim(0, 37)
    ax.set_ylim(1, 4.7)
    ax.set_xlabel("月份", fontsize=11)
    ax.set_ylabel("账户倍数", fontsize=11)
    ax.legend(fontsize=10.5, loc="upper left")
    ax.grid(alpha=0.3)
    ax.set_title("复利的引擎是“权益增长”，不是“你变大胆”", fontsize=12, color=DARK)
    savefig(fig, "fig_p6_compound.png")


# ---------------------------------------------------------------- v11：1.6 点差滑点 / 7.4 连亏连赚 / 9.4 失败归因

def fig_p1_quotes():
    """1.6 价格形成：左=买卖盘与点差结构；右=滑点（跳空穿过止损）示意"""
    fig = plt.figure(figsize=(14.5, 5.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.35], wspace=0.16)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    # ---- 左：买卖盘与点差 ----
    price_levels = [99.90, 99.94, 99.98, 100.02, 100.06, 100.10]
    depths = [3.2, 5.1, 7.8, 6.4, 4.2, 2.6]  # 各价位挂单量
    colors = [UP, UP, UP, DOWN, DOWN, DOWN]
    ax1.barh(price_levels, depths, color=colors, height=0.03, alpha=0.75, zorder=3)
    ax1.axhline(100.00, color=GRAY, lw=0.8, ls="--")
    ax1.fill_betweenx([99.98, 100.02], 0, 9.2, color=ORANGE, alpha=0.14, zorder=1)
    ax1.text(9.35, 100.00, "点差 = Ask − Bid\n(进出一次的成本)", fontsize=9.5, color=DARK, va="center", ha="left")
    ax1.annotate("卖价 Ask（你买入的价格）", xy=(7.8, 100.02), xytext=(2.0, 100.09),
                 fontsize=10, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))
    ax1.annotate("买价 Bid（你卖出的价格）", xy=(7.8, 99.98), xytext=(2.0, 99.87),
                 fontsize=10, color=UP, arrowprops=dict(arrowstyle="->", color=UP, lw=1.2))
    ax1.text(0.2, 99.70, "挂单量（流动性）——深度越厚，点差越窄\n伦敦时段窄 / 亚盘宽 / 数据瞬间放大数倍", fontsize=9.5, color=GRAY, va="top")
    ax1.set_xlim(0, 13)
    ax1.set_ylim(99.66, 100.20)
    ax1.set_xlabel("挂单量（示意）", fontsize=11)
    ax1.set_ylabel("价格", fontsize=11)
    ax1.grid(alpha=0.3, axis="x")
    ax1.set_title("买卖盘结构：你买用 Ask、卖用 Bid——一进一出天然亏一个点差", fontsize=11.5, color=DARK)
    # ---- 右：滑点 ----
    ax2.plot([0, 4], [100.00, 100.00], color=DARK, lw=2.0)
    ax2.plot([4, 4.05], [100.00, 99.80], color=DOWN, lw=2.0)  # 跳空
    ax2.plot([4.05, 10], [99.80, 99.80], color=DOWN, lw=2.0)
    ax2.axhline(99.95, color=GRAY, ls=":", lw=1.4)
    ax2.text(5.4, 99.955, "止损挂 99.95", fontsize=9, color=GRAY)
    ax2.annotate("实际成交 99.80\n（多亏 15 点——价位没人接单）", xy=(4.5, 99.80), xytext=(5.0, 99.62),
                 fontsize=9.5, color=DOWN, arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))
    ax2.text(0.2, 100.02, "周末开盘 / 数据瞬间 / 低流动性：止损单只能追跳空价\n一句话记牢：市价单和止损单会滑点，限价单不会",
             fontsize=9.5, color=DARK, va="bottom")
    ax2.set_xlim(0, 10.4)
    ax2.set_ylim(99.52, 100.10)
    ax2.set_xticks([])
    ax2.set_yticks([99.60, 99.80, 100.00])
    ax2.grid(alpha=0.3, axis="y")
    ax2.set_title("滑点：价格跳空穿过你的止损——不是平台坑你，是没人在那个价位接单", fontsize=11.5, color=DARK)
    fig.suptitle("价格怎么形成（1.6）：点差是固定成本，滑点高发在跳空——插针不是每次都是机构扫止损，有时只是没人接单（第 5 章 sweep 清单）",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p1_quotes.png")


def fig_p7_streaks():
    """7.4 连亏与连赚：两个螺旋的危险信号逐级升级；应对框在底部"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.6))
    stages1 = ["正常连亏\n（都符合计划）", "怀疑系统", "想改规则", "想加倍回本", "报复交易"]
    risk1 = [0.15, 0.35, 0.55, 0.78, 1.0]
    ax1.bar(range(5), risk1, color=[UP, ORANGE, ORANGE, ORANGE, DOWN], alpha=0.85, zorder=3)
    for i, (r, s) in enumerate(zip(risk1, stages1)):
        ax1.text(i, r + 0.03, s, ha="center", va="bottom", fontsize=9.5, color=DARK)
    ax1.axhline(0.85, color=DOWN, ls="--", lw=1.3)
    ax1.text(2.35, 0.87, "危险区：强制停手", fontsize=9.5, color=DOWN, va="bottom")
    ax1.annotate("开始怀疑：第一个危险信号", xy=(1, 0.35), xytext=(0.2, 0.68),
                 fontsize=9, color=GRAY, arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
    ax1.text(0.05, 1.12, "应对：降风险预算 0.5%→0.25% 继续做——不停手、不改系统、不加倍",
             fontsize=10, color=DARK, va="top")
    ax1.set_xlim(-0.5, 4.5)
    ax1.set_ylim(0, 1.25)
    ax1.set_xticks([])
    ax1.set_ylabel("违规风险 →", fontsize=11)
    ax1.grid(alpha=0.3, axis="y")
    ax1.set_title("连亏螺旋：从“正常连亏”到“报复交易”是渐进的——\n在怀疑阶段就拦截，别等到危险区", fontsize=11.5, color=DARK)
    stages2 = ["连赚", "过度自信\n（我悟了）", "想加仓位", "计划外交易", "回吐利润"]
    risk2 = [0.15, 0.4, 0.62, 0.82, 1.0]
    ax2.bar(range(5), risk2, color=[UP, ORANGE, ORANGE, DOWN, DOWN], alpha=0.85, zorder=3)
    for i, (r, s) in enumerate(zip(risk2, stages2)):
        ax2.text(i, r + 0.03, s, ha="center", va="bottom", fontsize=9.5, color=DARK)
    ax2.axhline(0.85, color=DOWN, ls="--", lw=1.3)
    ax2.text(2.35, 0.87, "危险区：连赚比连亏更危险", fontsize=9.5, color=DOWN, va="bottom")
    ax2.annotate("“我悟了”是最危险的一句话", xy=(2, 0.62), xytext=(0.4, 0.95),
                 fontsize=9, color=GRAY, arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
    ax2.text(0.05, 1.12, "应对：维持原仓位原风险——连赚是概率的馈赠，不是你变强了",
             fontsize=10, color=DARK, va="top")
    ax2.set_xlim(-0.5, 4.5)
    ax2.set_ylim(0, 1.25)
    ax2.set_xticks([])
    ax2.grid(alpha=0.3, axis="y")
    ax2.set_title("连赚螺旋：自满让你觉得规则“太保守”——\n计划外交易那一刻，利润开始回吐", fontsize=11.5, color=DARK)
    fig.suptitle("两个危险时刻（7.4）：连亏考验纪律，连赚考验清醒——危险信号都是渐进出现的，关键是尽早识别并在早期拦截",
                 fontsize=13, color=DARK, y=0.99)
    savefig(fig, "fig_p7_streaks.png")


def fig_p9_fail():
    """9.4 常见失败原因：左=五类原因频率排序（示意）；右=方法×仓位×执行三角"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.6), gridspec_kw={"width_ratios": [1.35, 1]})
    causes = ["忽视一致性规则", "过度交易", "违规（持仓/新闻/锁仓）", "报复交易", "重仓冲刺"]
    freq = [12, 16, 20, 24, 28]
    cols = [GRAY, ORANGE, ORANGE, DOWN, DOWN]
    ax1.barh(causes, freq, color=cols, height=0.55, zorder=3)
    for i, v in enumerate(freq):
        ax1.text(v + 0.6, i, "%d%%" % v, va="center", fontsize=10, color=DARK)
    ax1.text(0.5, 4.6, "数值为相对频率示意（按 9.4 排序绘制，非平台官方统计）", fontsize=9, color=GRAY)
    ax1.text(20, 3.1, "五条没有一条是“技术不行”——全在纪律层", fontsize=10.5, color=DOWN)
    ax1.set_xlim(0, 34)
    ax1.set_ylim(-0.6, 5.2)
    ax1.set_xlabel("相对频率 %（示意）", fontsize=11)
    ax1.grid(alpha=0.3, axis="x")
    ax1.set_title("考核失败原因频率：方法、仓位都教过了，失败发生在执行层", fontsize=11.5, color=DARK)
    # ---- 右：三角 ----
    tri = [(0, 0), (4, 0), (2, 3.46), (0, 0)]
    ax2.plot([p[0] for p in tri], [p[1] for p in tri], color=DARK, lw=2.2)
    ax2.text(2, -0.55, "方法（第 2-5 章）", ha="center", fontsize=11, color=UP, fontweight="bold")
    ax2.text(-0.4, 1.85, "仓位\n（第 6 章）", ha="right", fontsize=11, color=ORANGE, fontweight="bold")
    ax2.text(4.4, 1.85, "执行\n（第 7 章）", ha="left", fontsize=11, color=DOWN, fontweight="bold")
    ax2.plot([2], [1.15], "o", color=TEAL, ms=14, zorder=5)
    ax2.text(2, 1.15, "考核\n通过", ha="center", va="center", fontsize=10.5, color="white", zorder=6, fontweight="bold")
    ax2.text(2, -1.35, "三者缺一不可：重仓冲刺毁在仓位，\n报复交易毁在执行，违规毁在规则", fontsize=9.5, color=GRAY, ha="center")
    ax2.set_xlim(-1.4, 5.4)
    ax2.set_ylim(-1.9, 4.0)
    ax2.axis("off")
    ax2.set_title("考核期 = 方法 × 仓位 × 执行（9.4）", fontsize=11.5, color=DARK)
    fig.suptitle("考核为什么失败（9.4）：五类原因全是纪律问题——先把执行层堵住，再谈技术优化",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p9_fail.png")


# ---------------------------------------------------------------- v12：5.7 完整 SMC 交易流程

def fig_p5_smc_flow():
    """5.7 完整 SMC 交易流程：多级别背景 + 五步执行 + 与第 4 章系统的对照"""
    fig, ax = plt.subplots(figsize=(14.5, 6.4))
    style_ax(ax, xlim=(0, 14), ylim=(0, 6.6))
    # ---- 顶部背景框：多级别过滤 ----
    draw_box(ax, 0.4, 5.15, 13.2, 1.25, "背景（多级别过滤）：日线上升趋势 → 4H CHoCH 警告 → 1H 等做多回调",
             ec=GRAY, fs=11, tc=DARK)
    flow_arrow(ax, 1.7, 5.12, 1.7, 4.95, color=GRAY)
    # ---- 五步流程框 ----
    steps = [
        (0.6, "① 画结构\nswing 高低点\nBSL / SSL 池\n看涨 OB、FVG\n→ 2.4 / 5.2-5.6", TEAL),
        (3.2, "② 等 sweep\n插破前低 SSL\n快速收回 / 长影\n→ 3.2 / 5.3", ORANGE),
        (5.8, "③ 找入场区\nFVG / OB 区域\n15m 锤子 / 内包\n→ 4.3 / 5.5-5.6", TEAL),
        (8.4, "④ 执行\nOB 入场 + 确认\n止损 sweep 低点下\n→ 4.2 / 5.5", ORANGE),
        (11.0, "⑤ 管理\n1R 移保本\n跑向 BSL / 2R\n→ 4.4 / 4.13", TEAL),
    ]
    for i, (x, txt, col) in enumerate(steps):
        draw_box(ax, x, 2.7, 2.2, 2.2, txt, ec=col, fs=10, tc=DARK)
        if i < 4:
            flow_arrow(ax, x + 2.2, 3.8, x + 2.6, 3.8)
    # ---- 底部关键认知框 ----
    draw_box(ax, 0.4, 0.35, 13.2, 1.95,
             "关键认知：这套流程 = 第 4 章趋势回调系统的 SMC 翻译版——语言不同，数学一样。\n"
             "画结构=趋势判断（2.4）｜等 sweep=假突破确认（3.2）｜FVG/OB=回调入场区（4.3）\n"
             "止损 SSL 外=结构止损（4.2）｜目标 BSL=前高目标（4.13）",
             ec=TEAL, fs=10.5, tc=DARK)
    fig.suptitle("完整 SMC 交易流程（5.7）：多级别背景 → 五步执行 → 本质是第 4 章趋势回调系统的翻译版",
                 fontsize=13, color=DARK, y=0.985)
    savefig(fig, "fig_p5_smc_flow.png")


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
    fig_p8_orderflow()
    fig_p5_volume_profile()
    fig_p8_footprint()
    fig_p4_orb()
    fig_opt_strategies()
    fig_p1_asset_allocation()
    fig_p3_combo_bars()
    fig_p3_mtr()
    # ---------- v8 新增（6.13 风险预算制 / 9.8 考核进度阶梯 / 2.5 量价四规则） ----------
    fig_p6_risk_budget()
    fig_p9_progress()
    fig_p2_volume_rules()
    # ---------- v9 新增（8.9 绩效归因） ----------
    fig_p8_attribution()
    # ---------- v10 新增（6.7 凯利 / 6.8 破产概率 / 6.9 复利） ----------
    fig_p6_kelly()
    fig_p6_ruin()
    fig_p6_compound()
    # ---------- v11 新增（1.6 点差滑点 / 7.4 连亏连赚 / 9.4 失败归因） ----------
    fig_p1_quotes()
    fig_p7_streaks()
    fig_p9_fail()
    # ---------- v12 新增（5.7 完整 SMC 交易流程） ----------
    fig_p5_smc_flow()
    fig_prop_flow()
    fig_risk_curve()
    fig_call_put()
    fig_theta_decay()
    fig_greek_curves()
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
    fig_p2_spike_climax()
    fig_p3_wedge_contrast()
    fig_p3_h1h2()
    fig_p4_mm_four()
    fig_p4_channel_types()
    fig_p4_ff_20gb()
    fig_p4_state_tree()
    fig_p4_channel_evolve()
    fig_p4_range_density()
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


# ---------------------------------------------------------------- 图 2-10（PA_Agent 极速行情：尖峰与高潮）
def fig_p2_spike_climax():
    """2.10 尖峰识别五标准+分级（左）；买进高潮四阶段+三路径概率（右）"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.6))
    # 左：尖峰识别
    ax = axes[0]
    k = [(0, 100, 101, 99.5, 100.6), (1, 100.6, 101.5, 100, 100.8), (2, 100.8, 102, 100.3, 101.5),  # 背景
         (3, 101.5, 104, 101.3, 103.7), (4, 103.7, 106.2, 103.5, 105.9), (5, 105.9, 108.5, 105.7, 108.2),
         (6, 108.2, 111, 108, 110.7), (7, 110.7, 113.6, 110.5, 113.3), (8, 113.3, 116.2, 113.1, 115.8),  # 尖峰1-6
         (9, 115.8, 117, 115.2, 115.6),  # 暂停棒
         (10, 115.6, 116.5, 114.2, 114.6)]  # 回撤棒
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    mark(ax, 1.2, 102.5, "背景\n小实体", color=GRAY, fs=8.5, box=True)
    mark(ax, 5.7, 118.5, "尖峰 6 根：\n大实体（≥均值1.5-2倍）\n实体几乎无重叠\n上尾线短（≤实体30%）\n收盘持续创新高", color=UP, fs=9, box=True)
    mark(ax, 9, 118.3, "暂停棒\n小实体→禁追\nspike ending", color=ORANGE, fs=8.5, box=True)
    mark(ax, 10.2, 113.2, "回撤棒→\n尖峰确认结束", color=DOWN, fs=8.5, box=True)
    mark(ax, 5.5, 98.8, "1根=弱候选等跟随 | 2根=最低可路由（仅SPS） | 3-5根=标准尖峰 | 6根+=高潮预警（以衰竭信号为准）", color=DARK, fs=8.5, box=True)
    style_ax(ax, xlim=(-0.8, 11.8), ylim=(96, 121))
    ax.set_title("① 尖峰识别：连续大型趋势棒 + 短尾线 + 收盘创新高（Spike ≠ Breakout ≠ Gap ≠ Climax）", fontsize=11, color=DARK)
    # 右：买进高潮四阶段 + 三路径概率
    ax = axes[1]
    k = [(0, 100, 102.5, 99.5, 102), (1, 102, 104.5, 101.5, 104.1),  # 阶段1 趋势棒
         (2, 104.1, 107.8, 103.8, 107.4),  # 阶段2 高潮棒
         (3, 107.4, 110.5, 106.8, 108),  # 阶段3 拒绝棒（长上尾）
         (4, 108, 108.8, 105.8, 106.2),  # 阶段4 空头确认
         (5, 106.2, 107.5, 104.2, 104.8), (6, 104.8, 106, 102.8, 103.4)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    mark(ax, 0.8, 112.8, "阶段1：大趋势棒\n推动上涨", color=UP, fs=8.5, box=True)
    mark(ax, 2, 109.6, "阶段2：高潮棒\n（巨型实体）", color=ORANGE, fs=8.5, box=True)
    mark(ax, 3.4, 112.8, "阶段3：拒绝棒\n长上尾线\n（>实体50%）", color=DOWN, fs=8.5, box=True)
    mark(ax, 4.7, 108.6, "阶段4：空头趋势棒\n确认反转", color=DOWN, fs=8.5, box=True)
    mark(ax, 6.2, 101.5, "衰竭信号三件套：\n长上尾 / 小实体 / 反向棒\n任一出现即触发高潮", color=DARK, fs=8.5, box=True)
    draw_box(ax, 0.4, 97.4, 2.1, 1.4, "转通道延续\n≈60%", ec=UP, fs=9.5)
    draw_box(ax, 2.9, 97.4, 2.1, 1.4, "进入区间\n≈30%", ec=ORANGE, fs=9.5)
    draw_box(ax, 5.4, 97.4, 2.1, 1.4, "趋势反转\n≈10%\n仅诊断", ec=DOWN, fs=9.5)
    style_ax(ax, xlim=(-0.8, 8.2), ylim=(95, 115))
    ax.set_title("② 买进高潮四阶段序列 + 尖峰后三条路径概率（只做回撤 SPS，禁追尖峰 SCS）", fontsize=11, color=DARK)
    fig.suptitle("尖峰与高潮（Al Brooks）：尖峰是趋势的 Leg 1——2 根以上大趋势棒才可路由；高潮以衰竭信号为准，不以根数；高潮后至少等 10 根棒", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p2_spike_climax.png")


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


# ---------------------------------------------------------------- 图 4-11（PA_Agent 通道生命周期 + 画线四方法）
def fig_p4_channel_evolve():
    """4.21 通道演变五阶段 + 通道线四种画法"""
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.4))
    # 左：上涨通道五阶段演变
    ax = axes[0]
    k = [(0, 100, 102, 99.5, 101.5), (1, 101.5, 104, 101, 103.5), (2, 103.5, 106, 103, 105.5), (3, 105.5, 108, 105, 107.5),  # ①尖峰
         (4, 107.5, 109.5, 105.8, 108.6), (5, 108.6, 111, 107.2, 110.2), (6, 110.2, 112.5, 108.6, 111.8), (7, 111.8, 114, 110.5, 113.4),  # ②扩展
         (8, 113.4, 116.5, 112.8, 115.8), (9, 115.8, 117.5, 113.4, 114.5), (10, 114.5, 118.5, 113.9, 117.8), (11, 117.8, 119.5, 115.8, 116.8), (12, 116.8, 121, 116.2, 120.2),  # ③台阶
         (13, 120.2, 122.3, 119.2, 121.5), (14, 121.5, 123.2, 120.5, 122.6), (15, 122.6, 124, 121.8, 123.5), (16, 123.5, 124.7, 122.6, 124),  # ④收缩
         (17, 124, 125, 121.8, 122.3), (18, 122.3, 123.8, 121.5, 123.2), (19, 123.2, 124.2, 120.9, 121.4), (20, 121.4, 122.6, 120.2, 120.8)]  # ⑤区间
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c)
    ax.plot([3, 18], [105, 105 + 1.56 * 15], color=GRAY, ls="--", lw=1.2)  # 趋势线（经过 x3/x8 低点）
    ax.plot([10, 13], [117.8, 120.2], color=ORANGE, lw=1.0)  # 通道线上段示意
    mark(ax, 1.6, 109.5, "① 窄通道/尖峰\n连续大阳、几乎不回撤", color=UP, fs=9, box=True)
    mark(ax, 5.6, 115.6, "② 通道扩展\n回撤加大", color=UP, fs=9, box=True)
    mark(ax, 10.4, 123.5, "③ 宽通道/台阶\n多空更均衡", color=ORANGE, fs=9, box=True)
    mark(ax, 15, 126.5, "④ 收缩台阶\n推力递减=动能衰退", color=DOWN, fs=9, box=True)
    mark(ax, 19.4, 118, "⑤ 区间\n跌破趋势线", color=DOWN, fs=9, box=True)
    mark(ax, 10.5, 101.5, "趋势线（动态支撑）\n刺穿后重画：新线更水平=动能衰减\n连续两次重画=即将突破", color=GRAY, fs=8.5, box=True, va="top")
    mark(ax, 11, 130.5, "上边界=空头建仓区（仅诊断，不逆势）", color=DOWN, fs=9.5, box=True)
    style_ax(ax, xlim=(-0.8, 21.5), ylim=(95, 133))
    ax.set_title("① 上涨通道演变五阶段：尖峰 → 扩展 → 台阶 → 收缩 → 区间", fontsize=11.5, color=DARK)
    # 右：通道线四种画法
    ax = axes[1]
    hx = [1, 3, 5, 7, 9, 11, 13]
    hy = [10.5, 13, 15.2, 17, 18.4, 19.4, 20]
    lx = [0, 2, 4, 6, 8, 10, 12]
    ly = [8, 10.3, 12.4, 14.3, 15.9, 17.2, 18.2]
    ax.plot(lx, ly, color=GRAY, lw=1.6)
    ax.plot(hx, hy, color=DARK, lw=0.8, ls=":")
    ax.plot(hx, hy, "o", color=DARK, ms=4.5, zorder=5)
    ax.plot(lx, ly, "s", color=GRAY, ms=3.5, zorder=5)
    ax.plot([0, 13], [8.95, 20], color=TEAL, lw=1.8, label="① 平行线法（候选期首选）")
    ax.plot([0, 13], [16.1, 20], color=ORANGE, lw=1.8, ls="--", label="② 波段点法（扩张期）")
    ax.plot([0, 13], [11.7, 20.8], color="#9c27b0", lw=1.8, ls="-.", label="③ 最佳拟合线法（成熟期）")
    ax.plot([0, 13], [10.95, 21.0], color=DOWN, lw=1.8, ls=":", label="④ 平行投影法（异常刺穿）")
    mark(ax, 10.4, 21.9, "末端高点走平 →\n平行线法失灵，切换画法", color=DARK, fs=9, box=True, ha="left")
    mark(ax, 6.7, 7.1, "趋势线（低点连线）", color=GRAY, fs=9)
    mark(ax, 8.2, 14.2, "离趋势线最远高点\n（平行投影基准）", color=DOWN, fs=8, ha="left")
    ax.legend(fontsize=8.5, loc="lower left", framealpha=0.9)
    style_ax(ax, xlim=(-0.6, 15), ylim=(5.5, 24))
    ax.set_title("② 通道线四种画法：随通道阶段演进切换（避免主观性）", fontsize=11.5, color=DARK)
    fig.suptitle("通道生命周期与画线方法（Al Brooks）：通道=倾斜交易区间；上涨通道=空头旗形——上边界逆势仅诊断，顺势只做回撤；画法随阶段演进，多画法交叉验证", fontsize=12, color=DARK, y=0.99)
    savefig(fig, "fig_p4_channel_evolve.png")


# ---------------------------------------------------------------- 图 4-12（PA_Agent 区间密度判定 + 边界质量）
def fig_p4_range_density():
    """4.3 区间密度判定流程（紧凑度→CV）+ 边界质量对比"""
    fig = plt.figure(figsize=(15, 8.2))
    ax = fig.add_subplot(1, 2, 1)  # 左：密度判定决策树
    draw_box(ax, 2.9, 8.4, 5.4, 1.3, "区间宽度 ÷ 平均波段幅度\n= 紧凑度", ec=DARK, fs=11)
    draw_box(ax, 0.3, 6.0, 4.4, 1.4, "紧凑度 < 25%\nBarbwire 铁丝网\n不交易，等突破", ec=DOWN, fs=9.5)
    draw_box(ax, 4.9, 6.0, 4.4, 1.4, "紧凑度 25-35%\n过渡区\n只等突破，不做 fade", ec=ORANGE, fs=9.5)
    draw_box(ax, 9.5, 6.0, 4.0, 1.4, "紧凑度 ≥ 35%\n进入 CV 判定", ec=UP, fs=9.5)
    draw_box(ax, 2.9, 3.5, 5.4, 1.3, "CV = 最近 10 个波段\n标准差 ÷ 均值", ec=DARK, fs=11)
    draw_box(ax, 0.3, 1.1, 4.4, 1.4, "CV < 0.3 高密度\n边界清晰、波段均匀\n仅顺方向一侧边界刮头皮", ec=UP, fs=9.5)
    draw_box(ax, 4.9, 1.1, 4.4, 1.4, "CV 0.3-0.5 中密度\n降频\n只做边界处最强信号", ec=ORANGE, fs=9.5)
    draw_box(ax, 9.5, 1.1, 4.0, 1.4, "CV > 0.5 低密度\n边界不可靠\n只等突破，中部不用限价", ec=DOWN, fs=9.5)
    flow_arrow(ax, 4.1, 8.4, 2.5, 7.4, color=DARK, rad=-0.1)
    flow_arrow(ax, 5.6, 8.4, 7.1, 7.4, color=DARK, rad=0.1)
    flow_arrow(ax, 9.3, 8.4, 11.4, 7.4, color=DARK, rad=0.15)
    flow_arrow(ax, 11.5, 6.0, 5.6, 4.8, color=DARK, rad=0.3)
    flow_arrow(ax, 4.1, 3.5, 2.5, 2.5, color=DARK, rad=-0.1)
    flow_arrow(ax, 5.6, 3.5, 7.1, 2.5, color=DARK, rad=0.1)
    flow_arrow(ax, 9.3, 3.5, 11.4, 2.5, color=DARK, rad=0.15)
    mark(ax, 4.4, 8.0, "先测", color=DARK, fs=9)
    mark(ax, 9.5, 8.0, "达标", color=DARK, fs=9)
    mark(ax, 4.7, 4.55, "再测", color=DARK, fs=9)
    mark(ax, 10.2, 0.55, "判断优先级：Barbwire 优先于 CV；低密度与 Barbwire 的处理优先于其他一切判断", color=DARK, fs=9, box=True, ha="center", va="bottom")
    style_ax(ax, xlim=(0, 13.9), ylim=(0, 10.2))
    ax.set_title("① 区间密度两级判定：先紧凑度，再 CV", fontsize=11.5, color=DARK)
    # 右上：高质量边界
    ax = fig.add_subplot(2, 2, 2)
    k = [(0, 104, 106.5, 102.5, 105.5), (1, 105.5, 108.8, 105, 108.2), (2, 108.2, 109, 106.5, 107.2), (3, 107.2, 109.2, 107, 108.6),
         (4, 108.6, 108.8, 105.8, 106.4), (5, 106.4, 108, 104.5, 105.2), (6, 105.2, 106.5, 102, 102.8), (7, 102.8, 104.5, 101.2, 102),
         (8, 102, 104.8, 101.8, 104.2), (9, 104.2, 107.5, 103.5, 106.8), (10, 106.8, 109.5, 106, 109), (11, 109, 109.3, 107, 107.6),
         (12, 107.6, 108.5, 104.8, 105.5), (13, 105.5, 107, 101.8, 102.5), (14, 102.5, 104.5, 101.5, 102.2), (15, 102.2, 105.8, 101.8, 105.2),
         (16, 105.2, 109.2, 104.8, 108.6), (17, 108.6, 109, 106.2, 106.8), (18, 106.8, 108, 104.2, 105), (19, 105, 106.5, 102.2, 103)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c, width=0.5)
    hl_line(ax, -0.8, 20, 109.4, color=UP, lw=1.3)
    hl_line(ax, -0.8, 20, 101.4, color=DOWN, lw=1.3)
    ax.plot([-0.8, 20], [105.4, 105.4], color=GRAY, ls=":", lw=1.1)
    mark(ax, 2.6, 110.4, "上边界：3 次测试\n反应明显", color=UP, fs=8.5, box=True)
    mark(ax, 13, 100.3, "下边界：3 次测试\n边界区域窄", color=DOWN, fs=8.5, box=True, va="top")
    mark(ax, 10.5, 105.7, "EMA20 平坦、多次穿越", color=GRAY, fs=8.5)
    style_ax(ax, xlim=(-0.8, 20.5), ylim=(98.5, 112.5))
    ax.set_title("② 高质量边界：测试 ≥3 次 + 反应明显 + 区域窄（高密度区间）", fontsize=10.5, color=DARK)
    # 右下：低质量边界
    ax = fig.add_subplot(2, 2, 4)
    k = [(0, 103, 105.5, 101.5, 104.5), (1, 104.5, 107.5, 103.5, 106.8), (2, 106.8, 111, 106, 110.2), (3, 110.2, 112, 108, 108.8),
         (4, 108.8, 110, 105.5, 106.5), (5, 106.5, 109, 104, 108.2), (6, 108.2, 113.5, 107.5, 112.8), (7, 112.8, 113, 109.5, 110.5),
         (8, 110.5, 112, 106.5, 107.5), (9, 107.5, 110, 104.8, 105.5), (10, 105.5, 108.8, 103, 107.5), (11, 107.5, 111.5, 106.8, 110.8),
         (12, 110.8, 114.5, 110, 113.8), (13, 113.8, 114, 110, 111), (14, 111, 112.5, 106, 107.2), (15, 107.2, 110, 104.5, 105.8),
         (16, 105.8, 109, 103.2, 108.2), (17, 108.2, 112, 107.5, 111.2), (18, 111.2, 116, 110.5, 115.2), (19, 115.2, 115.5, 111, 112)]
    for x, o, h, l, c in k:
        candle(ax, x, o, h, l, c, width=0.5)
    hl_line(ax, -0.8, 20, 114.2, color=GRAY, lw=1.0, ls="--")
    hl_line(ax, -0.8, 20, 103.5, color=GRAY, lw=1.0, ls="--")
    mark(ax, 10, 117.6, "波段大小不一 + 方向偏移\n高点逐级抬高（不是典型区间）", color=ORANGE, fs=8.5, box=True)
    mark(ax, 2, 102.4, "测试不规律、影线穿透边界\n边界区域宽（低质量）", color=DOWN, fs=8.5, box=True, va="top")
    mark(ax, 18.5, 113.4, "边界被穿透", color=GRAY, fs=8)
    style_ax(ax, xlim=(-0.8, 20.5), ylim=(99, 119))
    ax.set_title("③ 低质量边界：测试 1-2 次 + 影线穿透 + 区域宽（低密度区间，谨慎/只等突破）", fontsize=10.5, color=DARK)
    fig.suptitle("区间密度判定与边界质量（Al Brooks）：先紧凑度后 CV——Barbwire 优先；高密度才在边界顺方向刮头皮，低密度只等突破", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p4_range_density.png")


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
