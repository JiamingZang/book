# -*- coding: utf-8 -*-
"""配对交易反例教学图：2026-01 z 深坑 -4.04——止损 vs 死扛（4.28 配图 2）"""
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


def get(code):
    df = ak.stock_zh_index_daily(symbol=code)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["close"]


a, b = get("sh000300"), get("sz399905")
df = pd.concat([a, b], axis=1, keys=["hs300", "zz500"]).dropna()
lr = np.log(df["hs300"] / df["zz500"])
win = 60
z = (lr - lr.rolling(win).mean()) / lr.rolling(win).std()
df["z"] = z

disp = df.loc["2025-12-22":"2026-03-31"]
norm = disp[["hs300", "zz500"]] / disp[["hs300", "zz500"]].iloc[0] * 100

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), dpi=110,
                               gridspec_kw={"height_ratios": [1, 1], "hspace": 0.16})
for ax in (ax1, ax2):
    ax.set_facecolor("white")
fig.patch.set_facecolor("white")

# ===== 上子图：归一化价格 =====
ax1.plot(norm.index, norm["hs300"], color=BLUE, lw=1.8, label="沪深300（sh000300）")
ax1.plot(norm.index, norm["zz500"], color=ORANGE, lw=1.8, label="中证500（sz399905）")
ax1.axvline(pd.Timestamp("2026-01-05"), color=GRAY, ls=":", lw=1)
ax1.axvline(pd.Timestamp("2026-01-12"), color=GRAY, ls=":", lw=1)
ax1.annotate("建仓 01-05：z=-2.84 触发信号（多 300 / 空 500）",
             xy=(pd.Timestamp("2026-01-05"), norm["zz500"].loc["2026-01-05"]),
             xytext=(pd.Timestamp("2025-12-24"), 103.5),
             fontsize=9, color="#263238", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax1.annotate("建仓后价差不收敛反而走远：\n500 一路走强（+18%），300 原地踏步",
             xy=(pd.Timestamp("2026-01-23"), norm["zz500"].loc["2026-01-23"]),
             xytext=(pd.Timestamp("2026-01-28"), 110.5),
             fontsize=9, color="#c62828", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#ef5350", lw=1.2))
ax1.set_ylabel("归一化价格（12-22 = 100）", fontsize=10)
ax1.set_ylim(92, 122)
ax1.legend(loc="upper left", fontsize=9, frameon=False)
ax1.set_title("配对交易反例：信号没错，但价差继续走远——止损 vs 死扛（2025-12-22 ~ 2026-03-31）",
              fontsize=13, color="#263238", pad=10)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# ===== 下子图：z-score =====
ax2.plot(disp.index, disp["z"], color=BLUE, lw=1.8, label="z-score（60 日滚动）")
ax2.axhline(0, color="#546e7a", lw=1.2)
ax2.axhline(-1, color=GRAY, ls="--", lw=1); ax2.axhline(1, color=GRAY, ls="--", lw=1)
ax2.axhline(-2, color="#26a69a", ls="--", lw=1.2); ax2.axhline(2, color="#ef5350", ls="--", lw=1.2)
ax2.fill_between(disp.index, -2, disp["z"].clip(upper=-2), color="#26a69a", alpha=0.12)

# 建仓点
ax2.plot([pd.Timestamp("2026-01-05")], [-2.84], marker="o", color="#1565c0", ms=9, zorder=6)
ax2.annotate("建仓 01-05：z=-2.84\n（规则内，信号本身没错）",
             xy=(pd.Timestamp("2026-01-05"), -2.84),
             xytext=(pd.Timestamp("2025-12-24"), -4.4),
             fontsize=9, color="#1565c0", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#1565c0", lw=1.2))
# 止损点
ax2.plot([pd.Timestamp("2026-01-08")], [-3.71], marker="o", color="#26a69a", ms=9, zorder=6)
ax2.annotate("止损 01-08：z=-3.71，继续走远\n→ 认错离场，亏损约 -2.8%\n（止损的价值：小亏离场）",
             xy=(pd.Timestamp("2026-01-08"), -3.71),
             xytext=(pd.Timestamp("2026-01-13"), -0.9),
             fontsize=9, color="#00695c", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#26a69a", lw=1.2))
# 深坑
ax2.plot([pd.Timestamp("2026-01-12")], [-4.04], marker="o", color="#ef5350", ms=9, zorder=6)
ax2.annotate("01-12 深坑：z=-4.04\n死扛者浮亏 -6.3%，06-30 扩大到 -12.5%",
             xy=(pd.Timestamp("2026-01-12"), -4.04),
             xytext=(pd.Timestamp("2026-02-10"), -3.9),
             fontsize=9, color="#c62828", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#ef5350", lw=1.2))
# 陷阱框
ax2.annotate("陷阱：01-16 后 z 名义回升，但价差（价格层面）仍在走远——\n60 日滚动窗口的均值/标准差在“自我修复”，z 回升 ≠ 价差回归。\n死扛者用 z 回升安慰自己，代价是 7 个月浮亏（08-12 仍 -5.7%）",
             xy=(pd.Timestamp("2026-02-06"), -1.2),
             xytext=(pd.Timestamp("2026-02-06"), -1.2),
             fontsize=9, color="#b71c1c", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor="#ef5350", lw=1))
ax2.legend(loc="lower right", fontsize=9, frameon=False)
ax2.set_ylabel("z-score", fontsize=10)
ax2.set_ylim(-5.0, 1.6)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.text(0.995, -0.25, "数据源：AkShare 新浪财经指数日线 · 等名义金额、未计交易成本 · 教学示意，不构成投资建议",
         transform=ax2.transAxes, ha="right", fontsize=8, color=GRAY)

for ax in (ax1, ax2):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

fig.subplots_adjust(hspace=0.16)
fig.savefig("handbook/images/fig_real_pair_stop.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_pair_stop.png")
