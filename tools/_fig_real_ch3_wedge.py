# -*- coding: utf-8 -*-
"""图 3-5R：上升楔形假突破 → 持续下跌（BTC 5 分钟，2026-08-11）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）
教学点：楔形收敛上推（三推渐高+低点渐高）→ 突破前高 64515 → 20 分钟跌回突破位=假突破
→ 楔形破位持续阴跌 6.5 小时到 63251（-2%）——呼应 3.9 楔形 75% 空头突破
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

UP = "#e53935"      # 涨（红）
DOWN = "#26a69a"    # 跌（绿）
GRAY = "#90a4ae"
DARK = "#263238"
ORANGE = "#ef6c00"
TEAL = "#00897b"
BLUE = "#1e3a6b"

def draw_panel(ax, i0, i1, title, marks, spans, trend_lines=()):
    seg = df.iloc[i0:i1].reset_index(drop=True)
    t = seg["time"].values
    o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
    for i in range(len(seg)):
        color = UP if c[i] >= o[i] else DOWN
        ax.plot([t[i], t[i]], [l[i], h[i]], color=color, lw=1.0, zorder=3)
        lo, hi = min(o[i], c[i]), max(o[i], c[i])
        ax.add_patch(plt.Rectangle((t[i] - pd.Timedelta(minutes=1.4), lo),
                                   pd.Timedelta(minutes=2.8), max(hi - lo, 1),
                                   facecolor=color, edgecolor=color, lw=0.4, zorder=4))
    for t0, t1, color, alpha in spans:
        ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)
    for x0, y0, x1, y1, color in trend_lines:
        ax.plot([pd.Timestamp(x0), pd.Timestamp(x1)], [y0, y1], color=color, lw=1.7,
                ls="--", zorder=5, alpha=0.9)
    for x, y, text, color, xoff, dy, fs in marks:
        ax.annotate(text, xy=(pd.Timestamp(x), y),
                    xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                    fontsize=fs, color=color, ha="center", va="center", zorder=6,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.1))
    ax.set_title(title, fontsize=11, color=DARK, loc="left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])

fig, ax = plt.subplots(1, 1, figsize=(15.5, 6.2), dpi=110)

i0 = df["time"].searchsorted(pd.Timestamp("2026-08-11 15:30"))
i1 = df["time"].searchsorted(pd.Timestamp("2026-08-12 03:20"))

spans = [
    ("2026-08-11 15:30", "2026-08-11 17:15", BLUE, 0.05),
    ("2026-08-11 17:15", "2026-08-11 20:00", BLUE, 0.09),
    ("2026-08-11 20:00", "2026-08-11 20:25", ORANGE, 0.13),
    ("2026-08-11 20:25", "2026-08-12 03:20", "#ef5350", 0.05),
]

trend_lines = [
    ("2026-08-11 18:05", 64312.7, "2026-08-11 19:55", 64400.0, ORANGE),
    ("2026-08-11 17:30", 64180.6, "2026-08-11 19:40", 64330.0, TEAL),
]

marks = [
    ("2026-08-11 15:30", 64300, "前期横盘 63800-64300\n突破前的\"位置背景\"", GRAY, 0, 300, 10),
    ("2026-08-11 18:05", 64312.7, "推1 64312", ORANGE, 40, 260, 11),
    ("2026-08-11 19:10", 64390.5, "推2 64390", ORANGE, 45, 260, 11),
    ("2026-08-11 19:55", 64400.0, "推3 动能最弱\n只比推2高10点", ORANGE, -75, 260, 10),
    ("2026-08-11 20:10", 64515.4, "突破 64515\n追多者入场", UP, 60, 220, 11),
    ("2026-08-11 20:22", 64316.0, "20分钟跌回突破位\n= 假突破（FBO）", DOWN, 55, -160, 10),
    ("2026-08-11 23:35", 63508.5, "楔形破位 持续阴跌", DOWN, -30, -180, 10),
    ("2026-08-12 02:40", 63251.6, "最低 63251\n累计 -2%", DOWN, 45, -140, 11),
]

draw_panel(ax, i0, i1,
           "图 3-5R 上升楔形假突破 → 持续下跌（BTCUSDT 5m，2026-08-11 15:30 ~ 08-12 03:20）",
           marks, spans, trend_lines)

fig.suptitle("", y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("handbook/images/fig_real_ch3_wedge.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved")
