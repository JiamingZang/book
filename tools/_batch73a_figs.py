# -*- coding: utf-8 -*-
"""
批次 73a：第 7 章 1 张新图（补缺图节 7.10）
- fig_p7_mastery_ladder.png   图 7-9  7.10 精通阶梯：从新手到直觉的八级

运行：python tools/_batch73a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_mastery_ladder():
    fig, ax = plt.subplots(figsize=(13.0, 7.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.8))

    ax.text(6.7, 7.35, "精通阶梯：大多数人停在“基于规则”之前——能从规则走到规则的自由裁量，已是前 5%",
            fontsize=12.5, color=DARK, ha="center", weight="bold")

    levels = [
        ("Newbie", "新手", "刚接触，凭感觉", GRAY),
        ("Beginner", "初学", "知道概念，不会用", GRAY),
        ("Apprentice", "学徒", "模仿他人，不稳定", GRAY),
        ("Intermediate", "中级", "开始有自己的判断", GRAY),
        ("Proficient", "熟练", "Rule-based 基于规则", TEAL),
        ("Advanced", "高阶", "Rule-based Discretionary\n基于规则的自由裁量", UP),
        ("Expert", "专家", "Discretionary 自由裁量", UP),
        ("Mastery", "精通", "Intuitive 直觉（规则内化）", ORANGE),
    ]
    n = len(levels)
    # 阶梯：右高左低的梯子
    for i, (en, cn, desc, color) in enumerate(levels):
        # 阶梯踏步（左下到右上）
        x0 = 1.2 + i * 1.35
        y0 = 1.3 + i * 0.5
        # 踏板
        ax.plot([x0, x0 + 1.1], [y0, y0], color=color, lw=3)
        # 竖板（下一个踏步的起点）
        if i < n - 1:
            ax.plot([x0 + 1.1, x0 + 1.1], [y0, y0 + 0.5], color=color, lw=2)
        # 级别标注
        draw_box(ax, x0 - 0.25, y0 + 0.12, 1.6, 0.62, en, ec=color, fs=8.2, tc=color)
        ax.text(x0 + 0.55, y0 - 0.28, cn, fontsize=7.8, color=DARK, ha="center")
        ax.text(x0 + 0.55, y0 - 0.52, desc, fontsize=6.2, color=GRAY, ha="center")

    # 前 5% 标注
    ax.annotate("前 5%", xy=(6.4 + 0.55, 1.3 + 5 * 0.5 + 0.9), xytext=(5.2, 5.6),
                fontsize=10, color=UP, weight="bold",
                arrowprops=dict(arrowstyle="->", color=UP, lw=1.5))

    # 底部说明
    draw_box(ax, 0.5, 0.12, 12.6, 0.95,
             "对照定位：本书第 4 章给规则（Rule-based）、第 7 章给流程（执行）、第 8 章给验证（数据反馈）——目标是把读者送到 Proficient → Advanced。\n"
             "往上靠笔数积累（8.7 的 100+ 笔）与复盘质量；职业化每日动作 = 事后读图，直到能对任何图表做细致的逐根 K 线解析",
             ec=DARK, fs=9.0, tc=DARK)

    savefig(fig, "fig_p7_mastery_ladder.png")


if __name__ == "__main__":
    fig_mastery_ladder()
    print("批次 73a 第 7 章 1 张图已生成")
