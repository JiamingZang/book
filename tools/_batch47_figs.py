# -*- coding: utf-8 -*-
"""批次47：第4章 P0 补图 5 张概念图
1. fig_p4_two_modes.png    —— 图 4-10 市场的两种模式：趋势跟踪 vs 均值回归（4.10节）
2. fig_p4_tharp.png        —— 图 4-11 Van Tharp 系统开发框架：系统要合身（4.11节）
3. fig_p4_scale_out.png    —— 图 4-12 分批止盈：三种结局（4.14节）
4. fig_p4_breakeven.png    —— 图 4-13 保本时机：别移太早（4.16节）
5. fig_p4_time_stop.png    —— 图 4-14 时间止损：不动也是风险（4.17节）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.gridspec import GridSpec

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


# ============ 图 4-10 市场的两种模式：趋势跟踪 vs 均值回归 ============
def fig_p4_two_modes():
    fig = plt.figure(figsize=(12.4, 7.4))
    gs = GridSpec(3, 2, height_ratios=[1.1, 4.4, 1.2], width_ratios=[1, 1],
                  hspace=0.55, wspace=0.16)
    axt = fig.add_subplot(gs[0, :])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[2, 1])

    # ---- 左：趋势市 → 趋势跟踪 ----
    seq = [
        (0, 100, 102, 99.5, 101.5),
        (1, 101.5, 103.5, 100.5, 102.8),
        (2, 102.8, 104.8, 102.2, 104.2),   # HH
        (3, 104.2, 105.0, 102.6, 103.4),   # 回调（HL）
        (4, 103.4, 106.2, 102.9, 105.8),   # 回调买入 → 新 HH
        (5, 105.8, 107.2, 104.8, 106.8),
        (6, 106.8, 108.8, 106.2, 108.2),   # HH
        (7, 108.2, 109.0, 106.8, 107.6),   # 回调（HL）
        (8, 107.6, 110.4, 107.1, 109.9),   # 回调买入
        (9, 109.9, 111.5, 109.0, 111.0),
    ]
    for x, o, h, l, c in seq:
        candle(ax1, x, o, h, l, c, width=0.55)

    # 200 均线（上升虚线）——方向过滤器
    ma = [99.5, 100.4, 101.4, 102.1, 103.0, 104.0, 105.2, 106.3, 107.5, 108.7]
    ax1.plot(range(10), ma, color=ORANGE, lw=2.2, ls="-", zorder=4)
    mark(ax1, 9, ma[-1], "200 均线：上方只做多", dy=0.7, color=ORANGE, fs=9, ha="right")

    # 回调买入点
    mark(ax1, 3, 103.4, "回调到 HL\n顺势买入", dy=0.9, color=UP, fs=9.5, box=True)
    mark(ax1, 7, 107.6, "回调买入", dy=0.9, color=UP, fs=9.5, box=True)
    hl_line(ax1, 2.5, 3.2, 103.4, color=GRAY, ls=":", lw=1.0)

    style_ax(ax1, xlim=(-0.8, 10.6), ylim=(97.5, 114))
    ax1.set_title("趋势市 → 趋势跟踪（假设趋势延续）", fontsize=11.5, color=DARK, pad=8)

    # ---- 右：区间市 → 均值回归 ----
    seq2 = [
        (0, 105.2, 107.0, 104.6, 106.6),
        (1, 106.6, 107.4, 105.4, 105.8),
        (2, 105.8, 106.9, 104.9, 105.4),   # 下沿
        (3, 105.4, 107.0, 105.0, 106.6),   # 下沿买入
        (4, 106.6, 108.0, 106.2, 107.4),   # 上沿
        (5, 107.4, 108.1, 105.6, 106.0),   # 上沿做空
        (6, 106.0, 107.2, 105.3, 106.8),
        (7, 106.8, 108.0, 106.4, 107.6),   # 上沿
        (8, 107.6, 108.2, 105.7, 106.1),   # 上沿做空
        (9, 106.1, 107.3, 105.4, 106.9),
    ]
    for x, o, h, l, c in seq2:
        candle(ax2, x, o, h, l, c, width=0.55)

    hl_line(ax2, -0.5, 10.2, 108.0, color=GRAY, ls="--", lw=1.3, label="区间上沿")
    hl_line(ax2, -0.5, 10.2, 105.3, color=GRAY, ls="--", lw=1.3, label="区间下沿")
    mark(ax2, 5, 107.6, "上沿做空", dy=0.7, color=DOWN, fs=9.5, box=True)
    mark(ax2, 8, 107.7, "上沿做空", dy=0.7, color=DOWN, fs=9.5, box=True)
    mark(ax2, 3, 105.4, "下沿做多", dy=-1.0, color=UP, fs=9.5, box=True)

    style_ax(ax2, xlim=(-0.8, 10.6), ylim=(103.5, 110))
    ax2.set_title("区间市 → 均值回归（假设价格回归均值）", fontsize=11.5, color=DARK, pad=8)

    # ---- 底部：两种错配死法 ----
    style_ax(ax3, xlim=(0, 6.2), ylim=(0, 1.4))
    style_ax(ax4, xlim=(0, 6.2), ylim=(0, 1.4))
    box(ax3, 0.2, 0.2, 5.7, 0.9,
        "错配①：区间里用趋势跟踪\n反复追突破被假突破打脸，来回被绞", "#ffebee", DOWN, fs=9.5)
    box(ax4, 0.2, 0.2, 5.7, 0.9,
        "错配②：趋势里用均值回归\n\"跌这么多该反弹了\"去接飞刀，被趋势碾过", "#fff3e0", ORANGE, fs=9.5)

    # ---- 顶部：模式匹配 + 方向过滤 ----
    style_ax(axt, xlim=(0, 12.4), ylim=(0, 1.4))
    box(axt, 0.2, 0.25, 12.0, 0.9,
        "模式匹配 + 方向过滤：200 周期均线当多空分界线——上方只做多、下方只做空；它不给你入场信号，只过滤方向",
        "#e8f4f2", TEAL, fs=11)

    fig.suptitle("市场只有两种模式：趋势与区间；赚钱逻辑也只有两种——状态机（4.7）就是在这两种模式间切换",
                 fontsize=12.5, color=DARK, y=0.94)
    savefig(fig, "fig_p4_two_modes.png")


# ============ 图 4-11 Van Tharp 系统开发框架 ============
def fig_p4_tharp():
    fig, ax = plt.subplots(figsize=(12.4, 6.6))
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 7.2)

    # 顶部金句
    box(ax, 0.4, 6.55, 12.2, 0.6,
        "没有\"最好\"的系统，只有\"适合你\"的系统——系统开发不是找圣杯，是设计与你匹配的规则",
        "#e8f4f2", TEAL, fs=11)

    # 三步流程
    box(ax, 0.4, 4.5, 3.6, 1.8,
        "① 先定义你自己\n能承受多大回撤？\n每天能盯盘多久？\n要稳定小赚还是偶尔大赚？\n心理弱点是什么（第 7 章）",
        "#e3f2fd", "#1e3a6b", fs=9.5)
    box(ax, 4.9, 4.5, 3.6, 1.8,
        "② 再设计期望值\n在\"合身\"的约束下\n设计一个正期望系统\n（第 2-5 章的方法）",
        "#e8f5e9", UP, fs=10)
    box(ax, 9.4, 4.5, 3.6, 1.8,
        "③ 最后配仓位\n用仓位管理（第 6 章）\n把期望值变成\n稳定的资金曲线\n仓位是系统的一部分，不是事后补的",
        "#fff3e0", ORANGE, fs=9.5)
    arrow(ax, 4.0, 5.4, 4.9, 5.4)
    arrow(ax, 8.5, 5.4, 9.4, 5.4)

    # 两个例子（① 的展开）
    box(ax, 0.4, 2.4, 6.0, 1.4,
        "例①：上班族只能晚上看盘\n→ 日内系统不适合你，波段系统才合身",
        "#f3f6fb", "#1e3a6b", fs=9.5)
    box(ax, 6.9, 2.4, 6.0, 1.4,
        "例②：心理上扛不住连续亏损\n→ 你需要高胜率系统（哪怕盈亏比低）\n而不是低胜率高盈亏比系统",
        "#f3f6fb", "#1e3a6b", fs=9.5)

    # 底部三个自问
    box(ax, 0.4, 0.35, 3.9, 1.2,
        "自问①\n我的时间精力\n匹配这个周期吗？",
        "#eceff1", GRAY, fs=9.5)
    box(ax, 4.6, 0.35, 3.9, 1.2,
        "自问②\n我的心理承受得住\n这个胜率和回撤吗？",
        "#eceff1", GRAY, fs=9.5)
    box(ax, 8.8, 0.35, 3.9, 1.2,
        "自问③\n我能一致执行它\n100 笔不变形吗？",
        "#eceff1", GRAY, fs=9.5)
    arrow(ax, 2.35, 2.4, 2.35, 1.55)
    arrow(ax, 6.55, 2.4, 6.55, 1.55)
    arrow(ax, 10.75, 2.4, 10.75, 1.55)

    style_ax(ax)
    fig.suptitle("系统开发逻辑：先定义自己 → 再设计期望值 → 最后配仓位；三个自问全\"是\"才是你的系统",
                 fontsize=12.5, color=DARK, y=0.97)
    savefig(fig, "fig_p4_tharp.png")


# ============ 图 4-12 分批止盈：三种结局 ============
def fig_p4_scale_out():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：价格路径 + 分批点 ----
    seq = [
        (0, 100, 102, 99.5, 101.5),
        (1, 101.5, 103.2, 100.6, 102.8),
        (2, 102.8, 103.6, 101.0, 101.8),   # 回调
        (3, 101.8, 105.0, 101.4, 104.5),   # 入场后上涨
        (4, 104.5, 105.2, 103.0, 103.6),   # 回踩
        (5, 103.6, 107.2, 103.4, 106.8),   # 到 1R（分批点）
        (6, 106.8, 108.2, 106.0, 107.5),
        (7, 107.5, 109.8, 107.1, 109.4),   # 到 2R（目标）
        (8, 109.4, 110.2, 108.6, 109.8),
        (9, 109.8, 111.5, 109.2, 111.0),   # 继续奔跑
    ]
    for x, o, h, l, c in seq:
        candle(ax1, x, o, h, l, c, width=0.55)

    hl_line(ax1, -0.5, 10.2, 101.0, color=DOWN, ls=":", lw=1.3, label="入场 101.0")
    hl_line(ax1, -0.5, 10.2, 103.0, color=ORANGE, ls="--", lw=1.3, label="1R = 103.0")
    hl_line(ax1, -0.5, 10.2, 105.0, color=UP, ls="--", lw=1.3, label="2R = 105.0（目标）")
    hl_line(ax1, -0.5, 10.2, 101.0, color=TEAL, ls="-", lw=1.2)

    mark(ax1, 5, 106.8, "到 1R：平 50%\n剩余止损→入场价", dy=0.8, color=ORANGE, fs=9.5, box=True)
    mark(ax1, 7, 109.4, "剩余 50% 到目标：大赚", dy=0.8, color=UP, fs=9.5, box=True)
    # 保本线提示
    annotate_mark(ax1, 5, 101.0, "保本线", 4.0, 100.2, color=TEAL, fs=9, ha="right")

    style_ax(ax1, xlim=(-0.8, 10.6), ylim=(98, 114))
    ax1.set_title("分批止盈路径：到 1R 平半仓 + 保本，剩余奔跑", fontsize=11.5, color=DARK, pad=8)

    # ---- 右：三种结局 ----
    style_ax(ax2, xlim=(0, 6.2), ylim=(0, 6.6))
    ax2.set_title("从此结果只有三种，没有\"赚了又还回去\"", fontsize=11.5, color=DARK, pad=8)
    box(ax2, 0.5, 4.7, 5.2, 1.2,
        "结局 1 小赚：保本被扫离场\n（0 或小赚——资金释放，再战下一笔）", "#eceff1", GRAY, fs=9.5)
    box(ax2, 0.5, 3.1, 5.2, 1.2,
        "结局 2 中赚：1R 部分落袋\n剩余部分保本/小赚离场", "#fff3e0", ORANGE, fs=9.5)
    box(ax2, 0.5, 1.5, 5.2, 1.2,
        "结局 3 大赚：1R 部分落袋\n剩余 50% 跑向目标/结构位", "#e8f5e9", UP, fs=9.5)
    box(ax2, 0.5, 0.2, 5.2, 1.0,
        "代价：直接冲到底，你少赚一半\n——接受它，你要的是稳定期望值曲线\n不是单笔最大化", "#e8f4f2", TEAL, fs=9.5)

    fig.suptitle("分批止盈：兼顾落袋与奔跑——分批最大的心理价值：把\"赚了又还回去\"从可能里删掉",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p4_scale_out.png")


# ============ 图 4-13 保本时机：别移太早 ============
def fig_p4_breakeven():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：移太早的代价 ----
    seq = [
        (0, 100, 102, 99.5, 101.5),
        (1, 101.5, 103.5, 101.0, 103.2),
        (2, 103.2, 104.6, 102.6, 103.8),   # 刚到 1R 附近
        (3, 103.8, 104.0, 101.6, 102.0),   # 正常回调 → 扫保本
        (4, 102.0, 106.2, 101.8, 105.8),   # 行情继续奔目标
        (5, 105.8, 108.0, 105.2, 107.5),
        (6, 107.5, 109.8, 107.0, 109.4),
    ]
    for x, o, h, l, c in seq:
        candle(ax1, x, o, h, l, c, width=0.55)

    hl_line(ax1, -0.5, 7.2, 101.0, color=TEAL, ls="-", lw=1.3, label="入场 101.0")
    hl_line(ax1, -0.5, 7.2, 103.8, color=ORANGE, ls="--", lw=1.3, label="刚到 1R 就保本")
    # 被扫点
    mark(ax1, 3, 101.6, "正常回调\n扫掉保本单", dy=-1.2, color=DOWN, fs=9.5, box=True)
    mark(ax1, 6, 109.4, "行情却奔目标而去", dy=0.8, color=UP, fs=9.5, box=True)
    # 从保本线出发的向上箭头（被扫后错过行情）
    arrows(ax1, 3.2, 101.4, 109.0, color=GRAY, lw=1.6)

    style_ax(ax1, xlim=(-0.8, 7.6), ylim=(97.5, 112.5))
    ax1.set_title("移太早：刚 1R 就保本 → 回调被扫 → 错过行情", fontsize=11.5, color=DARK, pad=8)

    # ---- 右：正确做法 ----
    seq2 = [
        (0, 100, 102, 99.5, 101.5),
        (1, 101.5, 103.5, 101.0, 103.2),
        (2, 103.2, 104.6, 102.6, 103.8),
        (3, 103.8, 105.4, 103.4, 105.0),   # 到 1R，波动大等到 1.5R
        (4, 105.0, 105.6, 103.2, 103.6),   # 回调不扫保本（止损已在 1R 之上）
        (5, 103.6, 107.0, 103.4, 106.6),
        (6, 106.6, 108.8, 106.2, 108.4),   # 到目标
    ]
    for x, o, h, l, c in seq2:
        candle(ax2, x, o, h, l, c, width=0.55)

    hl_line(ax2, -0.5, 7.2, 101.0, color=TEAL, ls="-", lw=1.3, label="入场 101.0")
    hl_line(ax2, -0.5, 7.2, 103.8, color=ORANGE, ls="--", lw=1.3, label="至少 1R 再保本（高波动 1.5R）")
    # 保本后止损线上移示意
    stops = [(2.8, 103.8), (4.0, 104.2), (5.2, 104.6)]
    xs = [s[0] for s in stops]
    ys = [s[1] for s in stops]
    ax2.plot(xs, ys, color=UP, lw=1.8, ls="-", marker="o", ms=4, zorder=5,
             label="保本后止损只进不退")
    mark(ax2, 4, 103.6, "正常回调\n不扫（止损已上移）", dy=-1.4, color=UP, fs=9.5, box=True)
    mark(ax2, 6, 108.4, "到目标", dy=0.8, color=UP, fs=9.5, box=True)

    ax2.legend(loc="lower right", fontsize=8, framealpha=0.9)
    style_ax(ax2, xlim=(-0.8, 7.6), ylim=(97.5, 112.5))
    ax2.set_title("合适时机：至少 1R（高波动 1.5R）再保本", fontsize=11.5, color=DARK, pad=8)

    fig.suptitle("保本时机：移太早是常见错误——保本后接受\"被扫个保本\"：0 成本离场 + 资金释放，比\"赚了还回去\"好得多",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p4_breakeven.png")


# ============ 图 4-14 时间止损：不动也是风险 ============
def fig_p4_time_stop():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：时间止损（横盘不动） ----
    seq = [
        (0, 100, 101.2, 99.6, 100.8),
        (1, 100.8, 101.8, 100.2, 101.2),   # 入场
        (2, 101.2, 101.6, 100.4, 100.9),   # 横盘 1
        (3, 100.9, 101.5, 100.5, 101.0),   # 横盘 2
        (4, 101.0, 101.7, 100.3, 100.7),   # 横盘 3
        (5, 100.7, 101.6, 100.4, 101.1),   # 横盘 4
        (6, 101.1, 101.7, 100.5, 100.9),   # 横盘 5
        (7, 100.9, 101.5, 100.6, 101.0),   # 横盘 6
        (8, 101.0, 101.6, 100.4, 100.8),   # 横盘 7 —— 主动离场
        (9, 100.8, 104.5, 100.6, 104.0),   # 之后才动（错过）
    ]
    for x, o, h, l, c in seq:
        candle(ax1, x, o, h, l, c, width=0.55)

    hl_line(ax1, -0.5, 10.2, 101.2, color=TEAL, ls="-", lw=1.3, label="入场 101.2")
    hl_line(ax1, -0.5, 10.2, 100.0, color=DOWN, ls=":", lw=1.3, label="止损 100.0")
    # 横盘带
    ax1.axhspan(100.2, 101.8, color=GRAY, alpha=0.12, zorder=1)
    mark(ax1, 4.5, 101.6, "5~8 根 K 线\n在入场价附近徘徊", dy=0.5, color=GRAY, fs=9.5, box=True)
    mark(ax1, 8, 100.8, "主动离场 / 减半仓", dy=-0.9, color=ORANGE, fs=9.5, box=True)
    mark(ax1, 9, 104.0, "之后才动\n（资金被占用错过）", dy=0.8, color=DOWN, fs=9, box=True)

    style_ax(ax1, xlim=(-0.8, 10.6), ylim=(98, 107))
    ax1.set_title("时间止损：入场后 5-8 根 K 线不动 → 主动离场或减半仓", fontsize=11.5, color=DARK, pad=8)

    # ---- 右：信号失效（另一种时间止损） ----
    seq2 = [
        (0, 100, 101.6, 99.8, 101.0),
        (1, 101.0, 102.4, 100.4, 101.8),   # 入场（回调到 HL）
        (2, 101.8, 102.2, 100.8, 101.3),   # 横盘
        (3, 101.3, 101.9, 100.5, 101.0),   # 跌破 HL（逻辑前提没了）
        (4, 101.0, 101.5, 99.9, 100.3),
        (5, 100.3, 101.2, 99.6, 100.8),   # 新低结构
        (6, 100.8, 101.0, 98.8, 99.0),    # 若等到止损 → 大亏
    ]
    for x, o, h, l, c in seq2:
        candle(ax2, x, o, h, l, c, width=0.55)

    hl_line(ax2, -0.5, 7.2, 100.4, color=TEAL, ls="--", lw=1.3, label="入场逻辑：回调到 HL（HL=100.4）")
    hl_line(ax2, -0.5, 7.2, 99.5, color=DOWN, ls=":", lw=1.3, label="止损 99.5")
    # HL 被破
    mark(ax2, 3, 100.5, "跌破 HL：\"为什么\"不存在了", dy=-1.3, color=DOWN, fs=9.5, box=True)
    mark(ax2, 3.2, 100.9, "这里就该主动离场\n（别等价格来打止损）", dy=0.7, color=ORANGE, fs=9.5, box=True)
    mark(ax2, 6, 99.0, "等到止损才走 → 亏更多", dy=-1.3, color=DOWN, fs=9.5, box=True)

    style_ax(ax2, xlim=(-0.8, 7.6), ylim=(97, 105.5))
    ax2.set_title("信号失效：入场逻辑的前提已变化 → 主动离场", fontsize=11.5, color=DARK, pad=8)

    fig.suptitle("时间止损：不动也是风险——时间也是成本；持仓占用保证金、承受隔夜风险，却换不来预期的移动",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p4_time_stop.png")


if __name__ == "__main__":
    fig_p4_two_modes()
    fig_p4_tharp()
    fig_p4_scale_out()
    fig_p4_breakeven()
    fig_p4_time_stop()
    print("批次47 五张图生成完成")
