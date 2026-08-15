# -*- coding: utf-8 -*-
"""
批次 69b：第 6 章 1 张新图（补缺图节）
- fig_p6_error_budget.png  图 6-1  6.1 考核规则决定仓位：犯错预算——日回撤5%×0.5%→10次 vs ×2%→2-3次；总回撤10%×0.5%→20次

运行：python tools/_batch69b_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)

plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "Microsoft YaHei", "SimHei", "Arial Unicode MS"]


def fig_error_budget():
    fig, ax = plt.subplots(figsize=(13.0, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.75, "考核规则决定仓位：'能亏几次'才是真约束", fontsize=13,
            color=DARK, ha="center", weight="bold")

    def budget_row(x, y, label, n, per, color, hit_label, gap=0.52):
        """画一行犯错预算方块"""
        ax.text(x, y + 0.42, label, fontsize=10.3, color=DARK, va="center", weight="bold")
        for i in range(n):
            bx = x + 2.1 + i * gap
            fc = color
            ec = color
            if i == n - 1 and hit_label == "爆":
                fc = "#ffcdd2"
            ax.add_patch(Rectangle((bx, y), min(0.42, gap - 0.1), 0.55, facecolor=fc, edgecolor=ec,
                                   lw=0.8, zorder=3))
            if i == n - 1:
                ax.text(bx + 0.21, y + 0.78, hit_label, fontsize=9.0, color=DOWN,
                        ha="center", weight="bold", va="bottom")

    # 行 1：日回撤 5% + 0.5% = 10 次
    budget_row(0.6, 5.3, "日回撤 5% × 单笔 0.5%\n= 10 次犯错预算", 10, 0.5, UP, "碰线")
    ax.text(9.1, 5.55, "一天最多错 10 次才碰线——\n'能亏几次'是 10，压力可控", fontsize=9.2,
            color=UP, va="center")

    # 行 2：日回撤 5% + 2% = 2-3 次
    budget_row(0.6, 3.7, "日回撤 5% × 单笔 2%\n= 2-3 次就爆", 3, 2.0, DOWN, "爆")
    ax.text(9.1, 3.95, "错 2-3 次直接碰线出局——\n你甚至等不到下午的行情", fontsize=9.2,
            color=DOWN, va="center")

    # 行 3：总回撤 10% + 0.5% = 20 次
    budget_row(0.6, 2.1, "总回撤 10% × 单笔 0.5%\n= 20 次犯错预算", 20, 0.5, TEAL, "出局", gap=0.36)
    ax.text(10.5, 2.35, "连续错 20 次才出局——\n活到趋势来的概率大增", fontsize=9.2,
            color=TEAL, va="center")

    draw_box(ax, 0.6, 0.2, 12.2, 1.15, "", ec=DOWN)
    ax.text(6.7, 0.95, "大多数考核失败，不是不会赚钱，而是某一天情绪上头重仓，把几周的努力一笔亏掉",
            fontsize=10.5, color=DARK, ha="center", weight="bold")
    ax.text(6.7, 0.42, "0.5% 的意义不是'少赚一点'，是'把出局概率压到可以忽略'——重仓不是加速达标，是加速出局",
            fontsize=9.2, color=DOWN, ha="center")

    savefig(fig, "fig_p6_error_budget.png")


if __name__ == "__main__":
    fig_error_budget()
    print("批次 69b 第 6 章 1 张图已生成")
