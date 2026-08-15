# -*- coding: utf-8 -*-
"""图 9-5R：账户规模的现实——"$500 做 Emini"是数学诈骗（用真实回测算学费）
数据源：data/_bt_ema_trades.csv（EMA20/50 回测 82 笔真实逐笔 R，BTC 1H，2026-07-02 ~ 08-10）
- 上：82 笔累计 R（峰 +3.72R 在第 5 笔，终值 -7.83R），右轴换算成美元学费（ES 每点 $50，5 点止损 = $250/笔）
  三档止损学费：5 点 $1,958 / 8 点 $3,132 / 10 点 $3,915——一个负期望系统就是一台学费榨汁机
- 左下：0.5% 单笔风险规则下，各账户规模可承受的止损点数（$500→0.05 点 … $50,000→5.00 点）
  ES 最小止损 5 点参考线：只有 ≥$50,000 才够得着——$500 账户只够买 0.05 点，一个报价跳动都扛不住
- 右下：$500 账户、1 手 ES、5 点止损（$250/笔）按真实 82 笔顺序滚动的账户资金
  第 5 笔冲到 $1,430 峰值（+186%），第 35 笔资金归零——练的不是"执行力"，是"恐惧"
教学点（9.9 账户规模的现实）：
- 学费 = 笔数 × 单笔风险 × 总 R：小账户不是"慢慢亏"，是亏到一半就没资格再练
- 最小止损是市场给的（5-10 点），不是你能选的；0.5% 规则要求账户 ≥$50,000 才能碰 ES
- 资金规模 ≠ 交易规模：就算 $100,000 也应只做 1 手 ES（6 章"实际风险"）
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 字体 fallback：Windows 用雅黑，Linux 用文泉驿
_zh = None
for cand in ["Microsoft YaHei", "WenQuanYi Zen Hei"]:
    if any(f.name == cand for f in font_manager.fontManager.ttflist):
        _zh = cand
        break
plt.rcParams["font.family"] = _zh or "sans-serif"
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
R = t["R"].values
cum = np.cumsum(R)
n = len(R)

# 账户规模数学
accts = np.array([500, 2500, 5000, 10000, 25000, 50000])
afford = accts * 0.005 / 50.0          # 0.5% 风险 ÷ 每点 $50 = 可承受止损点数
ES_MIN_STOP = 5.0                      # ES 最小止损 5 点（Brooks 口径 5-10 点取下限）

# $500 账户爆仓路径：1 手 ES、5 点止损 = $250/笔
cap0 = 500.0
RISK = 250.0
equity = cap0 + RISK * cum
zero_n = int(np.argmax(equity <= 0)) + 1   # 首次资金 ≤ 0 的第 n 笔

fig = plt.figure(figsize=(15.8, 7.0), dpi=110)
gs = fig.add_gridspec(2, 2, height_ratios=[1.35, 1.0], hspace=0.32, wspace=0.14,
                      left=0.055, right=0.965, top=0.93, bottom=0.075)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])

# ---------- 上：82 笔累计 R + 学费 ----------
x = np.arange(1, n + 1)
ax1.plot(x, cum, color=DARK, lw=1.6, zorder=4)
ax1.fill_between(x, cum, 0, where=(cum >= 0), color=UP, alpha=0.25, zorder=2)
ax1.fill_between(x, cum, 0, where=(cum < 0), color=DOWN, alpha=0.30, zorder=2)
ax1.axhline(0, color=GRAY, lw=0.9, zorder=3)

peak_i = int(cum.argmax())
ax1.scatter([peak_i + 1], [cum[peak_i]], color=UP, s=30, zorder=6)
ax1.annotate(f"峰值 +{cum[peak_i]:.2f}R（第 {peak_i + 1} 笔，资金 +186%）\n之后一路向下：负期望系统的高点都是假的",
             xy=(peak_i + 1, cum[peak_i]), xytext=(peak_i + 6, cum[peak_i] + 1.2),
             fontsize=9.5, color=UP, ha="left", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=UP, lw=1),
             arrowprops=dict(arrowstyle="->", color=UP, lw=1.2))

ax1.scatter([n], [cum[-1]], color=DOWN, s=30, zorder=6)
ax1.annotate(f"终值 {cum[-1]:.2f}R\n（82 笔学费总账，右轴美元）",
             xy=(n, cum[-1]), xytext=(n - 28, cum[-1] - 3.4),
             fontsize=9.5, color=DOWN, ha="center", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#e0f2f1", edgecolor=DOWN, lw=1),
             arrowprops=dict(arrowstyle="->", color=DOWN, lw=1.2))

# 右轴：5 点止损 $250/笔 的美元学费
ax1b = ax1.twinx()
ax1b.set_ylim(RISK * ax1.get_ylim()[0], RISK * ax1.get_ylim()[1])
ax1b.set_ylabel("美元学费（\$250/笔 = ES 5 点止损）", fontsize=10, color=GRAY)
ax1b.tick_params(colors=GRAY, labelsize=8.5)
for s in ["top"]:
    ax1b.spines[s].set_visible(False)

tuition = [
    (5, 250, "5 点止损", "1,958"),
    (8, 400, "8 点止损", "3,132"),
    (10, 500, "10 点止损", "3,915"),
]
ax1.text(n - 1.5, 3.6, "同样的 82 笔，止损越大学费越贵：",
         fontsize=9.5, color=DARK, ha="right", va="center", zorder=6)
for i, (pt, risk, label, dollar) in enumerate(tuition):
    ax1.text(n - 1.5, 2.15 - i * 0.85, f"{label}（\${risk}/笔）→ \${dollar}",
             fontsize=9.5, color=[BLUE, ORANGE, RED][i], ha="right", va="center",
             fontweight="bold", zorder=6)

ax1.set_title("图 9-5R 账户规模的现实：学费总账——82 笔真实回测累计 R 终值 -7.83R，ES 最小止损下就是 1,958~3,915 美元学费（数据：EMA20/50 回测 82 笔真实逐笔，BTC 1H，2026-07-02 ~ 08-10）",
              fontsize=11, color=DARK, loc="left")
ax1.set_xlabel("第几笔交易", fontsize=10)
ax1.set_ylabel("累计 R", fontsize=10)
ax1.set_xticks(np.arange(0, n + 1, 10))
ax1.set_ylim(-10.5, 5.2)
ax1.tick_params(labelsize=8.5)
for s in ["top", "right"]:
    ax1.spines[s].set_visible(False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# ---------- 左下：0.5% 规则可承受止损点数 ----------
labels = ["\$500", "\$2.5K", "\$5K", "\$10K", "\$25K", "\$50K"]
bars = ax2.bar(np.arange(len(accts)), afford, 0.62, color=BLUE, alpha=0.85, zorder=3)
# 够不到 5 点的用橙色/红色区分
for i, (v, bar) in enumerate(zip(afford, bars)):
    if v < ES_MIN_STOP:
        bar.set_color(RED if i == 0 else ORANGE)
    ax2.text(i, v + 0.12, f"{v:.2f} 点", ha="center", va="bottom",
             fontsize=9, color=DARK, fontweight="bold", zorder=6)

ax2.axhline(ES_MIN_STOP, color=DARK, lw=1.6, ls="--", zorder=4)
ax2.text(len(accts) - 0.45, ES_MIN_STOP + 0.22, "ES 最小止损 5 点\n（市场给的，不是你能选的）",
         fontsize=8.5, color=DARK, ha="right", va="bottom", fontweight="bold", zorder=6)
ax2.annotate("\$500 账户只够 0.05 点\n——一个报价跳动都扛不住",
             xy=(0, afford[0]), xytext=(0.6, 2.3),
             fontsize=9, color=RED, ha="left", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=RED, lw=1),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax2.text(len(accts) - 0.45, 1.3, "0.5% 单笔风险规则（第 6 章）：\n可承受止损点数 = 账户 × 0.5% ÷ \$50/点",
         fontsize=8.5, color=GRAY, ha="right", va="bottom", zorder=5)

ax2.set_xticks(np.arange(len(accts)))
ax2.set_xticklabels(labels, fontsize=9.5)
ax2.set_ylabel("0.5% 规则可承受止损点数", fontsize=9.5)
ax2.set_ylim(0, 6.6)
for s in ["top", "right"]:
    ax2.spines[s].set_visible(False)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.set_title("左：账户多大才配碰 ES？", fontsize=10, color=DARK, loc="left")

# ---------- 右下：$500 账户爆仓路径 ----------
alive = np.ones(n, dtype=bool)
alive[zero_n - 1:] = False
ax3.plot(x[alive], equity[alive], color=TEAL, lw=1.8, zorder=4, label="账户资金（第 1~34 笔）")
if zero_n < n:
    ax3.plot(x[~alive], equity[~alive], color=RED, lw=1.6, ls=":", zorder=4,
             label=f"已爆仓（继续硬撑的账面负数，第 {zero_n} 笔起）")

ax3.axhline(0, color=GRAY, lw=0.9, zorder=3)
ax3.fill_between(x, equity, 0, where=(equity < 0), color=RED, alpha=0.15, zorder=2)

peak_eq = equity.max()
ax3.scatter([peak_i + 1], [peak_eq], color=UP, s=26, zorder=6)
ax3.annotate(f"第 {peak_i + 1} 笔峰值 \${peak_eq:,.0f}\n（+186%：先让你尝到甜头）",
             xy=(peak_i + 1, peak_eq), xytext=(zero_n + 2, peak_eq * 0.9),
             fontsize=8.5, color=UP, ha="left", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=UP, lw=1),
             arrowprops=dict(arrowstyle="->", color=UP, lw=1.1))
ax3.scatter([zero_n], [0], color=RED, s=34, zorder=6)
ax3.annotate(f"第 {zero_n} 笔资金归零\n（此后是负数 = 已出局）",
             xy=(zero_n, 0), xytext=(zero_n - 4, -950),
             fontsize=9, color=RED, ha="right", fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=RED, lw=1),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax3.text(n - 1.5, equity[-1] + 120, f"账面终值 \${equity[-1]:,.0f}\n（若平台还让负数硬撑）",
         fontsize=8.5, color=RED, ha="right", va="bottom", zorder=6)
ax3.text(3, 600, "\$500 账户 · 1 手 ES · 5 点止损（\$250/笔）\n按真实 82 笔顺序滚动：\n练的不是执行力，是恐惧",
         fontsize=8.5, color=DARK, ha="left", va="center", zorder=6)

ax3.set_xticks(np.arange(0, n + 1, 10))
ax3.set_xlabel("第几笔交易", fontsize=9.5)
ax3.set_ylabel("账户资金（美元）", fontsize=9.5)
ax3.set_ylim(-1600, 1650)
for s in ["top", "right"]:
    ax3.spines[s].set_visible(False)
ax3.grid(axis="y", color="#eceff1", lw=0.7)
ax3.legend(loc="upper left", fontsize=8.5, frameon=False)
ax3.set_title("右：\$500 账户的真实死法——第 35 笔归零", fontsize=10, color=DARK, loc="left")

fig.text(0.995, 0.008, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔真实逐笔 R）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)

plt.savefig("handbook/images/fig_real_ch9_learning.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved handbook/images/fig_real_ch9_learning.png")
