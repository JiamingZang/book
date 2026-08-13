# -*- coding: utf-8 -*-
"""图 3-2 Pin Bar 专用教学图（替代与图 2-6 复用的 fig_p17_x123.png）
左：锤子线（长下影 + 小实体，支撑位反转）——影线 50% 入场 / 突破影线起点入场 / 止损最远端
右：吊颈线（长上影 + 小实体，阻力位反转）——看跌信号
风格与 draw_handbook_figs.py 一致（红涨绿跌、带引线标注、无坐标轴）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

UP, DOWN = "#26a69a", "#ef5350"
DARK, GRAY, ORANGE = "#263238", "#90a4ae", "#ff9800"
OUT = "handbook/images/fig_p3_pinbar.png"


def candle(ax, x, o, h, l, c, width=0.55):
    up = c >= o
    color = UP if up else DOWN
    ax.plot([x, x], [l, h], color=color, linewidth=1.1, zorder=2)
    ax.add_patch(Rectangle((x - width / 2, min(o, c)), width, abs(c - o),
                           facecolor=color, edgecolor=color, zorder=3))


def style_ax(ax, xlim, ylim):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_facecolor("white")


def hl(ax, x0, x1, y, color=ORANGE, ls="--", lw=1.2, label=None, dy=0.0):
    ax.plot([x0, x1], [y, y], color=color, ls=ls, lw=lw, zorder=2)
    if label:
        ax.text(x0, y + dy, label, fontsize=9.5, color=color, va="bottom", ha="left", zorder=5)


def ann(ax, x, y, text, xt, yt, color=DARK, fs=10.5, ha="left"):
    ax.annotate(text, xy=(x, y), xytext=(xt, yt),
                fontsize=fs, color=color, ha=ha, va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1,
                                connectionstyle="arc3,rad=0.12"),
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.8))


# ---------------- 左：锤子线（看涨） ----------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.3))
fig.patch.set_facecolor("white")
style_ax(ax1, xlim=(-1.5, 9.8), ylim=(86, 114))

# 背景：支撑位上方的回调段
for x, o, h, l, c in [(0, 99, 102, 96.5, 98), (1, 98, 101, 95, 97.5), (2, 97.5, 100, 95.2, 96.8)]:
    candle(ax1, x, o, h, l, c)
# 锤子线：长下影 + 小实体
candle(ax1, 3.6, 100, 104, 91, 102.2)
# 确认阳线
for x, o, h, l, c in [(5, 102.2, 106.5, 100.8, 105.8), (6.6, 105.8, 108, 104.5, 107)]:
    candle(ax1, x, o, h, l, c)

# 支撑线（前低/HL 区）
hl(ax1, -1.2, 3.6, 91, color=ORANGE, label="支撑位（前低，多次测试）", dy=-1.4)
# 影线 50% 入场线
hl(ax1, 2.9, 4.3, 95.5, color=UP, label="入场 1：影线 50% 挂限价", dy=0.6)
# 止损线
hl(ax1, 2.9, 4.3, 89.8, color=DOWN, label="止损：影线最远端外侧", dy=-1.6)

ann(ax1, 3.6, 91.5, "下影 ≥ 2× 实体（本例 ≈ 4.5 倍）\n空头砸破支撑被买盘拉回 = 看涨", 5.3, 93.5, color=UP)
ann(ax1, 5, 105.8, "入场 2：突破影线起点\n（更强确认，止损同上）", 6.9, 103.2, color=DARK)
ax1.text(0.02, 0.96, "锤子线（看涨）", transform=ax1.transAxes, fontsize=13,
         fontweight="bold", color=DARK, va="top", ha="left")

# ---------------- 右：吊颈线（看跌） ----------------
style_ax(ax2, xlim=(-1.5, 9.8), ylim=(86, 114))

# 背景：阻力位上方的冲高段
for x, o, h, l, c in [(0, 101, 105, 99.5, 103), (1, 103, 107.5, 101.5, 106), (2, 106, 109, 104.5, 107.5)]:
    candle(ax2, x, o, h, l, c)
# 吊颈线：长上影 + 小实体
candle(ax2, 3.6, 100, 110.5, 96, 98)
# 确认阴线
for x, o, h, l, c in [(5, 98, 100, 94.5, 95), (6.6, 95, 97, 92.5, 93.2)]:
    candle(ax2, x, o, h, l, c)

hl(ax2, -1.2, 3.6, 110.5, color=ORANGE, label="阻力位（前高，多次测试）", dy=1.2)
hl(ax2, 2.9, 4.3, 105.25, color=DOWN, label="入场 1：影线 50% 挂限价（做空）", dy=0.6)
hl(ax2, 2.9, 4.3, 111.8, color=UP, label="止损：影线最远端外侧", dy=1.2)

ann(ax2, 3.6, 110.2, "上影 ≥ 2× 实体\n多头冲高被空头压回 = 看跌", 5.3, 107.8, color=DOWN)
ann(ax2, 5, 95, "入场 2：跌破影线起点\n（更强确认，止损同上）", 6.9, 97.8, color=DARK)
ax2.text(0.02, 0.96, "吊颈线（看跌）", transform=ax2.transAxes, fontsize=13,
         fontweight="bold", color=DARK, va="top", ha="left")

fig.savefig(OUT, dpi=160, facecolor="white", bbox_inches="tight")
print("saved:", OUT)
