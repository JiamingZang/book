# -*- coding: utf-8 -*-
"""
批次 73b：第 1 章 1 张新图（补缺图节 1.10）
- fig_p1_futures_spec.png   图 1-9  1.10 期货合约规格速查：prop 考核主战场

运行：python tools/_batch73b_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_futures_spec():
    fig, ax = plt.subplots(figsize=(13.0, 7.2))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.6))

    ax.text(6.7, 7.15, "期货：prop 考核的主战场——合约规格下单前必查，直接进第 6 章仓位公式",
            fontsize=12.5, color=DARK, ha="center", weight="bold")

    # 品种表格
    headers = ["品种", "代码", "每点价值", "tick", "特点"]
    rows = [
        ["标普500 E-mini", "ES", "$50", "0.25 点 = $12.5", "流动性最好，日内首选"],
        ["纳指 E-mini", "NQ", "$20", "0.25 点 = $5", "波动比 ES 大（约 2 倍）"],
        ["道指", "YM", "$5", "1 点 = $5", "波动较小"],
        ["原油", "CL", "$1000", "0.01 点 = $10", "波动大，受基本面驱动"],
        ["黄金", "GC", "$100", "0.1 点 = $10", "避险，与美元负相关"],
    ]
    draw_box(ax, 0.5, 4.9, 12.6, 0.6, "", ec=DARK)
    for j, h in enumerate(headers):
        ax.text(1.15 + j * 2.6, 5.18, h, fontsize=9.5, color=DARK, ha="center", weight="bold")
    for i, row in enumerate(rows):
        ry = 4.4 - i * 0.62
        color = UP if row[0].startswith("标普") else TEAL
        for j, cell in enumerate(row):
            draw_box(ax, 0.7 + j * 2.55, ry - 0.3, 2.45, 0.52, cell, ec=color, fs=8.2,
                     tc=DARK if j in (0, 4) else color)
    ax.text(0.8, 1.15, "新手从 ES 起步更合理：NQ 波动约 ES 两倍，同样的止损距离，NQ 上被扫的概率高得多",
            fontsize=9.0, color=DARK)

    # 右侧机制
    draw_box(ax, 6.9, 0.9, 6.0, 4.4, "", ec=DARK)
    ax.text(9.9, 4.95, "四个核心机制", fontsize=10.5, color=DARK, ha="center", weight="bold")
    mechs = [
        "合约规格：固定乘数，直接进仓位公式",
        "tick 价值：最小变动，止损距离换算金额",
        "到期换月：主连合约，价差跳变要留意",
        "保证金：日内低 / 隔夜高，考核只用日内",
        "量价真实：集中成交量，Wyckoff/订单流最可靠",
    ]
    for i, m in enumerate(mechs):
        draw_box(ax, 7.2, 4.4 - i * 0.78, 5.4, 0.62, m, ec=TEAL, fs=8.8, tc=DARK)

    draw_box(ax, 0.5, 0.12, 12.6, 0.7,
             "prop 公司偏爱期货的原因：集中交易所、量价真实、合约标准、风控清晰——Topstep/Apex 都是期货 prop；ES/NQ 是日内价格行为最佳标的（南桥/Thomas Wade 都做 ES）",
             ec=DARK, fs=9.0, tc=DARK)

    savefig(fig, "fig_p1_futures_spec.png")


if __name__ == "__main__":
    fig_futures_spec()
    print("批次 73b 第 1 章 1 张图已生成")
