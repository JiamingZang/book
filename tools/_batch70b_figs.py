# -*- coding: utf-8 -*-
"""
批次 70b：第 7 章 1 张新图（补缺图节）
- fig_p7_newbie_errors.png   图 7-8  7.8 新手最常见错误（Brooks 清单）：8 种错误 × 对应军规/章节

运行：python tools/_batch70b_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_newbie_errors():
    fig, ax = plt.subplots(figsize=(13.0, 7.0))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.4))

    ax.text(6.7, 6.95, "新手最常见的错误（Brooks 清单）：几乎每条都对应本书一条军规", fontsize=13,
            color=DARK, ha="center", weight="bold")

    errs = [
        ("1", "过度交易", "没有优势的时段也做", "军规 4：只做计划信号", ORANGE),
        ("2", "追突破", "强势突破顶部买入、底部卖出", "军规 8：追单 = 计划外", ORANGE),
        ("3", "把回调当反转", "趋势中的回调逆势进场", "3.9：只有 20% 变反转", DOWN),
        ("4", "与趋势作对", "逆势摸顶抄底", "4.10：模式匹配", DOWN),
        ("5", "扛单", "止损不挂或手动取消", "军规 7：不浮亏加仓", DOWN),
        ("6", "报复交易", "亏损后加倍想一把赚回", "军规 2：连亏 2 笔收工", ORANGE),
        ("7", "过早止盈", "1 根 K 线赚 1 点就跑", "7.7：模式一致性", TEAL),
        ("8", "没有计划", "临时起意入场", "7.3：三时刻", ORANGE),
    ]

    for i, (num, name, desc, fix, color) in enumerate(errs):
        col = i // 4
        row = i % 4
        x0 = 0.5 + col * 6.5
        ry = 5.9 - row * 1.18
        draw_box(ax, x0, ry - 0.5, 1.0, 0.92, num, ec=color, fs=13, tc=color)
        draw_box(ax, x0 + 1.15, ry - 0.5, 5.2, 0.92, "", ec=color)
        ax.text(x0 + 3.7, ry + 0.18, name, fontsize=11, color=DARK,
                ha="center", weight="bold")
        ax.text(x0 + 3.7, ry - 0.22, desc, fontsize=8.6, color=GRAY, ha="center")
        draw_box(ax, x0 + 1.15, ry - 1.08, 5.2, 0.48, fix, ec=color, fs=8.6, tc=color)

    draw_box(ax, 0.5, 0.14, 12.6, 0.78,
             "用法：把清单贴在你的复盘表顶部，每天收盘后对照一遍——你不需要记住所有正确做法，只需要确认今天没犯清单上的错",
             ec=DARK, fs=9.3, tc=DARK)

    savefig(fig, "fig_p7_newbie_errors.png")


if __name__ == "__main__":
    fig_newbie_errors()
    print("批次 70b 第 7 章 1 张图已生成")
