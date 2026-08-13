# -*- coding: utf-8 -*-
"""
批次 70a：第 7 章 1 张新图（补缺图节）
- fig_p7_rules_ten.png   图 7-6  7.6 考核期十条军规速查：每条军规对应一种真实死法

运行：python tools/_batch70a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_rules_ten():
    fig, ax = plt.subplots(figsize=(13.0, 8.2))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 8.6))

    ax.text(6.7, 8.2, "考核期十条军规速查：每条军规对应一种真实死法", fontsize=13,
            color=DARK, ha="center", weight="bold")

    rules = [
        ("1", "单笔风险 ≤ 0.5%", "防单笔爆仓", DOWN),
        ("2", "每日最多 2-3 笔，连亏 2 笔当天收工", "防报复交易", ORANGE),
        ("3", "当天权益回撤到 3% 立即停手（留 2% 缓冲）", "防单日爆仓", DOWN),
        ("4", "只做计划清单里的信号，其他一律不做", "防过度交易", ORANGE),
        ("5", "数据公布前后 15 分钟不开新仓", "防数据黑天鹅", GRAY),
        ("6", "持仓目标到 1R 至少移止损保本", "防利润回吐", TEAL),
        ("7", "不浮亏加仓、不摊平、不锁仓", "防承诺升级", GRAY),
        ("8", "错过信号就错过，追单 = 计划外单", "防冲动追单", ORANGE),
        ("9", "每天复盘 15 分钟，记录执行率", "防无反馈", TEAL),
        ("10", "考核期 = 训练期：活下来 + 执行一致", "总纲：不是“快点达标”", UP),
    ]

    for i, (num, text, guard, color) in enumerate(rules):
        ry = 7.4 - i * 0.68
        draw_box(ax, 0.5, ry - 0.42, 0.85, 0.6, num, ec=color, fs=12, tc=color)
        draw_box(ax, 1.5, ry - 0.42, 8.6, 0.6, text, ec=color, fs=9.6, tc=DARK)
        draw_box(ax, 10.3, ry - 0.42, 2.9, 0.6, guard, ec=color, fs=9.0, tc=color)

    draw_box(ax, 0.5, 0.12, 12.6, 0.95,
             "十条不是建议，是硬约束——抄在纸上放桌面，入场前逐条核对；违规一次，当天强制收工（不管盈亏）。\n"
             "重仓不是加速达标，是加速出局：第 1/3 条守住资金线，第 2/4/8 条守住情绪线，第 10 条是总纲（呼应 6.1 犯错预算与 9.4 失败纪律）",
             ec=DARK, fs=9.2, tc=DARK)

    savefig(fig, "fig_p7_rules_ten.png")


if __name__ == "__main__":
    fig_rules_ten()
    print("批次 70a 第 7 章 1 张图已生成")
