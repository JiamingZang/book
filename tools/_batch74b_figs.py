# -*- coding: utf-8 -*-
"""
批次 74b：第 1 章 1 张新图（补缺图节 1.8）
- fig_p1_blackswan.png   图 1-9  1.8 基本面黑天鹅：数据炸弹日历 + 数据前纪律 + 价格是先行指标

运行：python tools/_batch74b_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_blackswan():
    fig, ax = plt.subplots(figsize=(13.0, 7.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.8))

    ax.text(6.7, 7.4, "基本面黑天鹅：你不需要会分析基本面，只需要知道有炸弹——知道它何时引爆，引爆前别站在坑里",
            fontsize=12, color=DARK, ha="center", weight="bold")

    # 左：数据日历
    draw_box(ax, 0.5, 3.0, 6.0, 4.0, "", ec=DARK)
    ax.text(3.5, 6.55, "炸弹日历（提前标出）", fontsize=10.5, color=DARK, ha="center", weight="bold")
    events = [
        ("FOMC 利率决议", "美元/黄金/美股", "每年 8 次，固定日历"),
        ("非农就业", "美元/黄金/股指", "每月第一个周五 20:30"),
        ("CPI 通胀", "各国货币/债券", "月度"),
        ("期权到期日", "三巫日/四巫日波动放大", "每月第三个周五"),
        ("风险情绪", "避险资产", "突发"),
    ]
    for i, (name, affect, when) in enumerate(events):
        ry = 5.9 - i * 0.72
        draw_box(ax, 0.9, ry - 0.32, 2.4, 0.58, name, ec=ORANGE, fs=8.4, tc=ORANGE)
        draw_box(ax, 3.4, ry - 0.32, 1.5, 0.58, affect[:6], ec=GRAY, fs=7.8, tc=GRAY)
        draw_box(ax, 5.0, ry - 0.32, 1.3, 0.58, when[:8], ec=GRAY, fs=7.4, tc=GRAY)

    # 右：数据前纪律
    draw_box(ax, 6.9, 3.0, 6.0, 4.0, "", ec=DOWN)
    ax.text(9.9, 6.55, "引爆前别站在坑里（三条纪律）", fontsize=10.5, color=DOWN, ha="center", weight="bold")
    rules = [
        "① 交易前看经济日历，炸弹时间写进周计划",
        "② 数据前 15 分钟不开新仓（军规第 5 条）",
        "③ 有持仓：提前收紧止损或减仓，别赌数据利好",
        "④ 期权到期日：成交量放大、信号失真、纪律同数据日",
    ]
    for i, r in enumerate(rules):
        draw_box(ax, 7.3, 5.75 - i * 0.66, 5.2, 0.54, r, ec=DOWN, fs=8.6, tc=DARK)

    # 底部：为什么数据击穿技术位 + 新闻已在价格里
    draw_box(ax, 0.5, 0.55, 6.0, 2.1,
             "为什么数据能击穿技术位：数据瞬间全市场注意力切到基本面，\n"
             "大量资金几秒内涌向同一方向——技术位那一刻没有承接力。\n"
             "数据事件是技术分析的例外，把例外当常态防。",
             ec=TEAL, fs=8.8, tc=TEAL)
    draw_box(ax, 6.9, 0.55, 6.0, 2.1,
             "新闻已经在价格里：机构在新闻发布前就已知道并交易。\n"
             "价格不是对新闻的反应，价格是新闻的先行指标——\n"
             "盯价格行为，别追新闻标题（第 2-3 章）。",
             ec=UP, fs=8.8, tc=UP)

    draw_box(ax, 0.5, 0.1, 12.6, 0.4,
             "数据瞬间的价格行为是机器+做市商主导的，不是你的价格行为——你看不懂那一刻的 K 线",
             ec=DARK, fs=8.8, tc=DARK)

    savefig(fig, "fig_p1_blackswan.png")


if __name__ == "__main__":
    fig_blackswan()
    print("批次 74b 第 1 章 1 张图已生成")
