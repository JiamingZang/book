# -*- coding: utf-8 -*-
"""图 1-4R：下跌趋势中的尖峰陷阱 → 扫损 → 加速下跌（BTC 5 分钟，2026-07-27 ~ 07-28）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）
教学点：下跌趋势（18:40 65410 → 21:25 64913）中 21:30-21:45 连续 3 根放量大阳尖峰
（21:25 低点 64913 → 尖峰顶 65718，+1.19%）→ 21:50 第一根反向大阴拒绝 → 22:40 跌破
尖峰起点 64947 扫损（-1.9%）→ 01:35 回测尖峰起点=逃命点 → 06:40 放量破位 → 09:05
最低 63059，距尖峰顶 -4.05%——呼应 1.13 加密高波动（日内 5-10% 常见）、2.11 高潮后
别追、5.6 sweep
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

UP = "#e53935"      # 涨（红）
DOWN = "#26a69a"    # 跌（绿）
GRAY = "#90a4ae"
DARK = "#263238"
ORANGE = "#ef6c00"
TEAL = "#00897b"
BLUE = "#1e3a6b"

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])

i0 = df["time"].searchsorted(pd.Timestamp("2026-07-27 18:30"))
i1 = df["time"].searchsorted(pd.Timestamp("2026-07-28 09:30"))
seg = df.iloc[i0:i1].reset_index(drop=True)
t = seg["time"].values
o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
v = seg["volume"].values

fig, (ax, axv) = plt.subplots(
    2, 1, figsize=(15.8, 7.0), dpi=110, sharex=True,
    gridspec_kw={"height_ratios": [3.0, 1.0], "hspace": 0.05})

# ---------- 上：K 线 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    ax.plot([t[i], t[i]], [l[i], h[i]], color=color, lw=1.0, zorder=3)
    lo, hi = min(o[i], c[i]), max(o[i], c[i])
    ax.add_patch(plt.Rectangle((t[i] - pd.Timedelta(minutes=1.4), lo),
                               pd.Timedelta(minutes=2.8), max(hi - lo, 1),
                               facecolor=color, edgecolor=color, lw=0.4, zorder=4))

spans = [
    ("2026-07-27 18:30", "2026-07-27 21:30", BLUE, 0.06),
    ("2026-07-27 21:30", "2026-07-27 21:50", ORANGE, 0.16),
    ("2026-07-27 21:50", "2026-07-27 22:45", "#ef5350", 0.10),
    ("2026-07-27 22:45", "2026-07-28 01:40", BLUE, 0.05),
    ("2026-07-28 01:40", "2026-07-28 06:40", BLUE, 0.04),
    ("2026-07-28 06:40", "2026-07-28 09:30", "#ef5350", 0.08),
]
for t0, t1, color, alpha in spans:
    ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)

# 尖峰起点水平线 64947.6（21:25 收盘）
ax.axhline(64947.6, color=GRAY, lw=1.0, ls=":", zorder=2, alpha=0.9)

# 尖峰顶水平线 65718
ax.axhline(65718.0, color=ORANGE, lw=1.0, ls=":", zorder=2, alpha=0.7)

marks = [
    ("2026-07-27 19:30", 65480, "下跌趋势：18:40 高点 65410 →\n持续阴跌到 21:25 低点 64913\n尖峰只是趋势中的反弹", GRAY, 0, 30, 10),
    ("2026-07-27 21:10", 65660, "尖峰：连续 3 根大阳\n21:25 起 +1.2% 放量冲高", UP, 0, 40, 11),
    ("2026-07-27 21:55", 65740, "尖峰顶 65718", UP, 30, 90, 11),
    ("2026-07-27 22:20", 64380, "22:40 跌破尖峰起点\n追高者止损被扫（-1.9%）", DOWN, -10, -60, 10),
    ("2026-07-28 01:35", 65280, "回测尖峰起点 65090\n= 逃命点 / 新空头入场", ORANGE, 0, 60, 10),
    ("2026-07-28 06:00", 64200, "06:40 放量破位", DOWN, 0, 120, 10),
    ("2026-07-28 09:05", 63070, "最低 63059\n距尖峰顶 -4.05%", DOWN, 30, -110, 11),
]
for x, y, text, color, xoff, dy, fs in marks:
    ax.annotate(text, xy=(pd.Timestamp(x), y),
                xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                fontsize=fs, color=color, ha="center", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1))

ax.set_title("图 1-4R 下跌趋势中的尖峰陷阱 → 扫损 → 加速下跌（BTCUSDT 5m，2026-07-27 18:30 ~ 07-28 09:30）",
             fontsize=11, color=DARK, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.set_yticks([])
ax.set_xticks([])

# ---------- 下：成交量 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    axv.bar(t[i], v[i], width=pd.Timedelta(minutes=2.8), color=color, alpha=0.75, zorder=3)
axv.axhline(45, color=GRAY, lw=1.0, ls=":", zorder=2, alpha=0.8)
axv.annotate("常态量 30-70", xy=(pd.Timestamp("2026-07-27 18:50"), 45),
             xytext=(pd.Timestamp("2026-07-27 18:50"), 120),
             fontsize=9, color=GRAY, ha="center", va="center",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9))
for x, y, text, color, xoff, dy in [
    ("2026-07-27 21:40", 200, "尖峰放量\nV≈110-200", UP, 10, 60),
    ("2026-07-28 07:00", 269, "破位放量\nV≈200-320", DOWN, 90, 40),
    ("2026-07-28 09:05", 304, "V≈305", DOWN, 40, -60),
]:
    axv.annotate(text, xy=(pd.Timestamp(x), y),
                 xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                 fontsize=9, color=color, ha="center", va="center", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=color, lw=0.9))
axv.set_title("成交量（小时级脉冲：尖峰与破位都是放量的）", fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axv.spines[s].set_visible(False)
axv.set_yticks([])

# 底部时间刻度：每 2 小时
tick_ts = pd.date_range("2026-07-27 19:00", "2026-07-28 09:00", freq="2h")
axv.set_xticks(tick_ts)
axv.set_xticklabels([x.strftime("%H:%M") for x in tick_ts], fontsize=8, color=GRAY)
axv.tick_params(length=0)

plt.savefig("handbook/images/fig_real_ch1_spike_sweep.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved")
