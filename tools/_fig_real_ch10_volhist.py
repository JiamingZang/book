# -*- coding: utf-8 -*-
"""图 10-5R 真实数据：波动率的分布不是正态——大部分时间平静、偶尔爆炸（IV Rank 的统计基础）
（10.5 波动率：QVIX/RV20 全历史分布，2015-02 ~ 2026-08，2787 个交易日）
- 上：RV20 全历史直方图 vs 同均值同方差正态曲线——右偏肥尾（偏度 2.13、峰度 6.10）
      左尾被 0 截断（波动率不能为负）、右尾长（P99 64.8%）；大部分时间平静（中位 15.8%）
- 下左：QVIX vs RV20 双直方图对比——IV 整体右移（78.1% 交易日 IV>RV、均值差 +2.25pct = VRP 溢价常态）
- 下右：IV Rank 分位数柱（P25/P50/P75/P90/P99）+ 说明（IV Rank 50=中位 19.4；右偏下平均数骗人）
"""
import sys
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

BLUE, ORANGE, GRAY = "#1565c0", "#ef6c00", "#90a4ae"
TEAL, RED, DARK = "#26a69a", "#ef5350", "#263238"
LIGHT = "#f5f7fa"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ---- 数据（与图 10-4R 同源）----
q = ak.index_option_50etf_qvix()
q["date"] = pd.to_datetime(q["date"])
q = q.set_index("date").sort_index()
etf = ak.fund_etf_hist_sina(symbol="sh510050")
etf["date"] = pd.to_datetime(etf["date"])
etf = etf.set_index("date").sort_index()
ret = np.log(etf["close"]).diff()
rv = (ret.rolling(20).std() * np.sqrt(252) * 100).rename("RV20")
df = pd.concat([q["close"].rename("QVIX"), rv], axis=1).dropna()

n_days = len(df)
rv_s, qv_s = df["RV20"], df["QVIX"]
rv_skew, rv_kurt = rv_s.skew(), rv_s.kurtosis()
qv_skew, qv_kurt = qv_s.skew(), qv_s.kurtosis()
pct_iv_gt_rv = (qv_s > rv_s).mean()
mean_sp = (qv_s - rv_s).mean()

print(f"天数 {n_days} | RV20 偏度 {rv_skew:.2f} 峰度 {rv_kurt:.2f} | QVIX 偏度 {qv_skew:.2f} 峰度 {qv_kurt:.2f}")
print(f"IV>RV {pct_iv_gt_rv:.1%} | 均值差 {mean_sp:.2f}")
for col in ["RV20", "QVIX"]:
    s = df[col]
    print(f"{col}: 均值 {s.mean():.2f} 中位 {s.median():.2f} P25 {s.quantile(.25):.2f} P75 {s.quantile(.75):.2f} P90 {s.quantile(.90):.2f} P99 {s.quantile(.99):.2f} 最大 {s.max():.2f}")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14.2, 7.4), dpi=110,
                                    gridspec_kw={"width_ratios": [1.12, 1.05, 0.83]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2, ax3):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：RV20 直方图 vs 正态 =====
bins = np.arange(0, 85, 2.5)
ax1.hist(rv_s, bins=bins, color=ORANGE, alpha=0.65, edgecolor="white", lw=0.4, zorder=3)
x = np.linspace(0, 85, 400)
mu, sd = rv_s.mean(), rv_s.std()
ax1.plot(x, len(rv_s) * 2.5 * (1 / (sd * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sd) ** 2),
         color=GRAY, lw=2, ls="--", label="同均值同方差的正态分布")
ax1.axvline(rv_s.median(), color=TEAL, lw=1.6, ls=":", label=f"中位 {rv_s.median():.1f}%")
ax1.axvline(mu, color=BLUE, lw=1.4, ls=":", label=f"均值 {mu:.1f}%（被右尾拉高）")
ax1.annotate("右尾长：偶尔爆炸\nP99 = 64.8%\n（2015 股灾 / 2016 熔断 / 2020 疫情 / 2025 极端）",
             xy=(64, 12), xytext=(50, 250),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax1.annotate("左尾被 0 截断\n（波动率不能为负）",
             xy=(2, 120), xytext=(8, 320),
             fontsize=9, color=GRAY, zorder=6,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0))
ax1.text(0.02, 0.97, f"右偏肥尾：偏度 {rv_skew:.2f} / 峰度 {rv_kurt:.2f}（正态 = 0）\n大部分时间平静（中位 15.8%），少数日子爆炸",
         transform=ax1.transAxes, fontsize=8.8, color=DARK, va="top",
         bbox=dict(boxstyle="round,pad=0.5", facecolor=LIGHT, edgecolor=GRAY, lw=0.8))
ax1.set_xlabel("已实现波动率 RV20（年化 %）", fontsize=10)
ax1.set_ylabel("天数（共 2787 个交易日）", fontsize=10)
ax1.set_title("现实（RV20）的分布：不是正态，是右偏肥尾", fontsize=12, color=DARK, pad=10)
ax1.legend(loc="upper right", fontsize=8.5, frameon=False)
ax1.set_xlim(0, 82)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# ===== 下左：QVIX vs RV20 双直方图 =====
bins2 = np.arange(0, 85, 2.5)
ax2.hist(rv_s, bins=bins2, color=ORANGE, alpha=0.5, edgecolor="white", lw=0.4, zorder=3,
         label=f"RV20（现实）：中位 {rv_s.median():.1f}%")
ax2.hist(qv_s, bins=bins2, color=BLUE, alpha=0.5, edgecolor="white", lw=0.4, zorder=3,
         label=f"QVIX（预期）：中位 {qv_s.median():.1f}%")
ax2.axvline(rv_s.median(), color=ORANGE, lw=1.4, ls=":")
ax2.axvline(qv_s.median(), color=BLUE, lw=1.4, ls=":")
ax2.annotate(f"IV 整体在 RV 右边：\n{pct_iv_gt_rv:.0f}% 交易日 IV > RV\n均值差 +{mean_sp:.1f}pct",
             xy=(22, 170), xytext=(28, 240),
             fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))
ax2.text(0.02, 0.97, "预期（QVIX）整体右移 = 波动率风险溢价：\n保险费（IV）长期卖得比事故成本（RV）贵",
         transform=ax2.transAxes, fontsize=8.8, color=DARK, va="top",
         bbox=dict(boxstyle="round,pad=0.5", facecolor=LIGHT, edgecolor=GRAY, lw=0.8))
ax2.set_xlabel("年化波动率（%）", fontsize=10)
ax2.set_ylabel("天数", fontsize=10)
ax2.set_title("预期（QVIX）vs 现实（RV20）：IV 右移 = VRP", fontsize=12, color=DARK, pad=10)
ax2.legend(loc="upper right", fontsize=8.5, frameon=False)
ax2.set_xlim(0, 82)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

# ===== 下右：IV Rank 分位数 =====
qs = [25, 50, 75, 90, 99]
vals = [qv_s.quantile(p / 100) for p in qs]
colors = [TEAL, BLUE, BLUE, ORANGE, RED]
bars = ax3.bar([str(p) for p in qs], vals, 0.55, color=colors, alpha=0.85)
for b, v in zip(bars, vals):
    ax3.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}", ha="center", fontsize=9.5,
             color=DARK, fontweight="bold")
ax3.axhline(qv_s.median(), color=GRAY, lw=1, ls=":")
ax3.set_ylim(0, 56)
ax3.set_ylabel("QVIX 值（%）", fontsize=10)
ax3.set_xlabel("历史分位数（IV Rank）", fontsize=10)
ax3.set_title("IV Rank = 你站在分布哪里", fontsize=12, color=DARK, pad=10)
ax3.text(0.02, 0.97, "IV Rank 50 = 当前 IV 在历史中位（19.4）——\n高于它倾向卖方、低于它倾向买方（低买高卖分界线）\n注意：中位 19.4 vs 均值 21.1——右偏让平均数骗人，\n判断高低用分位数不用均值",
         transform=ax3.transAxes, fontsize=8.6, color=DARK, va="top",
         bbox=dict(boxstyle="round,pad=0.5", facecolor=LIGHT, edgecolor=GRAY, lw=0.8))
ax3.grid(axis="y", color="#eceff1", lw=0.7)

fig.suptitle("波动率的分布不是正态：大部分时间平静、偶尔爆炸——QVIX / RV20 全历史分布（2015-02 ~ 2026-08）",
             fontsize=12.5, color=DARK, y=0.975)
fig.text(0.995, 0.008, "数据源：AkShare 新浪（QVIX = 50ETF 期权隐含波动率指数 / 510050 日线计算 RV20，2787 个交易日）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 0.955])
fig.savefig("handbook/images/fig_real_ch10_volhist.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch10_volhist.png")
