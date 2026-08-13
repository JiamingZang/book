# -*- coding: utf-8 -*-
"""图 7-1R 真实数据：一页真实交易日志的统计视图（7.5 交易日志：心理维度）
- 数据：EMA20/50 回测 82 笔真实逐笔记录（BTC 1H，2026-07-02 ~ 08-10，data/_bt_ema_trades.csv）
- 上：逐笔 R 柱状图（每根柱子=日志一行，绿=赢/红=亏），连亏段高亮
- 下：累计 R 曲线（steps-post）+ 统计框
- 教学结论：连亏段是心理高危时刻（最长 6 连亏=40% 胜率正常分布）；赢亏随机散布，
  别在连亏里找"该我赢了"（7.3 赌徒谬误）；期望值从日志表算出（6.3/8.3）
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
x = np.arange(1, n + 1)

# 连亏段（长度 >= 3）
streaks = []
i = 0
while i < n:
    if R[i] < 0:
        j = i
        while j < n and R[j] < 0:
            j += 1
        if j - i >= 3:
            streaks.append((i, j - 1))  # 0-based inclusive
        i = j
    else:
        i += 1

cum = np.concatenate([[0], R.cumsum()])
x_cum = np.concatenate([[0], x])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), dpi=110, sharex=True,
                               gridspec_kw={"height_ratios": [1.15, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：逐笔 R 柱状图 =====
colors = np.where(R >= 0, GREEN, RED)
ax1.bar(x, R, color=colors, width=0.72, zorder=3)
ax1.axhline(0, color=GRAY, lw=1)
for s0, s1 in streaks:
    ax1.axvspan(x[s0] - 0.5, x[s1] + 0.5, color=RED, alpha=0.10, zorder=1)

# 最长连亏 77-81 标注
ax1.annotate("第 77-81 笔：6 连亏（-3.7R）\n40% 胜率下的正常分布，却是心理最危险时刻\n日志价值=连亏时回看：这几笔是否都符合计划（7.4）\n符合→正常连亏，不改系统；有违规→执行问题",
             xy=(79, -0.45), xytext=(56, -1.7),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=RED, lw=1),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 开局 5-9 段：大赚后连亏
ax1.annotate("第 2 笔 +2.85R（全样本最大单笔）\n随后 5 连亏回吐——连赚时最危险\n'我悟了'是概率的馈赠，不是能力（7.3）",
             xy=(8, -0.5), xytext=(14, 1.35),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

ax1.text(42, 2.1, "赢亏随机散布，没有规律\n别在连亏里找'该我赢了'（7.3 赌徒谬误）\n连亏后加倍=用随机结果下注",
         fontsize=9.5, color=DARK, zorder=6,
         bbox=dict(boxstyle="round,pad=0.4", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

ax1.set_ylabel("单笔结果（R）", fontsize=10)
ax1.set_title("一页真实交易日志的统计视图：82 笔逐笔 R（每根柱子 = 日志一行）——连亏段是心理高危时刻",
              fontsize=13, color=DARK, pad=12)
ax1.set_xlim(0, n + 1)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# ===== 下：累计 R 曲线 =====
ax2.plot(x_cum, cum, drawstyle="steps-post", color=BLUE, lw=1.9, zorder=4)
ax2.fill_between(x_cum, 0, cum, step="post", where=(cum >= 0),
                 color=BLUE, alpha=0.08, interpolate=False)
ax2.fill_between(x_cum, 0, cum, step="post", where=(cum < 0),
                 color=RED, alpha=0.08, interpolate=False)
ax2.axhline(0, color=GRAY, lw=1)

# 峰值标注
peak_i = int(np.argmax(cum))
ax2.annotate("第 5 笔后累计 +3.7R（峰值）\n之后一路阴跌——趋势策略在震荡市反复止损",
             xy=(peak_i, cum[peak_i]), xytext=(peak_i - 30, 4.6),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 末端标注
ax2.annotate("82 笔后 -7.8R：期望值 -0.095R/笔\n大数定律下收敛到负值（6.3 公式）\n想上真钱？先回测/模拟盘验证（8.7）",
             xy=(n, cum[-1]), xytext=(n - 44, -6.2),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=RED, lw=1),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

ax2.set_ylabel("累计 R", fontsize=10)
ax2.set_xlabel("交易序号（第 1 ~ 82 笔，日志按平仓顺序一行一行填）", fontsize=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

# 统计框（右下）
wins = (R > 0).mean()
wr = np.abs(R[R > 0].mean() / R[R < 0].mean())
stats = (f"82 笔 · 29 个交易日 · BTC 1H（2026-07-02 ~ 08-10）\n"
         f"胜率 {wins * 100:.0f}% · 盈亏比 {wr:.2f} · 总 R {R.sum():.2f} · 平均 R {R.mean():.3f}\n"
         f"最长连亏 6 笔 · 最大单笔 +2.85R / -1.0R（止损到点）\n"
         f"SQN = {np.sqrt(n) * R.mean() / R.std():.2f}（期望为负）")
ax2.text(0.985, 0.04, stats, transform=ax2.transAxes, ha="right", va="bottom",
         fontsize=9.5, color=DARK, zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

fig.text(0.995, 0.015, "数据源：Binance BTCUSDT 5m K 线重采样 1H 逐笔回测记录 · 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig("handbook/images/fig_real_ch7_journal.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch7_journal.png")
