# -*- coding: utf-8 -*-
"""
批次 72a：第 5 章 2 张新图（补缺图节 5.1/5.14）
- fig_p5_worldview.png   图 5-1  5.1 核心世界观：机构 vs 散户，扫止损拿流动性——区分实证与叙事
- fig_p5_premium.png     图 5-12 5.14 溢价与折价：摆动范围中点分界"贵不贵"

运行：python tools/_batch72a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box, flow_arrow,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_worldview():
    fig, ax = plt.subplots(figsize=(13.0, 6.8))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.75, "SMC 核心世界观：止损密集的地方就是机构的目标——扫完止损后的方向才是真实方向",
            fontsize=12.5, color=DARK, ha="center", weight="bold")

    # 左：机构 + 散户
    draw_box(ax, 0.5, 3.5, 3.4, 2.4, "机构（聪明钱）\n\n需要对手盘才能建仓/出货\n→ 故意把价格推向止损密集区\n→ 扫掉止损拿到流动性", ec=DOWN, fs=9.0, tc=DOWN)
    draw_box(ax, 4.4, 3.5, 3.4, 2.4, "散户（可预测）\n\n在明显位置挂止损\n追突破\n在关键位抄底摸顶", ec=ORANGE, fs=9.0, tc=ORANGE)

    # 中间：扫止损
    flow_arrow(ax, 4.0, 4.7, 4.3, 4.7, color=DARK)
    ax.text(4.15, 5.0, "猎杀", fontsize=8.5, color=DARK, ha="center")

    # 右上：拿流动性
    draw_box(ax, 8.3, 3.5, 4.6, 2.4, "扫完止损 → 拿到流动性\n\n止损单被触发 = 机构吃到对手盘\n→ 反向走 = 机构的真实方向", ec=UP, fs=9.2, tc=UP)
    flow_arrow(ax, 7.9, 4.7, 8.2, 4.7, color=DARK)

    # 底部：实证 vs 叙事
    draw_box(ax, 0.5, 0.55, 6.0, 2.3, "实证（可验证）\n挂单和止损确实聚集在整数关口、前高前低附近——\n这是真实的市场微观结构", ec=TEAL, fs=9.2, tc=TEAL)
    draw_box(ax, 6.9, 0.55, 6.0, 2.3, "叙事（无法验证）\n“机构故意猎杀散户”无法证明——可能是蓄意，\n也可能只是流动性枯竭", ec=GRAY, fs=9.2, tc=GRAY)

    draw_box(ax, 0.5, 0.1, 12.6, 0.42,
             "正确态度：借用决策框架（等 sweep、不追突破、在流动性池附近警惕），不必相信阴谋论叙事——框架帮你少亏，叙事只会让你觉得自己看穿了市场",
             ec=DARK, fs=8.8, tc=DARK)

    savefig(fig, "fig_p5_worldview.png")


def fig_premium():
    fig, ax = plt.subplots(figsize=(13.0, 6.2))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 6.6))

    ax.text(6.7, 6.15, "溢价与折价：以当前摆动范围的中点为界——“贵不贵”决定这笔要不要执行",
            fontsize=12.5, color=DARK, ha="center", weight="bold")

    # 范围框：上=溢价，下=折价，中间=平衡点
    draw_box(ax, 2.2, 3.6, 9.0, 1.7, "溢价区 Premium：价格偏贵——机构在这里卖出", ec=DOWN, fs=10, tc=DOWN)
    draw_box(ax, 2.2, 1.2, 9.0, 1.7, "折价区 Discount：价格偏便宜——机构在这里买入", ec=UP, fs=10, tc=UP)
    # 中点线
    ax.plot([2.2, 11.2], [3.3, 3.3], color=DARK, lw=1.2, ls="--")
    ax.text(11.45, 3.28, "中点 = 公允价", fontsize=8.6, color=DARK, ha="left")

    # 用法标注
    draw_box(ax, 2.2, 5.45, 9.0, 0.5, "用法：上升趋势突破 → 等价格回调进折价区再做多；下降趋势突破 → 等反弹进溢价区再做空", ec=ORANGE, fs=8.8, tc=ORANGE)

    draw_box(ax, 0.5, 0.12, 12.6, 0.95,
             "为什么不追：机构低买高卖，你在溢价区追多、折价区追空 = 在机构准备离场的位置接盘。\n"
             "注意：折价区不是“必涨”是“概率占优”，仍需信号 K + sweep 确认；折价区 ≈ 第 4 章斐波那契 0.5-0.618 回撤带的 SMC 版本",
             ec=DARK, fs=9.0, tc=DARK)

    savefig(fig, "fig_p5_premium.png")


if __name__ == "__main__":
    fig_worldview()
    fig_premium()
    print("批次 72a 第 5 章 2 张图已生成")
