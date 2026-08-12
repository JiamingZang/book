# -*- coding: utf-8 -*-
"""510300 5分钟线微通道真实教学图（4.6 配图）"""
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.dates as mdates

RED, GREEN, GRAY = "#ef5350", "#26a69a", "#90a4ae"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

df = ak.stock_zh_a_minute(symbol='sh510300', period='5', adjust='')
df['day'] = pd.to_datetime(df['day'])
for c in ['open', 'high', 'low', 'close']:
    df[c] = df[c].astype(float)

# 绘制范围：07-24 全天 + 07-27 全天 + 07-28 开盘（次日反转预告）
seg = df[(df.day >= '2026-07-24') & (df.day <= '2026-07-28 09:40')].reset_index(drop=True)
print("绘图范围:", str(seg.day.iloc[0])[:16], "->", str(seg.day.iloc[-1])[:16], "共", len(seg), "根")

# ============ 绘图 ============
fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

plot = seg  # 全段绘制

for _, r in plot.iterrows():
    o, h, l, c = r['open'], r['high'], r['low'], r['close']
    t = r['day']
    up = c >= o
    color = RED if up else GREEN
    ax.plot([t, t], [l, h], color=color, lw=0.8, zorder=2)
    ax.add_patch(plt.Rectangle((t - pd.Timedelta(minutes=2.2), min(o, c)),
                               pd.Timedelta(minutes=4.4), abs(c - o) + 1e-9,
                               facecolor=color, edgecolor=color, lw=0.5, zorder=3))

# 微通道段（07-27 13:35 ~ 15:00）
mc = seg[(seg['day'] >= '2026-07-27 13:35') & (seg['day'] <= '2026-07-27 15:00')]
t0, t1 = mc['day'].iloc[0], mc['day'].iloc[-1]
# 下沿：连接首低点与末低点
lo0, lo1 = mc['low'].iloc[0], mc['low'].iloc[-1]
dt = (t1 - t0).total_seconds() / 86400.0
k = (lo1 - lo0) / dt  # 每日期斜率
# 上沿：平行线过段内最高点
hi_max = mc['high'].max()
t_hi = mc.loc[mc['high'].idxmax(), 'day']
ts = np.array([(t - t0).total_seconds() / 86400.0 for t in seg['day']])
lo_line = lo0 + k * ts
hi_line = (hi_max - k * (t_hi - t0).total_seconds() / 86400.0) + k * ts
mask = (seg['day'] >= t0 - pd.Timedelta(hours=1)) & (seg['day'] <= t1 + pd.Timedelta(hours=1))
ax.plot(seg['day'][mask], lo_line[mask], color="#1565c0", lw=1.6, ls="--", zorder=4)
ax.plot(seg['day'][mask], hi_line[mask], color="#1565c0", lw=1.6, ls="--", zorder=4)
ax.fill_between(seg['day'][mask], lo_line[mask], hi_line[mask], color="#1565c0", alpha=0.07, zorder=1)

# 标注
ax.annotate("微通道：18 根 5 分钟 K 线\n低点逐根抬高，无有效回调",
            xy=(t0 + pd.Timedelta(minutes=55), hi_max + 0.012),
            xytext=(t0 + pd.Timedelta(minutes=-5), hi_max + 0.030),
            fontsize=10.5, color="#1565c0", fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color="#1565c0", lw=1.2))

# 回调入场点：13:35 扫回调低点 4.690（高于上午低点 4.674 = 更高低点），13:40 阳线收回
sweep = seg[seg.day == '2026-07-27 13:35']
if len(sweep):
    et = sweep.day.iloc[0]
    ev = sweep.low.iloc[0]
    ax.plot([et], [ev], marker="o", color="#ef6c00", ms=8, zorder=6)
    ax.annotate("入场：13:40 阳线收回\n（13:35 扫回调低点 4.690 后 V 转，\n低点高于上午 4.674 = 更高低点）",
                xy=(et, ev),
                xytext=(et + pd.Timedelta(minutes=-40), ev - 0.030),
                fontsize=9.5, color="#ef6c00", fontweight="bold", zorder=6,
                arrowprops=dict(arrowstyle="->", color="#ef6c00", lw=1.2))

# 结局：次日 07-28 低开大跌
nxt = df[(df.day > '2026-07-27 15:00') & (df.day <= '2026-07-28 09:40')]
if len(nxt):
    last = nxt.close.iloc[-1]
    ax.annotate("次日 07-28：低开 4.69 → 收 4.627（-2.65%）\n18 根已近 Ali 统计极限（约 20 根后向反方倾斜）——\n通道末端不追多；跌破 14:35 低点即结构离场",
                xy=(nxt.day.iloc[-1], last),
                xytext=(nxt.day.iloc[0] - pd.Timedelta(minutes=50), last - 0.006),
                fontsize=9.5, color="#263238", fontweight="bold", zorder=6,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor="#ef6c00", lw=1),
                arrowprops=dict(arrowstyle="->", color="#ef6c00", lw=1.2))

# 刻度
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8.5)
ax.set_ylabel("价格", fontsize=10)
ax.set_title("沪深300ETF（510300）5 分钟：教科书级上升微通道（2026-07-27 下午）",
             fontsize=13, color="#263238", pad=12)
ax.text(0.995, -0.13, "数据源：新浪财经 5 分钟行情（510300.SH） · 教学示意，不构成投资建议",
        transform=ax.transAxes, ha="right", fontsize=8, color=GRAY)
ax.grid(axis="y", color="#eceff1", lw=0.7)
ax.set_zorder(0)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("handbook/images/fig_real_microchannel.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_microchannel.png")
