# -*- coding: utf-8 -*-
"""批次45c：fig_p3_framework.png（图 3-1）判定框架：背景 × 位置 × 形态 三道闸
信号质量 = 三因子相乘，缺一个就是零——任何一道不过就放弃
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from draw_handbook_figs import (style_ax, savefig, UP, DOWN, TEAL, DARK, GRAY, ORANGE)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


def box(ax, x, y, w, h, text, fc, ec, fs=10.5, tc=DARK, lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                facecolor=fc, edgecolor=ec, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, fontsize=fs, color=tc,
            ha="center", va="center", zorder=4)


def arrow(ax, x0, y0, x1, y1, color=DARK, lw=2.0, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw, ls=ls), zorder=2)


def fig_p3_framework():
    fig, ax = plt.subplots(figsize=(12.2, 6.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.6)

    # 顶部：信号出现
    box(ax, 4.6, 5.9, 2.8, 0.62, "看到一根信号 K（如锤子线）", "#e8f4f2", TEAL, fs=11)

    # 三道闸门（横向）
    gates = [
        (0.4, "闸 1：背景（大方向）\nHTF 方向一致吗？\n趋势还是区间？", "只做顺势信号", "#fff3e0", ORANGE),
        (4.2, "闸 2：位置（关键位）\n在支撑/阻力/结构点上吗？\n半空中的信号是噪音", "信号必须放在位置里读", "#e8f4f2", TEAL),
        (8.0, "闸 3：形态（信号 K）\n收盘/影线/实体合格吗？\n最后一道确认", "第 3.10 质量标准", "#fff3e0", ORANGE),
    ]
    for x, title, sub, fc, ec in gates:
        box(ax, x, 3.9, 3.4, 1.7, title, fc, ec, fs=10)
        ax.text(x + 1.7, 3.55, sub, fontsize=8.5, color=GRAY, ha="center", va="center", zorder=4)

    # 主流程箭头
    arrow(ax, 6.0, 5.9, 6.0, 5.65)
    arrow(ax, 6.0, 5.65, 6.0, 5.65)  # 起点已在闸上方
    arrow(ax, 2.1, 3.9, 2.1, 3.65)
    arrow(ax, 5.9, 3.9, 5.9, 3.65)
    arrow(ax, 9.7, 3.9, 9.7, 3.65)

    # 闸 1 -> 闸 2 -> 闸 3 横向箭头
    arrow(ax, 2.1, 4.75, 4.2, 4.75)
    arrow(ax, 5.9, 4.75, 8.0, 4.75)

    # 三个"否 → 放弃"分支
    for x in (2.1, 5.9, 9.7):
        ax.plot([x, x], [3.9, 2.9], color=DOWN, lw=1.8, ls="--", zorder=2)
        ax.text(x, 3.05, "否", fontsize=9.5, color=DOWN, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=DOWN, lw=0.8), zorder=5)
        ax.plot([x, x + 1.4], [2.9, 2.9], color=DOWN, lw=1.8, ls="--", zorder=2)
        ax.add_patch(Rectangle((x + 1.4, 2.55), 1.55, 0.7, facecolor="#ffebee",
                               edgecolor=DOWN, lw=1.4, zorder=3))
        ax.text(x + 2.18, 2.9, "放弃", fontsize=10, color=DOWN, ha="center", va="center", zorder=4)

    # 底部：通过 → 入场
    arrow(ax, 9.7, 3.65, 9.7, 2.3)
    box(ax, 7.7, 1.55, 4.0, 0.75, "三道闸全过 → 入场\n（按第 6 章仓位公式算好手数再执行）", "#e8f5e9", UP, fs=10.5, tc="#1b5e20")

    # 关键公式
    box(ax, 0.4, 1.55, 4.6, 0.75, "信号质量 = 背景 × 位置 × 形态\n三者相乘，缺一个就是零", "#e3f2fd", "#1e3a6b", fs=10.5)

    # 中间说明
    ax.text(6.0, 0.75, "三道闸把「感觉」替换成「清单」——这是对抗情绪的唯一工程化方法（第 7 章）",
            fontsize=10, color=DARK, ha="center", va="center", zorder=4)

    style_ax(ax)
    fig.suptitle("判定框架：背景 × 位置 × 形态——三道闸按顺序过，任何一道不过就放弃",
                 fontsize=12.5, color=DARK, y=0.97)
    savefig(fig, "fig_p3_framework.png")


if __name__ == "__main__":
    fig_p3_framework()
