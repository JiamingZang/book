# -*- coding: utf-8 -*-
"""
批次 76a：第 1 章 1 张新图（补缺图节 1.14）
- fig_p1_correlation.png   图 1-11  1.14 跨市场：相关性速查 + 风险叠加陷阱 + 三条对策

运行：python tools/_batch76a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_correlation():
    fig, ax = plt.subplots(figsize=(13.4, 7.6))
    style_ax(ax, xlim=(0, 13.8), ylim=(0, 8.0))

    ax.text(6.9, 7.6, "跨市场相关性：相关 ≠ 分散——高相关品种押两注，等于同一方向重仓",
            fontsize=12, color=DARK, ha="center", weight="bold")

    # ============ 左：相关性速查 ============
    draw_box(ax, 0.3, 0.9, 6.4, 6.2, "", ec=DARK)
    ax.text(3.5, 6.8, "① 相关性速查（同一驱动 → 同涨同跌）", fontsize=11, color=DARK, ha="center", weight="bold")

    pairs = [
        ("EURUSD / GBPUSD", "高度正相关", "都是非美货币对美元", UP),
        ("DXY / 非美货币", "负相关", "美元指数强 → 非美整体弱", DOWN),
        ("ES / NQ", "高度正相关", "都是美股指数", UP),
        ("黄金 / 美元", "通常负相关", "避险资金流向；但极端危机时同涨（流动性危机一切皆跌）", ORANGE),
    ]
    y = 6.35
    for pair, rel, desc, c in pairs:
        draw_box(ax, 0.55, y, 5.9, 1.25, "", ec=c)
        ax.text(0.75, y + 0.92, pair, fontsize=9.5, color=DARK, va="center", weight="bold")
        ax.text(3.9, y + 0.92, rel, fontsize=9.5, color=c, va="center", weight="bold")
        ax.text(0.75, y + 0.42, desc, fontsize=8.2, color=DARK, va="center")
        y -= 1.38

    ax.text(3.5, 0.52, "判断依据是\"背后的驱动因素\"，不是名字——同一个方向上的两笔 = 一笔",
            fontsize=8.8, color=DOWN, ha="center", style="italic")

    # ============ 右上：风险叠加陷阱 ============
    draw_box(ax, 7.0, 4.6, 6.5, 2.5, "", ec=DOWN)
    ax.text(10.25, 6.75, "② 风险叠加陷阱（最常见认知错误）", fontsize=11, color=DARK, ha="center", weight="bold")

    draw_box(ax, 7.2, 5.55, 6.1, 1.0, "", ec=DOWN)
    ax.text(10.25, 6.05, "做多 EURUSD 0.5% 风险", fontsize=9.2, color=DARK, ha="center", weight="bold")
    ax.text(10.25, 5.72, "+ 做多 GBPUSD 0.5% 风险", fontsize=9.2, color=DARK, ha="center")
    ax.text(10.25, 5.15, "= 实际 1% 押在同一个\"美元走弱\"上", fontsize=10, color=DOWN, ha="center", weight="bold")

    ax.text(10.25, 4.78, "以为是\"分散\"，其实是\"重仓\"——组合管理最常见的认知错误",
            fontsize=8.8, color=DARK, ha="center", style="italic")

    # ============ 右下：三条对策 ============
    draw_box(ax, 7.0, 0.9, 6.5, 3.3, "", ec=TEAL)
    ax.text(10.25, 3.9, "③ 三条对策", fontsize=11, color=DARK, ha="center", weight="bold")

    sols = [
        ("只选一个 / 合并算", "高相关品种只选一个做，或把仓位合并计算风险", TEAL),
        ("用 DXY 看方向", "DXY 走强，非美多头整体要小心——辅助判断，不单独入场", ORANGE),
        ("算组合总风险", "第 6 章仓位公式按单笔算，组合层面要额外做\"相关性修正\"", DOWN),
    ]
    y = 3.45
    for name, desc, c in sols:
        draw_box(ax, 7.2, y, 6.1, 0.68, "", ec=c)
        ax.text(7.35, y + 0.34, name, fontsize=9.2, color=c, va="center", weight="bold")
        ax.text(8.55, y + 0.34, desc, fontsize=8.2, color=DARK, va="center")
        y -= 0.8

    savefig(fig, "fig_p1_correlation.png")


if __name__ == "__main__":
    fig_correlation()
    print("batch76a done")
