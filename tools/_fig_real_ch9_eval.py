# -*- coding: utf-8 -*-
"""图 9-1R 真实数据：同一批交易记录，套上考核规则——0.5% vs 1% 风险（Prop 考核视角）
- 数据：EMA20/50 回测 82 笔真实逐笔记录（BTC 1H，2026-07-02 ~ 08-10，data/_bt_ema_trades.csv）
- 上：权益曲线两条（0.5% 蓝 / 1% 红）+ Phase 1 目标线 +10%（绿虚）+ 总回撤线 -10%（红虚）
- 下：回撤曲线两条 + -10% 线
- 教学结论：1% 第 79 笔打穿总回撤线 → 账户作废；0.5% 全程没碰线但也没达标
  （活下来≠能过，策略期望为负 → 先回测再买考核，呼应图 8-1R / 8.7 / 9.3）
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE = "#1565c0", "#ef6c00"
RED, TEAL, GRAY, DARK = "#ef5350", "#00897b", "#90a4ae", "#263238"
GREEN = "#26a69a"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

tr = pd.read_csv("data/_bt_ema_trades.csv", parse_dates=["t_in", "t_out"])
R = tr["R"].values
n = len(R)
x = np.arange(1, n + 1)  # 第几笔（1..82）

eq05 = pd.Series((1 + R * 0.005).cumprod())
eq10 = pd.Series((1 + R * 0.010).cumprod())
dd05 = (eq05 / eq05.cummax() - 1) * 100
dd10 = (eq10 / eq10.cummax() - 1) * 100

cross_i = int(np.argmax(dd10 <= -10.0))  # 第 80 笔（0-based 79）

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), dpi=110, sharex=True,
                               gridspec_kw={"height_ratios": [1.15, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：权益曲线（两个仓位）=====
ax1.axhline(1.10, color=GREEN, lw=1.6, ls="--", zorder=2)
ax1.axhline(0.90, color=RED, lw=1.6, ls="--", zorder=2)
ax1.axhline(1.0, color=GRAY, lw=1, ls=":")

ax1.plot(x, eq05.values, drawstyle="steps-post", color=BLUE, lw=1.9, zorder=4,
         label="0.5% 风险（单笔 0.5%）——82 笔全程没碰线")
ax1.plot(x, eq10.values, drawstyle="steps-post", color=RED, lw=1.9, zorder=4,
         label="1% 风险（单笔 1%）——第 80 笔打穿总回撤线")

# 1% 打穿段阴影（0.90 以下）
below = np.where(eq10.values < 0.90, 0.90, eq10.values)
ax1.fill_between(x, 0.90, below, step="post", where=(eq10.values < 0.90),
                 color=RED, alpha=0.18, zorder=1, interpolate=False)

# 目标线 / 总回撤线标签
ax1.text(1.5, 1.105, "+10% 目标线（Phase 1）——两条曲线都没碰到",
         fontsize=9.5, color=GREEN, fontweight="bold", zorder=6, va="bottom")
ax1.text(1.5, 0.885, "-10% 总回撤线（碰线即出局）",
         fontsize=9.5, color=RED, fontweight="bold", zorder=6, va="top")

# 1% 打穿标注
ax1.annotate("第 80 笔打穿 -10% → 账户作废\n前 79 笔全部白费\n考核只认结果：碰线即出局，不看过程",
             xy=(x[cross_i], eq10.iloc[cross_i]),
             xytext=(x[cross_i] - 34, 0.945),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=RED, lw=1),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 0.5% 教学标注
ax1.annotate("0.5% 风险：82 笔全程没碰 -10% 线\n最大回撤 -5.6%，终值 -3.9%\n活下来 ≠ 能过：策略本身期望为负（图 8-1R）",
             xy=(x[-3], eq05.iloc[-1]),
             xytext=(x[-3] - 60, 1.045),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 目标线教学
ax1.text(x[-1], 1.075, "想靠它过考核？先回测验证（8.2/8.7）\n别用买考核的钱试错",
         fontsize=9, color=DARK, ha="right", zorder=6)

ax1.set_ylabel("账户净值（起点 = 1.0）", fontsize=10)
ax1.set_title("同一批真实交易记录，套上考核规则：仓位决定你是活着还是出局（2026-07-02 ~ 08-10，82 笔）",
              fontsize=13, color=DARK, pad=12)
ax1.legend(loc="upper left", fontsize=9.5, frameon=False)
ax1.set_xlim(0, n + 1)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# 考核规则框（左上内）
rule = ("Phase 1 考核规则（常见）：\n盈利目标 +10% · 日回撤 ≤5% · 总回撤 ≤10%\n"
        "单笔风险建议 0.5%（第 6 章公式）")
ax1.text(0.015, 0.035, rule, transform=ax1.transAxes, ha="left", va="bottom",
         fontsize=9, color=DARK, zorder=7,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

# ===== 下：回撤曲线（两个仓位）=====
ax2.fill_between(x, 0, dd05.values, step="post", color=BLUE, alpha=0.35, zorder=2,
                 label="0.5% 回撤")
ax2.fill_between(x, 0, dd10.values, step="post", color=RED, alpha=0.45, zorder=3,
                 label="1% 回撤")
ax2.axhline(0, color=GRAY, lw=1)
ax2.axhline(-10.0, color=RED, lw=1.5, ls="--", zorder=4)
ax2.text(1.5, -10.7, "-10% 总回撤线", fontsize=9.5, color=RED, fontweight="bold", zorder=6)

# 1% 打穿标注
ax2.annotate("1% 回撤 -11.0%，越过总回撤线（第 80 笔）\n最差单日只有 -2.93%（1% 下）< 5% 日线\n→ 杀死账户的是总回撤线，不是日线",
             xy=(x[cross_i], dd10.iloc[cross_i]),
             xytext=(x[cross_i] - 36, -16.5),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=RED, lw=1),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 0.5% 最大回撤标注
dd05_i = int(dd05.idxmin())
ax2.annotate(f"0.5% 最大回撤 -5.64%（安全区，第 {dd05_i + 1} 笔）",
             xy=(x[dd05_i], dd05.iloc[dd05_i]),
             xytext=(x[dd05_i] - 30, -6.2),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

ax2.set_ylabel("回撤（%）", fontsize=10)
ax2.set_xlabel("交易序号（第 1 ~ 82 笔，按平仓顺序）", fontsize=10)
ax2.legend(loc="lower left", fontsize=9.5, frameon=False, ncol=2)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

# 指标框（右下）
wins = (R > 0).mean()
worst_day = tr.groupby(tr["t_in"].dt.date)["R"].sum().min()
streak = cur = 0
for r in R:
    cur = cur + 1 if r < 0 else 0
    streak = max(streak, cur)
stats = (f"样本：82 笔 · 29 个交易日 · BTC 1H（2026-07-02 ~ 08-10）\n"
         f"胜率 {wins * 100:.0f}% · 盈亏比 0.94 · 总 R {R.sum():.2f}\n"
         f"最长连亏 {streak} 笔（-3.7R）· 最差单日 {worst_day:.2f}R（08-10）\n"
         f"最差单笔 -1.0R（止损到点，未失控）")
ax2.text(0.985, 0.97, stats, transform=ax2.transAxes, ha="right", va="top",
         fontsize=9.5, color=DARK, zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

fig.text(0.995, 0.015, "数据源：Binance BTCUSDT 5m K 线重采样 1H 真实回测逐笔记录 · 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig("handbook/images/fig_real_ch9_eval.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch9_eval.png")
