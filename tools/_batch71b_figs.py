# -*- coding: utf-8 -*-
"""
批次 71b：第 3 章 1 张新图（补缺图节 3.10）
- fig_p3_signal_k.png   图 3-11  3.10 信号 K 的质量：Brooks 评判标准（强 vs 弱）

运行：python tools/_batch71b_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box, candle, hl_line,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_signal_k():
    fig, ax = plt.subplots(figsize=(13.0, 6.8))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.75, "信号 K 的质量：同样是锤子线，质量可以差很多——位置对是前提，信号 K 质量决定起跑线",
            fontsize=12.5, color=DARK, ha="center", weight="bold")

    # ---- 左：强信号 K（做多锤子示例）----
    draw_box(ax, 0.5, 0.85, 6.0, 5.4, "", ec=UP)
    ax.text(3.5, 5.85, "强信号 K（做多锤子）", fontsize=12, color=UP, ha="center", weight="bold")

    # 示例 K 线：两根
    # 前一根：阴线，收在偏低位
    candle(ax, 2.1, 3.1, 4.3, 3.0, 3.7, 0.30, 1.0, 5)
    # 信号 K：长下影阳线，收在高位，低点跌破前一根但收回
    candle(ax, 3.4, 2.4, 4.9, 3.6, 4.4, 0.30, 1.0, 6)
    ax.text(3.5, 2.2, "收盘在高位 + 阳线 + 长下影（拒绝下方）\n+ 低点跌破前棒但收回（假跌破最強）",
            fontsize=9.0, color=DARK, ha="center")

    features = [
        "① 收盘在高位：收在上半部分，越接近最高越好",
        "② 实体颜色对：做多信号最好是阳线",
        "③ 影线比例合理：下影长，上影不能太长",
        "④ 相对前棒：低点跌破前棒但收盘拉回",
        "⑤ 收盘远离前棒 + 上影 ≤ 1/3-1/2 + 少重叠",
        "⑥ 后续有强跟进：下一根继续同方向推进",
    ]
    for i, f in enumerate(features):
        draw_box(ax, 0.9, 5.0 - i * 0.68, 5.2, 0.55, f, ec=UP, fs=8.6, tc=DARK)

    # ---- 右：弱信号 K ----
    draw_box(ax, 6.9, 0.85, 6.0, 5.4, "", ec=DOWN)
    ax.text(9.9, 5.85, "弱信号 K", fontsize=12, color=DOWN, ha="center", weight="bold")

    # 示例 K 线：十字星式，上下影都长
    candle(ax, 8.6, 3.0, 3.4, 3.7, 4.4, 0.30, 1.0, 5)
    ax.text(9.9, 2.2, "收盘在中间 + 实体太小（接近十字星）\n+ 上下影都长 = 方向不明",
            fontsize=9.0, color=DARK, ha="center")

    weaks = [
        "收盘收在中间或不利端",
        "实体太小（接近十字星，犹豫）",
        "上下影都长（方向不明）",
        "入场 K 一出现就反向跌破入场点 = 坏兆头",
    ]
    for i, w in enumerate(weaks):
        draw_box(ax, 7.3, 5.0 - i * 0.68, 5.2, 0.55, w, ec=DOWN, fs=8.8, tc=DARK)

    draw_box(ax, 0.5, 0.12, 12.6, 0.62,
             "Brooks 区分信号 K 与入场 K：信号 K 给提示，挂单等突破；真正触发成交的叫入场 K，它应朝你的方向走（呼应 3.3 质量评分与 3.4 前一根越小越好）",
             ec=DARK, fs=9.2, tc=DARK)

    savefig(fig, "fig_p3_signal_k.png")


if __name__ == "__main__":
    fig_signal_k()
    print("批次 71b 第 3 章 1 张图已生成")
