# -*- coding: utf-8 -*-
"""
批次 68b：第 10 章 1 张新图（补缺图节）
- fig_p10_three_dims.png  图 10-1  10.1 期权三维度：方向 × 波动幅度 × 时间——三把锁必须同时打开

运行：python tools/_batch68b_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from draw_handbook_figs import (style_ax, savefig, draw_box, flow_arrow,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_three_dims():
    fig, ax = plt.subplots(figsize=(13.0, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.75, "方向交易 1 个变量 → 期权交易 3 个变量（三把锁必须同时打开）",
            fontsize=12.5, color=DARK, ha="center", weight="bold")

    # 左：方向交易（线性）
    draw_box(ax, 0.6, 3.4, 3.5, 2.2, "", ec=GRAY)
    ax.text(2.35, 5.25, "方向交易", fontsize=11.5, color=DARK, ha="center", weight="bold")
    ax.text(2.35, 4.3, "价格 → 盈亏 一一对应\n看涨就赚、看跌就亏\n线性、直接、可等待",
            fontsize=9.0, color=DARK, ha="center")
    ax.text(2.35, 3.62, "唯一变量：方向", fontsize=9.5, color=GRAY, ha="center")

    flow_arrow(ax, 4.2, 4.5, 5.4, 4.5, color=DARK)
    ax.text(4.8, 4.75, "多出", fontsize=9, color=DARK, ha="center")

    # 右：期权三维度（三把锁）
    dims = [
        ("维度 1：方向", "价格涨还是跌？（你已经会的）", UP, "✓"),
        ("维度 2：幅度 / 波动", "价格动得够不够大？动得不够照样亏", ORANGE, "✗"),
        ("维度 3：时间", "变动什么时候发生？到期作废——硬约束", DOWN, "✗"),
    ]
    dy = 5.0
    for name, desc, col, ok in dims:
        draw_box(ax, 5.6, dy - 0.78, 7.3, 1.05, "", ec=col)
        ax.text(5.9, dy - 0.32, name, fontsize=10.8, color=col, ha="left", weight="bold")
        ax.text(5.9, dy - 0.62, desc, fontsize=8.8, color=DARK, ha="left")
        ax.text(12.65, dy - 0.33, ok, fontsize=13, color=col, ha="center", weight="bold")
        if dy > 3.4:
            flow_arrow(ax, 9.25, dy - 0.78, 9.25, dy - 1.45, color=GRAY)
        dy -= 1.6

    # 底部：AND 逻辑 + 常见失败
    draw_box(ax, 0.6, 0.8, 7.3, 1.55, "", ec=TEAL)
    ax.text(4.25, 1.95, "三条件必须同时满足才赚钱", fontsize=11, color=DARK,
            ha="center", weight="bold")
    ax.text(4.25, 1.2, "方向 ✓ ＋ 幅度 ✓ ＋ 时间 ✓ ＝ 盈利\n期权 = 方向 × 波动 × 时间的合约",
            fontsize=9.0, color=DARK, ha="center")
    draw_box(ax, 8.2, 0.8, 4.7, 1.55, "", ec=DOWN)
    ax.text(10.55, 1.95, "为什么很多人方向看对还亏", fontsize=10.5, color=DOWN,
            ha="center", weight="bold")
    ax.text(10.55, 1.2, "价格涨了，但涨得太慢、太少\n或涨的时候已经快到期了",
            fontsize=9.0, color=DARK, ha="center")

    savefig(fig, "fig_p10_three_dims.png")


if __name__ == "__main__":
    fig_three_dims()
    print("批次 68b 第 10 章 1 张图已生成")
