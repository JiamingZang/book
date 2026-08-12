# -*- coding: utf-8 -*-
"""
P3-6 真实行情数据图（用 AkShare 拉取上证指数 sh000001 真实日线）
三张图对应三个教学场景，全部标注「品种 + 日期 + 数据源」：
- fig_real_trend.png   上升趋势 + 回调入场 + 止损纪律（4.3 系统一真实案例）
- fig_real_range.png   区间 -> 假突破 -> 真突破（4.4 系统二真实案例）
- fig_real_climax.png  极速下跌 + V 型反转（3.9 V 顶/V 底真实案例）

运行：python _real_figs.py
数据源：AkShare stock_zh_index_daily(symbol="sh000001")（东方财富）
风格对齐 draw_handbook_figs.py：TradingView 白底，红=下跌(239,83,80) 青=上涨(38,166,154)
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyArrowPatch
import akshare as ak

sys.stdout.reconfigure(encoding="utf-8")

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

UP = "#26a69a"
DOWN = "#ef5350"
TEAL = "#26a69a"
DARK = "#263238"
GRAY = "#90a4ae"
ORANGE = "#ff9800"
BLUE = "#42a5f5"

OUT = "handbook/images"


def load_index(d0, d1):
    """拉取上证指数日线并截取区间，返回 (dates, open, high, low, close)"""
    df = ak.stock_zh_index_daily(symbol="sh000001")
    df["date"] = df["date"].astype(str)
    df = df[(df["date"] >= d0) & (df["date"] <= d1)].reset_index(drop=True)
    return (df["date"].tolist(), df["open"].to_numpy(), df["high"].to_numpy(),
            df["low"].to_numpy(), df["close"].to_numpy())


def candle(ax, x, o, h, l, c, width=0.6, alpha=1.0):
    up = c >= o
    color = UP if up else DOWN
    ax.plot([x, x], [l, h], color=color, linewidth=1.0, alpha=alpha, zorder=3)
    body = abs(c - o)
    if body < 1e-6:
        ax.plot([x - width / 2, x + width / 2], [c, c], color=color, linewidth=1.6, zorder=4, alpha=alpha)
    else:
        ax.add_patch(Rectangle((x - width / 2, min(o, c)), width, body,
                               facecolor=color, edgecolor=color, alpha=alpha, zorder=4))
    return up


def hline(ax, x0, x1, y, color=TEAL, ls="--", lw=1.3):
    ax.plot([x0, x1], [y, y], color=color, ls=ls, lw=lw, zorder=2)


def annotate(ax, text, xy, xytext, color=DARK, fontsize=9.5, arrowstyle="-|>", lw=1.1):
    ax.annotate(text, xy=xy, xytext=xytext,
                arrowprops=dict(arrowstyle=arrowstyle, color=color, lw=lw),
                color=color, fontsize=fontsize, zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, alpha=0.9, lw=0.8))


def setup_axes(ax, dates, title, sub):
    n = len(dates)
    ax.set_xlim(-2, n + 2)
    ax.set_title(title, fontsize=13, color=DARK, pad=12)
    ticks = list(range(0, n, 5)) + [n - 1]
    ax.set_xticks(ticks)
    ax.set_xticklabels([dates[i][5:] for i in ticks], fontsize=8.5, color=GRAY)
    ax.grid(axis="y", color="#e0e0e0", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRAY)
    ax.text(0.005, 0.005, sub, transform=ax.transAxes, fontsize=8.5,
            color=GRAY, va="bottom", ha="left")


def fig_a():
    """上升趋势 + 回调入场 + 止损纪律（4.3）"""
    dates, o, h, l, c = load_index("2026-04-22", "2026-06-25")
    n = len(dates)
    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    for i in range(n):
        candle(ax, i, o[i], h[i], l[i], c[i])

    # 趋势线：4-24 低点 4061.1 -> 5-22 低点 4067.7
    i_low1, i_low2 = dates.index("2026-04-24"), dates.index("2026-05-22")
    ax.plot([i_low1, i_low2], [l[i_low1], l[i_low2]], color=TEAL, lw=1.5, ls="--", zorder=2)

    # 上升腿 1
    i_hh = dates.index("2026-05-14")
    annotate(ax, "上升腿 1：4061 → 4259（+4.9%）", xy=(i_hh, h[i_hh]),
             xytext=(i_low1 + 6, 4265), color=TEAL)
    # 回调
    annotate(ax, "HH 4258.9（5-14）", xy=(i_hh, h[i_hh]), xytext=(i_hh - 1, 4278), color=TEAL)
    annotate(ax, "回调：6 天 -4%", xy=(dates.index("2026-05-18"), o[dates.index("2026-05-18")]),
             xytext=(dates.index("2026-05-12"), 4130), color=ORANGE)
    # 入场：5-22 下影阳线
    i_ent = dates.index("2026-05-22")
    annotate(ax, "回调入场：5-22 下影阳线（pin bar）\n收盘 4113 确认", xy=(i_ent, c[i_ent]),
             xytext=(i_ent - 2, 4095), color=BLUE)
    # 止损线
    i_stop = dates.index("2026-05-28")
    hline(ax, 0, n - 1, 4060, color=DOWN, ls=":", lw=1.2)
    annotate(ax, "止损 4060（回调低点下方）", xy=(i_stop, 4059), xytext=(i_stop - 8, 3990), color=DOWN)
    # 目标
    hline(ax, 0, n - 1, 4258.9, color=TEAL, ls=":", lw=1.2)
    annotate(ax, "目标：前高 4258.9（≈2.5R）", xy=(i_hh, 4258.9), xytext=(i_hh + 5, 4292), color=TEAL)

    ax.text(0.985, 0.02, "结局：5-28 止损触发（约 -1R）——\n入场正确，但这次趋势没有延续；\n止损纪律把失败限制在 1R",
            transform=ax.transAxes, fontsize=9, color=DARK, ha="right", va="bottom",
            bbox=dict(boxstyle="round,pad=0.4", fc="#fff8e1", ec=ORANGE, lw=1))
    setup_axes(ax, dates, "图 A（真实数据）上证指数日线：上升趋势 → 回调入场 → 止损纪律",
               "数据源：AkShare 上证指数 sh000001 日线，2026-04-22 ~ 2026-06-25")
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig_real_trend.png", dpi=150)
    plt.close(fig)
    print("saved fig_real_trend.png")


def fig_b():
    """区间 -> 假突破 -> 真突破（4.4）"""
    dates, o, h, l, c = load_index("2025-08-25", "2025-11-14")
    n = len(dates)
    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    for i in range(n):
        candle(ax, i, o[i], h[i], l[i], c[i])

    # 区间框：上沿 3940 / 下沿 3800
    ax.axhspan(3800, 3940, color=TEAL, alpha=0.05, zorder=1)
    hline(ax, 0, n - 1, 3940, color=TEAL, lw=1.4)
    hline(ax, 0, n - 1, 3800, color=TEAL, lw=1.4)
    ax.text(0.6, 3962, "区间上沿 3940", fontsize=9.5, color=TEAL, va="bottom")
    ax.text(0.6, 3780, "区间下沿 3800", fontsize=9.5, color=TEAL, va="top")

    # 9-04 假突破
    i_fb = dates.index("2025-09-04")
    annotate(ax, "假突破：插破下沿到 3733\n随后收回区间（sweep）", xy=(i_fb, l[i_fb]),
             xytext=(i_fb - 1.5, 3720), color=ORANGE)
    # 10-13 精确测试
    i_t = dates.index("2025-10-13")
    annotate(ax, "下沿精确测试 3800.1 不破\n→ 当日大阳反弹（+2.3%）", xy=(i_t, l[i_t]),
             xytext=(i_t - 8, 3860), color=BLUE)
    # 10-27 真突破
    i_br = dates.index("2025-10-27")
    annotate(ax, "真突破：大阳收盘 3997\n站上上沿（放量）", xy=(i_br, c[i_br]),
             xytext=(i_br - 4, 3985), color=UP)
    # 11-03 回测
    i_rt = dates.index("2025-11-03")
    annotate(ax, "突破后回测上沿 3937 不破\n= 二次确认（高质量入场）", xy=(i_rt, l[i_rt]),
             xytext=(i_rt + 3, 3920), color=UP)
    # 11-14 新高
    i_nh = dates.index("2025-11-14")
    annotate(ax, "突破后新高 4034", xy=(i_nh, h[i_nh]), xytext=(i_nh - 1, 4046), color=TEAL)

    setup_axes(ax, dates, "图 B（真实数据）上证指数日线：区间 → 假突破 → 真突破",
               "数据源：AkShare 上证指数 sh000001 日线，2025-08-25 ~ 2025-11-14")
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig_real_range.png", dpi=150)
    plt.close(fig)
    print("saved fig_real_range.png")


def fig_c():
    """极速下跌 + V 型反转（3.9）"""
    dates, o, h, l, c = load_index("2026-03-06", "2026-04-23")
    n = len(dates)
    fig, ax = plt.subplots(figsize=(12.5, 6.8))
    for i in range(n):
        candle(ax, i, o[i], h[i], l[i], c[i])

    # 阶段高点参考线
    i_top = dates.index("2026-03-12")
    hline(ax, 0, n - 1, 4141.6, color=GRAY, ls=":", lw=1.2)
    ax.text(0.5, 4156, "下跌起点 4141.6（3-12）", fontsize=9, color=GRAY)

    # 极速下跌
    i_d0, i_d1 = dates.index("2026-03-13"), dates.index("2026-03-23")
    ax.annotate("", xy=(i_d1, l[i_d1]), xytext=(i_d0, h[i_d0]),
                arrowprops=dict(arrowstyle="-|>", color=DOWN, lw=1.8), zorder=5)
    annotate(ax, "极速下跌：7 天 -8%（阴线连排）", xy=(i_d0 + 3, 3960),
             xytext=(i_d0 + 5, 4010), color=DOWN)
    # 卖出高潮
    annotate(ax, "卖出高潮：恐慌大阴线\n低点 3794.7（3-23）", xy=(i_d1, l[i_d1]),
             xytext=(i_d1 - 2.5, 3835), color=ORANGE)
    # V 型反弹
    i_r1 = dates.index("2026-04-01")
    annotate(ax, "V 型反弹第一波：+4.2%", xy=(i_r1, h[i_r1]), xytext=(i_r1 + 2, 3968), color=UP)
    # 二次探底
    i_r2 = dates.index("2026-04-03")
    annotate(ax, "二次探底 3871：不破前低\n= 更高低点（反转确认）", xy=(i_r2, l[i_r2]),
             xytext=(i_r2 - 9, 3895), color=BLUE)
    # 4-08 突破
    i_br = dates.index("2026-04-08")
    annotate(ax, "大阳 +2.7% 突破反弹高点\n= 反转确立", xy=(i_br, c[i_br]),
             xytext=(i_br + 1, 4000), color=UP)
    # 完成
    i_end = dates.index("2026-04-23")
    annotate(ax, "反转完成：回补下跌起点 4115", xy=(i_end, h[i_end]),
             xytext=(i_end - 6, 4118), color=TEAL)

    setup_axes(ax, dates, "图 C（真实数据）上证指数日线：极速下跌 → V 型反转",
               "数据源：AkShare 上证指数 sh000001 日线，2026-03-06 ~ 2026-04-23")
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig_real_climax.png", dpi=150)
    plt.close(fig)
    print("saved fig_real_climax.png")


if __name__ == "__main__":
    fig_a()
    fig_b()
    fig_c()
    print("done")
