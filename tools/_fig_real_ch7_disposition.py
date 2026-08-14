# -*- coding: utf-8 -*-
"""图 7-1R 真实数据：规则系统的持仓时长——赢单拿得住、输单跑得快（处置效应的镜像）
（EMA20/50 趋势跟踪回测，BTC 1H，2026-07-02 ~ 08-10，82 笔，总 R -7.83，验证不合格——同图 8-1R 数据）
- 上左：赢单 vs 亏单持仓时长箱线+散点——赢单平均 8.4h ≈ 亏单 4.3h 的 2 倍，差距在赢单长尾（103h/38h/23h）
- 上右：处置效应镜像示意——人类（赚 1R 就跑/亏 3R 死扛）vs 规则系统（让利润奔跑/认错快）
- 下左：持仓时长 vs R 散点（对数刻度）——+2.85R 大单持仓 103h（拿住 4 天才有）、平均亏单 4.3h 认错
- 下右：统计框——82 笔（赢 33/亏 49）、平均赢 +0.41R/平均亏 −0.44R、前 3 大赢单 = 45%（80/20 呼应 7.1）
"""
import csv
import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

WIN = "#2e7d32"
LOSS = "#ef5350"
BLUE = "#1565c0"
ORANGE = "#ef6c00"
GRAY = "#90a4ae"
DARK = "#263238"
LIGHT = "#f5f7fa"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ---- 读取真实回测交易 ----
trades = []
with open("data/_bt_ema_trades.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        R = float(row["R"])
        t_in = datetime.datetime.strptime(row["t_in"], "%Y-%m-%d %H:%M:%S")
        t_out = datetime.datetime.strptime(row["t_out"], "%Y-%m-%d %H:%M:%S")
        h = (t_out - t_in).total_seconds() / 3600
        trades.append((R, h))
R = np.array([t[0] for t in trades])
H = np.array([t[1] for t in trades])
N = len(R)
wins = R > 0
losses = ~wins
win_R = R[wins].sum()
loss_R = R[losses].sum()
n_w, n_l = int(wins.sum()), int(losses.sum())
avg_win_h = H[wins].mean()
avg_loss_h = H[losses].mean()
avg_win_R = R[wins].mean()
avg_loss_R = R[losses].mean()
top3 = np.sort(R[wins])[::-1][:3]
pct_top1 = 100 * top3[0] / win_R
pct_top3 = 100 * top3.sum() / win_R
max_win_h = H[np.argmax(R)]
quick = (H < 5).sum()

fig, axs = plt.subplots(2, 2, figsize=(13, 8.6), dpi=110,
                        gridspec_kw={"width_ratios": [1.05, 0.95], "height_ratios": [1, 1]})
fig.patch.set_facecolor("white")
for ax in axs.flat:
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上左：赢 vs 亏持仓时长（箱线 + 散点）=====
ax1 = axs[0, 0]
rng = np.random.default_rng(7)
jw = rng.uniform(-0.18, 0.18, n_w)
jl = rng.uniform(-0.18, 0.18, n_l)
ax1.scatter(0 + jw, H[wins], s=22, color=WIN, alpha=0.75, edgecolor="white", lw=0.5, zorder=3, label=f"赢单 {n_w} 笔")
ax1.scatter(1 + jl, H[losses], s=22, color=LOSS, alpha=0.75, edgecolor="white", lw=0.5, zorder=3, label=f"亏单 {n_l} 笔")

bp = ax1.boxplot([H[wins], H[losses]], positions=[0, 1], widths=0.42, patch_artist=True, zorder=2,
                 medianprops=dict(color=DARK, lw=1.6),
                 boxprops=dict(facecolor="none", edgecolor=GRAY, lw=1.2),
                 whiskerprops=dict(color=GRAY, lw=1.2), capprops=dict(color=GRAY, lw=1.2),
                 flierprops=dict(marker="."))
ax1.set_yscale("log")
ax1.set_xticks([0, 1])
ax1.set_xticklabels(["赢单", "亏单"], fontsize=11)
ax1.set_ylabel("持仓时长（小时，对数刻度）", fontsize=10)
ax1.set_ylim(0.4, 300)
ax1.set_yticks([1, 2, 5, 10, 24, 50, 100])
ax1.set_yticklabels(["1h", "2h", "5h", "10h", "24h", "50h", "100h"])
ax1.axhline(24, color=GRAY, lw=1, ls=":", alpha=0.8)
ax1.text(1.06, 26, "一天 24h", fontsize=8.5, color=GRAY, va="bottom")
ax1.annotate(f"赢单平均 {avg_win_h:.1f}h\n≈ 亏单 {avg_loss_h:.1f}h 的 2 倍\n（长尾 103h/38h/23h 拉起来的）",
             xy=(0, avg_win_h), xytext=(0.36, 95),
             fontsize=9.5, color=WIN, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=WIN, lw=1.2))
ax1.annotate(f"亏单平均 {avg_loss_h:.1f}h\n认错快——4.3h 就砍",
             xy=(1, avg_loss_h), xytext=(1.28, 11),
             fontsize=9.5, color=LOSS, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=LOSS, lw=1.2))
ax1.text(0.02, 0.98, "大多数交易都是快进快出（中位数都是 2h），\n差距在赢单的尾部——那几笔大的拿得住",
         transform=ax1.transAxes, fontsize=9, color=DARK, va="top",
         bbox=dict(boxstyle="round,pad=0.45", facecolor=LIGHT, edgecolor=GRAY, lw=0.8))
ax1.set_title("持仓时长：赢单 vs 亏单（真实 82 笔）", fontsize=12, color=DARK, pad=10)
ax1.legend(loc="lower left", fontsize=9, frameon=False)

# ===== 上右：处置效应镜像示意 =====
ax2 = axs[0, 1]
ax2.axis("off")
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.text(0.5, 0.985, "处置效应 vs 规则系统：持仓时长的镜像",
         ha="center", fontsize=12, color=DARK, fontweight="bold")
rows = [
    ("", "盈利单持仓", "亏损单持仓", "后果"),
    ("人类（处置效应）", "≈2h 就跑（落袋为安）", "≈72h 死扛（不认错）", "平均盈利 < 平均亏损\n盈亏比倒挂"),
    ("规则系统（真实 82 笔）", f"{avg_win_h:.1f}h（让利润奔跑）", f"{avg_loss_h:.1f}h（认错快）", "盈利单拿得住\n亏损单砍得快"),
]
tbl = ax2.table(cellText=[r[1:] for r in rows[1:]],
                colLabels=rows[0][1:],
                cellLoc="center", loc="center",
                colWidths=[0.20, 0.24, 0.24, 0.32])
tbl.auto_set_font_size(False)
tbl.set_fontsize(9.5)
tbl.scale(1, 1.75)
for (rr, cc), cell in tbl.get_celld().items():
    cell.set_edgecolor(GRAY)
    cell.set_linewidth(0.8)
    if rr == 0:
        cell.set_facecolor("#e3eaf3")
        cell.set_text_props(color=DARK, fontweight="bold")
    elif rr == 1:
        cell.set_facecolor("#fdecea")
    else:
        cell.set_facecolor("#e8f5e9")
ax2.text(0.5, 0.19, "人类行为为示意（不是真实数据）——但规则系统的数字是真的：\n同样的 82 笔交易，赢单多拿 2 倍时间、亏单 4.3h 认错",
         ha="center", fontsize=9, color=GRAY,
         bbox=dict(boxstyle="round,pad=0.5", facecolor=LIGHT, edgecolor=GRAY, lw=0.8))
ax2.set_title("出场机制的镜像", fontsize=12, color=DARK, pad=10)

# ===== 下左：持仓时长 vs R 散点 =====
ax3 = axs[1, 0]
ax3.scatter(H[wins], R[wins], s=30, color=WIN, alpha=0.8, edgecolor="white", lw=0.5, zorder=3, label="赢单")
ax3.scatter(H[losses], R[losses], s=30, color=LOSS, alpha=0.8, edgecolor="white", lw=0.5, zorder=3, label="亏单")
ax3.axhline(0, color=GRAY, lw=1.1, ls="--")
ax3.axvline(24, color=GRAY, lw=1, ls=":", alpha=0.8)
ax3.text(25, -1.05, "持仓超过一天", fontsize=8.5, color=GRAY)
ax3.set_xscale("log")
ax3.set_xticks([1, 2, 5, 10, 24, 50, 100])
ax3.set_xticklabels(["1h", "2h", "5h", "10h", "24h", "50h", "100h"])
ax3.set_xlabel("持仓时长（小时，对数刻度）", fontsize=10)
ax3.set_ylabel("单笔 R", fontsize=10)
ax3.set_ylim(-1.15, 3.15)
ax3.annotate(f"+2.85R 最大赢单\n持仓 {max_win_h:.0f}h = 4 天\n（拿住才有的利润）",
             xy=(max_win_h, 2.85), xytext=(28, 2.25),
             fontsize=9.5, color=WIN, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=WIN, lw=1.2))
ax3.annotate(f"平均亏损单 −{abs(avg_loss_R):.2f}R\n持仓 {avg_loss_h:.1f}h——认错快\n（止损挂在入场时）",
             xy=(avg_loss_h, avg_loss_R), xytext=(0.55, -0.72),
             fontsize=9.5, color=LOSS, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=LOSS, lw=1.2))
ax3.text(0.02, 0.97, "左上方绿点 = 拿住的大赢单\n左下方红点 = 快速砍掉的亏损单",
         transform=ax3.transAxes, fontsize=9, color=DARK, va="top",
         bbox=dict(boxstyle="round,pad=0.45", facecolor=LIGHT, edgecolor=GRAY, lw=0.8))
ax3.set_title("持仓时长 × 单笔 R：拿得住才赚得到", fontsize=12, color=DARK, pad=10)
ax3.legend(loc="lower right", fontsize=9, frameon=False)

# ===== 下右：统计框 =====
ax4 = axs[1, 1]
ax4.axis("off")
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
stats = (f"同一笔交易序列：EMA20>50 只做多，2×ATR 跟踪止损（图 8-1R 的原始数据）\n"
         f"82 笔 · 赢 {n_w} / 亏 {n_l} · 胜率 {100*n_w/N:.0f}% · 总 R −7.83（系统本身验证不合格）\n\n"
         f"持仓时长：赢单平均 {avg_win_h:.1f}h vs 亏单平均 {avg_loss_h:.1f}h（≈2 倍）\n"
         f"中位数都是 2h——{quick} 笔（{100*quick/N:.0f}%）在 5h 内快进快出\n\n"
         f"盈亏：平均赢 +{avg_win_R:.2f}R vs 平均亏 −{abs(avg_loss_R):.2f}R（盈亏比 0.94）\n"
         f"最大赢单 +{top3[0]:.2f}R 持仓 {max_win_h:.0f}h = 赢单总利润的 {pct_top1:.0f}%\n"
         f"前 3 大赢单 = {pct_top3:.0f}%（80/20：利润是少数长持仓给的）\n\n"
         f"结论：机械出场 = 让利润奔跑 + 让亏损快走\n"
         f"人类处置效应正好相反（赚 1R 就跑、亏 3R 死扛）→ 盈亏比倒挂")
ax4.text(0.015, 0.96, stats, transform=ax4.transAxes, ha="left", va="top",
         fontsize=9.6, color=DARK, family="Microsoft YaHei", zorder=6,
         bbox=dict(boxstyle="round,pad=0.6", facecolor=LIGHT, edgecolor=GRAY, lw=0.9))
ax4.set_title("统计", fontsize=12, color=DARK, pad=10)

fig.suptitle("规则系统的持仓时长：赢单拿得住、输单跑得快——处置效应的真实镜像（EMA20/50，BTC 1H，2026-07-02 ~ 08-10）",
             fontsize=12.5, color=DARK, y=0.985)
fig.text(0.995, 0.008, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.02, 1, 0.965])
fig.savefig("handbook/images/fig_real_ch7_disposition.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch7_disposition.png")
