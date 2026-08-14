# -*- coding: utf-8 -*-
"""图 2-4R：恐慌抛售高潮 → 插针收回 → V 型反转（BTC 5 分钟，2026-07-20）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）
教学点（2.11 尖峰与高潮的卖出镜像实证）：
- 白天阴跌 12:45 高 64734 → 16:20 低 64250（低点下移）
- 16:30 量突增 V≈1065（≈18×常态 57.5）但价只小跌 = 大单涌出
- 16:35 恐慌插针：V≈1912（≈33×常态）、低点 63100（-1.8%）、长下影 1172 点、收盘收回 871 点
  = 2.11 卖出高潮"长下尾锤子"形态；扫掉 07-18 低 63312 + 07-19 低 64091 = 假破位/空头陷阱
- 16:40-17:35 快速收复（40 分钟回到插针前水平）→ 19:30 放量确认 64810
- 23:50 日高 65667，23:55 收 65599（距低点 +3.96%）= 卖出高潮后 V 形反转
- ETH 16:35 同步插针（低 1854.3、V≈4×常态）= 市场级事件
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

i0 = df["time"].searchsorted(pd.Timestamp("2026-07-20 12:00"))
i1 = df["time"].searchsorted(pd.Timestamp("2026-07-20 23:55"))
seg = df.iloc[i0:i1].reset_index(drop=True)
t = seg["time"].values
o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
v = seg["volume"].values

fig, (ax, axv) = plt.subplots(
    2, 1, figsize=(15.8, 6.0), dpi=110, sharex=True,
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
    ("2026-07-20 12:00", "2026-07-20 16:20", BLUE, 0.05),
    ("2026-07-20 16:20", "2026-07-20 16:40", ORANGE, 0.18),
    ("2026-07-20 16:40", "2026-07-20 19:00", TEAL, 0.10),
    ("2026-07-20 19:00", "2026-07-20 23:55", TEAL, 0.06),
]
for t0, t1, color, alpha in spans:
    ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)

# 结构低点水平线（被扫）
ax.axhline(64091.0, color=GRAY, lw=1.0, ls=":", zorder=2, alpha=0.9)
ax.text(pd.Timestamp("2026-07-20 12:10"), 64105, "07-19 低 64091（被扫）",
        fontsize=9, color=GRAY, ha="left", va="bottom")
ax.axhline(63312.0, color=GRAY, lw=1.0, ls=":", zorder=2, alpha=0.9)
ax.text(pd.Timestamp("2026-07-20 12:10"), 63326, "07-18 低 63312（被扫）",
        fontsize=9, color=GRAY, ha="left", va="bottom")

marks = [
    ("2026-07-20 14:20", 64780, "阴跌走弱：12:45 高 64734\n→ 16:20 低 64250\n低点不断下移", GRAY, -30, 40, 10),
    ("2026-07-20 16:28", 64420, "16:30 量突增 V≈1065\n价格却只小跌 = 大单涌出", ORANGE, -15, 70, 10),
    ("2026-07-20 16:35", 63380, "16:35 恐慌插针：V≈1912（30 倍常态）\n低点 63100（-1.8%）、长下影 1172 点\n收盘收回 871 点——追空者成交在最低点", DOWN, 40, -60, 10),
    ("2026-07-20 17:20", 63980, "16:40-17:35 快速收复\n40 分钟回到插针前水平", TEAL, 0, -90, 10),
    ("2026-07-20 19:35", 64920, "19:30 放量确认 64810\n= V 反转成立", UP, 30, 40, 10),
    ("2026-07-20 23:35", 65420, "23:50 日高 65667\n23:55 收 65599（距低点 +3.96%）", UP, -60, -70, 10),
]
for x, y, text, color, xoff, dy, fs in marks:
    ax.annotate(text, xy=(pd.Timestamp(x), y),
                xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                fontsize=fs, color=color, ha="center", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1))

ax.set_title("图 2-4R 恐慌抛售高潮 → 插针收回 → V 型反转（BTCUSDT 5m，2026-07-20 12:00 ~ 23:55）",
             fontsize=11, color=DARK, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.set_yticks([])
ax.set_xticks([])

# ---------- 下：成交量 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    axv.bar(t[i], v[i], width=pd.Timedelta(minutes=2.8), color=color, alpha=0.75, zorder=3)
axv.axhline(60, color=GRAY, lw=1.0, ls=":", zorder=2, alpha=0.8)
axv.annotate("常态量 ~60", xy=(pd.Timestamp("2026-07-20 12:10"), 60),
             xytext=(pd.Timestamp("2026-07-20 12:10"), 140),
             fontsize=9, color=GRAY, ha="center", va="center",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9))
for x, y, text, color, xoff, dy in [
    ("2026-07-20 16:30", 1065, "V≈1065\n≈18×常态", ORANGE, -10, 40),
    ("2026-07-20 16:35", 1912, "V≈1912\n≈30×常态！", DOWN, 25, -70),
    ("2026-07-20 19:30", 284, "确认放量\nV≈284", TEAL, 20, 40),
]:
    axv.annotate(text, xy=(pd.Timestamp(x), y),
                 xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                 fontsize=9, color=color, ha="center", va="center", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=color, lw=0.9))
axv.set_title("成交量（16:30-16:35 恐慌量 = 全天峰值，其余时段常态）", fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axv.spines[s].set_visible(False)
axv.set_yticks([])

# 底部时间刻度：每 2 小时
tick_ts = pd.date_range("2026-07-20 12:00", "2026-07-20 23:00", freq="2h")
axv.set_xticks(tick_ts)
axv.set_xticklabels([x.strftime("%H:%M") for x in tick_ts], fontsize=8, color=GRAY)
axv.tick_params(length=0)

plt.savefig("handbook/images/fig_real_ch2_panic.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved handbook/images/fig_real_ch2_panic.png")
