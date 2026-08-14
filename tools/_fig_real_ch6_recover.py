# -*- coding: utf-8 -*-
"""图 6-1R 真实数据：回本不对称——同一批 82 笔交易，仓位决定你未来要爬的坡
- 数据：EMA20/50 回测 82 笔真实逐笔记录（BTC 1H，2026-07-02 ~ 08-10，data/_bt_ema_trades.csv）
- 与图 6-2R（原 6-1R）同一序列、同一 7 档风险（0.5%→20%），新角度=回撤的回本成本
- 上：回本不对称理论曲线（y = 1/(1-d) - 1，亏损是乘性的）+ 真实 7 档实际最大回撤 → 回本所需涨幅
     0.5% → -5.6% → +5.9%（小坡）；2% → -21.0% → +26.6%（坡变陡）；20% → -93.7% → +1488%（悬崖）
     垂直虚线 -10% = 考核总回撤线：回本成本被锁在 +11.1% 以内（还能爬回来）
- 下：7 档风险的回本所需涨幅柱（对数刻度，5.9% 与 1488% 同框可比）+ 每柱数值
- 教学结论：回本难度随仓位指数爆炸——控制回撤就是控制你未来要爬的坡（6.1 表的真实数据版）
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, RED, TEAL, ORANGE, GRAY, DARK = "#1565c0", "#e53935", "#00897b", "#ef6c00", "#90a4ae", "#263238"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ---- 读取真实回测交易 ----
trades = []
with open("data/_bt_ema_trades.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        trades.append(float(row["R"]))
R = np.array(trades)
N = len(R)

# ---- 与图 6-2R 完全一致的 7 档风险 ----
risks = [0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2]
dd_max, rec = [], []
for f in risks:
    eq = np.cumprod(1 + f * R)
    peak = np.maximum.accumulate(eq)
    dd = (eq - peak) / peak * 100
    d = dd.min()          # 最大回撤（负值，%）
    dd_max.append(d)
    rec.append((1 / (1 + d / 100) - 1) * 100)  # 回本所需涨幅（%）

print("=== 7 档风险：最大回撤 → 回本所需涨幅 ===")
for r, d, g in zip(risks, dd_max, rec):
    print(f"  风险 {r*100:.0f}%: 最大回撤 {d:+.1f}% → 回本需 {g:+.1f}%")

# ---- 绘图 ----
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8.6), dpi=110,
                               gridspec_kw={"height_ratios": [1.22, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：回本不对称理论曲线 + 真实点 =====
dd_x = np.linspace(0, 96, 400)
curve_y = (1 / (1 - dd_x / 100) - 1) * 100
ax1.plot(dd_x, curve_y, color=BLUE, lw=2.2, zorder=3,
         label="回本所需涨幅 = 1/(1 − 回撤) − 1（亏损是乘性的：越深越贵）")

# 考核 -10% 线
ax1.axvline(-10, color=RED, lw=1.6, ls="--", zorder=4)
ax1.annotate("考核总回撤线 −10%：\n回本成本被锁在 +11.1% 以内\n——平台保证你“还能爬回来”",
             xy=(-10, 16), xytext=(-34, 210),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 真实 7 点（x = |回撤|，y = 回本涨幅）
xr = [-d for d in dd_max]
colors7 = ["#00897b", "#2e86c1", "#5fa8d3", "#90a4ae", "#ef6c00", "#e53935", "#c62828"]
for i, (x, y) in enumerate(zip(xr, rec)):
    ax1.scatter(x, y, s=64, color=colors7[i], zorder=6, edgecolor="white", lw=1)
    if i in (0, 2, 6):
        ax1.annotate(f"风险 {risks[i]*100:.0f}%：回撤 −{abs(dd_max[i]):.1f}% → 回本 +{rec[i]:.0f}%"
                     + ("（小坡）" if i == 0 else "（坡变陡）" if i == 2 else "（悬崖）"),
                     xy=(x, y), xytext=(x - 24, y + 150 if i != 0 else 190),
                     fontsize=9, color=colors7[i], fontweight="bold", zorder=6,
                     arrowprops=dict(arrowstyle="->", color=colors7[i], lw=1.1))

ax1.set_xlabel("最大回撤深度（%）", fontsize=10)
ax1.set_ylabel("回本所需涨幅（%）", fontsize=10)
ax1.set_ylim(0, 1650)
ax1.set_title("回本不对称的真实版本——同一批 82 笔交易 × 7 档风险：仓位决定你未来要爬的坡有多陡",
              fontsize=13, color=DARK, pad=12)
ax1.legend(loc="upper left", fontsize=9.5, frameon=False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# 小回撤区放大标注（线性轴下 5.9% 太小，画放大圈）
ax1.annotate("0.5% 风险：−5.6% → 只赚 +6.0% 就回本（几天的坡）",
             xy=(-5.6, 5.9), xytext=(8, 340),
             fontsize=9, color=TEAL, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#e0f2f1", edgecolor=TEAL, lw=1),
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1))

# ===== 下：回本所需涨幅柱（对数）=====
xr2 = np.arange(len(risks))
bars = ax2.bar(xr2, rec, 0.6, color=colors7, alpha=0.92, zorder=3)
for i, (r, g) in enumerate(zip(risks, rec)):
    ax2.text(i, g * 1.18, f"{g:+.0f}%", ha="center", va="bottom",
             fontsize=9, color=colors7[i], fontweight="bold", zorder=6)
ax2.axhline(11.1, color=RED, lw=1.4, ls="--", zorder=4)
ax2.text(6.4, 14, "考核 −10% 线对应的回本成本 +11.1%", fontsize=9, color=RED,
         ha="right", fontweight="bold", zorder=6)
ax2.set_xticks(xr2)
ax2.set_xticklabels([f"{r*100:.0f}%" for r in risks], fontsize=10)
ax2.set_xlabel("单笔风险", fontsize=10)
ax2.set_ylabel("回本所需涨幅（%，对数刻度）", fontsize=10)
ax2.set_yscale("log")
ax2.set_ylim(4, 4000)
ax2.set_title("同样的亏损路径，不同仓位的“回本坡高”：0.5% 的坡 5.9%，20% 的坡 1488%——差 250 倍",
              fontsize=12, color=DARK, pad=8)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

fig.text(0.995, 0.012, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔真实逐笔 R）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("handbook/images/fig_real_ch6_recover.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch6_recover.png")
