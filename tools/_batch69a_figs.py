# -*- coding: utf-8 -*-
"""
批次 69a：第 4 章 1 张新图（补缺图节）
- fig_p4_signal_vs_system.png  图 4-1  4.1 信号不等于系统：信号只答六问中的触发，系统六问全答——只解决第 2 个就下单是赌博

运行：python tools/_batch69a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box, flow_arrow,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_signal_vs_system():
    fig, ax = plt.subplots(figsize=(13.0, 6.6))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.8, "信号 ≠ 系统：信号只回答一个问题，系统回答六个", fontsize=13,
            color=DARK, ha="center", weight="bold")

    qs = ["① 背景：现在什么状态？", "② 触发：用什么信号进？",
          "③ 止损：放哪、为什么？", "④ 目标：看哪，RR 多少？",
          "⑤ 仓位：下多大？", "⑥ 过滤：什么情况不做？"]

    # 左：只靠信号（赌博）
    draw_box(ax, 0.5, 1.1, 5.9, 5.0, "", ec=DOWN)
    ax.text(3.45, 5.7, "只靠信号 = 赌博", fontsize=12, color=DOWN,
            ha="center", weight="bold")
    for i, q in enumerate(qs):
        ry = 5.0 - i * 0.72
        if i == 1:
            draw_box(ax, 0.9, ry - 0.42, 5.1, 0.62, q, ec=UP, fs=9.3, tc=DARK)
            ax.text(5.75, ry - 0.11, "✓", fontsize=12, color=UP, ha="center", weight="bold")
        else:
            draw_box(ax, 0.9, ry - 0.42, 5.1, 0.62, q, ec=GRAY, fs=9.3, tc=GRAY)
            ax.text(5.75, ry - 0.11, "？", fontsize=12, color=GRAY, ha="center", weight="bold")
    ax.text(3.45, 1.28, "只解决第 2 个就下单 → 赌博：\n其余五问留给临场情绪回答",
            fontsize=9.2, color=DOWN, ha="center")

    flow_arrow(ax, 6.5, 3.6, 7.4, 3.6, color=DARK)
    ax.text(6.95, 3.85, "≠", fontsize=13, color=DARK, ha="center", weight="bold")

    # 右：完整系统（交易）
    draw_box(ax, 7.5, 1.1, 5.6, 5.0, "", ec=UP)
    ax.text(10.3, 5.7, "完整系统 = 交易", fontsize=12, color=UP,
            ha="center", weight="bold")
    for i, q in enumerate(qs):
        ry = 5.0 - i * 0.72
        draw_box(ax, 7.9, ry - 0.42, 4.8, 0.62, q, ec=TEAL, fs=9.3, tc=DARK)
        ax.text(12.55, ry - 0.11, "✓", fontsize=12, color=UP, ha="center", weight="bold")
    ax.text(10.3, 1.28, "六要素具体到“没有临场决策的空间”\n规则写死 → 盘中只需执行，不需要思考",
            fontsize=9.2, color=UP, ha="center")

    draw_box(ax, 0.5, 0.12, 12.6, 0.75,
             "系统的真正作用，不是帮你赚更多，是帮你在情绪上头时不做蠢事——思考留给冷静的盘前，执行交给机械的盘中（第 7 章执行率由此而来）",
             ec=DARK, fs=9.3, tc=DARK)

    savefig(fig, "fig_p4_signal_vs_system.png")


if __name__ == "__main__":
    fig_signal_vs_system()
    print("批次 69a 第 4 章 1 张图已生成")
