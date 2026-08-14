# -*- coding: utf-8 -*-
"""图 1-1R：同样的追高，不同的杠杆，不同的死法（BTC 5 分钟，2026-06-30）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）
教学点：06-30 全天剧本——01:30 日高 60684（+1.4% 自开盘）→ 01:35 追多入场 60501（V=200）
→ 此后阴跌到 23:05 日低 58201（-3.80% 距入场）。四档实际杠杆的爆仓线（维持线口径：
爆仓距离 = 0.5 / 实际杠杆，与 1.5 正文"满仓 1:100 反向约 0.5% 触及维持线"一致）：
100x 线 60199（-0.5%）→ 02:50 触及爆仓（入场后 75 分钟）
50x  线 59896（-1.0%）→ 08:30 触及爆仓（V=143）
20x  线 58989（-2.5%）→ 20:20 放量触及爆仓（V=502，全天第 3 大）
10x  线 57476（-5.0%）→ 全天未触及（日低 -3.8%），但浮亏 -38% 账户权益
——同样的判断错误，杠杆只决定你死在哪一步；呼应 1.5 杠杆与爆仓数学、6.3 连亏/回撤
"""
import pandas as pd
import numpy as np
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
BLUE = "#1e3a6b"
RED2 = "#ef5350"
TEAL = "#00897b"

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])

i0 = df["time"].searchsorted(pd.Timestamp("2026-06-30 00:00"))
i1 = df["time"].searchsorted(pd.Timestamp("2026-06-30 23:55")) + 1
seg = df.iloc[i0:i1].reset_index(drop=True)
t = seg["time"].values
o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
v = seg["volume"].values

PREV_CLOSE = 59824.0     # 06-29 收盘
ENTRY = 60501.42         # 01:35 open（追多）
DAY_HIGH = 60683.84      # 01:30
DAY_LOW = 58201.0        # 23:05

# 爆仓线（维持线口径：爆仓距离 = 0.5 / 实际杠杆）
LIQ = {100: 60199.0, 50: 59896.0, 20: 58989.0, 10: 57476.0}

# 各杠杆"持仓存活"时间区间（入场 01:35 → 爆仓点 / 收盘）
t_entry = pd.Timestamp("2026-06-30 01:35")
liq_hit = {
    100: pd.Timestamp("2026-06-30 02:50"),
    50: pd.Timestamp("2026-06-30 08:30"),
    20: pd.Timestamp("2026-06-30 20:20"),
    10: pd.Timestamp("2026-06-30 23:55"),
}
liq_color = {100: RED2, 50: ORANGE, 20: BLUE, 10: TEAL}

fig, (ax, axv) = plt.subplots(
    2, 1, figsize=(15.8, 7.2), dpi=110, sharex=True,
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
    ("2026-06-30 00:00", "2026-06-30 01:30", ORANGE, 0.10),
    ("2026-06-30 01:30", "2026-06-30 08:30", RED2, 0.06),
    ("2026-06-30 08:30", "2026-06-30 20:20", BLUE, 0.05),
    ("2026-06-30 20:20", "2026-06-30 23:55", RED2, 0.10),
]
for t0, t1, color, alpha in spans:
    ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)

# 前收虚线
ax.axhline(PREV_CLOSE, color=GRAY, lw=1.1, ls="--", zorder=2, alpha=0.8)
ax.annotate("前收 59824", xy=(pd.Timestamp("2026-06-30 00:05"), PREV_CLOSE + 12),
            fontsize=9, color=GRAY, ha="left", va="bottom")

# 4 条爆仓线（从入场到各自爆仓/收盘）
for L in [100, 50, 20, 10]:
    y = LIQ[L]
    x0 = t_entry
    x1 = liq_hit[L]
    ax.plot([x0, x1], [y, y], color=liq_color[L], lw=1.7, ls="-", zorder=5)
    label = f"{L}x 线 {y:.0f}" + ("（未触及）" if L == 10 else "")
    ax.text(x1 + pd.Timedelta(minutes=8), y, label, fontsize=9, color=liq_color[L],
            ha="left", va="center", zorder=7)

# 入场标记（垂直短线 + 标注）
ax.plot([t_entry, t_entry], [ENTRY, DAY_HIGH + 60], color=ORANGE, lw=1.0, ls=":", zorder=5)

marks = [
    ("2026-06-30 01:30", DAY_HIGH, "01:30 日高 60684\n追多者在这里入场", UP, -40, 60, 11),
    ("2026-06-30 01:40", ENTRY, "01:35 追多 60501\nV=200 放量（FOMO）", ORANGE, 30, -55, 10),
    ("2026-06-30 02:50", LIQ[100], "02:50 100x 爆仓\n-0.5%（入场 75 分钟）", RED2, 55, -52, 10),
    ("2026-06-30 08:30", LIQ[50], "08:30 50x 爆仓\n-1.0%（V=143）", ORANGE, 130, 48, 10),
    ("2026-06-30 20:20", LIQ[20], "20:20 20x 爆仓\n-2.5%（V=502）", BLUE, -70, 48, 10),
    ("2026-06-30 21:30", 58381, "21:30 恐慌\nV=589 全天最大", DOWN, 40, -60, 10),
    ("2026-06-30 23:05", DAY_LOW, "23:05 日低 58201\n10x 未爆：浮亏 -38%", DOWN, -135, -58, 11),
]
for x, y, text, color, xoff, dy, fs in marks:
    ax.annotate(text, xy=(pd.Timestamp(x), y),
                xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                fontsize=fs, color=color, ha="center", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1))

ax.set_title("图 1-1R 同样的追高，不同的杠杆，不同的死法：四档实际杠杆的爆仓线画在同一根真实 K 线上（BTCUSDT 5m，2026-06-30，日高 60684 → 日低 58201，-3.8%）",
             fontsize=11, color=DARK, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.set_yticks([])
ax.set_xticks([])

# ---------- 下：成交量 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    axv.bar(t[i], v[i], width=pd.Timedelta(minutes=2.8), color=color, alpha=0.75, zorder=3)
for x, y, text, color, xoff, dy in [
    ("2026-06-30 01:37", 200, "追高 V=200", ORANGE, 25, -50),
    ("2026-06-30 08:32", 143, "50x 爆仓 V=143", ORANGE, 60, -50),
    ("2026-06-30 20:22", 502, "20x 爆仓 V=502", BLUE, 55, -50),
    ("2026-06-30 21:32", 589, "恐慌 V=589", DOWN, 60, -50),
]:
    axv.annotate(text, xy=(pd.Timestamp(x), y),
                 xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                 fontsize=9, color=color, ha="center", va="center", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=color, lw=0.9))
axv.set_title("成交量（追高 V=200、20x 爆仓 V=502、恐慌 V=589 为全天前三放量；50x 爆仓 V=143）",
              fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axv.spines[s].set_visible(False)
axv.set_yticks([])

tick_ts = pd.date_range("2026-06-30 02:00", "2026-06-30 22:00", freq="4h")
axv.set_xticks(tick_ts)
axv.set_xticklabels([x.strftime("%H:%M") for x in tick_ts], fontsize=8, color=GRAY)
axv.tick_params(length=0)

plt.savefig("handbook/images/fig_real_ch1_liquidation.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved")
