# -*- coding: utf-8 -*-
"""BTC 1H 均线趋势跟踪真实图（第4章 4.27）
左：趋势段 07-01 21:00 ~ 07-05 09:00——价格 84 小时守在 EMA20 上方，回踩不破 = 入场
右：下跌段 07-31 09:00 ~ 08-02 09:00——价格 48 小时压在 EMA20 下方，反弹失败 = 入场
EMA20 蓝线、EMA50 橙线；红涨绿跌；右下角数据源。
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

RED, GREEN, GRAY = "#ef5350", "#26a69a", "#90a4ae"
BLUE, ORANGE, DARK = "#1565c0", "#ef6c00", "#263238"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False


def draw_candles(ax, seg, body_w=0.32):
    for _, r in seg.iterrows():
        o, h, l, c = r["open"], r["high"], r["low"], r["close"]
        t = r["time"]
        up = c >= o
        color = RED if up else GREEN
        ax.plot([t, t], [l, h], color=color, lw=0.8, zorder=2)
        ax.add_patch(plt.Rectangle((t - pd.Timedelta(minutes=body_w * 60), min(o, c)),
                                   pd.Timedelta(minutes=body_w * 120), abs(c - o) + 1e-9,
                                   facecolor=color, edgecolor=color, lw=0.5, zorder=3))


def fmt_ax(ax, title, src):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("价格 (USDT)", fontsize=10)
    ax.set_title(title, fontsize=12.5, color=DARK, pad=12)
    ax.text(0.995, -0.16, src, transform=ax.transAxes, ha="right", fontsize=8, color=GRAY)
    ax.grid(axis="y", color="#eceff1", lw=0.7)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)


df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
h1 = df.resample("1h", on="time").agg(
    open=("open", "first"), high=("high", "max"), low=("low", "min"),
    close=("close", "last"), volume=("volume", "sum")).dropna().reset_index()
h1["ema20"] = h1["close"].ewm(span=20, adjust=False).mean()
h1["ema50"] = h1["close"].ewm(span=50, adjust=False).mean()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6.5), dpi=110,
                               gridspec_kw={"wspace": 0.16})
fig.patch.set_facecolor("white")

# ============ 左：趋势段（价格在 EMA20 上方 84 小时） ============
seg1 = h1[(h1.time >= "2026-07-01 21:00") & (h1.time <= "2026-07-05 09:00")].reset_index(drop=True)
draw_candles(ax1, seg1)
ax1.plot(seg1["time"], seg1["ema20"], color=BLUE, lw=1.6, zorder=4, label="EMA20")
ax1.plot(seg1["time"], seg1["ema50"], color=ORANGE, lw=1.2, zorder=4, label="EMA50")

# 标注：均线定方向
ax1.annotate("07-01 21:00 起价格守在 EMA20 上方 84 小时\n= 多头趋势：只做多（4.27 用法 1）",
             xy=(pd.Timestamp("2026-07-01 21:00"), h1.loc[h1.time >= "2026-07-01 21:00", "close"].iloc[0]),
             xytext=(pd.Timestamp("2026-07-02 02:00"), seg1["high"].max() - 150),
             fontsize=9.5, color=BLUE, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#e3f2fd", edgecolor=BLUE, lw=1),
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))

# 找回踩 EMA20 的低点（HL）
dip = seg1[(seg1["low"] - seg1["ema20"]).abs() < 130]
if len(dip):
    d0 = dip.iloc[len(dip) // 2]
    ax1.annotate("回踩 EMA20 不破 + HL = 入场\n（均线定方向，结构定入场）",
                 xy=(d0["time"], d0["ema20"]),
                 xytext=(d0["time"] + pd.Timedelta(hours=8), d0["ema20"] - 260),
                 fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

ax1.legend(loc="lower right", fontsize=9)
fmt_ax(ax1, "BTC 1 小时：趋势段——价格 84 小时守在 EMA20 上方（2026-07-01 21:00 ~ 07-05 09:00）",
       "数据源：Binance BTCUSDT 1H K 线（5m 聚合）· 教学示意")

# ============ 右：下跌段（价格在 EMA20 下方 48 小时） ============
seg2 = h1[(h1.time >= "2026-07-31 09:00") & (h1.time <= "2026-08-02 09:00")].reset_index(drop=True)
draw_candles(ax2, seg2)
ax2.plot(seg2["time"], seg2["ema20"], color=BLUE, lw=1.6, zorder=4, label="EMA20")
ax2.plot(seg2["time"], seg2["ema50"], color=ORANGE, lw=1.2, zorder=4, label="EMA50")

ax2.annotate("07-31 09:00 起价格压在 EMA20 下方 48 小时\n= 空头趋势：只做空（反弹不追多）",
             xy=(pd.Timestamp("2026-07-31 09:00"), h1.loc[h1.time >= "2026-07-31 09:00", "close"].iloc[0]),
             xytext=(pd.Timestamp("2026-07-31 14:00"), seg2["high"].max() + 120),
             fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3e0", edgecolor=ORANGE, lw=1),
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

dip2 = seg2[(seg2["high"] - seg2["ema20"]).abs() < 130]
if len(dip2):
    d1 = dip2.iloc[len(dip2) // 2]
    ax2.annotate("反弹至 EMA20 失败 = 入场做空\n（LH 结构 + 均线压制）",
                 xy=(d1["time"], d1["ema20"]),
                 xytext=(d1["time"] - pd.Timedelta(hours=14), d1["ema20"] + 240),
                 fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

ax2.legend(loc="lower right", fontsize=9)
fmt_ax(ax2, "BTC 1 小时：下跌段——价格 48 小时压在 EMA20 下方（2026-07-31 09:00 ~ 08-02 09:00）",
       "数据源：Binance BTCUSDT 1H K 线（5m 聚合）· 教学示意")

fig.savefig("handbook/images/fig_real_ma.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_ma.png")
