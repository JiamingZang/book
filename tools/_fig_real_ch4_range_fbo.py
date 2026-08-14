# -*- coding: utf-8 -*-
"""图 4-2R：区间突破失败 → 下沿破位 → 加速下跌（BTC 5 分钟，2026-08-10 ~ 08-11）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）
教学点：横盘区间 64960-65100（1.5h）→ 20:00 突破上沿冲高 65238（追多者入场）
→ 3 根内跌回区间 = 假突破（FBO）→ 20:35 跌破下沿 → 21:30 放量加速下杀（V=310）
→ 22:40 反抽无力 = 逃命点 → 02:35 最低 63806（距突破高 -2.2%，区间高度的 3 倍）
——呼应 4.4"插破边界又收回=假突破，是区间交易者的朋友"、3.11 80-20 法则
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

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])

i0 = df["time"].searchsorted(pd.Timestamp("2026-08-10 17:30"))
i1 = df["time"].searchsorted(pd.Timestamp("2026-08-11 03:00"))
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
    ("2026-08-10 17:30", "2026-08-10 19:55", BLUE, 0.06),
    ("2026-08-10 19:55", "2026-08-10 20:15", ORANGE, 0.15),
    ("2026-08-10 20:15", "2026-08-10 21:30", "#ef5350", 0.06),
    ("2026-08-10 21:30", "2026-08-10 22:45", "#ef5350", 0.10),
    ("2026-08-10 22:45", "2026-08-11 03:00", BLUE, 0.05),
]
for t0, t1, color, alpha in spans:
    ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)

# 区间上沿/下沿
ax.axhline(65099.1, color=GRAY, lw=1.2, ls="--", zorder=2, alpha=0.9)
ax.axhline(64958.9, color=GRAY, lw=1.2, ls="--", zorder=2, alpha=0.9)

marks = [
    ("2026-08-10 18:15", 65140, "横盘区间 64960-65100\n1.5 小时 边界多次测试", BLUE, 0, 60, 11),
    ("2026-08-10 20:00", 65300, "突破上沿 65099\n冲高 65238 追多者入场", UP, 0, 60, 11),
    ("2026-08-10 20:15", 65020, "3 根内跌回区间\n= 假突破（FBO）", DOWN, 10, -90, 10),
    ("2026-08-10 20:40", 64820, "跌破下沿 64959\n区间被打破", DOWN, -5, -110, 10),
    ("2026-08-10 21:40", 64600, "21:30 放量下杀\nV=310 恐慌抛售", DOWN, 0, -90, 10),
    ("2026-08-10 22:35", 64900, "反抽无力 64888\n= 逃命点 / 新空头入场", ORANGE, 30, 80, 10),
    ("2026-08-11 01:50", 63950, "最低 63806\n距突破高 -2.2%\n= 区间高度的 3 倍", DOWN, 30, -90, 11),
]
for x, y, text, color, xoff, dy, fs in marks:
    ax.annotate(text, xy=(pd.Timestamp(x), y),
                xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                fontsize=fs, color=color, ha="center", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1))

ax.set_title("图 4-2R 区间突破失败 → 下沿破位 → 加速下跌（BTCUSDT 5m，2026-08-10 17:30 ~ 08-11 03:00）",
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
    ("2026-08-10 21:35", 310, "恐慌 V=310", DOWN, 30, -60),
    ("2026-08-10 23:20", 151, "破位续跌\nV=120-230", DOWN, 60, 50),
]:
    axv.annotate(text, xy=(pd.Timestamp(x), y),
                 xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                 fontsize=9, color=color, ha="center", va="center", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=color, lw=0.9))
axv.set_title("成交量（假突破时量不大，破位与加速时才真正放量）", fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axv.spines[s].set_visible(False)
axv.set_yticks([])

tick_ts = pd.date_range("2026-08-10 18:00", "2026-08-11 02:00", freq="2h")
axv.set_xticks(tick_ts)
axv.set_xticklabels([x.strftime("%H:%M") for x in tick_ts], fontsize=8, color=GRAY)
axv.tick_params(length=0)

plt.savefig("handbook/images/fig_real_ch4_range_fbo.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved")
