# -*- coding: utf-8 -*-
"""
批次 71a：第 3 章 2 张新图（补缺图节 3.6/3.7）
- fig_p3_volume_score.png   图 3-6  3.6 量价三问评分器：信号的最后一道滤网
- fig_p3_winrate_ladder.png 图 3-7  3.7 信号组合的胜率排序：高胜率 vs 低胜率

运行：python tools/_batch71a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_volume_score():
    fig, ax = plt.subplots(figsize=(13.0, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 6.8))

    ax.text(6.7, 6.35, "量价三问：形态合格后，用量给信号打分——三问全过才是高质量信号", fontsize=13,
            color=DARK, ha="center", weight="bold")

    qs = [
        ("问 1", "趋势方向的移动有没有量？", "顺势信号放量跟随 = 加分", UP),
        ("问 2", "回调 / 反弹有没有量？", "缩量回调 = 健康；放量回调 = 趋势要变", ORANGE),
        ("问 3", "突破关键位有没有量？", "放量突破 = 真；缩量突破 = 假突破高发", DOWN),
    ]
    for i, (qnum, q, ans, color) in enumerate(qs):
        ry = 5.5 - i * 1.25
        draw_box(ax, 0.5, ry - 0.42, 1.1, 0.8, qnum, ec=color, fs=11, tc=color)
        draw_box(ax, 1.8, ry - 0.42, 5.6, 0.8, q, ec=color, fs=10, tc=DARK)
        draw_box(ax, 7.6, ry - 0.42, 5.6, 0.8, ans, ec=color, fs=9.5, tc=color)

    # 评分规则条
    draw_box(ax, 0.5, 1.25, 3.9, 0.9, "三问全过 = 高质量信号\n按规则入场", ec=UP, fs=9.5, tc=UP)
    draw_box(ax, 4.7, 1.25, 3.9, 0.9, "一问不过 = 降级处理\n等更好的位置或更明确的量", ec=ORANGE, fs=9.0, tc=ORANGE)
    draw_box(ax, 8.9, 1.25, 3.9, 0.9, "两问不过 = 放弃\n等下一个", ec=DOWN, fs=9.5, tc=DOWN)

    draw_box(ax, 0.5, 0.12, 12.6, 0.8,
             "量不是第四个入场条件，是给前三道闸（背景×位置×形态）的评分器——把“模糊的感觉”变成“可执行的规则”\n"
             "注意：外汇的量是 tick 近似只能参考，期货的量才真（第 2.5 限定）",
             ec=DARK, fs=9.2, tc=DARK)

    savefig(fig, "fig_p3_volume_score.png")


def fig_winrate_ladder():
    fig, ax = plt.subplots(figsize=(13.0, 6.6))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.0))

    ax.text(6.7, 6.6, "信号组合的胜率排序：高胜率是主力 setup，低胜率是“不该做”清单", fontsize=13,
            color=DARK, ha="center", weight="bold")

    highs = [
        "上升趋势回调到前支撑 / HL 区\n+ 缩量 + 锤子 / 吞没 → 做多",
        "关键阻力假突破 + 放量收回 → 做空",
        "结构突破（HL 跌破）后的第一次回抽\n+ 拒绝 → 顺势入场",
    ]
    lows = [
        "趋势中途的 pin bar 反转（逆大方向）",
        "没有背景的孤立吞没",
        "区间中部的任何信号",
    ]

    # 左：高胜率
    draw_box(ax, 0.5, 0.85, 6.0, 5.3, "", ec=UP)
    ax.text(3.5, 5.7, "高胜率组合（顺势 + 位置 + 形态）", fontsize=12, color=UP,
            ha="center", weight="bold")
    for i, h in enumerate(highs):
        draw_box(ax, 0.9, 4.7 - i * 1.3, 5.2, 1.1, h, ec=TEAL, fs=9.2, tc=DARK)
    ax.text(3.5, 1.0, "主力 setup：做它、统计它（第 8 章）、优化它",
            fontsize=9.2, color=UP, ha="center")

    # 右：低胜率
    draw_box(ax, 6.9, 0.85, 6.0, 5.3, "", ec=DOWN)
    ax.text(9.9, 5.7, "低胜率组合（逆势 + 半空位置）", fontsize=12, color=DOWN,
            ha="center", weight="bold")
    for i, l in enumerate(lows):
        draw_box(ax, 7.3, 4.7 - i * 1.3, 5.2, 1.1, l, ec=GRAY, fs=9.6, tc=GRAY)
    ax.text(9.9, 1.0, "不该做的清单：写进规则书，不是为了“万一可以做”，\n是为了在盘中止住你的手",
            fontsize=9.2, color=DOWN, ha="center")

    draw_box(ax, 0.5, 0.1, 12.6, 0.62,
             "大多数人是在连亏之后才意识到自己在做低胜率单——先知道哪些是低胜率的，比知道哪些是高胜率的更救命",
             ec=DARK, fs=9.3, tc=DARK)

    savefig(fig, "fig_p3_winrate_ladder.png")


if __name__ == "__main__":
    fig_volume_score()
    fig_winrate_ladder()
    print("批次 71a 第 3 章 2 张图已生成")
