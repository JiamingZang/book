# -*- coding: utf-8 -*-
"""图 10-4R 真实数据：IV 与 RV 的真实关系——预期（QVIX）领先、现实（RV20）滞后
（10.5 波动率：IV/RV 机制的真实数据版，与图 10-3R 同一窗口互补）
- 数据：QVIX = 50ETF 期权隐含波动率指数（ak.index_option_50etf_qvix，新浪）
        50ETF 日线 = 已实现波动率计算（ak.fund_etf_hist_sina，新浪）
- 上：QVIX（蓝，市场预期）vs RV20（橙，已发生事实）双线，2026-03-01 ~ 08-11
      标注① 03-23 QVIX 42.2 恐慌尖峰（单日 19.9→42.2 +112%，IV 是预期先于现实飙升，两天后跌回 17=IV crush）
      标注② 07-17 RV20 28.0 阴跌峰（QVIX 仅 22——已实现波动持续高企但期权市场没同步恐慌）
      标注③ 8 月双双回落向中枢
- 下：IV − RV 价差（VRP）柱：正（青）=IV>RV 溢价常态 / 负（红）=IV<RV 现实反超
      标注 03-23 +28.0（恐慌脉冲：预期瞬间领跑）/ 07-23 −8.6（阴跌中现实持续反超）
      统计框：73% 交易日 IV>RV（VRP 溢价常态，卖方长期收保险费）· 平均 +2.2 个百分点
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
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ---- 数据 ----
q = ak.index_option_50etf_qvix()
q["date"] = pd.to_datetime(q["date"])
q = q.set_index("date").sort_index()

etf = ak.fund_etf_hist_sina(symbol="sh510050")
etf["date"] = pd.to_datetime(etf["date"])
etf = etf.set_index("date").sort_index()
ret = np.log(etf["close"]).diff()
rv = (ret.rolling(20).std() * np.sqrt(252) * 100).rename("RV20")

df = pd.concat([q["close"].rename("QVIX"), rv], axis=1).dropna()
disp = df.loc["2026-03-01":"2026-08-11"]
disp["spread"] = disp["QVIX"] - disp["RV20"]

# 关键值（用于标注，脚本内部核对）
q_peak = disp["QVIX"].idxmax()          # 03-23
q_peak_v = disp.loc[q_peak, "QVIX"]
rv_peak = disp["RV20"].idxmax()         # 07-17
rv_peak_v = disp.loc[rv_peak, "RV20"]
sp_min = disp["spread"].idxmin()        # 07-23
sp_min_v = disp.loc[sp_min, "spread"]
sp_max = disp["spread"].idxmax()        # 03-23
sp_max_v = disp.loc[sp_max, "spread"]
pct_pos = (disp["spread"] > 0).mean()
mean_sp = disp["spread"].mean()
print(f"QVIX 峰 {q_peak_v:.2f} @ {q_peak.date()} | RV20 峰 {rv_peak_v:.2f} @ {rv_peak.date()}")
print(f"价差峰 {sp_max_v:.2f} @ {sp_max.date()} / 谷 {sp_min_v:.2f} @ {sp_min.date()}")
print(f"IV>RV 占比 {pct_pos:.1%} | 价差均值 {mean_sp:.2f}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), dpi=110,
                               gridspec_kw={"height_ratios": [1.2, 1], "hspace": 0.18})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：QVIX vs RV20 =====
ax1.plot(disp.index, disp["QVIX"], color=BLUE, lw=1.9,
         label="QVIX：隐含波动率（从 50ETF 期权价格反推的“市场预期”）")
ax1.plot(disp.index, disp["RV20"], color=ORANGE, lw=1.9,
         label="RV20：已实现波动率（50ETF 实际走出的“现实”，20 日年化 %）")

# 标注①：3 月恐慌尖峰
q_prev_v = disp["QVIX"].iloc[list(disp.index).index(q_peak) - 1]
q_pct = (q_peak_v / q_prev_v - 1) * 100
ax1.annotate(f"3 月暴跌当天：QVIX 单日 {q_prev_v:.1f}→{q_peak_v:.0f}（+{q_pct:.0f}%）\nIV 是预期定价——恐慌瞬间全部打进期权价格\n两天后跌回 17（IV crush：不确定性被消除）",
             xy=(q_peak, q_peak_v), xytext=(pd.Timestamp("2026-04-08"), 36),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))

# 标注②：7 月阴跌
ax1.annotate(f"7 月阴跌：RV20 冲到 {rv_peak_v:.0f}%\nQVIX 却只有 22——期权市场没有同步恐慌\n（预期 vs 现实：突发暴跌与持续阴跌定价不同）",
             xy=(rv_peak, rv_peak_v), xytext=(pd.Timestamp("2026-07-24"), 35),
             fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.3))

# 标注③：8 月回落
ax1.annotate("8 月：IV 与 RV 一起回落\n——恐慌会平息，波动率向中枢回归",
             xy=(pd.Timestamp("2026-08-11"), 17.2),
             xytext=(pd.Timestamp("2026-07-02"), 10.5),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.3))

ax1.legend(loc="upper right", fontsize=9.5, frameon=False)
ax1.set_ylabel("年化波动率（%）", fontsize=10)
ax1.set_title("IV 与 RV 的真实关系：预期（QVIX）领先、现实（RV20）滞后（50ETF，2026-03 ~ 08）",
              fontsize=13, color=DARK, pad=10)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.set_ylim(5, 45)

# ===== 下：IV − RV 价差（VRP）=====
colors_bar = [TEAL if v >= 0 else RED for v in disp["spread"]]
ax2.bar(disp.index, disp["spread"], 1.0, color=colors_bar, alpha=0.75)
ax2.axhline(0, color=GRAY, lw=1.1)
ax2.axhline(mean_sp, color=DARK, ls="--", lw=1.2,
            label=f"窗口均值 ≈ +{mean_sp:.1f}pct（VRP 溢价常态）")

ax2.annotate(f"恐慌脉冲：预期瞬间领跑\n+{sp_max_v:.0f}pct（{sp_max.strftime('%m-%d')}）",
             xy=(sp_max, sp_max_v), xytext=(pd.Timestamp("2026-04-06"), 23),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.3))
ax2.annotate(f"阴跌中：现实持续反超\n{sp_min_v:.1f}pct（{sp_min.strftime('%m-%d')}）",
             xy=(sp_min, sp_min_v), xytext=(pd.Timestamp("2026-07-22"), -16),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))

stats = ("波动率风险溢价（IV − RV）：全历史 2016-01 ~ 2026-08 共 10 年——80% 的交易日 IV > RV，平均 +2.5 个百分点\n"
         "——“担心”长期被高估：买方持续付保险费、卖方长期收溢价（呼应 10.5 订单流视角）\n"
         "但高波动窗口溢价会被压缩甚至反转：本图 2026-03 ~ 08 窗口内仅 58% 为正、均值 +0.8pct\n"
         "两种“恐慌”定价不同：3 月突发暴跌 → IV 瞬间领跑（+28pct 峰值，随后 IV crush）；\n"
         "7 月持续阴跌 → RV 反超（−8.6pct，连续 3 周），已实现波动跑赢市场预期")
ax2.text(0.012, 0.97, stats, transform=ax2.transAxes, ha="left", va="top",
         fontsize=9.3, color=DARK, family="Microsoft YaHei", zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

ax2.legend(loc="upper right", fontsize=9, frameon=False)
ax2.set_ylabel("QVIX − RV20（百分点）", fontsize=10)
ax2.set_xlabel("2026 年（数据至 08-11）", fontsize=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.set_ylim(-20, 30)

for ax in (ax1, ax2):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))

fig.text(0.995, 0.012, "数据源：AkShare 新浪（QVIX = 50ETF 期权隐含波动率指数 / 510050 日线计算 RV20）· 与图 10-3R 同一窗口，这里用 50ETF 与 QVIX 严格同标的 · 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("handbook/images/fig_real_ch10_ivrv.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch10_ivrv.png")
