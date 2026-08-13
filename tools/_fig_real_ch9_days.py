# -*- coding: utf-8 -*-
"""图 9-2R 真实数据：考核的隐形杀手不是爆仓，是平庸（Prop 考核视角·天数维度）
- 数据：EMA20/50 回测 82 笔真实逐笔记录（BTC 1H，2026-07-02 ~ 08-10，data/_bt_ema_trades.csv）
- 上：0.5% 风险净值按交易日聚合（29 天）+ Phase 1 目标线 +8%（绿虚）+ 总回撤线 -10%（红虚）
     峰值 +1.87%（第 2 天）离 +8% 差 6.1pct → "第 2 天就是巅峰，之后 27 天阴跌"
- 下：每日 R 柱（绿赢红亏）：第 1 天 +3.10R 唯一大赢日，其余 28 天总和 -10.9R；第 29 天 -2.93R 最差日
- 教学结论：既不出局也不达标 = 平庸 = 考核费无限续费；轻仓保不死，但系统不合格时"活着"也是烧钱
  （呼应 9.1 商业逻辑 / 9.3 数学 / 9-1R 的"活下来≠能过"）
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, RED, TEAL, GRAY, DARK = "#1565c0", "#ef5350", "#00897b", "#90a4ae", "#263238"
GREEN = "#26a69a"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

tr = pd.read_csv("data/_bt_ema_trades.csv", parse_dates=["t_in", "t_out"])
tr["date"] = tr["t_in"].dt.date
daily = tr.groupby("date")["R"].sum().sort_index()
days = daily.index
x = np.arange(1, len(daily) + 1)  # 第 1..29 个交易日

d_ret = daily.apply(lambda r: 1 + r * 0.005)  # 当日净值乘数（0.5% 风险）
d_eq = d_ret.cumprod()  # 逐日净值
d_dd = (d_eq / d_eq.cummax() - 1) * 100  # 逐日回撤（未画，仅统计用）

peak_i = int(d_eq.values.argmax())
peak_d = x[peak_i]
peak_val = (d_eq.max() - 1) * 100
final_val = (d_eq.iloc[-1] - 1) * 100
max_dd = d_dd.min()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8.2), dpi=110, sharex=True,
                               gridspec_kw={"height_ratios": [1.15, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：逐日净值（0.5% 风险，29 个交易日）=====
ax1.axhline(1.08, color=GREEN, lw=1.6, ls="--", zorder=2)
ax1.axhline(0.90, color=RED, lw=1.6, ls="--", zorder=2)
ax1.axhline(1.0, color=GRAY, lw=1, ls=":")
ax1.text(0.8, 1.082, "+8% 目标线（Phase 1）——峰值离它还有 6.1 个百分点",
         fontsize=9.5, color=GREEN, fontweight="bold", zorder=6, va="bottom")
ax1.text(0.8, 0.888, "-10% 总回撤线——最大回撤 -5.6%，也没碰到",
         fontsize=9.5, color=RED, fontweight="bold", zorder=6, va="top")

# 平庸带（0.94 ~ 1.06 之间 = 哪条线都不沾）
ax1.axhspan(0.94, 1.06, color=GRAY, alpha=0.08, zorder=1)

ax1.plot(x, d_eq.values, drawstyle="steps-post", color=BLUE, lw=2.2, zorder=4,
         label="0.5% 风险净值（按日聚合：82 笔 ÷ 29 天 ≈ 每天 2.8 笔）")

# 峰值标注（第 2 天 +1.87%）
ax1.annotate(f"第 {peak_d} 天就是巅峰：+{peak_val:.1f}%\n82 笔里最好的一天在第 1 天（+3.10R）\n之后 27 天再也没摸到过这个高点",
             xy=(peak_d, d_eq.iloc[peak_i]),
             xytext=(peak_d - 12, 1.030),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#e0f2f1", edgecolor=TEAL, lw=1),
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 终值标注
ax1.annotate(f"29 天白耗：终值 {final_val:.1f}%\n既不出局、也不达标 → 平庸\n（考核费蒸发，请重新购买）",
             xy=(len(daily), d_eq.iloc[-1]),
             xytext=(len(daily) - 14, 0.935),
             fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#f5f7fa", edgecolor=GRAY, lw=1),
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))

# 平庸带标注
ax1.text(len(daily) - 1, 1.048, "「平庸走廊」：1.5 个月净值在 ±4% 里晃",
         fontsize=9, color=GRAY, ha="right", zorder=6, fontweight="bold")

ax1.set_ylabel("账户净值（起点 = 1.0）", fontsize=10)
ax1.set_title("考核的隐形杀手不是爆仓，是平庸——同一批 82 笔真实交易 × 0.5% 风险（2026-07-02 ~ 08-10）",
              fontsize=13, color=DARK, pad=12)
ax1.legend(loc="lower left", fontsize=9, frameon=False)
ax1.set_xlim(0, len(daily) + 1)
ax1.set_ylim(0.885, 1.115)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# 统计框（右上内）
stats = (f"样本：82 笔 ÷ 29 个交易日（每天平均 2.8 笔）\n"
         f"29 天里只有 {int((daily > 0).sum())} 天盈利（{(daily > 0).mean() * 100:.0f}%）\n"
         f"最好日 +3.10R（第 1 天）· 最差日 -2.93R（第 29 天）\n"
         f"第 2~29 天 R 总和 {daily.iloc[1:].sum():+.1f}R（大赢日之后全是阴跌）\n"
         f"峰值 +{peak_val:.1f}% · 终值 {final_val:.1f}% · 最大回撤 {max_dd:.1f}%")
ax1.text(0.985, 0.045, stats, transform=ax1.transAxes, ha="right", va="bottom",
         fontsize=8.8, color=DARK, zorder=7,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

# ===== 下：每日 R 柱状图 =====
colors = [GREEN if r >= 0 else RED for r in daily.values]
ax2.bar(x, daily.values, color=colors, alpha=0.85, zorder=3, width=0.72)
ax2.axhline(0, color=GRAY, lw=1.1, zorder=4)

# 第 1 天唯一大赢日
ax2.annotate("第 1 天 +3.10R：82 笔里唯一的大赢日\n（+2.85R 那笔大单）——概率馈赠，不是系统变强",
             xy=(1, daily.iloc[0]),
             xytext=(3.2, 3.05),
             fontsize=9, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 第 29 天最差日
ax2.annotate("第 29 天 -2.93R：最差日\n（末期阴跌收尾）",
             xy=(len(daily), daily.iloc[-1]),
             xytext=(len(daily) - 13, -2.35),
             fontsize=9, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 后半段阴跌标注
ax2.annotate("前 8 天还有起伏\n后 21 天只有 {0} 天为正（合计 {1:.1f}R）".format(
                 int((daily.iloc[8:] > 0).sum()), daily.iloc[8:].sum()),
             xy=(23, daily.iloc[22]),
             xytext=(15.5, 2.0),
             fontsize=9, color=GRAY, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))

ax2.set_ylabel("当日 R 合计", fontsize=10)
ax2.set_xlabel("第 N 个交易日（2026-07-02 起，29 个交易日；每日 1-4 笔按平仓日聚合）", fontsize=10)
ax2.set_ylim(-3.6, 3.8)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

fig.text(0.995, 0.015, "数据源：Binance BTCUSDT 5m K 线重采样 1H 真实回测逐笔记录 · 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig("handbook/images/fig_real_ch9_days.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch9_days.png")
print(f"校验: 峰值第{peak_d}天 +{peak_val:.2f}% | 终值 {final_val:.2f}% | 最大回撤 {max_dd:.2f}% | "
      f"盈利日 {(daily>0).sum()}/29 | 第2~29天R {daily.iloc[1:].sum():.2f}")
