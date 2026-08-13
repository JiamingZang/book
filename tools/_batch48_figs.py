# -*- coding: utf-8 -*-
"""批次48：P0 补图 4 张
1. fig_p4_state_exit.png     —— 图 4-19 不同市场状态下的出场调整（4.20节）
2. fig_p6_losing_streak.png  —— 图 6-2 连亏是必然，不是意外（6.3节）
3. fig_p6_add_position.png   —— 图 6-7 加仓：新手不宜，盈利才加（6.10节）
4. fig_p6_size_psych.png     —— 图 6-8 "我不在乎"的头寸规模（6.11节）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from draw_handbook_figs import (candle, hl_line, mark, annotate_mark, arrows,
                                style_ax, savefig, UP, DOWN, TEAL, DARK, GRAY, ORANGE)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False


def box(ax, x, y, w, h, text, fc, ec, fs=10.5, tc=DARK, lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                facecolor=fc, edgecolor=ec, lw=lw, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, fontsize=fs, color=tc,
            ha="center", va="center", zorder=4, linespacing=1.5)


def arrow(ax, x0, y0, x1, y1, color=DARK, lw=2.0, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                 arrowstyle="-|>", mutation_scale=16,
                                 color=color, lw=lw, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", zorder=2))


# ============ 图 4-19 不同市场状态下的出场调整 ============
def fig_p4_state_exit():
    fig, ax = plt.subplots(figsize=(12.4, 6.6))
    ax.set_xlim(0, 12.6)
    ax.set_ylim(0, 7.0)

    # 顶部标题
    box(ax, 0.4, 6.4, 11.8, 0.55,
        "出场策略按市场状态调——入场决定胜率下限，出场按状态调整才能把盈利上限最大化",
        "#e8f4f2", TEAL, fs=11)

    # 五状态卡片（3 + 2 布局）
    cards = [
        (0.4, 4.5, "趋势明确\n让利润奔跑\n结构移动止损，不轻易止盈\n（系统一思维）", "#e8f5e9", UP),
        (4.4, 4.5, "区间震荡\n边界止盈，不贪\n区间目标有限\n到中线/边界就落袋（系统二）", "#e3f2fd", "#1e3a6b"),
        (8.4, 4.5, "高波动（ATR 大）\n放宽止损、减小仓位\n目标可放大\n（给价格呼吸空间）", "#fff3e0", ORANGE),
        (2.4, 2.4, "低波动（ATR 小）\n收紧目标\n注意时间止损（不动就走）", "#f3e5f5", "#7b1fa2"),
        (6.4, 2.4, "数据公布前\n收紧止损或减仓\n防黑天鹅打掉利润\n（呼应第 1 章）", "#ffebee", DOWN),
    ]
    for x, y, t, fc, ec in cards:
        box(ax, x, y, 3.7, 1.75, t, fc, ec, fs=10)

    # 底部：期权版出场（进阶）
    box(ax, 0.4, 0.35, 5.8, 1.4,
        "出场工具的另一个维度——期权（进阶）\n保护性 Put = 时间版止损：\n止损会被震荡扫掉，Put 保险持仓还能继续拿",
        "#eceff1", GRAY, fs=9.5)
    box(ax, 6.6, 0.35, 5.8, 1.4,
        "垂直价差 = 下单即物理锁死最大亏损\n（10.6 用途三，适合小资金表达方向）\n出场用价格管理风险，期权用合约管理风险",
        "#eceff1", GRAY, fs=9.5)

    style_ax(ax)
    fig.suptitle("出场不是一刀切：五种市场状态，五种调整", fontsize=12.5, color=DARK, y=0.97)
    savefig(fig, "fig_p4_state_exit.png")


# ============ 图 6-2 连亏是必然，不是意外 ============
def fig_p6_losing_streak():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：资金曲线 + 连亏路径示意 ----
    # 模拟 40% 胜率的资金曲线（先涨一段，再来一段 5 连亏）
    eq = [100, 100.6, 101.3, 100.8, 101.6, 102.4, 101.9, 102.8, 103.6,
          103.0, 102.3, 101.6, 100.9, 100.2, 99.6, 100.3, 101.1,
          100.6, 101.5, 102.3, 101.8, 102.6]
    xs = list(range(len(eq)))
    ax1.plot(xs, eq, color=TEAL, lw=2.2, zorder=4)
    ax1.fill_between(xs, eq, 98, color=TEAL, alpha=0.08, zorder=1)

    # 连亏段高亮（x=9 到 x=14 的 5 连亏）
    ax1.axvspan(8.5, 14.5, color=DOWN, alpha=0.10, zorder=1)
    mark(ax1, 11.5, 99.8, "5 连亏\n（0.6^5 ≈ 7.8%）", dy=0.6, color=DOWN, fs=9.5, box=True)
    mark(ax1, 3, 103.5, "正常波动，不是系统坏了", dy=0.5, color=UP, fs=9.5, box=True)
    # 100 笔周期内几乎必然出现
    annotate_mark(ax1, 11.5, 101.6, "100 笔里至少一段 5 连亏 ≈ 99.9%", 8.0, 104.6,
                  color=ORANGE, fs=9.5, ha="left")

    style_ax(ax1, xlim=(-0.6, 22.6), ylim=(98.5, 105.5))
    ax1.set_title("连亏路径：40% 胜率系统里的正常样子", fontsize=11.5, color=DARK, pad=8)

    # ---- 右：正确 vs 错误反应 ----
    style_ax(ax2, xlim=(0, 6.2), ylim=(0, 6.6))
    ax2.set_title("连亏来了，你怎么反应", fontsize=11.5, color=DARK, pad=8)
    box(ax2, 0.5, 5.0, 5.2, 1.3,
        "最常见的死法（错误）：\n连亏 → 怀疑系统坏了 →\n临场改规则/改仓位 → 放弃正期望系统",
        "#ffebee", DOWN, fs=9.5)
    box(ax2, 0.5, 2.9, 5.2, 1.5,
        "正确的预期（正确）：\n连亏一定会来 → \"又来了\" →\n按计划继续 → 概率迟早兑现\n（0.5% 风险保证你不会出局）",
        "#e8f5e9", UP, fs=9.5)
    box(ax2, 0.5, 0.6, 5.2, 1.5,
        "核心：连亏不是系统坏了，是概率的正常样子。\n问题不是\"怎么避免连亏\"，\n而是\"连亏时你的仓位能不能扛过去\"",
        "#e8f4f2", TEAL, fs=9.5)
    arrow(ax2, 3.1, 5.0, 3.1, 4.4)
    arrow(ax2, 3.1, 2.9, 3.1, 2.1)

    fig.suptitle("连亏是必然：没有心理准备的第一次 5 连亏，会让你放弃一个本来正期望值的系统",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p6_losing_streak.png")


# ============ 图 6-7 加仓：新手不宜，盈利才加 ============
def fig_p6_add_position():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：盈利加仓 vs 浮亏摊平 ----
    # 上半：盈利加仓（K 线上升，加仓点标注）
    seq_up = [
        (0, 100, 102, 99.5, 101.5),
        (1, 101.5, 103.5, 101.0, 103.2),
        (2, 103.2, 105.0, 102.8, 104.6),   # 突破确认
        (3, 104.6, 105.6, 103.4, 104.0),   # 回调
        (4, 104.0, 106.8, 103.8, 106.4),   # 加仓点（盈利）
        (5, 106.4, 108.2, 106.0, 107.8),
        (6, 107.8, 109.8, 107.4, 109.4),   # 加仓 2
    ]
    for x, o, h, l, c in seq_up:
        candle(ax1, x, o, h, l, c, width=0.55)
    hl_line(ax1, -0.5, 7.2, 104.6, color=UP, ls="--", lw=1.2, label="突破确认")
    mark(ax1, 4, 106.4, "盈利加仓\n止损上移", dy=0.7, color=UP, fs=9, box=True)
    mark(ax1, 6, 109.4, "再确认再加", dy=0.7, color=UP, fs=9, box=True)

    # 下半：浮亏摊平（K 线下跌，越加越套）
    seq_dn = [
        (0, 106, 107, 104.5, 105.2),   # 入场
        (1, 105.2, 106, 103.8, 104.2), # 浮亏
        (2, 104.2, 105, 102.6, 103.0), # 加仓（错）
        (3, 103.0, 103.8, 101.4, 101.8),
        (4, 101.8, 102.6, 100.2, 100.6), # 再加（错）
        (5, 100.6, 101.4, 99.0, 99.4),
        (6, 99.4, 100.2, 97.8, 98.2),   # 深套
    ]
    for x, o, h, l, c in seq_dn:
        candle(ax1, x + 0.0, o, h, l, c, width=0.55)
    hl_line(ax1, -0.5, 7.2, 105.2, color=TEAL, ls=":", lw=1.1, label="入场 105.2")
    mark(ax1, 2, 103.0, "浮亏加仓\n（摊平）", dy=-1.0, color=DOWN, fs=9, box=True)
    mark(ax1, 4, 100.6, "越加越套", dy=-1.2, color=DOWN, fs=9, box=True)
    mark(ax1, 6, 98.2, "小亏变深套", dy=-1.2, color=DOWN, fs=9, box=True)

    style_ax(ax1, xlim=(-0.8, 7.6), ylim=(96, 112))
    ax1.set_title("盈利加仓（上）vs 浮亏摊平（下）：数学是灾难", fontsize=11.5, color=DARK, pad=8)

    # ---- 右：三边界 ----
    style_ax(ax2, xlim=(0, 6.2), ylim=(0, 6.6))
    ax2.set_title("Al Brooks 给加仓画的三条边界", fontsize=11.5, color=DARK, pad=8)
    box(ax2, 0.5, 5.0, 5.2, 1.2,
        "① 新手不做\n加仓要求精确判断\"前提仍有效\"\n新手最常把反转当回调", "#ffebee", DOWN, fs=9.5)
    box(ax2, 0.5, 3.4, 5.2, 1.2,
        "② 只加 1-2 次，且要有完整计划\n加几次/间隔/大小/退出\n计划外的加仓叫摊平", "#fff3e0", ORANGE, fs=9.5)
    box(ax2, 0.5, 1.8, 5.2, 1.2,
        "③ 浮亏不加，盈利才加\n只在突破继续、趋势确认时加\n并上移止损保护已实现利润", "#e8f5e9", UP, fs=9.5)
    box(ax2, 0.5, 0.3, 5.2, 1.0,
        "考核期结论：完全不加仓（军规第 7 条）\n目标先活下来；实盘稳定后再写进规则书", "#e8f4f2", TEAL, fs=9.5)

    fig.suptitle("加仓是把双刃剑：用得好让利润奔跑（海龟），用得差是爆仓加速器",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p6_add_position.png")


# ============ 图 6-8 "我不在乎"的头寸规模 ============
def fig_p6_size_psych():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：执行变形的根源 ----
    style_ax(ax1, xlim=(0, 6.2), ylim=(0, 6.6))
    ax1.set_title("执行变形的根源：这笔亏了会很痛", fontsize=11.5, color=DARK, pad=8)
    box(ax1, 0.5, 5.2, 5.2, 1.1,
        "怕痛\n（仓位太大 → 情绪燃料）", "#ffebee", DOWN, fs=10)
    box(ax1, 0.5, 3.4, 5.2, 1.1,
        "提前止盈\n（赚一点就跑，吃不到趋势）", "#fff3e0", ORANGE, fs=10)
    box(ax1, 0.5, 1.9, 5.2, 1.1,
        "止损犹豫\n（该走不走，小亏变大亏）", "#fff3e0", ORANGE, fs=10)
    box(ax1, 0.5, 0.4, 5.2, 1.1,
        "报复加仓\n（想一把捞回来，越陷越深）", "#ffebee", DOWN, fs=10)
    arrow(ax1, 3.1, 5.2, 3.1, 4.5)
    arrow(ax1, 3.1, 3.4, 3.1, 3.0)
    arrow(ax1, 3.1, 1.9, 3.1, 1.5)

    # ---- 右：仓位解 ----
    style_ax(ax2, xlim=(0, 6.2), ylim=(0, 6.6))
    ax2.set_title("仓位解：小到\"我不在乎\"", fontsize=11.5, color=DARK, pad=8)
    box(ax2, 0.5, 5.2, 5.2, 1.1,
        "常规仓位再减 50%-75% 做训练仓\n（模拟期/考核前期尤其如此）", "#e8f5e9", UP, fs=10)
    box(ax2, 0.5, 3.7, 5.2, 1.1,
        "亏了也不影响心情\n情绪的燃料消失 → 能做正确的事", "#e8f5e9", UP, fs=10)
    box(ax2, 0.5, 2.2, 5.2, 1.1,
        "执行一致本身就是最大的优势来源\n不是赚得少，是先保证做得对", "#e8f4f2", TEAL, fs=10)
    box(ax2, 0.5, 0.5, 5.2, 1.2,
        "焦虑是信号，不是性格缺陷：\n先找原因——仓位太大？逆势单？\n执行率稳定后再逐步放大\n放大的是权益，不是胆量", "#fff3e0", ORANGE, fs=9.5)
    arrow(ax2, 3.1, 5.2, 3.1, 4.8)
    arrow(ax2, 3.1, 3.7, 3.1, 3.3)
    arrow(ax2, 3.1, 2.2, 3.1, 1.7)

    fig.suptitle("\"我不在乎\"的头寸规模：心理问题往往有仓位解",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p6_size_psych.png")


if __name__ == "__main__":
    fig_p4_state_exit()
    fig_p6_losing_streak()
    fig_p6_add_position()
    fig_p6_size_psych()
    print("批次48 四张图生成完成")
