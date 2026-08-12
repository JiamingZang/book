# -*- coding: utf-8 -*-
"""配对交易真实教学图：沪深300 vs 中证500 价差 z-score 偏离→回归（4.28 配图）"""
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

# 显示窗口：2026-06-01 起（rolling 用更早数据）
disp = df.loc["2026-06-01":"2026-08-12"]
# 归一化价格（窗口起点 = 100）
norm = disp[["hs300", "zz500"]] / disp[["hs300", "zz500"]].iloc[0] * 100

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), dpi=110,
                               gridspec_kw={"height_ratios": [1, 1], "hspace": 0.14})
for ax in (ax1, ax2):
    ax.set_facecolor("white")
fig.patch.set_facecolor("white")

# ===== 上子图：归一化价格 =====
ax1.plot(norm.index, norm["hs300"], color=BLUE, lw=1.8, label="沪深300（sh000300）")
ax1.plot(norm.index, norm["zz500"], color=ORANGE, lw=1.8, label="中证500（sz399905）")
ax1.axvline(pd.Timestamp("2026-07-01"), color=GRAY, ls=":", lw=1)
ax1.axvline(pd.Timestamp("2026-07-20"), color=GRAY, ls=":", lw=1)
ax1.axvline(pd.Timestamp("2026-08-12"), color=GRAY, ls=":", lw=1)
ax1.annotate("7-01 建仓：多 300 / 空 500\n（500 相对 300 涨过头，z=-2.35）",
             xy=(pd.Timestamp("2026-07-01"), norm["zz500"].loc["2026-07-01"]),
             xytext=(pd.Timestamp("2026-06-03"), 99.0),
             fontsize=9, color="#263238", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax1.annotate("7-20 建仓：空 300 / 多 500\n（300 相对 500 走强过度，z=+3.42）",
             xy=(pd.Timestamp("2026-07-20"), norm["hs300"].loc["2026-07-20"]),
             xytext=(pd.Timestamp("2026-07-22"), 91.5),
             fontsize=9, color="#263238", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
ax1.set_ylabel("归一化价格（6-01 = 100）", fontsize=10)
ax1.set_ylim(86, 112)
ax1.legend(loc="upper left", fontsize=9, frameon=False)
ax1.set_title("配对交易真实案例：价差偏离 → 回归（沪深300 vs 中证500，2026-06-01 ~ 08-12）",
              fontsize=13, color="#263238", pad=10)
ax1.grid(axis="y", color="#eceff1", lw=0.7)

# ===== 下子图：z-score =====
ax2.plot(disp.index, disp["z"], color=BLUE, lw=1.8, label="z-score（60 日滚动）")
ax2.axhline(0, color="#546e7a", lw=1.2)
ax2.axhline(1, color=GRAY, ls="--", lw=1); ax2.axhline(-1, color=GRAY, ls="--", lw=1)
ax2.axhline(2, color="#ef5350", ls="--", lw=1.2); ax2.axhline(-2, color="#26a69a", ls="--", lw=1.2)
ax2.fill_between(disp.index, 2, disp["z"].clip(lower=2), color="#ef5350", alpha=0.12)
ax2.fill_between(disp.index, -2, disp["z"].clip(upper=-2), color="#26a69a", alpha=0.12)

# 信号 1：建仓/平仓
ax2.plot([pd.Timestamp("2026-07-01")], [-2.35], marker="o", color="#26a69a", ms=9, zorder=6)
ax2.annotate("建仓① 7-01 z=-2.35：多 300 空 500\n→ 7-14 z 回 0 附近平仓，净约 +5%（等名义）",
             xy=(pd.Timestamp("2026-07-01"), -2.35),
             xytext=(pd.Timestamp("2026-06-03"), -4.3),
             fontsize=9, color="#00695c", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#26a69a", lw=1.2))
# 教训框：不止盈会怎样
ax2.annotate("若 7-01 建仓后不止盈：7-20 z 反向冲到 +3.42（±2σ 之外 5.8 倍）——\n“回归”是统计不是承诺，目标定死 + 止损机械才是纪律",
             xy=(pd.Timestamp("2026-07-20"), 3.42),
             xytext=(pd.Timestamp("2026-07-23"), 4.6),
             fontsize=9, color="#c62828", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor="#ef5350", lw=1),
             arrowprops=dict(arrowstyle="->", color="#ef5350", lw=1.2))
# 信号 2：建仓/平仓
ax2.plot([pd.Timestamp("2026-07-20")], [3.42], marker="o", color="#ef5350", ms=9, zorder=6)
ax2.annotate("建仓② 7-20 z=+3.42：空 300 多 500\n→ 8-12 z=0.03 平仓，净约 +6.5%（等名义）",
             xy=(pd.Timestamp("2026-08-12"), 0.03),
             xytext=(pd.Timestamp("2026-08-04"), -3.8),
             fontsize=9, color="#b71c1c", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#ef5350", lw=1.2))
ax2.legend(loc="upper right", fontsize=9, frameon=False)
ax2.set_ylabel("z-score", fontsize=10)
ax2.set_ylim(-5.2, 5.0)
ax2.set_xlabel("", fontsize=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.text(0.995, -0.22, "数据源：AkShare 新浪财经指数日线 · 等名义金额、未计交易成本 · 教学示意，不构成投资建议",
         transform=ax2.transAxes, ha="right", fontsize=8, color=GRAY)

for ax in (ax1, ax2):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

fig.subplots_adjust(hspace=0.16)
fig.savefig("handbook/images/fig_real_pair.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_pair.png")
