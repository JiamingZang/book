# -*- coding: utf-8 -*-
"""图 1-1R 真实数据：BTC vs ETH 波动率对比（Binance 5m，2026-06-29 ~ 08-13）
- 上：归一化价格（起点 100）——同涨同跌（呼应 1.14 相关性）
- 下：24h 滚动波动率（日均化 1σ %）——高峰=恐慌/事件（呼应 1.8），低谷=平静（呼应 1.13 波动极大/止损要宽）
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

btc = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
eth = pd.read_csv("data/ethusdt_5m.csv", parse_dates=["time"])
btc["r"] = btc["close"].pct_change()
eth["r"] = eth["close"].pct_change()

# 归一化价格（起点 100）
p0b, p0e = btc["close"].iloc[0], eth["close"].iloc[0]
btc["px"] = btc["close"] / p0b * 100
eth["px"] = eth["close"] / p0e * 100

# 24h 滚动波动（一天 288 根 5m，日均化 1σ %）
W = 288
btc["vol"] = btc["r"].rolling(W).std() * np.sqrt(W) * 100
eth["vol"] = eth["r"].rolling(W).std() * np.sqrt(W) * 100

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), dpi=110,
                               gridspec_kw={"height_ratios": [1, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：归一化价格 =====
ax1.plot(btc["time"], btc["px"], color=BLUE, lw=1.3, label="BTC（比特币）")
ax1.plot(eth["time"], eth["px"], color=ORANGE, lw=1.3, label="ETH（以太坊）")

# 关键区段阴影：7/02 附近暴跌（波动高峰）
ax1.axvspan(pd.Timestamp("2026-06-30 00:00"), pd.Timestamp("2026-07-05 00:00"),
            color=RED, alpha=0.06, zorder=1)
ax1.text(pd.Timestamp("2026-06-30 12:00"), 111, "6/30-7/02 恐慌暴跌\n（波动率高峰，呼应 1.8 数据事件/黑天鹅）",
         fontsize=9, color=RED, fontweight="bold", zorder=6)

ax1.text(pd.Timestamp("2026-08-06 12:00"), 100.5, "8/9 前后平静\n（波动率谷底）",
         fontsize=9, color=TEAL, fontweight="bold", zorder=6)

ax1.set_ylabel("归一化价格（起点 = 100）", fontsize=10)
ax1.set_title("BTC vs ETH：同涨同跌的兄弟品种，波动率却不同（Binance 5m，2026-06-29 ~ 08-13）",
              fontsize=13, color=DARK, pad=12)
ax1.legend(loc="upper left", fontsize=10, frameon=False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

# ===== 下：24h 滚动波动率 =====
ax2.plot(btc["time"], btc["vol"], color=BLUE, lw=1.3, label="BTC 24h 滚动波动（日均 1σ %）")
ax2.plot(eth["time"], eth["vol"], color=ORANGE, lw=1.3, label="ETH 24h 滚动波动（日均 1σ %）")
ax2.axvspan(pd.Timestamp("2026-06-30 00:00"), pd.Timestamp("2026-07-05 00:00"),
            color=RED, alpha=0.06, zorder=1)

# 峰谷标注
peak_t = pd.Timestamp("2026-07-02 12:00")
ax2.annotate("峰值：BTC 2.9% / ETH 3.7%\n恐慌时波动率飙升（1σ 即如此，2σ 就是 6-7%）",
             xy=(peak_t, 3.7), xytext=(pd.Timestamp("2026-07-06 12:00"), 4.1),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

valley_t = pd.Timestamp("2026-08-09 12:00")
ax2.annotate("谷底：BTC 0.4% / ETH 0.6%\n平静期波动率腰斩再腰斩",
             xy=(valley_t, 0.6), xytext=(pd.Timestamp("2026-08-04 12:00"), 1.6),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

ax2.axhline(2.0, color=GRAY, lw=1, ls=":")
ax2.text(pd.Timestamp("2026-06-29 09:00"), 2.05, "对照：ES/NQ 等成熟股指的日均波动约 1% 以内",
         fontsize=9, color=GRAY, zorder=6)

ax2.set_ylabel("24h 滚动波动率（日均 1σ %）", fontsize=10)
ax2.set_xlabel("2026 年（月-日）", fontsize=10)
ax2.legend(loc="upper left", fontsize=10, frameon=False)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))

# 统计框（右下）
stats = ("BTC：5m 收益 σ = 0.098%，日均波动 1.67%，年化 32%\n"
         "ETH：5m 收益 σ = 0.133%，日均波动 2.25%，年化 43%\n"
         "ETH 波动 ≈ BTC 的 1.35 倍——同族品种脾气也不同")
ax2.text(0.985, 0.97, stats, transform=ax2.transAxes, ha="right", va="top",
         fontsize=9.5, color=DARK, family="Microsoft YaHei", zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

fig.text(0.995, 0.015, "数据源：Binance BTCUSDT / ETHUSDT 5m K 线 · 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig("handbook/images/fig_real_ch1_vol.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch1_vol.png")
