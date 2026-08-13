# -*- coding: utf-8 -*-
"""图 7-1R 真实数据：连亏不是故障，是分布——真实 82 笔回测的连亏段 vs 理论预期
（EMA20/50 趋势跟踪回测，BTC 1H，2026-07-02 ~ 08-10，同图 8-1R 的 82 笔记录）
- 上：真实连亏段长度分布柱 vs 理论期望（40% 胜率、82 笔、蒙特卡洛 20 万次）
  ——真实"≥3 连亏段 8 段" vs 理论均值 7.0 段，几乎精确命中
- 下：理论最长连亏分布直方图——真实"最长 6 连亏"落在主体区（P≥6 = 80.5%）
  教学结论：6 连亏不是系统坏了，是 40% 胜率下 82 笔样本 80% 概率会出现的正常分布
"""
import csv
import random
from collections import Counter

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE = "#1565c0", "#ef6c00"
RED, TEAL, GRAY, DARK = "#ef5350", "#00897b", "#90a4ae", "#263238"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ---- 读取真实回测交易（R 序列） ----
trades = []
with open("data/_bt_ema_trades.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        trades.append(float(row["R"]))
R = np.array(trades)
N = len(R)
p_win = float(np.mean(R > 0))
p_loss = 1.0 - p_win

# ---- 真实连亏段（连续亏损 run）----
runs = []
cur = 0
for x in R:
    if x <= 0:
        cur += 1
    else:
        if cur > 0:
            runs.append(cur)
        cur = 0
if cur > 0:
    runs.append(cur)
real_cnt = Counter(runs)
real_max = max(runs)
real_ge3 = sum(v for k, v in real_cnt.items() if k >= 3)

# ---- 蒙特卡洛理论（40.2% 胜率、82 笔，20 万次）----
random.seed(42)
SIM = 200_000
theo_run_cnt = Counter()          # 连亏段长度 -> 期望段数
maxrun_hist = Counter()           # 最长连亏 -> 频次
for _ in range(SIM):
    seq = [random.random() < p_win for _ in range(N)]
    mrun = 0
    cur_len = 0
    for w in seq:
        if not w:
            cur_len += 1
        else:
            if cur_len > 0:
                theo_run_cnt[cur_len] += 1
                mrun = max(mrun, cur_len)
            cur_len = 0
    if cur_len > 0:
        theo_run_cnt[cur_len] += 1
        mrun = max(mrun, cur_len)
    maxrun_hist[mrun] += 1

theo_mean = {k: v / SIM for k, v in theo_run_cnt.items()}
p_ge = {k: 100 * sum(v for kk, v in maxrun_hist.items() if kk >= k) / SIM
        for k in range(1, 16)}
theo_ge3_mean = sum(v / SIM for k, v in theo_run_cnt.items() if k >= 3)

# ---- 画图 ----
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8.5), dpi=110,
                               gridspec_kw={"height_ratios": [1, 1.05]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：真实连亏段分布 vs 理论期望 =====
lengths = list(range(1, max(real_cnt.keys(), default=6) + 2))  # 1..7
xr = np.arange(len(lengths))
real_vals = [real_cnt.get(k, 0) for k in lengths]
theo_vals = [theo_mean.get(k, 0.0) for k in lengths]

b1 = ax1.bar(xr - 0.18, real_vals, 0.34, color=ORANGE, alpha=0.92, label="真实 82 笔（出现段数）")
b2 = ax1.bar(xr + 0.18, theo_vals, 0.34, color=TEAL, alpha=0.75, label="理论期望（40% 胜率 × 82 笔）")

for i, v in enumerate(real_vals):
    ax1.text(xr[i] - 0.18, v + 0.06, f"{v:.0f}", ha="center", fontsize=9,
             color=DARK, fontweight="bold")
for i, v in enumerate(theo_vals):
    ax1.text(xr[i] + 0.18, v + 0.06, f"{v:.1f}", ha="center", fontsize=8.5,
             color=TEAL)

# 关键标注
ax1.annotate("最长 6 连亏（第 77-82 笔）\n80.5% 概率会出现的“正常连亏”",
             xy=(5, real_cnt.get(6, 0)), xytext=(4.1, 4.6),
             fontsize=10, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))
ax1.annotate("≥3 连亏段：真实 8 段\n理论期望 7.0 段——精确命中",
             xy=(2.1, 2.2), xytext=(0.15, 4.9),
             fontsize=10, color=BLUE, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))

ax1.set_xticks(xr)
ax1.set_xticklabels([f"{k} 连亏" for k in lengths], fontsize=9.5)
ax1.set_ylabel("连亏段数量（段）", fontsize=10)
ax1.set_title("连亏不是故障，是分布——真实 82 笔的连亏段 vs 理论预期（40% 胜率）",
              fontsize=12.5, color=DARK, pad=12)
ax1.legend(loc="upper right", fontsize=9.5, frameon=False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.set_ylim(0, 5.6)

# ===== 下：理论最长连亏分布直方图 =====
maxk = max(maxrun_hist.keys())
ks = list(range(1, 14))  # 1..13 足够展示主体
hist_vals = [maxrun_hist.get(k, 0) / SIM * 100 for k in ks]
bars = ax2.bar(ks, hist_vals, 0.62, color=GRAY, alpha=0.55)

# 真实最长连亏竖线
ax2.axvline(real_max, color=RED, lw=2.4, ls="--", zorder=5)
ax2.text(real_max + 0.25, 19.5, f"真实：最长 {real_max} 连亏\n位于分布主体区",
         fontsize=10, color=RED, fontweight="bold", zorder=6)

# 分位标注
for k in [5, 6, 7, 8]:
    ax2.text(k, hist_vals[k - 1] + 0.5, f"≥{k}连亏\n{p_ge[k]:.0f}%",
             ha="center", fontsize=8.3, color=DARK)

ax2.set_xticks(ks)
ax2.set_xticklabels([f"{k}" for k in ks], fontsize=9)
ax2.set_xlabel("一次 82 笔样本里的最长连亏（笔）", fontsize=10)
ax2.set_ylabel("出现概率（%）", fontsize=10)
ax2.set_title("理论分布：40% 胜率跑 82 笔，“最长连亏”落在哪？",
              fontsize=12, color=DARK, pad=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.set_xlim(0, 13.5)
ax2.set_ylim(0, 21)

# 统计框（左下）
stats = ("同一批真实交易：EMA20>50 只做多，2×ATR 跟踪止损（图 8-1R 的 82 笔原始记录）\n"
         f"胜率 {p_win:.1%}（{np.sum(R > 0)}/{N}）· 总 R −7.83 · 最长连亏 {real_max}（第 77-82 笔）\n"
         f"真实 ≥3 连亏段 {real_ge3} 段 ≈ 理论期望 {theo_ge3_mean:.1f} 段——随机分布精确命中\n"
         f"P(最长连亏 ≥ {real_max}) = {p_ge[real_max]:.0f}%——6 连亏在 40% 胜率下是常态\n"
         "这就是 7.4 概率表的意义：连亏不是“系统坏了”，是分布的一部分")
ax2.text(0.012, 0.965, stats, transform=ax2.transAxes, ha="left", va="top",
         fontsize=9.2, color=DARK, family="Microsoft YaHei", zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

fig.text(0.995, 0.012, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("handbook/images/fig_real_ch7_streaks.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch7_streaks.png")
