# -*- coding: utf-8 -*-
"""图 8-4R 真实数据：真实回测的 R 分布——止损纪律的指纹 + 赢在尾部
（EMA20/50 趋势跟踪回测，BTC 1H，2026-07-02 ~ 08-10，同图 8-1R 的 82 笔）
- 上：82 笔 R 直方图——亏单全部锁死在 -1R 内（止损纪律的指纹），赢单右尾最长 +2.85R
      33 赢 / 49 亏，平均 -0.10R/笔，赢单均值 +0.41R，亏单均值 -0.44R
- 下：按 R 降序的单笔柱 + 累计 R 线——前 5 大赢单 +7.79R = 赢单总利润 57%，
      去掉前 5 大 → -15.6R；82 笔终点 -7.83R（SQN -1.4）
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE = "#1565c0", "#ef6c00"
RED, TEAL, GRAY, DARK = "#ef5350", "#00897b", "#90a4ae", "#263238"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ---- 读取真实回测交易 ----
trades = []
with open("data/_bt_ema_trades.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        trades.append(float(row["R"]))
R = np.array(trades)
N = len(R)
wins = R[R > 0]
losses = R[R <= 0]
total = R.sum()
s = np.sort(R)[::-1]
cum_sorted = np.cumsum(s)
top5 = cum_sorted[4]
without_top5 = total - top5

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(14, 6.6), dpi=110,
    gridspec_kw={"height_ratios": [1.05, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)

# ===== 上：R 直方图 =====
bins = np.arange(-1.05, 3.15, 0.2)
hist, edges = np.histogram(R, bins=bins)
centers = (edges[:-1] + edges[1:]) / 2
colors = [TEAL if c > 0 else RED for c in centers]
ax1.bar(centers, hist, width=0.19, color=colors, alpha=0.88)

ax1.axvline(0, color=GRAY, lw=1, ls=":")
ax1.axvline(R.mean(), color=ORANGE, lw=1.6, ls="--")
ax1.text(R.mean() - 0.02, 24, f"平均 {R.mean():+.2f}R/笔", ha="right", va="top",
         fontsize=9.5, color=ORANGE, fontweight="bold")
ax1.axvline(wins.mean(), color=TEAL, lw=1.2, ls="--")
ax1.text(wins.mean() + 0.03, 27, f"赢单均值 {wins.mean():+.2f}R", ha="left",
         fontsize=9, color=TEAL, fontweight="bold")
ax1.axvline(losses.mean(), color=RED, lw=1.2, ls="--")
ax1.text(losses.mean() - 0.03, 27, f"亏单均值 {losses.mean():+.2f}R", ha="right",
         fontsize=9, color=RED, fontweight="bold")

ax1.annotate(f"最大赢单 {wins.max():+.2f}R\n（唯一超过 +1.5R 的右尾）",
             xy=(wins.max(), 1), xytext=(1.9, 9),
             fontsize=9, color=DARK, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))

# 止损墙标注
ax1.annotate("止损墙：49 笔亏损全部锁死在 −1R 内\n（−0.91 ~ −1.00，滑点+止损微超）——没有一根扛单巨亏",
             xy=(-0.95, 16), xytext=(-1.02, 20),
             fontsize=9, color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))

ax1.set_ylabel("笔数", fontsize=10)
ax1.set_title("真实回测的 R 分布：亏单被止损锁死在 −1R（纪律的指纹），赢靠少数大 R 撑起（EMA20/50 趋势跟踪，BTC 1H，2026-07-02 ~ 08-10）",
              fontsize=12, color=DARK, pad=10)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.set_xticks(np.arange(-1.0, 3.1, 0.5))
ax1.set_xlim(-1.15, 3.25)

# 统计框
stats = (f"82 笔：33 赢 / 49 亏（胜率 40%）· 平均每笔 {R.mean():+.2f}R · 中位 {np.median(R):+.2f}R\n"
         f"赢单总 {wins.sum():+.2f}R / 亏单总 {losses.sum():+.2f}R · 标准差 {R.std():.2f}R · SQN {R.mean()*np.sqrt(N)/R.std():.2f}\n"
         f"P10 {np.percentile(R,10):+.2f} · P25 {np.percentile(R,25):+.2f} · P50 {np.percentile(R,50):+.2f} · P75 {np.percentile(R,75):+.2f} · P90 {np.percentile(R,90):+.2f}\n"
         f"超过一半交易不赚钱（中位为负），赢单里也只有少数大 R 显著为正")
ax1.text(0.012, 0.97, stats, transform=ax1.transAxes, ha="left", va="top",
         fontsize=8.8, color=DARK, family="Microsoft YaHei",
         bbox=dict(boxstyle="round,pad=0.45", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

# ===== 下：R 降序 + 累计 =====
x = np.arange(1, N + 1)
ax2.bar(x, s, 0.8, color=[TEAL if v > 0 else RED for v in s], alpha=0.85, label="单笔 R（按从大到小排序）")
ax2.axhline(0, color=GRAY, lw=1, ls=":")

# 前 5 大赢单高亮
ax2.axvspan(0.5, 5.5, color=TEAL, alpha=0.10, zorder=1)
ax2.annotate(f"前 5 大赢单 +{top5:.2f}R\n= 赢单总利润的 {top5/wins.sum()*100:.0f}%\n去掉它们 → {without_top5:+.1f}R",
             xy=(3, s[2]), xytext=(10, 2.35),
             fontsize=9.5, color=TEAL, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 累计 R 线（右轴）
ax2b = ax2.twinx()
ax2b.plot(x, cum_sorted, color=BLUE, lw=2, label="累计 R（从最赚到最亏逐笔累加）")
ax2b.axhline(without_top5, color=GRAY, lw=1, ls="--")
ax2b.text(62, without_top5 + 0.5, f"去掉前 5 大赢单 → {without_top5:+.1f}R", fontsize=9, color=GRAY)
ax2b.set_ylabel("累计 R（R 倍数）", fontsize=10, color=BLUE)
ax2b.tick_params(axis="y", colors=BLUE)
ax2b.spines["top"].set_visible(False)
ax2b.set_ylim(-22, 16)

ax2.annotate(f"82 笔终点 {total:+.2f}R\n平均 {R.mean():+.3f}R/笔——验证不合格",
             xy=(N, cum_sorted[-1]), xytext=(58, cum_sorted[-1] - 2.6),
             fontsize=9.5, color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

ax2.set_xticks([1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 82])
ax2.set_xlim(0.5, N + 1)
ax2.set_xlabel("交易序号（按单笔 R 从大到小排序：最赚 → 最亏）", fontsize=10)
ax2.set_ylabel("单笔 R", fontsize=10)
ax2.legend(loc="upper right", fontsize=8.8, frameon=False)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

fig.text(0.995, 0.012, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("handbook/images/fig_real_ch8_rdist.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch8_rdist.png")
