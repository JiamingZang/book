# -*- coding: utf-8 -*-
"""图 8-1R 真实数据：简单趋势策略的回测输出（BTC 1H，2026-07-02 ~ 08-10）
- 上：权益曲线（每笔风险 0.5%，累计净值）——阶梯式逐笔变化
- 下：回撤曲线（% 回撤，填充）——标注最大回撤
- 策略诚实标注为亏损（总 R -7.8，SQN -1.43）：验证的价值=上模拟盘前发现系统不行
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BLUE, ORANGE = "#1565c0", "#ef6c00"
RED, TEAL, GRAY, DARK = "#ef5350", "#00897b", "#90a4ae", "#263238"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

tr = pd.read_csv("data/_bt_ema_trades.csv", parse_dates=["t_in", "t_out"])
R = tr["R"].values
eq = pd.Series((1 + R * 0.005).cumprod())
peak = eq.cummax()
dd = (eq - peak) / peak * 100

# 逐笔 x 坐标（按平仓时间）
x = tr["t_out"]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), dpi=110,
                               sharex=True,
                               gridspec_kw={"height_ratios": [1.15, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：权益曲线 =====
ax1.plot(x, eq.values, drawstyle="steps-post", color=BLUE, lw=1.8, label="累计净值（每笔风险 0.5%）")
ax1.axhline(1.0, color=GRAY, lw=1, ls=":")
ax1.fill_between(x, 1.0, eq.values, step="post", where=(eq.values >= 1.0),
                 color=BLUE, alpha=0.08, interpolate=False)
ax1.fill_between(x, 1.0, eq.values, step="post", where=(eq.values < 1.0),
                 color=RED, alpha=0.08, interpolate=False)

# 最大回撤区间标注（回撤起点到终点）
dd_min_i = int(dd.idxmin())
dd_start = eq.cummax().iloc[dd_min_i]  # 回撤起点净值
ax1.annotate("最大回撤区间：从净值 1.019 一路跌到 0.961（-5.6%）\n最后一笔亏损把前期盈利全部吐回",
             xy=(x.iloc[dd_min_i], eq.iloc[dd_min_i]),
             xytext=(pd.Timestamp("2026-07-20"), 1.035),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

ax1.text(x.iloc[0] + pd.Timedelta(days=1), 0.985, "初期小赚（7 月初趋势段）\n随后震荡市反复止损",
         fontsize=9, color=DARK, zorder=6)

ax1.set_ylabel("累计净值（起点 = 1.0）", fontsize=10)
ax1.set_title("真实回测输出：EMA20/50 趋势跟踪在 BTC 1H——结果是亏损的，这正是验证的价值（2026-07-02 ~ 08-10）",
              fontsize=13, color=DARK, pad=12)
ax1.legend(loc="upper left", fontsize=10, frameon=False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

# ===== 下：回撤曲线 =====
ax2.fill_between(x, 0, dd.values, step="post", color=RED, alpha=0.55)
ax2.axhline(0, color=GRAY, lw=1)
dd_min = dd.min()
ax2.annotate(f"最大回撤 {dd_min:.2f}%\n（第 {dd_min_i + 1}/{len(tr)} 笔）",
             xy=(x.iloc[dd_min_i], dd_min),
             xytext=(pd.Timestamp("2026-07-22"), dd_min - 3.5),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax2.set_ylabel("回撤（%）", fontsize=10)
ax2.set_xlabel("平仓时间（2026-07 ~ 08）", fontsize=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

# 指标框（右下）
sqn = np.sqrt(len(R)) * R.mean() / R.std()
wins = (R > 0).mean()
wr = np.abs(R[R > 0].mean() / R[R < 0].mean()) if (R < 0).any() else float("nan")
stats = (f"策略：EMA20>50 做多，2×ATR 跟踪止损，跌破 EMA50 离场（只做多）\n"
         f"样本：82 笔 · 40 天 · BTC 1H（2026-07-02 ~ 08-10）\n"
         f"胜率 {wins * 100:.0f}% · 盈亏比 {wr:.2f} · 总 R {R.sum():.2f} · 平均 R {R.mean():.3f}\n"
         f"SQN = {sqn:.2f}（< 1.6，差）· 最大回撤 {dd_min:.2f}%")
ax2.text(0.985, 0.97, stats, transform=ax2.transAxes, ha="right", va="top",
         fontsize=9.5, color=DARK, zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

fig.text(0.995, 0.015, "数据源：Binance BTCUSDT 5m K 线重采样 1H · 教学示意（参数未优化），不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig("handbook/images/fig_real_ch8_backtest.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch8_backtest.png")
