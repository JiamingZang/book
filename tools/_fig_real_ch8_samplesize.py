# -*- coding: utf-8 -*-
"""图 8-2R 真实数据：样本量幻觉——同一个 82 笔回测，前 20 笔"看起来赚"，82 笔才看清是亏的
（EMA20/50 趋势跟踪回测，BTC 1H，2026-07-02 ~ 08-10，同图 8-1R 的 82 笔）
- 上：累计 R 曲线——峰值 +3.72R 在第 5 笔、前 20 笔仍 +0.58R、约第 24 笔转负、终值 -7.83R
- 下：前 N 笔平均 R/笔 检查点柱——结论随样本量翻转（+0.74 → -0.095 R/笔）
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE = "#1565c0", "#ef6c00"
RED, TEAL, GRAY, DARK = "#ef5350", "#00897b", "#90a4ae", "#263238"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ---- 读取真实回测交易 ----
trades = []
with open("data/_bt_ema_trades.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        trades.append(float(row["R"]))
R = np.array(trades)
N = len(R)
cum = np.cumsum(R)

# 峰值与转负点
peak_i = int(np.argmax(cum))
zero_cross = int(np.argmax(cum < 0))  # 首次转负（若从未转负则返回 0）
if cum[zero_cross] >= 0:
    zero_cross = N  # 未转负

# 检查点
checkpoints = [5, 10, 20, 30, 40, 50, 60, 70, 82]
cpts = [(n, cum[n - 1] / n) for n in checkpoints]

x = np.arange(1, N + 1)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8.5), dpi=110,
                               gridspec_kw={"height_ratios": [1.25, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：累计 R 曲线 =====
# 前 20 笔高亮（"看起来赚"的窗口）
ax1.axvspan(0.5, 20.5, color=TEAL, alpha=0.10, zorder=1)
ax1.text(10.5, 3.0, "前 20 笔：+0.58R\n“看起来像正期望值”\n——最危险的窗口",
         fontsize=9.5, color=TEAL, ha="center", fontweight="bold", zorder=6)

ax1.plot(x, cum, drawstyle="steps-post", color=BLUE, lw=1.8, label="累计 R（逐笔）")
ax1.axhline(0, color=GRAY, lw=1, ls=":")

# 峰值标注
ax1.annotate(f"峰值 +{cum[peak_i]:.2f}R（第 {peak_i + 1} 笔）\n“这系统要发财”",
             xy=(peak_i + 1, cum[peak_i]), xytext=(12, 4.4),
             fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

# 转负标注
ax1.annotate(f"第 {zero_cross + 1} 笔起转负\n之后一路阴跌",
             xy=(zero_cross + 1, 0), xytext=(zero_cross + 18, -3.2),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 终点标注
ax1.annotate(f"82 笔终值 {cum[-1]:.2f}R\n平均 {-cum[-1] / N:.3f}R/笔——验证不合格",
             xy=(N, cum[-1]), xytext=(58, -5.8),
             fontsize=9.5, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

ax1.set_ylabel("累计 R（R 倍数）", fontsize=10)
ax1.set_title("样本量幻觉：同一个回测，前 20 笔“看起来赚”，82 笔才看清是亏的（真实回测：EMA20/50 趋势跟踪，BTC 1H，2026-07-02 ~ 08-10）",
              fontsize=12.5, color=DARK, pad=12)
ax1.legend(loc="upper right", fontsize=9.5, frameon=False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.set_xticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 82])
ax1.set_xlim(0.5, N + 1)

# ===== 下：前 N 笔平均 R 检查点 =====
xr = np.arange(len(cpts))
colors_bar = [TEAL if v >= 0 else RED for _, v in cpts]
bars = ax2.bar(xr, [v for _, v in cpts], 0.6, color=colors_bar, alpha=0.85)
ax2.axhline(0, color=GRAY, lw=1)

for i, (n, v) in enumerate(cpts):
    ax2.text(xr[i], v + (0.02 if v >= 0 else -0.05), f"{v:+.2f}",
             ha="center", fontsize=9, color=DARK if v >= 0 else RED, fontweight="bold")

# 结论区标注
ax2.text(4.3, -0.30, "前 20 笔结论：正期望值（错）",
         fontsize=9.5, color=TEAL, fontweight="bold", ha="center", zorder=6)
ax2.text(7.8, -0.30, "82 笔结论：−0.10R/笔（对）",
         fontsize=9.5, color=RED, fontweight="bold", ha="center", zorder=6)

ax2.set_xticks(xr)
ax2.set_xticklabels([f"前{n}笔" for n, _ in cpts], fontsize=9)
ax2.set_ylabel("累计 R ÷ 笔数（R/笔）", fontsize=10)
ax2.set_xlabel("回测样本量（只看前 N 笔时得到的平均期望值）", fontsize=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)

# 统计框（左下）
stats = ("同一批真实交易：EMA20>50 只做多，2×ATR 跟踪止损（图 8-1R 的 82 笔原始记录）\n"
         "前 5 笔 +0.74R/笔 → 前 20 笔 +0.03R/笔 → 前 40 笔 −0.08R/笔 → 82 笔 −0.10R/笔\n"
         "结论随样本量翻转：20 笔时“正期望”，82 笔时“负期望”\n"
         "峰值 +3.72R 出现在第 5 笔——如果只回测 5 笔，你会押上真钱\n"
         "这就是 8.7 要求“验证 100+ 笔”的原因：样本量就是信息量（呼应 7.3 近因偏差）")
ax2.text(0.012, 0.97, stats, transform=ax2.transAxes, ha="left", va="top",
         fontsize=9.3, color=DARK, family="Microsoft YaHei", zorder=6,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f7fa", edgecolor=GRAY, lw=0.8))

fig.text(0.995, 0.012, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("handbook/images/fig_real_ch8_samplesize.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch8_samplesize.png")
