# -*- coding: utf-8 -*-
"""
批次 74a：第 4 章 1 张新图（补缺图节 4.25）
- fig_p4_rules_banlist.png   图 4-27  4.25 决策执行口诀与禁止清单

运行：python tools/_batch74a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_rules_banlist():
    fig, ax = plt.subplots(figsize=(13.0, 7.6))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 8.0))

    ax.text(6.7, 7.55, "决策执行口诀 10 条 + 禁止行为清单：遇到清单任何一条，停止交易或放弃当前信号",
            fontsize=12.5, color=DARK, ha="center", weight="bold")

    # 左：10 条口诀
    draw_box(ax, 0.5, 0.85, 6.0, 6.4, "", ec=UP)
    ax.text(3.5, 6.85, "执行口诀 10 条", fontsize=11.5, color=UP, ha="center", weight="bold")
    mantras = [
        "1. 看不懂，等；极端混乱，等",
        "2. 尖峰中只顺势——禁 SCS、禁追高潮",
        "3. 通道/区间只顺 direction",
        "4. 宽通道不追突破，顺边界/回撤",
        "5. 区间只顺一侧；中性则等",
        "6. 反转/MTR 只诊断不下单",
        "7. 楔形回撤可顺势；末端楔形禁追顺势",
        "8. 信号必须等收盘",
        "9. 止损/方程不过关直接放弃",
        "10. 二次入场失败后不再第三次",
    ]
    for i, m in enumerate(mantras):
        draw_box(ax, 0.9, 6.35 - i * 0.54, 5.2, 0.44, m, ec=TEAL, fs=8.4, tc=DARK)

    # 右：禁止清单
    draw_box(ax, 6.9, 0.85, 6.0, 6.4, "", ec=DOWN)
    ax.text(9.9, 6.85, "禁止行为清单（任一项即停手）", fontsize=11.5, color=DOWN, ha="center", weight="bold")
    bans = [
        "未识别周期位置就交易 / 数据不足仍下单",
        "尖峰中做反转；买进/卖出高潮后追原方向",
        "区间中追普通突破；区间中部入场",
        "宽通道中追突破；任何逆势",
        "AIL 中做空、AIS 中做多；方向不一致",
        "用长外包棒两端突破直接入场",
        "二次入场价明显优于第一次仍强做",
        "信号棒过长/止损过大仍强做；方程不过仍下单",
        "为“更好看”扭曲结构止损凑方程",
        "止损后立即反手；连续两笔止损后不重新评估",
    ]
    for i, b in enumerate(bans):
        draw_box(ax, 7.3, 6.35 - i * 0.54, 5.2, 0.44, b, ec=DOWN, fs=8.2, tc=DARK)

    draw_box(ax, 0.5, 0.1, 12.6, 0.62,
             "一句话记忆：决策 = 门控 + 方程——方向不明先等（门控），三价定死再算盈亏比（方程）；止损永远挂在结构失效位外 1 跳，不是挂在你希望的地方",
             ec=DARK, fs=9.2, tc=DARK)

    savefig(fig, "fig_p4_rules_banlist.png")


if __name__ == "__main__":
    fig_rules_banlist()
    print("批次 74a 第 4 章 1 张图已生成")
