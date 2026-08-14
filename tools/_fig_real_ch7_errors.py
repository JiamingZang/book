# -*- coding: utf-8 -*-
"""图 7-2R：心态错误的地图——一个真实下跌日里，七个错误会出现在哪里（BTC 5 分钟，2026-07-13）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）
教学点：07-13 全天剧本——08:15 放量冲高 64425（接近前高 64464，追多者入场 = FOMO）
→ 08:40 放量下杀 63568（突破失败确认，破位不走 = 损失厌恶）
→ 09:00-14:00 阴跌 700 点（只找支撑 = 确认偏差）
→ 15:30 反抽 63207 无力（"回到成本价就走" = 锚定/处置效应）
→ 20:45 跌破前低（"跌这么多该反弹了"抄底 = 近因偏差）
→ 21:40 越跌越买摊平（= 承诺升级）→ 22:15 恐慌最低 62101（较日高 -3.6%，割肉/摊平最重）
——一天可以犯完七个错误，账户从 64425 扛到 62101；正确动作只有 08:40 破位确认就走
——呼应 7.2 行为金融七个错误、7.6 军规第 2/6/7 条、2-4R 恐慌高潮
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
BLUE = "#1e3a6b"
RED2 = "#ef5350"

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])

i0 = df["time"].searchsorted(pd.Timestamp("2026-07-13 07:00"))
i1 = df["time"].searchsorted(pd.Timestamp("2026-07-13 23:55")) + 1
seg = df.iloc[i0:i1].reset_index(drop=True)
t = seg["time"].values
o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
v = seg["volume"].values

PREV_CLOSE = 64176.0
DAY_HIGH = 64425.0
DAY_LOW = 62101.0

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
    ("2026-07-13 07:00", "2026-07-13 08:15", BLUE, 0.06),
    ("2026-07-13 08:15", "2026-07-13 08:40", ORANGE, 0.15),
    ("2026-07-13 08:40", "2026-07-13 14:00", RED2, 0.06),
    ("2026-07-13 14:00", "2026-07-13 17:00", ORANGE, 0.10),
    ("2026-07-13 17:00", "2026-07-13 20:35", BLUE, 0.05),
    ("2026-07-13 20:35", "2026-07-13 22:15", RED2, 0.12),
    ("2026-07-13 22:15", "2026-07-13 23:55", BLUE, 0.05),
]
for t0, t1, color, alpha in spans:
    ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)

# 前收虚线
ax.axhline(PREV_CLOSE, color=GRAY, lw=1.2, ls="--", zorder=2, alpha=0.9)
ax.annotate("前收 64176", xy=(pd.Timestamp("2026-07-13 07:05"), PREV_CLOSE + 12),
            fontsize=9, color=GRAY, ha="left", va="bottom")

marks = [
    ("2026-07-13 08:15", 64425, "08:15 放量冲高 64425\n接近前高 64464 → 追多\n= FOMO（5）怕错过", UP, -30, 55, 11),
    ("2026-07-13 08:40", 63568, "08:40 放量下杀 63568\n突破失败确认 = 止损信号\n不走：错误从这里开始", DOWN, 20, -100, 10),
    ("2026-07-13 11:00", 62741, "09:00-14:00 阴跌 700 点\n死扛 + 只找支撑\n= 损失厌恶（1）+ 确认偏差（4）", DOWN, 30, -95, 10),
    ("2026-07-13 15:30", 63207, "15:30 反抽 63207 无力\n“回到成本价 64425 就走”\n= 锚定（6）+ 处置效应（2）", ORANGE, 60, 70, 10),
    ("2026-07-13 20:45", 62584, "20:45 跌破前低\n“跌这么多该反弹了”抄底\n= 近因偏差（3）", DOWN, 10, -95, 10),
    ("2026-07-13 21:40", 62256, "21:40 越跌越买摊平\n= 承诺升级（7）", DOWN, -20, -110, 10),
    ("2026-07-13 22:15", 62101, "22:15 恐慌最低 62101\n较日高 -3.6%\n割肉/摊平仓位最重", DOWN, 50, -60, 11),
]
for x, y, text, color, xoff, dy, fs in marks:
    ax.annotate(text, xy=(pd.Timestamp(x), y),
                xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                fontsize=fs, color=color, ha="center", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1))

ax.set_title("图 7-2R 心态错误的地图：一个真实下跌日里，七个错误会出现在哪里（BTCUSDT 5m，2026-07-13，日高 64425 → 日低 62101，-3.6%）",
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
    ("2026-07-13 08:12", 167, "冲高 V=167", UP, -15, -55),
    ("2026-07-13 08:42", 211, "破位 V=211", DOWN, 20, -55),
    ("2026-07-13 21:42", 419, "恐慌 V=419", DOWN, 60, -55),
    ("2026-07-13 22:17", 420, "V=420", DOWN, 30, 30),
]:
    axv.annotate(text, xy=(pd.Timestamp(x), y),
                 xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                 fontsize=9, color=color, ha="center", va="center", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=color, lw=0.9))
axv.set_title("成交量（冲高/破位/恐慌三处放量，恐慌段 V=419/420 为全天最大）", fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axv.spines[s].set_visible(False)
axv.set_yticks([])

tick_ts = pd.date_range("2026-07-13 08:00", "2026-07-13 22:00", freq="2h")
axv.set_xticks(tick_ts)
axv.set_xticklabels([x.strftime("%H:%M") for x in tick_ts], fontsize=8, color=GRAY)
axv.tick_params(length=0)

plt.savefig("handbook/images/fig_real_ch7_errors.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved")
