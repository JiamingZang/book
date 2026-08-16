# -*- coding: utf-8 -*-
"""给无图小节补教学示意图：1.12 / 5.9 / 6.6 / 8.13 / 10.7 / 10.9"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from draw_handbook_figs import (
    candle, style_ax, mark, annotate_mark, hl_line, savefig,
    UP, DOWN, TEAL, DARK, GRAY, ORANGE,
)
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "Droid Sans Fallback", "sans-serif"]

OUT = os.path.join("handbook", "images")


def fig_forex_structure():
    """1.12 外汇：为什么量不真实、点差是主要成本"""
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2))
    # 左：OTC 无中央账本 → tick 量近似
    ax = axes[0]
    style_ax(ax, xlim=(-0.5, 10.5), ylim=(0, 10))
    # 三个做市商节点
    for x, y in [(1.5, 7), (5, 5), (8.5, 7.5)]:
        ax.add_patch(plt.Circle((x, y), 0.75, fc="white", ec=TEAL, lw=1.6, zorder=3))
    ax.text(1.5, 7, "银行A", ha="center", va="center", fontsize=10, color=DARK, zorder=4)
    ax.text(5, 5, "银行B", ha="center", va="center", fontsize=10, color=DARK, zorder=4)
    ax.text(8.5, 7.5, "ECN", ha="center", va="center", fontsize=10, color=DARK, zorder=4)
    ax.plot([2.3, 4.2], [6.9, 5.4], color=GRAY, lw=1.2, zorder=1)
    ax.plot([5.8, 7.6], [5.4, 7.2], color=GRAY, lw=1.2, zorder=1)
    ax.plot([2.3, 7.6], [7.2, 7.4], color=GRAY, lw=1.2, zorder=1)
    ax.text(5, 8.8, "外汇 = 无数做市商各自报价的 OTC 市场", fontsize=12, color=DARK, ha="center", fontweight="bold")
    ax.text(5, 1.2, "没有中央撮合 → 没有统一成交量账本\n你看到的 tick 量只是“报价跳动次数”，不是真实成交吨位", fontsize=11, color=DARK, ha="center", va="center", bbox=dict(boxstyle="round,pad=0.4", fc="#f5f7fa", ec=GRAY, lw=1))
    ax.set_title("① 为什么“量不真实”", fontsize=12, color=DARK)
    # 右：点差 = 固定成本，频率越高侵蚀越重
    ax = axes[1]
    style_ax(ax, xlim=(0, 10), ylim=(0, 10))
    xs = np.arange(1, 10)
    cost_scalp = 0.35 + 0.09 * xs
    cost_swing = 0.12 + 0.02 * xs
    ax.bar(xs - 0.2, cost_scalp, width=0.35, color=DOWN, alpha=0.85, label="刮头皮（交易频率高）")
    ax.bar(xs + 0.2, cost_swing, width=0.35, color=UP, alpha=0.85, label="波段（交易频率低）")
    ax.set_xticks(xs)
    ax.set_xticklabels([f"第{i}笔" for i in xs], fontsize=8)
    ax.set_yticks([])
    ax.set_ylim(0, 1.5)
    ax.legend(fontsize=9, loc="upper left", frameon=False)
    ax.text(5, 9.2, "点差是每笔固定成本：同一套信号，频率越高成本累积越快", fontsize=11, color=DARK, ha="center", fontweight="bold")
    ax.text(5, 0.7, "止损越近，点差占风险比例越高——\nexotic 点差大 = 把窄止损的盈亏比吃穿", fontsize=11, color=DARK, ha="center", va="bottom", bbox=dict(boxstyle="round,pad=0.4", fc="#f5f7fa", ec=GRAY, lw=1))
    ax.set_title("② 为什么点差是主要成本", fontsize=12, color=DARK)
    fig.suptitle("外汇要点：没有中央账本 → 量只能当参考；没有手续费 → 成本主要是点差，频率越高越致命", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p1_forex_structure.png")


def fig_verify_narrative():
    """5.9 验证心态：事后叙事 vs 事前规则"""
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2))
    # 左：事后叙事
    ax = axes[0]
    style_ax(ax, xlim=(0, 10), ylim=(0, 10))
    for x, y in [(1, 8.5), (4, 8.5), (7, 8.5), (9.5, 8.5)]:
        ax.add_patch(plt.Circle((x, y), 0.45, fc="white", ec=GRAY, lw=1.4, zorder=3))
    ax.text(1, 8.5, "先有结果", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    ax.text(4, 8.5, "再找理由", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    ax.text(7, 8.5, "讲成故事", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    ax.text(9.5, 8.5, "下次照做", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    for x0, x1 in [(1.5, 3.5), (4.5, 6.5), (7.5, 9.0)]:
        ax.annotate("", xy=(x1, 8.5), xytext=(x0, 8.5), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.3))
    ax.text(5, 4.5, "问题：每一笔都能事后编出理由\n但下一笔开仓时你仍然不知道\n该依据什么——复盘变成自我感动", fontsize=11, color=DOWN, ha="center", va="center", bbox=dict(boxstyle="round,pad=0.5", fc="#fff5f5", ec=DOWN, lw=1.2))
    ax.text(5, 9.4, "事后叙事：结果 → 理由 → 故事", fontsize=12, color=DOWN, ha="center", fontweight="bold")
    ax.set_title("① 事后叙事（复盘陷阱）", fontsize=12, color=DARK)
    # 右：事前规则
    ax = axes[1]
    style_ax(ax, xlim=(0, 10), ylim=(0, 10))
    for x, y in [(1, 8.5), (4, 8.5), (7, 8.5), (9.5, 8.5)]:
        ax.add_patch(plt.Circle((x, y), 0.45, fc="white", ec=UP, lw=1.6, zorder=3))
    ax.text(1, 8.5, "先写条件", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    ax.text(4, 8.5, "按条件执行", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    ax.text(7, 8.5, "记录结果", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    ax.text(9.5, 8.5, "统计修正", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
    for x0, x1 in [(1.5, 3.5), (4.5, 6.5), (7.5, 9.0)]:
        ax.annotate("", xy=(x1, 8.5), xytext=(x0, 8.5), arrowprops=dict(arrowstyle="->", color=UP, lw=1.3))
    ax.text(5, 4.5, "条件在结果之前写下，执行不因盈亏改变\n100 笔后统计的是“规则”而不是“故事”\n——这才是第 8 章验证闭环的起点", fontsize=11, color=UP, ha="center", va="center", bbox=dict(boxstyle="round,pad=0.5", fc="#f2fbf7", ec=UP, lw=1.2))
    ax.text(5, 9.4, "事前规则：条件 → 执行 → 统计 → 修正", fontsize=12, color=UP, ha="center", fontweight="bold")
    ax.set_title("② 事前规则（可验证闭环）", fontsize=12, color=DARK)
    fig.suptitle("验证心态：同样一笔交易，事后叙事让你自我感动，事前规则让你积累可统计的样本", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p5_verify_narrative.png")


def fig_cost_erosion():
    """6.6 成本：点差/滑点/隔夜利息如何侵蚀期望值"""
    fig, ax = plt.subplots(figsize=(13, 6.2))
    style_ax(ax, xlim=(0, 10), ylim=(0, 10))
    # 期望值柱状：毛期望 vs 扣除三种成本后的净期望
    cats = ["毛期望", "扣点差", "扣滑点", "扣隔夜", "净期望"]
    vals = [5.0, 4.1, 3.4, 2.9, 2.6]
    colors = [TEAL, ORANGE, ORANGE, ORANGE, DOWN]
    bars = ax.bar(np.arange(len(cats)), vals, width=0.55, color=colors, alpha=0.9, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.12, f"{v:.1f}", ha="center", fontsize=11, color=DARK, fontweight="bold")
    ax.set_xticks(np.arange(len(cats)))
    ax.set_xticklabels(cats, fontsize=11)
    ax.set_yticks([])
    ax.set_ylim(0, 6.2)
    ax.axhline(0, color=GRAY, lw=1)
    ax.text(4.5, 9.3, "成本不是“小钱”，是每笔都从期望值里扣的固定项", fontsize=12.5, color=DARK, ha="center", fontweight="bold")
    ax.text(4.5, 0.6, "高频/窄止损交易对成本最敏感：同样的信号，点差占比高 → 净期望可能由正转负\n隔夜利息是持仓成本；滑点在数据/流动性差时不是理论值，是真实成交价差", fontsize=11, color=DARK, ha="center", bbox=dict(boxstyle="round,pad=0.4", fc="#f5f7fa", ec=GRAY, lw=1))
    ax.set_title("成本侵蚀期望值：毛期望 − 点差 − 滑点 − 隔夜 = 你真正拿到的期望值", fontsize=12, color=DARK)
    savefig(fig, "fig_p6_cost_erosion.png")


def fig_tick_chart():
    """8.13 Tick 图：时间图 vs Tick 图；TX-D 触及 vs 收盘"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.3), gridspec_kw={"width_ratios": [1.5, 1]})
    # 左：同一段行情在时间图与 Tick 图上的不同观感
    ax = axes[0]
    style_ax(ax, xlim=(-0.8, 18), ylim=(94, 108))
    # 时间图：横盘时段占很多K，但成交量小
    k_time = [(0, 99.5, 100.6, 99.1, 100.2), (1, 100.2, 100.7, 99.5, 99.9), (2, 99.9, 100.8, 99.4, 100.4),
              (3, 100.4, 101, 99.8, 100.2), (4, 100.2, 101.5, 100, 101.3), (5, 101.3, 103.2, 101, 103),
              (6, 103, 105.6, 102.8, 105.4), (7, 105.4, 107.2, 105.2, 107)]
    for i, (x, o, h, l, c) in enumerate(k_time):
        candle(ax, x, o, h, l, c, width=0.55)
    # 用灰框表示时间图上的“无聊横盘”对应大段时间
    ax.add_patch(plt.Rectangle((-0.5, 98.8), 4.5, 1.7, fill=False, ec=GRAY, lw=1.2, ls="--", zorder=1))
    ax.text(2, 101.6, "时间图：这段横盘\n占了 4 根 K 线", fontsize=9.5, color=GRAY, ha="center")
    ax.text(9, 108.5, "同一段行情，时间图看“磨蹭”", fontsize=11.5, color=DARK, ha="center", fontweight="bold")
    ax.set_title("① 时间图：K 线按时间等分，横盘也占K线", fontsize=11, color=DARK)
    # 右半：Tick 图压缩横盘、放大活跃
    ax = axes[1]
    style_ax(ax, xlim=(-0.8, 11), ylim=(94, 108))
    k_tick = [(0, 100.4, 101.5, 100, 101.3), (1, 101.3, 103.2, 101, 103), (2, 103, 105.6, 102.8, 105.4), (3, 105.4, 107.2, 105.2, 107)]
    for i, (x, o, h, l, c) in enumerate(k_tick):
        candle(ax, x, o, h, l, c, width=0.6)
    ax.text(1.5, 108.5, "Tick 图：按成交笔数切 K 线，\n横盘被压缩、活跃段被拉长", fontsize=10, color=UP, ha="center", fontweight="bold")
    ax.text(1.5, 96.2, "大成交量时 K 线多、走得快\n小成交量时 K 线少、走得慢\n——把“失衡持续了多久”摊开", fontsize=9.5, color=DARK, ha="center", bbox=dict(boxstyle="round,pad=0.4", fc="#f5f7fa", ec=UP, lw=1))
    ax.set_title("② Tick 图：横盘被压缩，失衡被放大", fontsize=11, color=DARK)
    fig.suptitle("Tick 图：把时间轴换成成交笔数——你不再问“过了多久”，而是问“同样的成交量里，失衡有没有持续”", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p8_tick_chart.png")


def fig_options_coord():
    """10.7 期权放回全书坐标"""
    fig, ax = plt.subplots(figsize=(13, 6.5))
    style_ax(ax, xlim=(-1, 11), ylim=(-1, 8))
    # 中心：价格行为观点
    ax.add_patch(plt.Rectangle((3.8, 2.8), 2.4, 1.8, fc="#e8f0fe", ec=TEAL, lw=2, zorder=3))
    ax.text(5, 3.7, "观点来自价格行为\n（第 2-5 章）", ha="center", va="center", fontsize=11.5, color=DARK, fontweight="bold", zorder=4)
    # 四个角：方向/风险/波动/时间
    nodes = [
        (0.5, 6.5, "方向\n表达载体", TEAL, "第 4 章"),
        (9.5, 6.5, "风险\n锁死/对冲", ORANGE, "第 6 章"),
        (9.5, 0.5, "波动率\nIV/VIX", DOWN, "第 10.5"),
        (0.5, 0.5, "时间\nTheta/到期", GRAY, "第 10.4"),
    ]
    for x, y, t, c, ref in nodes:
        ax.add_patch(plt.Circle((x, y), 1.15, fc="white", ec=c, lw=1.8, zorder=3))
        ax.text(x, y + 0.2, t.split("\n")[0], ha="center", va="center", fontsize=11, color=c, fontweight="bold", zorder=4)
        ax.text(x, y - 0.35, t.split("\n")[1] if len(t.split("\n")) > 1 else "", ha="center", va="center", fontsize=9, color=DARK, zorder=4)
        ax.text(x, y - 1.0, ref, ha="center", va="center", fontsize=9, color=GRAY, zorder=4)
    for (x0, y0), (x1, y1) in [((0.5, 6.5), (3.8, 3.7)), ((9.5, 6.5), (6.2, 3.7)), ((9.5, 0.5), (6.2, 3.7)), ((0.5, 0.5), (3.8, 3.7))]:
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2, connectionstyle="arc3,rad=0.15"))
    ax.text(5, 7.4, "期权不改变观点，只改变观点的成本、风险与收益形状", fontsize=13, color=DARK, ha="center", fontweight="bold")
    ax.text(5, -0.4, "本书坐标：方向来自价格行为，期权负责把风险/波动/时间三个维度变成可管理的工具", fontsize=10.5, color=GRAY, ha="center")
    savefig(fig, "fig_p10_options_coord.png")


def fig_brooks_options():
    """10.9 Brooks 的期权极简主义"""
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2))
    # 左：极简工具树
    ax = axes[0]
    style_ax(ax, xlim=(-1, 11), ylim=(0, 10))
    ax.add_patch(plt.Rectangle((3.4, 7.6), 3.2, 1.8, fc="#e8f0fe", ec=TEAL, lw=2, zorder=3))
    ax.text(5, 8.5, "价格行为\n（第 2-3 章）", ha="center", va="center", fontsize=11, color=DARK, fontweight="bold", zorder=4)
    for y, t in [(4.9, "看涨 → 买 Call / Call 价差"), (2.3, "看跌 → 买 Put / Put 价差")]:
        ax.add_patch(plt.Rectangle((1.2, y), 7.6, 1.3, fc="white", ec=UP if "涨" in t else DOWN, lw=1.6, zorder=3))
        ax.text(5, y + 0.65, t, ha="center", va="center", fontsize=11, color=DARK, zorder=4)
    ax.annotate("", xy=(5, 7.6), xytext=(5, 6.3), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4))
    ax.annotate("", xy=(3.5, 4.9), xytext=(3.5, 3.6), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4))
    ax.text(5, 1.0, "只用最简单工具：Call/Put/价差\n不碰复杂结构——注意力留给图表", fontsize=10.5, color=DARK, ha="center", bbox=dict(boxstyle="round,pad=0.4", fc="#f5f7fa", ec=GRAY, lw=1))
    ax.set_title("① Brooks 的极简工具", fontsize=12, color=DARK)
    # 右：为什么隔夜用期权
    ax = axes[1]
    style_ax(ax, xlim=(0, 10), ylim=(0, 10))
    ax.add_patch(plt.Rectangle((0.6, 6.8), 8.8, 2.6, fc="#fff8e1", ec=ORANGE, lw=1.6, zorder=2))
    ax.text(5, 8.6, "隔夜持仓：裸期货/股票 = 跳空风险全暴露", fontsize=11.5, color=DOWN, ha="center", fontweight="bold", zorder=3)
    ax.text(5, 7.6, "买入期权 = 最大亏损锁死在权利金，跳空也伤不到更多", fontsize=11, color=DARK, ha="center", zorder=3)
    ax.annotate("", xy=(5, 6.8), xytext=(5, 5.6), arrowprops=dict(arrowstyle="->", color=UP, lw=1.6))
    ax.add_patch(plt.Rectangle((0.6, 2.0), 8.8, 3.0, fc="#f2fbf7", ec=UP, lw=1.6, zorder=2))
    ax.text(5, 4.4, "入场判断完全来自价格行为", fontsize=11.5, color=UP, ha="center", fontweight="bold", zorder=3)
    ax.text(5, 3.2, "不需要懂复杂希腊字母/策略——它们只会分散你对图表的注意力", fontsize=10.5, color=DARK, ha="center", zorder=3)
    ax.text(5, 0.8, "结论：理解层（IV/希腊字母）用来避坑，执行层保持极简", fontsize=11, color=DARK, ha="center", fontweight="bold")
    ax.set_title("② 为什么隔夜用期权", fontsize=12, color=DARK)
    fig.suptitle("Al Brooks 的期权观：价格行为是所有交易的基础，期权只是表达观点的载体——理解可以深，工具必须简单", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p10_brooks_options.png")


if __name__ == "__main__":
    fig_forex_structure()
    fig_verify_narrative()
    fig_cost_erosion()
    fig_tick_chart()
    fig_options_coord()
    fig_brooks_options()
    print("全部新图完成")


def fig_temperament():
    """1.9 品种脾气：波动/时段/成本/量真假"""
    fig, ax = plt.subplots(figsize=(13, 6.5))
    style_ax(ax, xlim=(-1, 11), ylim=(0, 10))
    cats = [("外汇", "点差/隔夜", "tick 量", "伦敦纽约", "波动中等"),
            ("期货", "佣金", "真实量", "开盘/美盘", "波动大"),
            ("股票", "佣金+税", "真实量", "9:30-16:00", "波动中"),
            ("加密", "资金费率", "各所分散", "7×24", "波动极大"),
            ("黄金", "点差", "OTC tick", "纽约", "波动中")]
    for i, (name, cost, vol, sess, wav) in enumerate(cats):
        x = 1 + i * 2
        ax.add_patch(plt.Rectangle((x-0.7, 1.0), 1.4, 8.0, fc="#f5f7fa", ec=GRAY, lw=1.0, zorder=1))
        ax.text(x, 8.6, name, ha="center", fontsize=13, color=DARK, fontweight="bold", zorder=3)
        ax.text(x, 7.4, f"成本：{cost}", ha="center", fontsize=9.5, color=DOWN, zorder=3)
        ax.text(x, 6.2, f"量：{vol}", ha="center", fontsize=9.5, color=TEAL, zorder=3)
        ax.text(x, 5.0, f"时段：{sess}", ha="center", fontsize=9.5, color=GRAY, zorder=3)
        ax.text(x, 3.8, f"波动：{wav}", ha="center", fontsize=9.5, color=ORANGE, zorder=3)
    ax.text(5, 9.4, "品种脾气 = 波动尺度 × 活跃时段 × 成本结构 × 量是否真实", fontsize=13, color=DARK, ha="center", fontweight="bold")
    ax.text(5, 0.4, "同一套价格行为，放在不同品种上执行细节完全不同——选品种是系统设计的一部分，不是随便挑一个", fontsize=11, color=GRAY, ha="center")
    savefig(fig, "fig_p1_temperament.png")


def fig_stock_short():
    """1.11 股票做空限制"""
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2))
    # 左：做空流程
    ax = axes[0]
    style_ax(ax, xlim=(0, 10), ylim=(0, 10))
    steps = ["借券", "卖出", "等待跌", "买回归还"]
    for i, s in enumerate(steps):
        x = 1 + i * 2.6
        ax.add_patch(plt.Circle((x, 5), 0.9, fc="white", ec=TEAL, lw=1.6, zorder=3))
        ax.text(x, 5, s, ha="center", va="center", fontsize=10.5, color=DARK, zorder=4)
        if i < len(steps)-1:
            ax.annotate("", xy=(x+1.6, 5), xytext=(x+0.95, 5), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4))
    ax.text(5, 8.8, "做空流程：先借券才能卖——不是想卖就能卖", fontsize=11.5, color=DARK, ha="center", fontweight="bold")
    ax.text(5, 1.5, "借不到券 = 无法做空\n这是股票和外汇/期货最大的结构性差异", fontsize=10.5, color=DOWN, ha="center", bbox=dict(boxstyle="round,pad=0.4", fc="#fff5f5", ec=DOWN, lw=1.2))
    ax.set_title("① 做空要先借券", fontsize=12, color=DARK)
    # 右：Rule 201
    ax = axes[1]
    style_ax(ax, xlim=(0, 10), ylim=(0, 10))
    ax.add_patch(plt.Rectangle((0.6, 6.5), 8.8, 2.5, fc="#fff8e1", ec=ORANGE, lw=1.6, zorder=2))
    ax.text(5, 8.2, "Rule 201：单日跌幅达 10% 后", fontsize=12, color=DOWN, ha="center", fontweight="bold", zorder=3)
    ax.text(5, 7.2, "限制对该股票追加卖空——不是“价格下跌时一律不能追空”", fontsize=10.5, color=DARK, ha="center", zorder=3)
    ax.annotate("", xy=(5, 6.5), xytext=(5, 5.4), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4))
    ax.add_patch(plt.Rectangle((0.6, 2.2), 8.8, 3.0, fc="#f2fbf7", ec=UP, lw=1.6, zorder=2))
    ax.text(5, 4.4, "触发的是“限制追加卖空”", fontsize=11, color=UP, ha="center", fontweight="bold", zorder=3)
    ax.text(5, 3.2, "已经持有的空单不受影响\n极端行情里的流动性保护，不是做空禁令", fontsize=10, color=DARK, ha="center", zorder=3)
    ax.text(5, 0.8, "如果你主要做空，股票不是好战场——外汇/期货做空更自由", fontsize=11, color=DARK, ha="center", fontweight="bold")
    ax.set_title("② Rule 201 的真实含义", fontsize=12, color=DARK)
    fig.suptitle("股票做空：借券门槛 + 触发式卖空限制——结构性约束决定它不适合做空主线", fontsize=12.5, color=DARK, y=0.99)
    savefig(fig, "fig_p1_stock_short.png")


def fig_choose_instrument():
    """1.15 选品种决策树"""
    fig, ax = plt.subplots(figsize=(13, 6.5))
    style_ax(ax, xlim=(-1, 11), ylim=(0, 12))
    # root
    ax.add_patch(plt.Rectangle((3.4, 10.2), 3.2, 1.4, fc="#e8f0fe", ec=TEAL, lw=2, zorder=3))
    ax.text(5, 10.9, "先问目标", ha="center", va="center", fontsize=12, color=DARK, fontweight="bold", zorder=4)
    # level1
    for x, t in [(1.2, "考期货 prop"), (5, "考外汇 prop"), (8.8, "实盘/波段")]:
        ax.add_patch(plt.Rectangle((x-1.1, 7.4), 2.2, 1.3, fc="white", ec=GRAY, lw=1.5, zorder=3))
        ax.text(x, 8.05, t, ha="center", va="center", fontsize=10, color=DARK, zorder=4)
        ax.annotate("", xy=(x, 7.4), xytext=(5, 10.2), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2, connectionstyle="arc3,rad=0.1"))
    # level2
    for x, t in [(1.2, "ES / NQ"), (5, "EURUSD 等主流对"), (8.8, "股指/商品/黄金")]:
        ax.add_patch(plt.Rectangle((x-1.1, 4.4), 2.2, 1.3, fc="#f2fbf7", ec=UP, lw=1.5, zorder=3))
        ax.text(x, 5.05, t, ha="center", va="center", fontsize=10, color=DARK, zorder=4)
        ax.annotate("", xy=(x, 5.7), xytext=(x, 7.4), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
    # final
    ax.add_patch(plt.Rectangle((2.4, 1.2), 5.2, 1.5, fc="#fff8e1", ec=ORANGE, lw=1.8, zorder=3))
    ax.text(5, 1.95, "再匹配：周期（日内/波段）× 方法（量价/纯PA）× 波动承受", ha="center", va="center", fontsize=10.5, color=DARK, fontweight="bold", zorder=4)
    for x in [1.2, 5, 8.8]:
        ax.annotate("", xy=(5, 2.7), xytext=(x, 4.4), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0, connectionstyle="arc3,rad=0.12"))
    ax.text(5, 11.4, "选品种决策：目标 → 周期 → 方法 → 波动承受", fontsize=13, color=DARK, ha="center", fontweight="bold")
    ax.text(5, -0.1, "新手先聚焦单一品种：一个品种的 1000 小时，比十个品种各 100 小时有效得多", fontsize=10.5, color=GRAY, ha="center")
    savefig(fig, "fig_p1_choose_instrument.png")


if __name__ == "__main__":
    fig_forex_structure()
    fig_verify_narrative()
    fig_cost_erosion()
    fig_tick_chart()
    fig_options_coord()
    fig_brooks_options()
    fig_temperament()
    fig_stock_short()
    fig_choose_instrument()
    print("全部新图完成")
