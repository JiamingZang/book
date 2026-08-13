# -*- coding: utf-8 -*-
"""图 6-2R 真实数据：同样的 82 笔交易，仓位决定回撤深度与是否爆仓
（EMA20/50 趋势跟踪回测，BTC 1H，2026-07-02 ~ 08-10，总 R -7.83，验证不合格——同图 8-1R 数据）
- 上：不同单笔风险（0.5%→20%）下的账户净值曲线——回撤≈线性、期末净值≈指数衰减
- 下：各风险档位的最大回撤 vs 期末净值对比柱——仓位是"存活"开关，不是"收益"旋钮
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

# ---- 各风险档位的净值与回撤 ----
risks = [0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2]
curves, dd_max, ends = [], [], []
for f in risks:
    eq = np.cumprod(1 + f * R)
    peak = np.maximum.accumulate(eq)
    dd = (eq - peak) / peak * 100
    curves.append(eq)
    dd_max.append(dd.min())
    ends.append(eq[-1] * 100)

x = np.arange(N)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8.5), dpi=110,
                               gridspec_kw={"height_ratios": [1.25, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：净值曲线族 =====
colors = ["#1565c0", "#2e86c1", "#5fa8d3", "#90a4ae", "#ef6c00", "#e53935", "#c62828"]
labels = ["0.5%", "1%", "2%", "3%", "5%", "10%", "20%"]
for eq, c, lab in zip(curves, colors, labels):
    ax1.plot(x + 1, eq, drawstyle="steps-post", color=c, lw=1.6,
             label=f"单笔风险 {lab}" + ("（≈爆仓）" if lab == "20%" else ""))

ax1.axhline(1.0, color=GRAY, lw=1, ls=":")

# 关键标注：1% 与 20%
ax1.annotate("1% 风险：最大回撤 −11%\n即使系统验证不合格，账户也活着",
             xy=(N, 0.923), xytext=(30, 1.12),
             fontsize=9.5, color=BLUE, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
ax1.annotate("20% 风险：最大回撤 −93.7%\n只剩 11.7% 本金——考核/实盘早出局",
             xy=(N, 0.117), xytext=(40, 0.62),
             fontsize=9.5, color="#c62828", fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color="#c62828", lw=1.2))

ax1.set_ylabel("账户净值（起点 = 1.0）", fontsize=10)
ax1.set_title("同样的 82 笔交易，仓位决定你是亏 11% 还是爆仓（真实回测：EMA20/50 趋势跟踪，BTC 1H，2026-07-02 ~ 08-10）",
              fontsize=12.5, color=DARK, pad=12)
ax1.legend(loc="upper left", fontsize=9.5, frameon=False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.set_xticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 82])
ax1.set_xlim(0.5, N + 1)

# ===== 下：最大回撤 vs 期末净值 =====
xr = np.arange(len(risks))
w = 0.34
bars_dd = ax2.bar(xr - w / 2, dd_max, w, color=RED, alpha=0.85, label="最大回撤（%）")
bars_end = ax2.bar(xr + w / 2, ends, w, color=DARK, alpha=0.55, label="期末净值（%，起点 100）")

# 回撤≈线性拟合示意
ax2.plot(xr, dd_max, "o-", color=RED, lw=1.2, ms=3, alpha=0.5)

ax2.axhline(-10, color=GRAY, lw=1.2, ls="--")
ax2.text(6.35, -11.5, "典型 prop 考核总回撤上限 −10%",
         fontsize=9, color=GRAY, ha="right", zorder=6)

for i, (d, e) in enumerate(zip(dd_max, ends)):
    ax2.text(xr[i] - w / 2, d - 2.5, f"{d:.0f}%", ha="center", fontsize=8.5, color=RED)
    ax2.text(xr[i] + w / 2, e + 1.5, f"{e:.0f}", ha="center", fontsize=8.5, color=DARK)

ax2.set_xticks(xr)
ax2.set_xticklabels([f"{r * 100:.0f}%" for r in risks])
ax2.set_ylabel("百分比（%）", fontsize=10)
ax2.set_xlabel("单笔风险（每笔占总资金的比例）", fontsize=10)
ax2.legend(loc="upper right", fontsize=9.5, frameon=False)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

# 统计框（左下）
stats = ("同一笔交易序列：EMA20>50 只做多，2×ATR 跟踪止损（图 8-1R 的原始数据）\n"
         "82 笔 · 胜率 40% · 总 R −7.83（系统本身验证不合格）\n"
         "风险 0.5% → 回撤 −5.6%   ·   1% → −11.0%   ·   2% → −21.0%\n"
         "风险 5% → −45.4%   ·   10% → −71.8%   ·   20% → −93.7%（几乎爆仓）\n"
         "规律：回撤 ≈ 随风险线性上升，期末净值 ≈ 随风险指数衰减\n"
         "——仓位是“存活”的开关，不是“多赚”的旋钮（呼应 6.1 犯错预算 / 6.8 破产概率）")
ax2.text(0.012, 0.97, stats, transform=ax2.transAxes, ha="left", va="top",
         fontsize=9.3, color=DARK, family="Microsoft YaHei", zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

fig.text(0.995, 0.012, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("handbook/images/fig_real_ch6_risk.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch6_risk.png")
