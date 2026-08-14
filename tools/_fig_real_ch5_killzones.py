# -*- coding: utf-8 -*-
"""图 5-4R 真实数据：Kill Zones 的实证——24 小时波动率与成交量分布（BTC 5m，2026-07-15 ~ 08-13 共 30 天）
- 数据：Binance BTCUSDT 5m K 线（data/btcusdt_5m.csv），按北京时间聚合
- 上：每小时 5m 收益率绝对值均值（波动率代理）；下：每小时成交量
- 背景色带：亚盘（06:00-14:00，薄）、伦敦 Kill Zone（15:00-18:00，夏令时 15:00 开盘）、
  纽约 Kill Zone（21:00-24:00，夏令时 21:30 开盘）、伦敦-纽约重叠（20:00-24:00）
- 教学：5.8 Kill Zones 的真实数据验证——纽约开盘（21-22 点）波动率/量能全天峰值、亚盘（4-7 点）谷底、
  伦敦-纽约重叠（20-24 点）持续高活跃；Kill Zone 是"信号密集窗口"的实证，不是开关
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

UP, DOWN, GRAY, DARK, TEAL, ORANGE, BLUE = "#e53935", "#26a69a", "#90a4ae", "#263238", "#00897b", "#ef6c00", "#1565c0"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"]).sort_values("time")
recent = df[df["time"] >= "2026-07-15"].copy()
recent["hour"] = recent["time"].dt.hour
recent["ret"] = recent["close"].pct_change().abs() * 100

g = recent.groupby("hour").agg(
    vol_avg=("ret", "mean"),
    vsum=("volume", "sum"),
    n=("volume", "count")).reset_index()
g["vmean_n"] = g["vol_avg"] / g["vol_avg"].mean()
g["vsum_n"] = g["vsum"] / g["vsum"].mean()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13.5, 7.6), dpi=110,
                               gridspec_kw={"hspace": 0.30})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

H = np.arange(24)

def zone(ax, y0, y1):
    """Kill Zones 背景色带"""
    ax.axvspan(6, 14, color=GRAY, alpha=0.10, zorder=0)
    ax.axvspan(15, 18, color=TEAL, alpha=0.14, zorder=0)
    ax.axvspan(20, 24, color=ORANGE, alpha=0.14, zorder=0)

# ===== 上：波动率 =====
zone(ax1, 0, 2)
ax1.bar(H, g["vmean_n"], color=[TEAL if 15 <= x <= 18 else (ORANGE if 20 <= x <= 23 else (GRAY if 6 <= x <= 14 else "#78909c")) for x in H],
        edgecolor="white", lw=0.5)
ax1.set_ylabel("波动率（相对全天均值）", fontsize=10, color=DARK)
ax1.set_ylim(0, 1.6)
# 峰值标注
ax1.annotate("纽约开盘 21:30\n全天峰值 vol 1.30×", xy=(21, 1.30), xytext=(21, 1.48),
             fontsize=9.5, color=ORANGE, ha="center", va="bottom",
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
ax1.annotate("伦敦开盘 15:00\nvol 1.05-1.09×", xy=(15, 1.05), xytext=(15, 1.25),
             fontsize=9.5, color=TEAL, ha="center", va="bottom",
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))
ax1.annotate("亚盘 4-7 点谷底\nvol 0.83-0.88×", xy=(5, 0.87), xytext=(7.5, 0.45),
             fontsize=9.5, color=GRAY, ha="center",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax1.set_title("① 波动率（每 5 分钟收益率绝对值，按北京小时聚合，相对全天均值）——Kill Zone 实证：纽约开盘最剧烈、亚盘最平静", fontsize=11, color=DARK, loc="left")

# ===== 下：成交量 =====
zone(ax2, 0, 2)
ax2.bar(H, g["vsum_n"], color=[TEAL if 15 <= x <= 18 else (ORANGE if 20 <= x <= 23 else (GRAY if 6 <= x <= 14 else "#78909c")) for x in H],
        edgecolor="white", lw=0.5)
ax2.set_ylabel("成交量（相对全天均值）", fontsize=10, color=DARK)
ax2.set_ylim(0, 2.1)
ax2.annotate("纽约开盘 21-22 点\n量能 1.66-1.72×（峰值）", xy=(22, 1.72), xytext=(22, 1.95),
             fontsize=9.5, color=ORANGE, ha="center", va="bottom",
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
ax2.annotate("伦敦-纽约重叠 20-24 点\n量能持续 1.17-1.72×", xy=(20.5, 1.17), xytext=(16.5, 1.95),
             fontsize=9.5, color=DARK, ha="center", va="bottom",
             arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))
ax2.annotate("亚盘量能 0.58-0.79×", xy=(4, 0.59), xytext=(3.2, 0.95),
             fontsize=9.5, color=GRAY, ha="center",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax2.set_title("② 成交量（按北京小时聚合，相对全天均值）——信号密集 ≠ 只在 Kill Zone 做单，Kill Zone 是加权项不是开关（5.8）", fontsize=11, color=DARK, loc="left")

for ax, xt in ((ax1, True), (ax2, True)):
    ax.set_xticks(H)
    ax.set_xticklabels([f"{h}:00" for h in H], fontsize=8, color=DARK, rotation=0)
    ax.grid(axis="y", ls=":", lw=0.5, color=GRAY, alpha=0.4)

fig.suptitle("Kill Zones 的真实数据验证（BTC 5m，2026-07-15 ~ 08-13，30 天）：纽约开盘是全天波动率与量能峰值、亚盘是谷底——机构活跃窗口不是叙事，是分布", fontsize=12.5, color=DARK, y=0.99)
fig.text(0.5, 0.015, "色带：灰 = 亚盘（6-14 点，流动性薄） | 青 = 伦敦 Kill Zone（15-18 点） | 橙 = 纽约 Kill Zone 与伦敦-纽约重叠（20-24 点）",
         fontsize=9, color=GRAY, ha="center")
plt.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.06, hspace=0.30)
plt.savefig("handbook/images/fig_real_ch5_killzones.png", dpi=110, facecolor="white", bbox_inches="tight")
print("已生成 handbook/images/fig_real_ch5_killzones.png")
