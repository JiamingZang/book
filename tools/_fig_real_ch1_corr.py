# -*- coding: utf-8 -*-
"""图 1-3R 真实数据：BTC 与 ETH 的相关性不是常数
数据：Binance BTCUSDT/ETHUSDT 5m K 线（2026-06-29 ~ 08-13，12960 根）
上=5m 收益散点按波动分位着色（Q1 青 r=0.17 ~ Q4 红 r=0.90，拟合线斜率随波动变陡）
下左=各波动档相关性柱（0.17→0.51→0.78→0.90 单调攀升）
下右=每日 24h 滚动相关性曲线（0.63~0.93）+ 总体 0.86 虚线
核心实证：相关性是波动的函数——平静期近乎独立（0.17），剧烈期同步起舞（0.90），
"分散"是平静期的错觉，呼应 1.14 风险叠加陷阱。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False

# ---------- 数据 ----------
btc = pd.read_csv("data/btcusdt_5m.csv")
eth = pd.read_csv("data/ethusdt_5m.csv")
btc["time"] = pd.to_datetime(btc["time"])
eth["time"] = pd.to_datetime(eth["time"])
df = pd.merge(btc[["time", "close"]], eth[["time", "close"]], on="time", suffixes=("_btc", "_eth"))
df = df.sort_values("time").reset_index(drop=True)
df["r_btc"] = np.log(df["close_btc"]).diff()
df["r_eth"] = np.log(df["close_eth"]).diff()
df = df.dropna().reset_index(drop=True)

# 按 BTC 5m 绝对收益分 4 档
abs_r = df["r_btc"].abs()
q = pd.qcut(abs_r, 4, labels=[1, 2, 3, 4])
df["Q"] = q.astype(int)

# 每档统计
stats = []
for i in range(1, 5):
    sub = df[df["Q"] == i]
    stats.append({
        "Q": i,
        "corr": sub["r_btc"].corr(sub["r_eth"]),
        "avg_abs_bp": sub["r_btc"].abs().mean() * 10000,
    })
S = pd.DataFrame(stats)
CORR = {row.Q: row.corr for row in S.itertuples()}
BP = {row.Q: row.avg_abs_bp for row in S.itertuples()}

TOTAL_CORR = df["r_btc"].corr(df["r_eth"])

# 每日 24h 滚动相关性（288 根 5m）取每日末值
df["roll24"] = df["r_btc"].rolling(288).corr(df["r_eth"])
df["date"] = df["time"].dt.date
daily = df.groupby("date")["roll24"].last().dropna().reset_index()
daily["date"] = pd.to_datetime(daily["date"])

# ---------- 颜色 ----------
C1, C2, C3, C4 = "#26a69a", "#42a5f5", "#ffa726", "#e53935"
QCOLOR = {1: C1, 2: C2, 3: C3, 4: C4}
GRAY = "#9e9e9e"
TXT = "#333333"

# ---------- 画布 ----------
fig = plt.figure(figsize=(14.28, 9.2), dpi=100)
fig.patch.set_facecolor("white")

# ===== 上：散点图 =====
ax1 = fig.add_axes([0.075, 0.54, 0.87, 0.39])
# 抽样显示（保持分位比例）：全样本 12959 点太多，每档抽 ~1800 点
np.random.seed(42)
for i in range(1, 5):
    sub = df[df["Q"] == i]
    n = min(len(sub), 1800)
    idx = np.random.choice(sub.index, n, replace=False)
    sub = sub.loc[idx]
    ax1.scatter(sub["r_btc"] * 100, sub["r_eth"] * 100, s=7, alpha=0.45,
                color=QCOLOR[i], label=f"Q{i} 波动{BP[i]:.1f}bp/5m  r={CORR[i]:.2f}", linewidths=0)
    # 拟合线 y = a + b*x
    b, a = np.polyfit(sub["r_btc"], sub["r_eth"], 1)
    xs = np.linspace(sub["r_btc"].min(), sub["r_btc"].max(), 100)
    ax1.plot(xs * 100, (a + b * xs) * 100, color=QCOLOR[i], lw=1.8, alpha=0.9)

lim = 0.021 * 100  # ±2.1%
ax1.set_xlim(-lim, lim)
ax1.set_ylim(-lim, lim)
ax1.axhline(0, color=GRAY, lw=0.8, alpha=0.6)
ax1.axvline(0, color=GRAY, lw=0.8, alpha=0.6)
ax1.set_xlabel("BTC 5 分钟收益（%）", fontsize=12)
ax1.set_ylabel("ETH 5 分钟收益（%）", fontsize=12)
ax1.set_title("BTC 与 ETH 的 5 分钟收益：平静时散点≈圆（两笔独立交易），剧烈时聚成直线（同一笔交易）",
              fontsize=13, fontweight="bold", color=TXT, pad=10)
ax1.legend(loc="upper left", fontsize=9.5, framealpha=0.9, borderaxespad=0.6)
ax1.grid(True, lw=0.4, alpha=0.25)

# 标注 Q1 / Q4
ax1.annotate("平静 Q1：r=0.17\n散点≈圆 → 近乎两笔独立交易",
             xy=(-1.55, -1.35), xytext=(-1.75, 1.05),
             fontsize=10.5, color=C1, fontweight="bold",
             arrowprops=dict(arrowstyle="-", color=C1, lw=1.2))
ax1.annotate("剧烈 Q4：r=0.90\n散点≈直线 → 同一笔交易的镜像",
             xy=(1.35, 1.28), xytext=(0.55, 1.75),
             fontsize=10.5, color=C4, fontweight="bold",
             arrowprops=dict(arrowstyle="-", color=C4, lw=1.2))

# ===== 下左：分位相关性柱 =====
ax2 = fig.add_axes([0.075, 0.10, 0.42, 0.34])
labels = [f"Q1\n最平静\n{BP[1]:.1f}bp/5m", f"Q2\n{BP[2]:.1f}bp/5m", f"Q3\n{BP[3]:.1f}bp/5m", f"Q4\n最剧烈\n{BP[4]:.1f}bp/5m"]
colors = [C1, C2, C3, C4]
vals = [CORR[1], CORR[2], CORR[3], CORR[4]]
bars = ax2.bar(range(4), vals, color=colors, width=0.62, edgecolor="white", zorder=3)
for b, v in zip(bars, vals):
    ax2.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}", ha="center", va="bottom",
             fontsize=12, fontweight="bold", color=TXT)
ax2.set_xticks(range(4))
ax2.set_xticklabels(labels, fontsize=9.5)
ax2.set_ylim(0, 1.05)
ax2.set_ylabel("5m 收益相关性 r", fontsize=11)
ax2.set_title("相关性随波动单调攀升：0.17 → 0.51 → 0.78 → 0.90", fontsize=12, fontweight="bold", color=TXT, pad=8)
ax2.grid(axis="y", lw=0.4, alpha=0.25, zorder=0)
ax2.set_axisbelow(True)
ax2.spines[["top", "right"]].set_visible(False)

# ===== 下右：每日滚动相关性 =====
ax3 = fig.add_axes([0.565, 0.10, 0.38, 0.34])
ax3.plot(daily["date"], daily["roll24"], color="#1565c0", lw=1.8, zorder=3)
ax3.fill_between(daily["date"], daily["roll24"], 0, color="#1565c0", alpha=0.12, zorder=2)
ax3.axhline(TOTAL_CORR, color=GRAY, lw=1.2, ls="--", alpha=0.8)
ax3.text(daily["date"].iloc[2], TOTAL_CORR + 0.02, f"全样本 r={TOTAL_CORR:.2f}",
         fontsize=10, color=GRAY, fontweight="bold")
dmin = daily.loc[daily["roll24"].idxmin()]
dmax = daily.loc[daily["roll24"].idxmax()]
ax3.annotate(f"谷 {dmin['roll24']:.2f}\n({dmin['date']:%m-%d})",
             xy=(dmin["date"], dmin["roll24"]), xytext=(dmin["date"] - pd.Timedelta(days=1.2), dmin["roll24"] - 0.17),
             fontsize=9.5, color="#1565c0",
             arrowprops=dict(arrowstyle="-", color="#1565c0", lw=1))
ax3.annotate(f"峰 {dmax['roll24']:.2f}\n({dmax['date']:%m-%d})",
             xy=(dmax["date"], dmax["roll24"]), xytext=(dmax["date"] + pd.Timedelta(days=0.4), dmax["roll24"] + 0.09),
             fontsize=9.5, color="#1565c0",
             arrowprops=dict(arrowstyle="-", color="#1565c0", lw=1))
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
ax3.set_ylim(0, 1.15)
ax3.set_ylabel("24h 滚动相关性 r", fontsize=11)
ax3.set_title(f"每日 24h 滚动相关性（{daily['roll24'].min():.2f} ~ {daily['roll24'].max():.2f}，不是常数）",
              fontsize=12, fontweight="bold", color=TXT, pad=8)
ax3.grid(True, lw=0.4, alpha=0.25)
ax3.spines[["top", "right"]].set_visible(False)

out = "handbook/images/fig_real_ch1_corr.png"
fig.savefig(out, dpi=100, facecolor="white")
print("saved", out)

# ---------- 像素验证 ----------
from PIL import Image
im = np.array(Image.open(out).convert("RGB"))
h, w, _ = im.shape
total = h * w
for name, rgb in [("Q1青", C1), ("Q2蓝", C2), ("Q3橙", C3), ("Q4红", C4)]:
    r, g, b = int(rgb[1:3], 16), int(rgb[3:5], 16), int(rgb[5:7], 16)
    mask = (abs(im[:, :, 0].astype(int) - r) < 40) & (abs(im[:, :, 1].astype(int) - g) < 40) & (abs(im[:, :, 2].astype(int) - b) < 40)
    print(f"{name}: {mask.sum() / total * 100:.2f}%")
print("size:", im.shape[1], "x", im.shape[0])
