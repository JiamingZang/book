# -*- coding: utf-8 -*-
"""图 2-3R 真实数据：尖峰 → 第二波衰竭 → 高潮 → 回调（BTC 1H，2026-07-14 ~ 07-16）
- 数据：Binance BTCUSDT 5m K 线重采样 1H（data/btcusdt_5m.csv）
- 上：1H K 线（红涨绿跌）+ 尖峰①高亮（7/14 20:00-23:00 四连阳 +3.0%，启动 K 线实体 6x 均值量 4.8x）
      + 第二波②高亮（7/15 20:00-23:00 涨幅递减 +0.67→+0.43→+0.04% = EGO 最后疯狂）
      + 高潮③（7/15 23:00 冲 65600 长上影小实体 + 次日阴线 = 衰竭三件套）
      + 回调标注（65600→63380 = -3.4%，回撤尖峰的 80% > 61.8% 失败线 → 转区间）
- 下：成交量柱（尖峰段红），启动量 3109 vs 第二波 1153 = 买方弹药腰斩（紧迫感衰竭的量能证据）
- 教学：2.11 尖峰五标准/高潮三件套/反弹容忍度的真实验证（合成图 2-14 的真实数据版）
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

UP, DOWN, GRAY, DARK, TEAL, ORANGE = "#e53935", "#26a69a", "#90a4ae", "#263238", "#00897b", "#ef6c00"
BLUE = "#1565c0"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"]).sort_values("time").set_index("time")
h1 = df.resample("1h").agg({"open": "first", "high": "max", "low": "min",
                            "close": "last", "volume": "sum"}).dropna().reset_index()

# 展示窗口：7/14 18:00 ~ 7/16 12:00
disp = h1[(h1["time"] >= "2026-07-14 18:00") & (h1["time"] <= "2026-07-16 12:00")].reset_index(drop=True)
t = disp["time"].values
o, h, l, c = disp["open"].values, disp["high"].values, disp["low"].values, disp["close"].values
v = disp["volume"].values

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), dpi=110, sharex=True,
                               gridspec_kw={"height_ratios": [3.2, 1], "hspace": 0.06})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：K 线 =====
for i in range(len(disp)):
    color = UP if c[i] >= o[i] else DOWN
    ax1.plot([t[i], t[i]], [l[i], h[i]], color=color, lw=1.0, zorder=3)
    lo, hi = min(o[i], c[i]), max(o[i], c[i])
    ax1.add_patch(plt.Rectangle((t[i] - pd.Timedelta(minutes=18), lo),
                                pd.Timedelta(minutes=36), max(hi - lo, 1),
                                facecolor=color, edgecolor=color, lw=0.5, zorder=4))

# 尖峰①背景（7/14 20:00 ~ 23:00）
ax1.axvspan(pd.Timestamp("2026-07-14 20:00"), pd.Timestamp("2026-07-14 23:30"),
            color=TEAL, alpha=0.10, zorder=1)
# 第二波②背景（7/15 20:00 ~ 23:30）
ax1.axvspan(pd.Timestamp("2026-07-15 20:00"), pd.Timestamp("2026-07-15 23:30"),
            color=ORANGE, alpha=0.12, zorder=1)
# 高潮后回落区（7/16 00:00 起）
ax1.axvspan(pd.Timestamp("2026-07-16 00:00"), pd.Timestamp("2026-07-16 12:00"),
            color=GRAY, alpha=0.08, zorder=1)

# 标注① 尖峰
ax1.annotate("尖峰①：7/14 20:00-23:00 四连阳 +3.0%\n启动 K 线实体 6×均值、量 4.8 倍\n（连续大实体/无重叠/短尾线/收盘创新高）",
             xy=(pd.Timestamp("2026-07-14 22:00"), 64744),
             xytext=(pd.Timestamp("2026-07-14 18:30"), 65350),
             fontsize=9, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 标注② 第二波衰竭
ax1.annotate("第二波②：涨幅递减\n+0.67% → +0.43% → +0.04%\n量能腰斩（启动 1837 vs 首波 3109）\n= 看似新突破，实为最后疯狂（EGO）",
             xy=(pd.Timestamp("2026-07-15 21:00"), 65577),
             xytext=(pd.Timestamp("2026-07-15 12:30"), 65300),
             fontsize=9, color=ORANGE, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

# 标注③ 高潮 K 线
ax1.annotate("高潮③：23:00 冲 65600\n收盘只 +0.04%（长上影小实体）\n+ 次日 00:00 阴线 = 衰竭三件套齐\n燃料烧完",
             xy=(pd.Timestamp("2026-07-15 23:00"), 65600),
             xytext=(pd.Timestamp("2026-07-15 22:10"), 64600),
             fontsize=9, color="#c62828", fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor="#c62828", lw=1),
             arrowprops=dict(arrowstyle="->", color="#c62828", lw=1.2))

# 回调标注
ax1.annotate("回调：65600 → 63380（-3.4%）\n= 回撤掉尖峰的 80%\n超过 61.8% 失败线 → 转区间",
             xy=(pd.Timestamp("2026-07-17 06:00"), 63950),
             xytext=(pd.Timestamp("2026-07-16 01:00"), 64350),
             fontsize=9, color=DARK, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))

ax1.axhline(63380, color=GRAY, lw=1, ls=":", zorder=2)
ax1.text(pd.Timestamp("2026-07-14 18:20"), 63430, "63380 = 高潮后低点（-3.4%）",
         fontsize=8.5, color=GRAY, zorder=6)

ax1.set_ylabel("BTC 价格（USD）", fontsize=10)
ax1.set_title("尖峰 → 第二波衰竭 → 高潮 → 回调：同一轮上涨的完整生命周期（BTC 1H，2026-07-14 ~ 07-16）",
              fontsize=13, color=DARK, pad=10)
ax1.set_ylim(62400, 66400)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# ===== 下：成交量 =====
vol_colors = [UP if c[i] >= o[i] else DOWN for i in range(len(disp))]
# 尖峰启动量高亮
for i in range(len(disp)):
    if disp["time"].iloc[i] in (pd.Timestamp("2026-07-14 20:00"), pd.Timestamp("2026-07-14 23:00")):
        vol_colors[i] = TEAL
    if disp["time"].iloc[i] in (pd.Timestamp("2026-07-15 20:00"), pd.Timestamp("2026-07-15 21:00")):
        vol_colors[i] = ORANGE
ax2.bar(t, v, color=vol_colors, alpha=0.85, width=pd.Timedelta(minutes=36), zorder=3)

ax2.annotate("首波启动量 3109 BTC\n（量 4.8 倍 = 紧迫感）",
             xy=(pd.Timestamp("2026-07-14 20:00"), 3109),
             xytext=(pd.Timestamp("2026-07-14 20:20"), 3450),
             fontsize=9, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))
ax2.annotate("第二波量能腰斩：1153\n买方弹药不足 = 衰竭的量证",
             xy=(pd.Timestamp("2026-07-15 23:00"), 1153),
             xytext=(pd.Timestamp("2026-07-15 19:00"), 2400),
             fontsize=9, color=ORANGE, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

ax2.set_ylabel("成交量（BTC）", fontsize=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
ax1.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))

fig.text(0.995, 0.015, "数据源：Binance BTCUSDT 5m K 线重采样 1H · 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig("handbook/images/fig_real_ch2_spike.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch2_spike.png")
