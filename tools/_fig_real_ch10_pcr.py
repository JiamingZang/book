# -*- coding: utf-8 -*-
"""图 10-7R 真实数据：期权的两个情绪温度计——PCR（谁在交易）vs QVIX（定价多恐慌）
（10.6 用途四跨式/10.8 陷阱：事件前后期权市场真实行为的完整剧本）
- 数据：PCR = 50ETF 期权每日认沽成交量/认购成交量（ak.option_daily_stats_sse，上交所）
        QVIX = 50ETF 期权隐含波动率指数（ak.index_option_50etf_qvix，新浪）
        510050 收盘价（ak.fund_etf_hist_sina，新浪），2026-01-05 ~ 08-14（149 个交易日）
- 上：510050 收盘价 + QVIX（右轴）——市场背景：03-23 恐慌日 510050 -3.01% 收 2.868（年内低点）
      同日 QVIX 42.2 尖峰（全年最高）——恐慌瞬间打进期权价格
- 中：PCR 认沽/认购比柱状 + 100 线——认沽比认购活跃即防御/看跌交易占上风
      标注① 03-03 PCR 121.4（全年最高：认沽最活跃），但 QVIX 只有 18.3——PCR 高 ≠ 波动预期高
      标注② 03-23 恐慌日 PCR 84.3（中位偏上）——恐慌日买卖双方都放量，PCR 反而不是最高
      -> PCR 回答"谁在买保险"，QVIX 回答"保险多贵"，两个温度计各说各话
- 下：期权总成交量柱状——03-23 恐慌日 218 万手（全年第二大），6 月也有 233 万手峰值
      8 月平静期萎缩到 63 万手（恐慌日的 1/3）——没人讨论的时候期权最便宜
三件事（10.6/10.8 应用）：
- ① 恐慌日期权市场自己最忙：价格大跌 + QVIX 尖峰 + 期权成交放量同步发生（呼应 10.5"恐慌打进期权价格"）
- ② PCR 与 QVIX 是不同温度计：03-03 PCR 最高而 QVIX 低位、03-23 QVIX 尖峰而 PCR 中位——认沽活跃≠波动预期高；
   判断"期权贵不贵"看 QVIX/IV Rank（10-6R），判断"情绪偏防御还是偏激进"看 PCR（呼应 10.8 别混用指标）
- ③ 平静期双低 = 买方相对友好的窗口：8 月 QVIX 16.6 低位 + 成交 63 万手 + PCR 70 附近——
   "没人讨论的时候期权最便宜"，低 IV 低成交时买方期权性价比最高（呼应 10.5 低 IV 买 / 10-6R 低 IV Rank / 10.6 用途四跨式时机）
"""
import sys
import time
import datetime as dt
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager

sys.stdout.reconfigure(encoding="utf-8")

# 字体 fallback：Windows 用雅黑，Linux 用文泉驿
_zh = None
for cand in ["Microsoft YaHei", "WenQuanYi Zen Hei"]:
    if any(f.name == cand for f in font_manager.fontManager.ttflist):
        _zh = cand
        break
plt.rcParams["font.family"] = _zh or "sans-serif"
plt.rcParams["axes.unicode_minus"] = False

BLUE, ORANGE, GRAY = "#1565c0", "#ef6c00", "#90a4ae"
TEAL, RED, DARK = "#26a69a", "#ef5350", "#263238"
GREEN = "#2e7d32"

# ---- 数据：上交所每日统计（PCR + 成交量）----
stats = []
d = dt.date(2026, 1, 2)
end = dt.date(2026, 8, 14)
while d <= end:
    if d.weekday() < 5:
        ds = d.strftime("%Y%m%d")
        try:
            x = ak.option_daily_stats_sse(date=ds)
            row = x[x["合约标的名称"].astype(str).str.contains("50ETF")]
            if len(row):
                r = row.iloc[0]
                stats.append((ds, float(r["认沽/认购"]), float(r["总成交量"])))
        except Exception:
            pass
    d += dt.timedelta(days=1)
    time.sleep(0.1)

df = pd.DataFrame(stats, columns=["date", "PCR", "vol"])
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date").sort_index()
print(f"期权每日统计 {len(df)} 个交易日 | PCR 均值 {df['PCR'].mean():.1f} | 区间 {df['PCR'].min():.1f} ~ {df['PCR'].max():.1f}")

# ---- 数据：QVIX + 510050 ----
q = ak.index_option_50etf_qvix()
q["date"] = pd.to_datetime(q["date"])
q = q.set_index("date").sort_index()

etf = ak.fund_etf_hist_sina(symbol="sh510050")
etf["date"] = pd.to_datetime(etf["date"])
etf = etf.set_index("date").sort_index()

df = df.join(q["close"].rename("QVIX"), how="left").join(etf["close"].rename("PX"), how="left")
df = df.loc["2026-01-01":"2026-08-14"].dropna(subset=["PCR"])
print(f"合并后 {len(df)} 天")

# 关键值
pcr_max = df["PCR"].idxmax()
pcr_max_v = df.loc[pcr_max, "PCR"]
q_peak = df["QVIX"].idxmax()
q_peak_v = df.loc[q_peak, "QVIX"]
q_peak_pcr = df.loc[q_peak, "PCR"]
vol_max = df["vol"].idxmax()
vol_max_v = df.loc[vol_max, "vol"]
pcr_min = df["PCR"].idxmin()
pcr_min_v = df.loc[pcr_min, "PCR"]
last_q = df["QVIX"].dropna().iloc[-1]
last_vol = df["vol"].iloc[-1]
print(f"PCR 峰 {pcr_max_v:.1f} @ {pcr_max.date()} (QVIX {df.loc[pcr_max,'QVIX']:.1f})")
print(f"QVIX 峰 {q_peak_v:.1f} @ {q_peak.date()} (PCR {q_peak_pcr:.1f})")
print(f"成交量峰 {vol_max_v/1e4:.0f} 万 @ {vol_max.date()} | PCR 谷 {pcr_min_v:.1f} @ {pcr_min.date()}")
print(f"期末 QVIX {last_q:.1f} | 期末成交 {last_vol/1e4:.0f} 万")

# ---- 绘图 ----
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15.6, 9.2), dpi=110,
                                     gridspec_kw={"height_ratios": [1.0, 0.85, 0.75], "hspace": 0.30,
                                                  "left": 0.055, "right": 0.965, "top": 0.94, "bottom": 0.06})

# 上：价格 + QVIX
ax1.plot(df.index, df["PX"], color=GRAY, lw=1.4, zorder=3, label="510050 收盘价（左轴）")
ax1b = ax1.twinx()
ax1b.plot(df.index, df["QVIX"], color=BLUE, lw=1.8, zorder=4, label="QVIX 隐含波动率（右轴）")
ax1b.set_ylim(0, 50)
ax1b.set_ylabel("QVIX（%）", fontsize=10, color=BLUE)
ax1b.tick_params(colors=BLUE, labelsize=8.5)
for s in ["top"]:
    ax1b.spines[s].set_visible(False)
ax1.set_ylabel("510050 收盘价", fontsize=10)
ax1.set_ylim(2.7, 3.3)

ax1.annotate(f"3 月恐慌：510050 -3.01% 收 2.868（年内低点）\nQVIX 同日 42.2 尖峰（全年最高，+112%）\n恐慌瞬间打进期权价格",
             xy=(q_peak, 2.868), xytext=(q_peak - dt.timedelta(days=38), 3.24),
             fontsize=9.5, color=RED, ha="left", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=RED, lw=1),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax1.scatter([q_peak], [2.868], color=RED, s=28, zorder=6)
ax1.text(dt.datetime(2026, 8, 5), 2.76, "8 月平静期：QVIX 16.6 低位 + 成交萎缩",
         fontsize=9, color=DARK, ha="left", zorder=6)

for ax in (ax1,):
    ax.tick_params(labelsize=8.5)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.legend(loc="upper left", fontsize=8.5, frameon=False)
ax1.set_title("图 10-7R 期权的两个情绪温度计：PCR（谁在交易）vs QVIX（定价多恐慌）——2026 年上半年 50ETF 期权真实全景（数据源：上交所每日统计 + 新浪 QVIX/510050）",
              fontsize=11.5, color=DARK, loc="left")

# 中：PCR
pos = df["PCR"] >= 100
ax2.bar(df.index, df["PCR"], width=0.8, color=[TEAL if p else GRAY for p in pos], alpha=0.75, zorder=3)
ax2.axhline(100, color=DARK, lw=1.4, ls="--", zorder=4)
ax2.text(df.index[0], 102.5, "PCR=100：认沽成交量=认购成交量（认沽占上风 = 防御/看跌交易更活跃）",
         fontsize=8.5, color=DARK, va="bottom", zorder=5)

ax2.annotate(f"PCR 全年最高 {pcr_max_v:.0f}（认沽最活跃，3 月初阴跌）\n但 QVIX 只有 {df.loc[pcr_max,'QVIX']:.0f}——认沽活跃 ≠ 波动预期高",
             xy=(pcr_max, pcr_max_v), xytext=(pcr_max - dt.timedelta(days=52), 112),
             fontsize=9, color=TEAL, ha="left", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#e0f2f1", edgecolor=TEAL, lw=1),
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))
ax2.annotate(f"恐慌日 PCR 只有 {q_peak_pcr:.0f}：\n买卖双方都放量，PCR 反而不是最高",
             xy=(q_peak, q_peak_pcr), xytext=(q_peak - dt.timedelta(days=6), 94),
             fontsize=9, color=RED, ha="right", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=RED, lw=1),
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

ax2.set_ylabel("PCR 认沽/认购（%）", fontsize=10)
ax2.set_ylim(40, 132)
ax2.tick_params(labelsize=8.5)
for s in ["top", "right"]:
    ax2.spines[s].set_visible(False)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.text(dt.datetime(2026, 8, 5), 47, "PCR 均值 76：平时认购比认沽活跃（买方偏乐观）",
         fontsize=8.5, color=GRAY, ha="left", zorder=6)

# 下：成交量
ax3.bar(df.index, df["vol"] / 1e4, width=0.8, color=BLUE, alpha=0.6, zorder=3)
ax3.annotate(f"恐慌日成交 {vol_max_v/1e4:.0f} 万手（全年最大之一）",
             xy=(vol_max, vol_max_v / 1e4), xytext=(vol_max - dt.timedelta(days=48), vol_max_v / 1e4 * 0.82),
             fontsize=9, color=BLUE, ha="left", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#e3f2fd", edgecolor=BLUE, lw=1),
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
ax3.annotate(f"8 月萎缩到 {last_vol/1e4:.0f} 万手（恐慌日的 1/3）\n没人讨论的时候，期权最便宜",
             xy=(df.index[-1], last_vol / 1e4), xytext=(df.index[-1] - dt.timedelta(days=22), 175),
             fontsize=9, color=DARK, ha="left", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#eceff1", edgecolor=GRAY, lw=1),
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))

ax3.set_ylabel("期权总成交量（万手）", fontsize=10)
ax3.set_ylim(0, 260)
ax3.tick_params(labelsize=8.5)
for s in ["top", "right"]:
    ax3.spines[s].set_visible(False)
ax3.grid(axis="y", color="#eceff1", lw=0.7)

for ax in (ax1, ax2, ax3):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.tick_params(axis="x", labelsize=8.5)

fig.text(0.995, 0.012, "数据源：上交所 50ETF 期权每日统计（option_daily_stats_sse）+ 新浪 QVIX / 510050 日线 · 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)

plt.savefig("handbook/images/fig_real_ch10_pcr.png", dpi=110, facecolor="white", bbox_inches="tight")
print("saved handbook/images/fig_real_ch10_pcr.png")
