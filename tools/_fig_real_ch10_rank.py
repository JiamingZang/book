# -*- coding: utf-8 -*-
"""图 10-6R 真实数据：IV Rank 就是你的买卖仪表盘——低买高卖画在历史上
（QVIX 全历史时间序列 + 分位阈值带 + 恐慌尖峰 + VRP 分组实证，2015-02 ~ 2026-08，2787 个交易日）
- 上：QVIX 全历史时间序列——P25=16.3 低买线 / P75=23.3 高卖线 / P90=30.7 极端线；
      <P25 淡青=便宜（买方优势）、>P75 淡橙=贵（卖方优势）、>P90 淡红=极端（卖方纪律）；
      标注大恐慌尖峰（2015-08 股灾 63.8 / 2016-01 熔断 39.0 / 2018-02 波动率炸弹 33.1 /
      2020-03 疫情 40.6 / 2024-10 大涨后 53.5 / 2026-03 恐慌 42.2）；当前 2026-08 QVIX 17.2 = Rank 31
- 下：按 IV Rank 分 6 组——每组 当前 QVIX 均值 vs 未来 20 日 RV 均值：
      6 组全部 IV > 未来 RV（VRP 结构性常态，不是某区专属）
"""
import sys
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

sys.stdout.reconfigure(encoding="utf-8")

BLUE, ORANGE, GRAY = "#1565c0", "#ef6c00", "#90a4ae"
TEAL, RED, DARK = "#26a69a", "#ef5350", "#263238"
LIGHT = "#f5f7fa"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ---- 数据（与图 10-4R/10-5R 同源）----
q = ak.index_option_50etf_qvix()
q["date"] = pd.to_datetime(q["date"])
q = q.set_index("date").sort_index()
etf = ak.fund_etf_hist_sina(symbol="sh510050")
etf["date"] = pd.to_datetime(etf["date"])
etf = etf.set_index("date").sort_index()
ret = np.log(etf["close"]).diff()
rv = (ret.rolling(20).std() * np.sqrt(252) * 100).rename("RV20")
df = pd.concat([q["close"].rename("QVIX"), rv], axis=1).dropna()
qv, rv_s = df["QVIX"], df["RV20"]
n = len(df)
p25, p75, p90 = qv.quantile(.25), qv.quantile(.75), qv.quantile(.90)
cur, cur_rank = qv.iloc[-1], qv.rank(pct=True).iloc[-1]

# 未来 20 日 RV 均值（对齐：t 日 = mean(RV[t+1..t+20])）
fwd = rv_s[::-1].rolling(20).mean()[::-1].shift(-1)

# 峰值事件（数据验证过）
events = [
    ("2015-08-26", 63.8, "2015-08 股灾"),
    ("2016-01-29", 39.0, "2016-01 熔断"),
    ("2018-02-09", 33.1, "2018-02\n波动率炸弹"),
    ("2020-03-16", 40.6, "2020-03 疫情"),
    ("2024-10-08", 53.5, "2024-10\n大涨后"),
    ("2026-03-23", 42.2, "2026-03 恐慌"),
]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14.5, 7.0), dpi=110,
                               gridspec_kw={"height_ratios": [1.35, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：QVIX 全历史时间序列 + 阈值带 =====
ax1.axhspan(0, p25, color=TEAL, alpha=0.09, zorder=1)
ax1.axhspan(p75, p90, color=ORANGE, alpha=0.12, zorder=1)
ax1.axhspan(p90, 68, color=RED, alpha=0.08, zorder=1)
ax1.plot(qv.index, qv.values, color=BLUE, lw=1.3, zorder=3, label="QVIX（50ETF 期权隐含波动率）")
ax1.axhline(p25, color=TEAL, lw=1.5, ls="--")
ax1.text(qv.index[30], p25 + 0.7, f"P25 = {p25:.1f} 低买线（买方优势）", fontsize=9, color=TEAL, fontweight="bold")
ax1.axhline(p75, color=ORANGE, lw=1.5, ls="--")
ax1.text(qv.index[30], p75 + 0.7, f"P75 = {p75:.1f} 高卖线（卖方优势）", fontsize=9, color=ORANGE, fontweight="bold")
ax1.axhline(p90, color=RED, lw=1.5, ls="--")
ax1.text(qv.index[30], p90 + 0.7, f"P90 = {p90:.1f} 极端（卖方纪律区）", fontsize=9, color=RED, fontweight="bold")

for i, (d, v, label) in enumerate(events):
    dt = pd.Timestamp(d)
    xpos = mdates.date2num(dt)
    yoff = 6 if i % 2 == 0 else -12
    ax1.annotate(f"{label}\n{v:.0f}", xy=(xpos, v), xytext=(xpos + 120, v + yoff),
                 fontsize=8.8, color=RED, fontweight="bold", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))

# 当前点标注
ax1.annotate(f"当前 {cur:.1f}\nIV Rank {cur_rank*100:.0f}——中低位",
             xy=(mdates.date2num(qv.index[-1]), cur), xytext=(mdates.date2num(qv.index[-1]) - 260, 34),
             fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

ax1.set_ylabel("QVIX（年化隐含波动率 %）", fontsize=10)
ax1.set_title("IV Rank 就是你的买卖仪表盘：QVIX 全历史 + 分位阈值带（2015-02 ~ 2026-08，2787 个交易日）",
              fontsize=12.5, color=DARK, pad=10)
ax1.legend(loc="upper left", fontsize=9, frameon=False)
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax1.set_ylim(0, 68)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# ===== 下：按 IV Rank 分组：当前 IV vs 未来 20 日 RV =====
bins = [(0.0, 0.10, "P0-10"), (0.10, 0.25, "P10-25"), (0.25, 0.50, "P25-50"),
        (0.50, 0.75, "P50-75"), (0.75, 0.90, "P75-90"), (0.90, 1.0, "P90-100")]
rk = qv.rank(pct=True)
xpos = np.arange(len(bins))
w = 0.34
for i, (lo, hi, name) in enumerate(bins):
    mask = (rk > lo) & (rk <= hi)
    iv_m, fwd_m = qv[mask].mean(), fwd[mask].mean()
    cnt = mask.sum()
    ax2.bar(xpos[i] - w / 2, iv_m, w, color=BLUE, alpha=0.85, label="当前 IV（QVIX）" if i == 0 else None)
    ax2.bar(xpos[i] + w / 2, fwd_m, w, color=ORANGE, alpha=0.85, label="未来 20 日 RV" if i == 0 else None)
    ax2.text(xpos[i] - w / 2, iv_m + 1, f"{iv_m:.1f}", ha="center", fontsize=8.6, color=BLUE, fontweight="bold")
    ax2.text(xpos[i] + w / 2, fwd_m + 1, f"{fwd_m:.1f}", ha="center", fontsize=8.6, color=ORANGE, fontweight="bold")
    ax2.text(xpos[i], -4.5, f"{cnt}天", ha="center", fontsize=8, color=GRAY)

ax2.text(2.5, 42, "6 组全部 IV > 未来 20 日 RV：\nVRP 不是某个区专属，是结构性常态\n（卖方长期收保费，买方长期付保费）",
         fontsize=9.5, color=DARK, fontweight="bold", ha="center",
         bbox=dict(boxstyle="round,pad=0.5", facecolor=LIGHT, edgecolor=GRAY, lw=0.8))
ax2.annotate("低 IV 区：价差小但尾部风险可控\n买方买的是“便宜保险 + 尾部非对称”",
             xy=(0, 13), xytext=(0.1, 24), fontsize=9, color=TEAL, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1))
ax2.annotate("高 IV 区：价差最厚但尾部风险最大\n卖方收的是“最贵保费”，要 10.5 的纪律",
             xy=(5, 42), xytext=(3.4, 30), fontsize=9, color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))

ax2.set_xticks(xpos)
ax2.set_xticklabels([b[2] for b in bins], fontsize=9)
ax2.set_ylabel("年化波动率（%）", fontsize=10)
ax2.set_xlabel("当前 QVIX 所在历史分位区（IV Rank）", fontsize=10)
ax2.legend(loc="upper left", fontsize=9, frameon=False)
ax2.set_ylim(0, 48)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

fig.text(0.995, 0.008, "数据源：AkShare 新浪（QVIX = 50ETF 期权隐含波动率指数 / 510050 日线计算 RV20，2787 个交易日）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig("handbook/images/fig_real_ch10_rank.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch10_rank.png")
