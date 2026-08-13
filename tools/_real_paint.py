# -*- coding: utf-8 -*-
"""
matplotlib 手绘教学级 K 线图：真实 5m 数据 + 全可控标注
（箭头/文字框/水平线/通道/指标窗格/成交量副图），替代 lightweight-charts headless 截图。

用法: python -X utf8 tools/_real_paint.py
输出: handbook/images/fig_real_*.png（6 张）
"""
import csv, datetime, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "handbook", "images")

RED = "#ef5350"; GREEN = "#26a69a"; BLUE = "#1565c0"; ORANGE = "#ef6c00"
DARK = "#263238"; PURPLE = "#7b1fa2"; GRAY = "#90a4ae"


def load(path, t0=None, t1=None):
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = datetime.datetime.strptime(row["time"], "%Y-%m-%d %H:%M")
            if t0 and t < t0: continue
            if t1 and t > t1: continue
            rows.append({"t": t, "o": float(row["open"]), "h": float(row["high"]),
                         "l": float(row["low"]), "c": float(row["close"]),
                         "v": float(row["volume"])})
    return rows


def atr(rows, n=14):
    out = [None] * len(rows)
    prev_close = None
    trs = []
    for i, r in enumerate(rows):
        if prev_close is not None:
            tr = max(r["h"] - r["l"], abs(r["h"] - prev_close), abs(r["l"] - prev_close))
            trs.append(tr)
            if len(trs) > n: trs.pop(0)
            if len(trs) == n:
                out[i] = sum(trs) / n
        prev_close = r["c"]
    return out


def mm(dt):
    return datetime.datetime.strptime("2026-" + dt, "%Y-%m-%d %H:%M")


# ---------------- 绘图原语 ----------------

def plot_candles(ax, rows, xs, w=0.62):
    for x, r in zip(xs, rows):
        up = r["c"] >= r["o"]
        col = RED if up else GREEN
        ax.vlines(x, r["l"], r["h"], color=col, linewidth=1.0, zorder=2)
        lo, hi = min(r["o"], r["c"]), max(r["o"], r["c"])
        if hi - lo < 1e-9:
            ax.plot([x - w / 2, x + w / 2], [r["o"]] * 2, color=col, linewidth=1.4, zorder=2)
        else:
            ax.add_patch(plt.Rectangle((x - w / 2, lo), w, hi - lo,
                                       facecolor=col, edgecolor=col, linewidth=0.5, zorder=2))


def add_marker(ax, rows, xs, mtime, pos, color, text, dx=0, dy=0):
    """pos: 'above'/'below'；dx: x 偏移(根数)，dy: 额外价格偏移"""
    i = next(k for k, r in enumerate(rows) if r["t"] == mm(mtime))
    x = xs[i]; r = rows[i]
    ymin, ymax = ax.get_ylim()
    gap = (ymax - ymin) * 0.03
    if pos == "above":
        yt = r["h"] + gap + dy
        ax.annotate(text, xy=(x, r["h"]), xytext=(x + dx, yt),
                    ha="center", va="bottom", fontsize=10.5, color=DARK, zorder=5,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6,
                                    shrinkA=0, shrinkB=2),
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color,
                              lw=0.9, alpha=0.95))
    else:
        yt = r["l"] - gap - dy
        ax.annotate(text, xy=(x, r["l"]), xytext=(x + dx, yt),
                    ha="center", va="top", fontsize=10.5, color=DARK, zorder=5,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6,
                                    shrinkA=0, shrinkB=2),
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color,
                              lw=0.9, alpha=0.95))


def add_pricelines(ax, rows, pricelines):
    xmax = len(rows) - 1
    for price, color, text, dash in pricelines:
        ax.axhline(price, color=color, linestyle="--" if dash else "-",
                   linewidth=1.1, alpha=0.85, zorder=1)
        ax.text(xmax + 1.2, price, "%s %.1f" % (text, price), color=color,
                fontsize=9.5, va="center", ha="left", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color,
                          lw=0.8, alpha=0.95))


def add_overlay(ax, rows, xs, color, lw, dash, pts, label=None, atr_ax=None):
    """pts: [(时间str, value)]；label 非空则进图例；atr_ax 非空则画到独立窗格"""
    tmap = {r["t"]: i for i, r in enumerate(rows)}
    xx, yy = [], []
    for ts, v in pts:
        i = tmap.get(mm(ts))
        if i is not None and v is not None:
            xx.append(xs[i]); yy.append(v)
    target = atr_ax if atr_ax is not None else ax
    target.plot(xx, yy, color=color, linewidth=lw, linestyle="--" if dash else "-",
                alpha=0.95, zorder=3, label=label)


def set_time_ticks(ax, rows, xs):
    step = max(1, round(len(rows) / 6))
    ticks = list(range(0, len(rows), step))
    ax.set_xticks(xs[ticks])
    ax.set_xticklabels([rows[i]["t"].strftime("%m-%d %H:%M") for i in ticks],
                       fontsize=8.5, rotation=28, ha="right")


# ---------------- 总装配 ----------------

def draw(name, title, subtitle, rows,
         markers=None, pricelines=None, overlays=None, atr_panel=False):
    n = len(rows)
    xs = np.arange(n)
    fig = plt.figure(figsize=(14.8, 8.8))
    if atr_panel:
        gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 3.9, 1.2], hspace=0.12)
        axA = fig.add_subplot(gs[0]); ax = fig.add_subplot(gs[1], sharex=axA)
        axV = fig.add_subplot(gs[2], sharex=axA)
    else:
        gs = fig.add_gridspec(2, 1, height_ratios=[3.9, 1.2], hspace=0.12)
        ax = fig.add_subplot(gs[0]); axV = fig.add_subplot(gs[1], sharex=ax)
        axA = None
    fig.subplots_adjust(left=0.055, right=0.985, top=0.93, bottom=0.075)

    fig.suptitle(title, fontsize=15.5, fontweight="bold", x=0.013, ha="left", y=0.995)
    fig.text(0.013, 0.955, subtitle, fontsize=10, color="#546e7a", va="top", ha="left")

    plot_candles(ax, rows, xs)
    ax.grid(axis="y", color="#e2e8f0", linewidth=0.7, alpha=0.9)
    ax.set_ylabel("价格", fontsize=9)
    ax.tick_params(labelsize=9, colors="#37474f")
    ax.tick_params(labelbottom=False)
    ax.ticklabel_format(style="plain", axis="y")
    lo = min(r["l"] for r in rows); hi = max(r["h"] for r in rows)
    span = hi - lo
    ax.set_ylim(lo - span * 0.09, hi + span * 0.15)
    ax.set_xlim(-1.2, n + 11)

    if overlays:
        for o in overlays:
            color, lw, dash, pts = o[0], o[1], o[2], o[3]
            aax = axA if (len(o) > 4 and o[4] == "atr") else None
            label = o[5] if len(o) > 5 else None
            add_overlay(ax, rows, xs, color, lw, dash, pts, label, aax)
    if markers:
        for m in markers:
            add_marker(ax, rows, xs, m[0], m[1], m[2], m[3],
                       m[4] if len(m) > 4 else 0, m[5] if len(m) > 5 else 0)
    if pricelines:
        add_pricelines(ax, rows, pricelines)
    if ax.get_legend_handles_labels()[0]:
        ax.legend(loc="upper left", fontsize=9, framealpha=0.92)

    if axA is not None:
        axA.set_facecolor("#f5f8fd")
        axA.tick_params(labelsize=8, colors="#546e7a")
        axA.tick_params(labelbottom=False)
        axA.ticklabel_format(style="plain", axis="y")
        axA.set_ylabel("ATR(14)", fontsize=9)
        axA.grid(axis="y", color="#e2e8f0", linewidth=0.6, alpha=0.7)
        if axA.get_legend_handles_labels()[0]:
            axA.legend(loc="upper left", fontsize=9, framealpha=0.92)

    # 成交量副图
    vcols = [RED if r["c"] >= r["o"] else GREEN for r in rows]
    axV.bar(xs, [r["v"] for r in rows], width=0.72, color=vcols, alpha=0.5, zorder=2)
    axV.set_ylim(0, max(r["v"] for r in rows) * 1.2)
    axV.set_ylabel("成交量", fontsize=9)
    axV.grid(axis="y", color="#e2e8f0", linewidth=0.6, alpha=0.6)
    axV.tick_params(labelsize=8.5, colors="#37474f")
    axV.yaxis.set_major_formatter(FuncFormatter(lambda v, p: "%dk" % (v / 1000) if v >= 1000 else "%.0f" % v))
    set_time_ticks(axV, rows, xs)

    out = os.path.join(OUT, name + ".png")
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)
    print("OK", name, os.path.getsize(out), "bytes")


# ---------------- 各图定义（短而完整的教学剧情段） ----------------

BTC = os.path.join(DATA, "btcusdt_5m.csv")
ETH = os.path.join(DATA, "ethusdt_5m.csv")


def fig_eth_2leg():
    """图 2-1R：双底 → 第一腿 → 回调 → 第二腿 → 高位回落（BTC 07-14 晚）"""
    rows = load(BTC, mm("07-14 19:15"), mm("07-15 02:40"))
    mk = [
        ("07-14 19:20", "below", BLUE, "双底① 62762", -3, 0),
        ("07-14 20:05", "below", BLUE, "双底② 62780", 3, 0),
        ("07-14 21:20", "above", RED, "第一腿 64182", 0, 0),
        ("07-14 22:00", "below", ORANGE, "回调 63581", 2, 0),
        ("07-14 23:30", "above", RED, "第二腿 64966", 0, 0),
        ("07-15 01:10", "above", GREEN, "高位回落", 0, 0),
    ]
    pl = [(62780, BLUE, "双底支撑", False)]
    draw("fig_real_eth_2leg",
         "BTC/USDT 5 分钟：两段式移动（push-pull）",
         "Binance 真实数据 2026-07-14 19:15 ~ 07-15 02:40 · 90 根 5m K 线\n"
         "双底 62762/62780 → 第一腿 +2.2% → 回调 -0.9% → 第二腿 +2.2% → 高位回落",
         rows, markers=mk, pricelines=pl)


def fig_btc_range():
    """图 4-4R：区间边界双测 → 突破 → 高潮 → 回落（ETH 07-02 晚）"""
    rows = load(ETH, mm("07-02 15:30"), mm("07-03 00:15"))
    mk = [
        ("07-02 17:35", "above", ORANGE, "上沿① 1652", 0, 0),
        ("07-02 19:10", "above", ORANGE, "上沿② 1657", 0, 0),
        ("07-02 19:55", "below", BLUE, "下沿③ 1644", 0, 0),
        ("07-02 20:30", "above", RED, "突破 1669", 0, 0),
        ("07-02 22:10", "above", RED, "高潮 1725", 0, 0),
        ("07-03 00:00", "above", GREEN, "回落", 0, 0),
    ]
    pl = [(1657, ORANGE, "上沿", False), (1614, BLUE, "下沿", False)]
    draw("fig_real_btc_range",
         "ETH/USDT 5 分钟：区间边界测试与突破",
         "Binance 真实数据 2026-07-02 15:30 ~ 07-03 00:15 · 106 根 5m K 线\n"
         "上沿 1652/1657 双测 → 下沿 1644 回踩 → 突破 1669 → 高潮 1725（+4%）→ 回落",
         rows, markers=mk, pricelines=pl)


def fig_btc_day():
    """图 4-5R：突破生命周期——成功回踩 vs 失败深回调 → 第二腿（BTC 06-29）"""
    rows = load(BTC, mm("06-29 08:40"), mm("06-29 16:20"))
    mk = [
        ("06-29 11:25", "above", RED, "突破 60233", 0, 0),
        ("06-29 11:35", "below", BLUE, "回踩守住", 0, 0),
        ("06-29 13:10", "below", GREEN, "深回调 59392", 0, 0),
        ("06-29 14:15", "above", RED, "第二腿 60346", 0, 0),
    ]
    pl = [(59700, ORANGE, "区间上沿", False), (58900, BLUE, "区间下沿", False)]
    draw("fig_real_btc_day",
         "BTC/USDT 5 分钟：突破生命周期——成功与失败",
         "Binance 真实数据 2026-06-29 08:40 ~ 16:20 · 93 根 5m K 线\n"
         "区间 58900-59700 → 突破 60233 → 回踩守住 → 深回调 59392（失败，别反手）→ 第二腿 60346",
         rows, markers=mk, pricelines=pl)


def fig_btc_sweep():
    """图 5-1R：sweep → CHoCH → LH 反抽 → 新低（BTC 07-02 早）"""
    rows = load(BTC, mm("07-02 04:10"), mm("07-02 11:10"))
    mk = [
        ("07-02 06:20", "above", RED, "扫多单 61334", 0, 0),
        ("07-02 08:20", "below", GREEN, "跌破前低 CHoCH", -9, 0),
        ("07-02 08:40", "below", BLUE, "新低 59588", 9, 0),
        ("07-02 09:40", "above", PURPLE, "LH 反抽 60325", 0, 0),
    ]
    pl = [(59876, BLUE, "前低", True), (61334, ORANGE, "sweep 高点", True)]
    draw("fig_real_btc_sweep",
         "BTC/USDT 5 分钟：sweep → CHoCH → 下跌日",
         "Binance 真实数据 2026-07-02 04:10 ~ 11:10 · 85 根 5m K 线\n"
         "冲高 61334 扫多单止损 → 跌破前低 59876（CHoCH）→ LH 反抽 60325 → 新低 59588，全天 -2.8%",
         rows, markers=mk, pricelines=pl)


def fig_trailing_stop():
    """图 4-8：移动止损——HL 阶梯（结构法）vs ATR 通道（BTC 06-29 晚）"""
    rows = load(BTC, mm("06-29 22:10"), mm("06-30 02:35"))
    hl_marks = [("06-29 22:15", 59011.0), ("06-29 23:10", 59097.6), ("06-30 00:25", 59584.5)]
    # 结构法阶梯止损：HL 确认后抬到 HL 下方 40 点，只进不退
    step = []; cur = None; hli = 0
    for r in rows:
        t = r["t"].timestamp()
        while hli < len(hl_marks) and t >= mm(hl_marks[hli][0]).timestamp():
            cur = hl_marks[hli][1] - 40
            hli += 1
        if cur is not None:
            step.append((r["t"].strftime("%m-%d %H:%M"), cur))
    atrs = atr(rows)
    up = [(r["t"].strftime("%m-%d %H:%M"), r["c"] + 1.6 * a) for r, a in zip(rows, atrs) if a]
    dn = [(r["t"].strftime("%m-%d %H:%M"), r["c"] - 1.6 * a) for r, a in zip(rows, atrs) if a]
    ov = [
        (BLUE, 2, False, step, None, "结构阶梯止损（只进不退）"),
        (ORANGE, 1, True, up, None, "1.6×ATR 通道"),
        (ORANGE, 1, True, dn),
    ]
    mk = [
        ("06-29 22:15", "below", BLUE, "HL1 59011", -3, 0),
        ("06-29 23:10", "below", BLUE, "HL2 59097", 0, 0),
        ("06-30 00:25", "below", BLUE, "HL3 59584", 0, 0),
        ("06-30 01:30", "above", RED, "新高 60683", 0, 0),
    ]
    draw("fig_real_trailing_stop",
         "BTC/USDT 5 分钟：移动止损两种机制",
         "Binance 真实数据 2026-06-29 22:10 ~ 06-30 02:35 · 54 根 5m K 线\n"
         "HL 59011 → 59097 → 59584 逐级抬高：蓝色阶梯 = 结构移动法；橙色虚线 = 1.6×ATR 通道跟随",
         rows, overlays=ov, markers=mk)


def fig_atr():
    """图 6-3：ATR 波动率通道——平静 → 爆发（BTC 07-01 午后）"""
    rows = load(BTC, mm("07-01 15:00"), mm("07-01 23:15"))
    atrs = atr(rows)
    up = [(r["t"].strftime("%m-%d %H:%M"), r["c"] + 1.5 * a) for r, a in zip(rows, atrs) if a]
    dn = [(r["t"].strftime("%m-%d %H:%M"), r["c"] - 1.5 * a) for r, a in zip(rows, atrs) if a]
    atr_line = [(r["t"].strftime("%m-%d %H:%M"), a) for r, a in zip(rows, atrs) if a]
    ov = [
        (ORANGE, 1, True, up, None, "±1.5×ATR 通道"),
        (ORANGE, 1, True, dn),
        (PURPLE, 2, False, atr_line, "atr", "ATR(14)"),
    ]
    mk = [
        ("07-01 20:45", "below", BLUE, "平静期低点 58326", 0, 0),
        ("07-01 22:20", "above", RED, "爆发 60092", 0, 0),
    ]
    draw("fig_real_atr",
         "BTC/USDT 5 分钟：ATR 波动率通道",
         "Binance 真实数据 2026-07-01 15:00 ~ 23:15 · 100 根 5m K 线\n"
         "前 6 小时平静（ATR~97，通道窄）→ 21:00 后爆发（ATR~169，通道张开）；顶部紫色窗格 = ATR(14) 仪表盘",
         rows, overlays=ov, markers=mk, atr_panel=True)


# ---------------- main ----------------

FIGS = [fig_eth_2leg, fig_btc_range, fig_btc_day, fig_btc_sweep, fig_trailing_stop, fig_atr]

if __name__ == "__main__":
    for fn in FIGS:
        fn()
    print("done")
