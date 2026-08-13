# -*- coding: utf-8 -*-
"""
批次 75b：第 1 章 1 张新图（补缺图节 1.16）
- fig_p1_ashare.png   图 1-12  1.16 A 股：规则速查 + 波段税成本 + 三条差异三条应对

运行：python tools/_batch75b_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_ashare():
    fig, ax = plt.subplots(figsize=(13.4, 7.6))
    style_ax(ax, xlim=(0, 13.8), ylim=(0, 8.0))

    ax.text(6.9, 7.6, "A 股不是另一套市场：同一套价格行为 + 三条特殊规则（T+1 / 涨跌停 / 政策驱动）",
            fontsize=12, color=DARK, ha="center", weight="bold")

    # ============ 左：规则速查 ============
    draw_box(ax, 0.3, 0.9, 6.4, 6.2, "", ec=DARK)
    ax.text(3.5, 6.8, "① 规则速查（关键差异高亮）", fontsize=11, color=DARK, ha="center", weight="bold")

    rules = [
        ("当日回转", "T+1（当天买次日才能卖）", "T+0", DOWN),
        ("涨跌停", "主板 ±10% / 创业科创 ±20% / ST ±5%", "无", DOWN),
        ("交易时段", "9:30-11:30、13:00-15:00", "日盘 + 夜盘", GRAY),
        ("集合竞价", "9:15-9:25 开盘、14:57-15:00 收盘", "开盘竞价", GRAY),
        ("最小单位", "100 股（1 手）", "1 手（规格固定）", GRAY),
        ("做空", "融券受限、门槛高", "自由", ORANGE),
        ("杠杆", "融资最多约 1:1", "保证金制，灵活", ORANGE),
    ]
    y = 6.35
    for name, aval, fval, c in rules:
        draw_box(ax, 0.55, y, 5.9, 0.62, "", ec=c)
        ax.text(0.75, y + 0.31, name, fontsize=8.8, color=DARK, va="center", weight="bold")
        ax.text(2.05, y + 0.31, aval, fontsize=8.0, color=c, va="center", weight="bold")
        ax.text(5.35, y + 0.31, "期货/外汇: " + fval, fontsize=8.0, color=DARK, va="center", ha="right")
        y -= 0.76

    ax.text(3.5, 0.52, "T+1 与涨跌停是和本书日内体系冲突最大的两条——周期要放大，止损要推迟",
            fontsize=8.6, color=DOWN, ha="center", style="italic")

    # ============ 右上：成本 ============
    draw_box(ax, 7.0, 4.3, 6.5, 2.8, "", ec=DARK)
    ax.text(10.25, 6.75, "② 成本结构 = 波段税（高频的隐形杀手）", fontsize=11, color=DARK, ha="center", weight="bold")

    costs = [
        ("印花税", "卖出单边 0.05%", "2023 年 8 月起减半，仍是主要成本"),
        ("佣金", "约万 2.5（双边）", "可和券商谈，网上开户更低"),
        ("过户费", "约 0.001%（双边）", "金额小，但买卖都有"),
    ]
    y = 6.25
    for name, rate, desc in costs:
        draw_box(ax, 7.2, y, 6.1, 0.55, "", ec=GRAY)
        ax.text(7.35, y + 0.27, name, fontsize=8.8, color=DARK, va="center", weight="bold")
        ax.text(8.3, y + 0.27, rate, fontsize=8.6, color=DOWN, va="center", weight="bold")
        ax.text(9.8, y + 0.27, desc, fontsize=7.8, color=DARK, va="center")
        y -= 0.68

    draw_box(ax, 7.2, 4.5, 6.1, 1.15, "", ec=DOWN)
    ax.text(10.25, 5.25, "算账：10 万满仓进出一次 ≈ 102 元（50+50+2）",
            fontsize=9, color=DARK, ha="center", weight="bold")
    ax.text(10.25, 4.82, "一年高频 100 次 = 1 万元 = 年化 10% 成本——结构天然惩罚高频，\n和外汇/期货的\"点差+佣金\"不同，它更接近\"波段税\"",
            fontsize=8.2, color=DARK, ha="center")

    # ============ 右下：三条差异三条应对 ============
    draw_box(ax, 7.0, 0.9, 6.5, 3.0, "", ec=TEAL)
    ax.text(10.25, 3.6, "③ 三条差异 → 三条应对", fontsize=11, color=DARK, ha="center", weight="bold")

    diffs = [
        ("周期放大", "T+1 无法日内纠错 → 用日线/周线价格行为，分钟级方法水土不服", TEAL),
        ("止损推迟一天", "T+1 当天买的仓位止损最早明天生效 → 按两天波动算仓位（第 6 章 ATR）", ORANGE),
        ("涨跌停 = 流动性断层", "一字板无人成交，跌停板上止损卖不出去 → 它不是信号，是滑点的极端版", DOWN),
    ]
    y = 3.15
    for name, desc, c in diffs:
        draw_box(ax, 7.2, y, 6.1, 0.68, "", ec=c)
        ax.text(7.35, y + 0.34, name, fontsize=9.2, color=c, va="center", weight="bold")
        ax.text(8.35, y + 0.34, desc, fontsize=8.2, color=DARK, va="center")
        y -= 0.8

    ax.text(10.25, 0.52, "市场特性：散户贡献约 6 成交易量 → 价格行为同样有效但题材炒作更疯；政策 = 最高等级的数据黑天鹅（呼应 1.8）",
            fontsize=8.4, color=DARK, ha="center", style="italic")

    savefig(fig, "fig_p1_ashare.png")


if __name__ == "__main__":
    fig_ashare()
    print("batch75b done")
