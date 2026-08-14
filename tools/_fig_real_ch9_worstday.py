# -*- coding: utf-8 -*-
"""图 9-4R：考核中最危险的一天——08-10 五连亏日，正常 0.5% 只亏 1.5%，报复 ×2 一天打穿 5% 日回撤线
数据源：data/_bt_ema_trades.csv（EMA20/50 回测 82 笔真实逐笔 R，BTC 1H，2026-07-02 ~ 08-10，29 个交易日）
- 上：29 个交易日每日 R 和（红负/绿正），中位 -0.35、最差 -2.93（08-10）、最好 +3.10；正收益日仅 8/29
- 最差日 08-10：5 笔全亏 R = [-0.85, -0.63, -0.39, -0.48, -0.59]（5 连亏的一天）
- 下：同一天 3 种资金管理路径的当日累计亏损：
  固定 0.5%：-0.43% → -0.74% → -0.94% → -1.18% → -1.47%（远低于 5% 日回撤线）
  连亏×1.5：-0.43% → -0.90% → -1.34% → -2.15% → -3.64%（逼近 5%）
  连亏×2：  -0.43% → -1.05% → -1.84% → -3.75% → -8.47%（第 5 笔打穿 5% 日回撤线 → 一天出局）
教学点（9.4 常见失败原因 2/4 + 7.6 军规第 3 条）：
- "一天亏穿日回撤"不是市场给的，是自己加的——单日最差也打不死纪律者
- 40% 胜率下连亏必现（图 7-2R），考核期你一定会遇到这样的日子；日回撤线就是逼你收手
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

UP = "#e53935"      # 涨/正（红）
DOWN = "#26a69a"    # 跌/负（绿）
BLUE = "#1565c0"
ORANGE = "#ef6c00"
RED = "#c62828"
GRAY = "#90a4ae"
DARK = "#263238"
TEAL = "#00897b"

t = pd.read_csv("data/_bt_ema_trades.csv")
t["day"] = pd.to_datetime(t["t_in"]).dt.date
g = t.groupby("day").agg(n=("R", "count"), R=("R", "sum")).reset_index()
g = g.sort_values("day").reset_index(drop=True)

fig, (ax, ax2) = plt.subplots(
    2, 1, figsize=(15.8, 6.6), dpi=110, sharex=False,
    gridspec_kw={"height_ratios": [1.5, 1.0], "hspace": 0.16})

# ---------- 上：29 日每日 R 和 ----------
days = g["day"].values
rsum = g["R"].values
x = np.arange(len(g))
colors = [UP if r >= 0 else DOWN for r in rsum]
ax.bar(x, rsum, 0.7, color=colors, alpha=0.9, zorder=3)
ax.axhline(0, color=GRAY, lw=0.9, zorder=2)

# 最差日高亮
wi = int(g["R"].idxmin())
ax.bar(wi, rsum[wi], 0.7, color=ORANGE, alpha=1.0, zorder=4, edgecolor=DARK)
ax.annotate(f"最差日 08-10\n5 笔全亏 总 R {rsum[wi]:.2f}\n0.5% 风险日亏 −1.47%\n（5% 日回撤线没碰到）",
            xy=(wi, rsum[wi]), xytext=(wi - 4.5, rsum[wi] - 2.6),
            fontsize=9.5, color=DARK, ha="center", va="top", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3e0", edgecolor=ORANGE, lw=1),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

ax.text(len(g) - 1, 3.35, f"最好日 +{g['R'].max():.1f}R\n（仅 8/29 天为正）",
        fontsize=9, color=UP, ha="right", va="center", zorder=6)
ax.text(0.5, 3.35, "正收益日 8 / 29（负期望系统：多数日子在亏，考核是熬出来的）",
        fontsize=9, color=GRAY, ha="left", va="center", zorder=5)

ax.set_title("图 9-4R 考核中最危险的一天——最差日 08-10 五连亏：纪律只亏 1.5%，报复 ×2 一天打穿 5% 日回撤线（数据：EMA20/50 回测 82 笔真实逐笔，BTC 1H，2026-07-02 ~ 08-10）",
             fontsize=11, color=DARK, loc="left")
ax.set_ylabel("当日总 R", fontsize=10)
ax.set_ylim(-5.6, 4.0)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#eceff1", lw=0.7)

# 底部日期刻度：每 5 天
tick_idx = list(range(0, len(g), 5))
ax.set_xticks(tick_idx)
ax.set_xticklabels([str(days[i])[5:] for i in tick_idx], fontsize=8, color=GRAY)
ax.tick_params(length=0)

# ---------- 下：最差日 3 种路径 ----------
R5 = np.array([-0.85, -0.63, -0.39, -0.48, -0.59])
paths = [
    (np.array([0.005] * 5), BLUE, "固定 0.5%（纪律）", "日亏 −1.47%", 2.4, 0),
    (np.array([0.005, 0.0075, 0.01125, 0.016875, 0.0253125]), ORANGE, "连亏 ×1.5", "日亏 −3.64%（逼近 5%）", 1.7, 0),
    (np.array([0.005, 0.01, 0.02, 0.04, 0.08]), RED, "连亏 ×2", "日亏 −8.47%（打穿 5%）", 1.8, 0),
]
xx = np.arange(1, 6)
for risks, color, label, note, lw, _ in paths:
    cum = np.cumsum(risks * R5) * 100
    ax2.plot(xx, cum, marker="o", ms=5, color=color, lw=lw, zorder=4, label=label)
    ax2.annotate(note, xy=(5, cum[-1]), xytext=(5.15, cum[-1]),
                 fontsize=8.5, color=color, ha="left", va="center", zorder=6,
                 fontweight="bold" if "打穿" in note else "normal")

ax2.axhline(-5, color=DARK, lw=1.8, ls="--", zorder=3)
ax2.text(0.6, -5.25, "日回撤线 −5%（触及即出局）", fontsize=9, color=DARK,
         ha="left", va="top", fontweight="bold", zorder=6)

ax2.set_xticks(xx)
ax2.set_xticklabels([f"第 {i} 笔\nR {R5[i-1]:.2f}" for i in xx], fontsize=8.5, color=GRAY)
ax2.set_ylabel("当日累计亏损（%）", fontsize=10)
ax2.set_ylim(-10.5, 0.6)
for s in ["top", "right"]:
    ax2.spines[s].set_visible(False)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.legend(loc="lower left", fontsize=9, frameon=False)
ax2.set_title("最差日 08-10 的 5 笔（全是亏损）：同一天、同一批交易，三条资金管理路线的当日累计亏损",
              fontsize=10, color=DARK, loc="left")

fig.text(0.995, 0.008, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔真实逐笔 R）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)

plt.savefig("handbook/images/fig_real_ch9_worstday.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved handbook/images/fig_real_ch9_worstday.png")
