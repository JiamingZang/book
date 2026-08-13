# -*- coding: utf-8 -*-
"""
批次 68a：第 1 章 2 张新图（补缺图节）
- fig_p1_instruments.png      图 1-3  1.2 品种对比：外汇/期货/股票CFD/加密/黄金 × 时间/杠杆/量真实性/Prop适用
- fig_p1_longshort_spec.png   图 1-5  1.4 做多做空与合约规格：做多vs做空机制 + 三个计量单位 + 算例

运行：python tools/_batch68a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from draw_handbook_figs import (style_ax, savefig, draw_box, flow_arrow,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


# ================================================================ 图 1-3 品种对比
def fig_instruments():
    fig, ax = plt.subplots(figsize=(13.0, 6.8))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.4))

    ax.text(6.7, 7.05, "品种对比：机制差异直接决定策略与成本", fontsize=13,
            color=DARK, ha="center", weight="bold")

    rows = [
        ("外汇", "周一5:00~周六5:00\n近 24h", "最高\n1:30~1:500", "无统一真实量\ntick 量近似", "流动性最大、点差小", "最主流（FTMO 等）", UP),
        ("期货", "日盘+夜盘", "中等\n保证金制", "真实", "合约标准化\n到期交割", "Topstep/Apex 主流", UP),
        ("股票/指数 CFD", "跟交易所时段", "中等", "部分真实\n底层有交易所数据", "差价合约是衍生品\nPDT/做空限制/财报跳空", "常见", GRAY),
        ("加密货币", "7×24 无休", "高", "真实但分散", "波动最大、易插针", "少数平台", DOWN),
        ("现货黄金", "近 24h", "高", "近似", "避险资产\n与美元负相关", "常见", GRAY),
    ]
    x0, y0 = 0.55, 1.15
    col_w = [1.9, 2.2, 1.9, 2.2, 2.6, 2.0]
    xpos = [x0]
    for w in col_w:
        xpos.append(xpos[-1] + w)
    headers = ["品种", "交易时间", "杠杆", "量真实性", "特点", "Prop 适用"]
    # 表头
    for i, (h, xx) in enumerate(zip(headers, xpos)):
        ax.add_patch(Rectangle((xx, y0 + 4 * 1.05 + 0.28), col_w[i], 0.62,
                               facecolor=DARK, edgecolor=DARK, zorder=3))
        ax.text(xx + col_w[i] / 2, y0 + 4 * 1.05 + 0.59, h, fontsize=10.5,
                color="white", ha="center", va="center", zorder=5, weight="bold")
    # 行
    for r, (name, t1, t2, t3, t4, t5, col) in enumerate(rows):
        ry = y0 + (4 - r) * 1.05
        vals = [name, t1, t2, t3, t4, t5]
        for i, (v, xx) in enumerate(zip(vals, xpos)):
            fc = "white"
            if i == 0:
                fc = "#e8f5e9" if col == UP else ("#ffebee" if col == DOWN else "#f5f5f5")
            ax.add_patch(Rectangle((xx, ry), col_w[i], 1.05, facecolor=fc,
                                   edgecolor="#b0bec5", lw=0.8, zorder=2))
            ax.text(xx + col_w[i] / 2, ry + 0.525, v, fontsize=8.6,
                    color=DARK if i else col, ha="center", va="center", zorder=4,
                    weight="bold" if i == 0 else "normal")

    # 底部推论
    draw_box(ax, 0.55, 0.2, 12.3, 0.75,
             "推论 ① 依赖量价（Wyckoff/订单流）→ 选期货；纯价格行为 → 两者都行  ② prop 考核盘绝大多数是外汇或期货模拟盘——先确认你考的是哪种",
             ec=TEAL, fs=9.3, tc=DARK)

    savefig(fig, "fig_p1_instruments.png")


# ================================================================ 图 1-5 做多做空与合约规格
def fig_longshort_spec():
    fig, ax = plt.subplots(figsize=(13.0, 6.6))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.8, "做多做空与三个计量单位", fontsize=13, color=DARK,
            ha="center", weight="bold")

    # 左：做多 vs 做空
    draw_box(ax, 0.5, 4.2, 3.9, 2.1, "", ec=UP)
    ax.text(2.45, 6.0, "做多（Buy）低买高卖", fontsize=11, color=UP, ha="center", weight="bold")
    ax.text(2.45, 4.75, "先买入 → 等价格涨\n再卖出平仓\n涨了你赚钱", fontsize=9.3, color=DARK, ha="center")
    flow_arrow(ax, 4.45, 5.3, 5.35, 5.3, color=DARK)
    draw_box(ax, 5.4, 4.2, 3.9, 2.1, "", ec=DOWN)
    ax.text(7.35, 6.0, "做空（Sell）先卖后买", fontsize=11, color=DOWN, ha="center", weight="bold")
    ax.text(7.35, 4.75, "先借入卖出 → 等价格跌\n再低价买回还\n跌了你赚钱", fontsize=9.3, color=DARK, ha="center")
    ax.text(6.7, 3.95, "外汇/CFD 天然支持做空，平台自动完成借贷——做空心态坑：信号到了就执行，和做多一视同仁（第 7 章）",
            fontsize=8.8, color=GRAY, ha="center")

    # 中：三个计量单位
    ax.text(6.7, 3.4, "三个计量单位：下单前必须查清平台规格", fontsize=11,
            color=DARK, ha="center", weight="bold")
    units = [
        ("点（Pip）", "外汇最小报价单位\n多数货币对 1 pip = 0.0001\n（日元对 = 0.01）\nEURUSD 1.0850→1.0851 = 1 pip"),
        ("点值（Pip Value）", "1 标准手（100,000 单位）\n每动 1 pip ≈ $10\n（美元计价对）\n盈亏与仓位计算的基础"),
        ("合约乘数", "期货每点值多少钱\n由合约决定：\nES 每点 $50\nNQ 每点 $20，CL 每点 $1000"),
    ]
    ux = 0.7
    for name, desc in units:
        draw_box(ax, ux, 1.55, 3.9, 1.7, "", ec=TEAL)
        ax.text(ux + 1.95, 3.0, name, fontsize=10.5, color=DARK, ha="center", weight="bold")
        ax.text(ux + 1.95, 2.15, desc, fontsize=8.4, color=DARK, ha="center")
        ux += 4.1

    # 底部：算例 + 警示
    draw_box(ax, 0.7, 0.25, 7.2, 0.95, "", ec=UP)
    ax.text(4.3, 0.83, "算例：EURUSD 1.0850 → 1.0890 = 40 pips", fontsize=9.6,
            color=DARK, ha="center", weight="bold")
    ax.text(4.3, 0.42, "1 标准手盈利 = 40 × $10 = $400", fontsize=9.6,
            color=UP, ha="center", weight="bold")
    draw_box(ax, 8.1, 0.25, 4.7, 0.95, "", ec=DOWN)
    ax.text(10.45, 0.83, "点值坑：EURJPY 1 pip = 0.01、微型手缩小 100 倍", fontsize=8.8,
            color=DARK, ha="center")
    ax.text(10.45, 0.45, "这些数字是仓位计算的输入（第 6 章）——查错一个，仓位错一个量级",
            fontsize=8.8, color=DOWN, ha="center", weight="bold")

    savefig(fig, "fig_p1_longshort_spec.png")


if __name__ == "__main__":
    fig_instruments()
    fig_longshort_spec()
    print("批次 68a 第 1 章 2 张图全部生成")
