# -*- coding: utf-8 -*-
"""图 6-4R：止损后价格回来了——单笔 -1R 的懊悔与概率的真相（BTC 5 分钟，2026-07-18 ~ 07-19）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）+ data/_bt_ema_trades.csv 第 28 笔真实逐笔
案例（EMA20/50 系统 82 笔中的最大亏损单，R=-1.00，每笔风险 0.5%）：
- 07-18 20:00 入场 64218（多单）→ 21:00 止损 64025（-1R，止损距离 192.9 点）
- 21:10 low 63982.8 触止损；随后 00:50 收盘 64294 第一次回到入场价上方（约 4 小时后）
- 08:25 high 64906（+1.07%）、10:05 high 64967（+1.17%）= 07-19 全天最高
- 07-20 16:35 恐慌插针 low 63100：若扛单浮亏 = (64218-63100)/192.9 ≈ 5.8R（呼应图 2-4R）
教学点（6.5 被扫≠做错 + 6.4 期望值 + 7.2 处置效应）：
- 单笔止损看起来"错了"——白亏 1R 后价格涨回 +1.17%；但 82 笔 49 亏全被 -1R 锁死
- 不止损的代价不是"多赚 1.17%"，而是 07-20 浮亏 -5.8R（6 倍风险）的尾部
- 被扫 ≠ 做错：约 50% 被扫是陷阱；懊悔→报复→放弃规则才是真陷阱
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
RED = "#c62828"

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])

i0 = df["time"].searchsorted(pd.Timestamp("2026-07-18 19:00"))
i1 = df["time"].searchsorted(pd.Timestamp("2026-07-19 12:00"))
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

# 背景分段：入场前 / 持仓期 / 止损后
spans = [
    ("2026-07-18 19:00", "2026-07-18 20:00", TEAL, 0.06),
    ("2026-07-18 20:00", "2026-07-18 21:10", ORANGE, 0.16),
    ("2026-07-18 21:10", "2026-07-19 12:00", BLUE, 0.05),
]
for t0, t1, color, alpha in spans:
    ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)

# 入场价 / 止损位水平线
ax.axhline(64218.0, color=TEAL, lw=1.2, ls="--", zorder=2, alpha=0.9)
ax.text(pd.Timestamp("2026-07-18 19:05"), 64230, "入场 64218（多单）",
        fontsize=9, color=TEAL, ha="left", va="bottom")
ax.axhline(64025.15, color=RED, lw=1.4, ls="-", zorder=2, alpha=0.9)
ax.text(pd.Timestamp("2026-07-18 19:05"), 64012, "止损 64025（-1R）",
        fontsize=9, color=RED, ha="left", va="top")

marks = [
    ("2026-07-18 20:00", 64140, "20:00 入场\n64218", TEAL, -30, 30, 10),
    ("2026-07-18 21:08", 64100, "21:00 止损\n21:10 低 63982 触线\n-1R（0.5% 风险）", RED, -15, -110, 10),
    ("2026-07-19 00:50", 64300, "00:50 收盘 64294\n第一次回到入场价上方\n（止损后约 4 小时）", ORANGE, 0, -95, 10),
    ("2026-07-19 08:25", 64906, "08:25 高 64906\n+1.07%", UP, 25, -55, 10),
    ("2026-07-19 10:05", 64967, "10:05 全天最高 64967\n+1.17%——止损后\n一天内涨回 +1.2%", UP, -90, -45, 10),
]
for x, y, text, color, xoff, dy, fs in marks:
    ax.annotate(text, xy=(pd.Timestamp(x), y),
                xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                fontsize=fs, color=color, ha="center", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1))

# 插针提示（窗口外，用文字引 2-4R）
ax.text(pd.Timestamp("2026-07-19 11:50"), 63680,
        "次日 07-20 恐慌插针 63100：\n若扛单浮亏约 -5.8R（见图 2-4R）",
        fontsize=9.5, color=RED, ha="right", va="center", zorder=6,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=RED, lw=1.1))

ax.set_title("图 6-4R 止损后价格回来了——单笔 -1R 的懊悔与概率的真相（BTCUSDT 5m，2026-07-18 19:00 ~ 07-19 12:00）",
             fontsize=11, color=DARK, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.set_yticks([])
ax.set_xticks([])

# ---------- 下：成交量 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    axv.bar(t[i], v[i], width=pd.Timedelta(minutes=2.8), color=color, alpha=0.75, zorder=3)
axv.axhline(20, color=GRAY, lw=1.0, ls=":", zorder=2, alpha=0.8)
axv.annotate("常态量 ~19", xy=(pd.Timestamp("2026-07-18 19:05"), 20),
             xytext=(pd.Timestamp("2026-07-18 19:05"), 52),
             fontsize=9, color=GRAY, ha="center", va="center",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9))
for x, y, text, color, xoff, dy in [
    ("2026-07-18 21:10", 67, "21:00-21:10 放量下杀\n（V≈67 = 3.5×常态）", RED, -15, 30),
    ("2026-07-19 08:25", 60, "08:25 突破放量\nV≈60", UP, 20, 35),
]:
    axv.annotate(text, xy=(pd.Timestamp(x), y),
                 xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                 fontsize=9, color=color, ha="center", va="center", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=color, lw=0.9))
axv.set_title("成交量（21:00 止损当刻放量下杀；08:25 突破前高放量确认回升）", fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axv.spines[s].set_visible(False)
axv.set_yticks([])

# 底部时间刻度：每 2 小时
tick_ts = pd.date_range("2026-07-18 19:00", "2026-07-19 11:00", freq="2h")
axv.set_xticks(tick_ts)
axv.set_xticklabels([x.strftime("%m-%d %H:%M") for x in tick_ts], fontsize=8, color=GRAY)
axv.tick_params(length=0)

plt.savefig("handbook/images/fig_real_ch6_stoploss.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved handbook/images/fig_real_ch6_stoploss.png")
