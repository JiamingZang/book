# -*- coding: utf-8 -*-
"""批次45b：fig_p2_position.png（图 2-3）同一根锤子线，位置不同天差地别
左：下跌后 + 支撑位上的锤子线 = 黄金信号；右：上涨中途 + 无支撑的锤子线 = 噪音
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from draw_handbook_figs import (candle, hl_line, mark, annotate_mark, arrows,
                                style_ax, savefig, UP, DOWN, TEAL, DARK, GRAY, ORANGE)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


def fig_p2_position():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：下跌后 + 支撑位上的锤子线 ----
    seq1 = [
        (0, 110, 111, 106, 106.5), (1, 106.5, 108, 103.5, 104),
        (2, 104, 106.5, 101, 101.5), (3, 101.5, 104, 99, 99.5),
        (4, 99.5, 102, 96, 96.5),   # 下跌到支撑区
        (5, 96.5, 99, 92.5, 96.5),  # 测试支撑（低点 92.5）
        (6, 96.5, 99, 94.5, 98.5),  # 再次测试
        (7, 98.5, 103, 95.5, 96.5),  # 锤子线：长下影 95.5，收在 96.5
        (8, 96.5, 101, 96, 100.5),  # 跟随阳线确认
        (9, 100.5, 105, 100, 104.5),
        (10, 104.5, 108, 103.5, 107.5),
    ]
    for x, o, h, l, c in seq1:
        candle(ax1, x, o, h, l, c, width=0.55)
    # 支撑位：多次测试低点区域 95-96
    hl_line(ax1, -0.5, 11.2, 95.5, color=TEAL, ls="-", lw=1.6, label="支撑位（多次测试）")
    # 锤子线强调
    ax1.add_patch(Rectangle((7 - 0.75, 94.5), 1.5, 8.0, facecolor=ORANGE, alpha=0.15,
                            edgecolor=ORANGE, lw=1.0, zorder=1))
    annotate_mark(ax1, 7, 96.5, "锤子线：空头砸破支撑\n被强力接住（长下影）", 2.4, 108.5, color=ORANGE, fs=10)
    mark(ax1, 8, 100.5, "跟随阳线确认", dy=2.2, color=TEAL, fs=10, box=True)
    mark(ax1, 5, 92.5, "砸下去", dy=-2.2, color=DOWN, fs=9.5)
    style_ax(ax1, xlim=(-0.8, 11.8), ylim=(88, 112))

    # ---- 右：上涨中途 + 无支撑的锤子线 ----
    seq2 = [
        (0, 96, 100, 95, 99.5), (1, 99.5, 103, 98.5, 102.5),
        (2, 102.5, 106, 101.5, 105.5), (3, 105.5, 109, 104.5, 108.5),
        (4, 108.5, 112, 107.5, 111.5),
        (5, 111.5, 114, 107.5, 112),  # 上涨中途的锤子线（长下影）
        (6, 112, 115, 110.5, 114),    # 只是抖动，继续随机
        (7, 114, 116, 112, 113),
        (8, 113, 117, 112, 116.5),
        (9, 116.5, 119, 115.5, 118),
        (10, 118, 120.5, 116, 117),
    ]
    for x, o, h, l, c in seq2:
        candle(ax2, x, o, h, l, c, width=0.55)
    ax2.add_patch(Rectangle((5 - 0.75, 106.5), 1.5, 7.0, facecolor=GRAY, alpha=0.18,
                            edgecolor=GRAY, lw=1.0, zorder=1))
    annotate_mark(ax2, 5, 112, "同样的锤子线\n前不着村后不着店", 1.8, 116.5, color=GRAY, fs=10)
    mark(ax2, 6, 114, "只是正常波动的一次抖动", dy=2.2, color=GRAY, fs=9.5, box=True)
    mark(ax2, 2, 105.5, "上涨中途：没有结构支撑", dy=2.2, color=DARK, fs=9.5)
    annotate_mark(ax2, 9, 118, "后续没有可交易的跟随\n——噪音，不是信号", 10.6, 112.5, color=DARK, fs=10, ha="right")
    style_ax(ax2, xlim=(-0.8, 11.8), ylim=(88, 124))

    fig.suptitle("同一根锤子线：位置 1 支撑位上 = 黄金（左）；位置 2 上涨半空中 = 噪音（右）——先看位置，再看形态",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p2_position.png")


if __name__ == "__main__":
    fig_p2_position()
