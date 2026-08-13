# -*- coding: utf-8 -*-
"""波动率均值回归真实教学图：上证指数 20 日实现波动率（10.5 配图）"""
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BLUE, ORANGE, GRAY = "#1565c0", "#ef6c00", "#90a4ae"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

df = ak.stock_zh_index_daily(symbol="sh000001")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
ret = df["close"].pct_change()
rv = ret.rolling(20).std() * np.sqrt(252) * 100
df["rv20"] = rv

disp = df.loc["2026-03-01":"2026-08-12"]
center = disp["rv20"].mean()
print(f"窗口内 RV20 均值: {center:.1f}%")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8.5), dpi=110,
                               gridspec_kw={"height_ratios": [1, 1], "hspace": 0.16})
for ax in (ax1, ax2):
    ax.set_facecolor("white")
fig.patch.set_facecolor("white")

# ===== 上子图：价格 =====
ax1.plot(disp.index, disp["close"], color=BLUE, lw=1.8)
ax1.annotate("3 月下旬回调低点 3813",
             xy=(pd.Timestamp("2026-03-23"), 3813),
             xytext=(pd.Timestamp("2026-03-05"), 4020),
             fontsize=9, color="#263238", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax1.annotate("5 月中旬高点 4242（05-13）\n（随后横盘：波动率谷底）",
             xy=(pd.Timestamp("2026-05-13"), 4242.6),
             xytext=(pd.Timestamp("2026-05-15"), 4060),
             fontsize=9, color="#263238", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax1.annotate("7 月暴跌低点 3764（07-17）\n（-10% 级别回调）",
             xy=(pd.Timestamp("2026-07-17"), 3764.2),
             xytext=(pd.Timestamp("2026-06-25"), 4020),
             fontsize=9, color="#c62828", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#ef5350", lw=1.2))
ax1.set_ylabel("上证指数收盘", fontsize=10)
ax1.set_title("波动率均值回归：恐慌时飙升、平静时压缩（上证指数 sh000001，2026-03 ~ 08）",
              fontsize=13, color="#263238", pad=10)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# ===== 下子图：RV20 =====
ax2.plot(disp.index, disp["rv20"], color=ORANGE, lw=1.8,
         label="20 日实现波动率（年化 %）：已发生波动的量化")
ax2.axhline(center, color="#546e7a", ls="--", lw=1.2, label=f"窗口均值 ≈ {center:.0f}%（波动率中枢）")
ax2.fill_between(disp.index, disp["rv20"], center, color=ORANGE, alpha=0.10)

# 峰 1
ax2.plot([pd.Timestamp("2026-04-14")], [22.2], marker="o", color="#ef5350", ms=9, zorder=6)
ax2.annotate("峰① 04-14：22.2%\n3 月暴跌余波，波动率飙升",
             xy=(pd.Timestamp("2026-04-14"), 22.2),
             xytext=(pd.Timestamp("2026-04-16"), 26.5),
             fontsize=9, color="#c62828", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#ef5350", lw=1.2))
# 谷 1（窗口内真实谷底：05-12 的 7.5%）
ax2.plot([pd.Timestamp("2026-05-12")], [7.5], marker="o", color="#26a69a", ms=9, zorder=6)
ax2.annotate("谷① 05-12：7.5%\n横盘压缩——低 IV 买期权/卖波动率的背景",
             xy=(pd.Timestamp("2026-05-12"), 7.5),
             xytext=(pd.Timestamp("2026-05-18"), 8.2),
             fontsize=9, color="#00695c", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#26a69a", lw=1.2))
# 峰 2
ax2.plot([pd.Timestamp("2026-07-21")], [22.4], marker="o", color="#ef5350", ms=9, zorder=6)
ax2.annotate("峰② 07-21：22.4%\n7 月暴跌——波动率再次飙升\n（与图 4-4R 微通道次日反转同期）",
             xy=(pd.Timestamp("2026-07-21"), 22.4),
             xytext=(pd.Timestamp("2026-07-23"), 27.5),
             fontsize=9, color="#c62828", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#ef5350", lw=1.2))
# 回落
ax2.annotate("8 月回落：19.7%（08-10）\n——恐慌会平息，波动率向中枢回归",
             xy=(pd.Timestamp("2026-08-10"), 19.7),
             xytext=(pd.Timestamp("2026-07-30"), 13.0),
             fontsize=9, color="#00695c", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#26a69a", lw=1.2))

ax2.legend(loc="upper right", fontsize=8.5, frameon=False)
ax2.set_ylabel("RV20（年化 %）", fontsize=10)
ax2.set_ylim(5, 30)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.text(0.995, -0.25, "实现波动率 = 20 日收益率标准差年化；IV/VIX 是市场对未来的预期——价格玩趋势，波动率玩回归（10.5）· 数据源：AkShare 新浪财经 · 教学示意，不构成投资建议",
         transform=ax2.transAxes, ha="right", fontsize=8, color=GRAY)

for ax in (ax1, ax2):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

fig.subplots_adjust(hspace=0.16)
fig.savefig("handbook/images/fig_real_vol.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_vol.png")
