# -*- coding: utf-8 -*-
"""图 1-3R 真实数据：BTC 时段活跃度（批次 121 级联重编号：原 1-1R→1-2R→1-3R）（Binance 5m，2026-06-29 ~ 08-13）
- 上：北京时间各小时平均波动（点）——峰值在北京 6 时（美盘）
- 下：北京时间各小时总成交量（BTC）——峰值在北京 5 时
- 教学点：加密的黄金时段是美盘（北京 22 时-8 时），与外汇的伦敦-纽约重叠
  （北京 20-24 时）不重合——品种不同，时段分布要用真实数据验证（1.7）
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TEAL, ORANGE, GRAY, DARK = "#26a69a", "#ef6c00", "#90a4ae", "#263238"
RED = "#ef5350"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
df["bj"] = (df["time"] + pd.Timedelta(hours=8)).dt.hour
df["rng"] = df["high"] - df["low"]
g = df.groupby("bj").agg(avg=("rng", "mean"), vol=("volume", "sum")).reset_index()
x = g["bj"].values
h = np.arange(24)


def seg_color(hh):
    if hh >= 22 or hh < 8:
        return ORANGE
    if 15 <= hh < 22:
        return TEAL
    return GRAY


colors = [seg_color(int(v)) for v in x]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8.6), dpi=110,
                               gridspec_kw={"height_ratios": [1, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# 美盘背景带（北京 22-24 时 + 0-8 时）
for ax in (ax1, ax2):
    ax.axvspan(-0.5, 7.5, color=ORANGE, alpha=0.06, zorder=0)
    ax.axvspan(21.5, 23.5, color=ORANGE, alpha=0.06, zorder=0)
    ax.axvspan(7.5, 14.5, color=GRAY, alpha=0.06, zorder=0)
    ax.axvspan(14.5, 21.5, color=TEAL, alpha=0.06, zorder=0)

# ===== 上：平均波动 =====
bars1 = ax1.bar(x, g["avg"], width=0.75, color=colors, zorder=3, alpha=0.9)
peak1 = int(g.loc[g["avg"].idxmax(), "bj"])
ax1.annotate(f"峰值 {g['avg'].max():.0f} 点（北京 {peak1} 时，美盘）",
             xy=(peak1, g["avg"].max()), xytext=(16, g["avg"].max() * 0.92),
             fontsize=10, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))
# 谷底标注
valley1 = int(g.loc[g["avg"].idxmin(), "bj"])
ax1.annotate(f"谷底 {g['avg'].min():.0f} 点（北京 {valley1} 时）",
             xy=(valley1, g["avg"].min()), xytext=(8, g["avg"].min() * 0.9),
             fontsize=9, color=GRAY, zorder=6,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))

ax1.set_ylabel("平均波动（high−low，点）", fontsize=10.5)
ax1.set_title("BTC 真实时段活跃度：加密的黄金时段是美盘，不是伦敦-纽约重叠\n"
              "（北京时间 · Binance 5m · 2026-06-29 ~ 08-13，共 12,960 根 K 线）",
              fontsize=12.5, color=DARK, pad=12)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.set_xlim(-0.5, 23.5)
ax1.set_xticks(np.arange(0, 24, 3))

# ===== 下：总成交量 =====
ax2.bar(x, g["vol"] / 1000, width=0.75, color=colors, zorder=3, alpha=0.9)
peak2 = int(g.loc[g["vol"].idxmax(), "bj"])
ax2.annotate(f"峰值 {g['vol'].max()/1000:.0f}（千 BTC）北京 {peak2} 时",
             xy=(peak2, g["vol"].max() / 1000), xytext=(14.5, g["vol"].max() / 1000 * 0.93),
             fontsize=10, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))

ax2.set_ylabel("总成交量（千 BTC）", fontsize=10.5)
ax2.set_xlabel("北京时间（时）", fontsize=10.5)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.set_xlim(-0.5, 23.5)
ax2.set_xticks(np.arange(0, 24, 3))

# 时段图例（右上）
ax2.text(0.985, 0.97, "■ 美盘（北京22时-7时）   ■ 欧盘（15-21时）   ■ 亚盘（8-14时）",
         transform=ax2.transAxes, ha="right", va="top", fontsize=9.5, color=DARK,
         bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=GRAY, lw=0.8))

# 统计框（左下）
stats = ("美盘（北京22时-7时）占全天成交量 52%，波动均值 80 点\n"
         "欧盘（15-21时）24%，亚盘（8-14时）23%，波动均值约 70 点\n"
         "峰值（5-6时）≈ 谷底（2时）的 2.6 倍\n"
         "对照：外汇黄金窗口在伦敦-纽约重叠（北京20-24时，1.7）\n"
         "——品种不同，时段分布要用真实数据验证，别照搬外汇时段表")
ax2.text(0.015, 0.97, stats, transform=ax2.transAxes, ha="left", va="top",
         fontsize=9.2, color=DARK, family="Microsoft YaHei", zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

fig.text(0.995, 0.012, "数据源：Binance BTCUSDT 5m K 线（data/btcusdt_5m.csv）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig("handbook/images/fig_real_ch1_sessions.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch1_sessions.png")
