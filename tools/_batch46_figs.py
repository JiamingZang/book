# -*- coding: utf-8 -*-
"""批次46：第4章 P0 补图 5 张概念图
1. fig_p4_six_elements.png  —— 图 4-1 系统六要素（4.2节）
2. fig_p4_turtle.png       —— 图 4-9 海龟交易法则（4.9节）
3. fig_p4_exit_ev.png      —— 图 4-10 出场：期望值的另一半（4.12节）
4. fig_p4_lifecycle.png    —— 图 4-12 一笔交易完整生命周期（4.18节）
5. fig_p4_case.png         —— 图 4-13 完整案例：一笔交易从入场到出场（4.19节）
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

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


# ============ 图 4-1 系统六要素 ============
def fig_p4_six_elements():
    fig, ax = plt.subplots(figsize=(12.2, 6.4))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 7.0)

    # 顶部标题行：交易要回答的六个问题
    box(ax, 0.4, 6.35, 3.4, 0.55, "信号只回答：这里能不能进？", "#eceff1", GRAY, fs=10)
    box(ax, 8.2, 6.35, 3.8, 0.55, "交易要回答：六个问题都有答案", "#e8f5e9", UP, fs=10)

    # 六个要素卡片（2行3列）
    items = [
        (0.5, 4.6, "① 背景判断", "当前趋势/区间？\n用什么结构判断——写死", "#e3f2fd", "#1e3a6b"),
        (4.5, 4.6, "② 入场触发", "具体信号：\n假突破/锤子/吞没？——写死", "#e3f2fd", "#1e3a6b"),
        (8.5, 4.6, "③ 止损位置", "放哪、为什么：\n放结构外，不是固定点数", "#e3f2fd", "#1e3a6b"),
        (0.5, 2.5, "④ 止盈/目标", "前高前低 / RR≥2 才做\n入场前定死", "#fff3e0", ORANGE),
        (4.5, 2.5, "⑤ 仓位大小", "按风险百分比算\n（第 6 章）", "#fff3e0", ORANGE),
        (8.5, 2.5, "⑥ 过滤器", "什么情况不做：\n数据前/震荡/逆势/非活跃", "#fff3e0", ORANGE),
    ]
    for x, y, t, d, fc, ec in items:
        box(ax, x, y, 3.6, 1.7, f"{t}\n{d}", fc, ec, fs=10.5)

    # 底部：写下来才算系统
    arrow(ax, 4.6, 2.5, 4.6, 1.75)
    arrow(ax, 8.6, 2.5, 8.6, 1.75)
    box(ax, 1.9, 0.55, 3.6, 1.05, "写下来才算系统\n模糊的规则 = 给情绪留门", "#e8f4f2", TEAL, fs=10.5)
    box(ax, 6.9, 0.55, 4.6, 1.05, "入场前逐条打勾 → 执行率\n（第 8 章验证的基础）", "#e8f4f2", TEAL, fs=10.5)
    arrow(ax, 5.5, 1.08, 6.9, 1.08)

    style_ax(ax)
    fig.suptitle("系统六要素：六问都答出确定答案，才是交易——没有临场决策的空间",
                 fontsize=12.5, color=DARK, y=0.97)
    savefig(fig, "fig_p4_six_elements.png")


# ============ 图 4-9 海龟交易法则 ============
def fig_p4_turtle():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：海龟四规则流程 ----
    style_ax(ax1, xlim=(0, 6.2), ylim=(0, 6.6))
    ax1.set_title("海龟四规则（全是客观数字，零主观）", fontsize=11.5, color=DARK, pad=8)
    rules = [
        (0.5, 5.3, "入场\n价格突破 20 日最高 → 做多\n跌破 20 日最低 → 做空", "#e3f2fd", "#1e3a6b"),
        (0.5, 3.6, "止损\n2 × ATR（波动越大仓位越小）", "#ffebee", DOWN),
        (0.5, 1.9, "加仓\n每涨 0.5×ATR 加 1 单位\n最多 4 单位（金字塔）", "#fff3e0", ORANGE),
        (0.5, 0.2, "离场\n跌破 10 日最低 → 平仓", "#e8f5e9", UP),
    ]
    for x, y, t, fc, ec in rules:
        box(ax1, x, y, 5.2, 1.25, t, fc, ec, fs=10)
    for yy in (5.3 + 1.25, 3.6 + 1.25, 1.9 + 1.25):
        arrow(ax1, 3.1, yy, 3.1, yy - 1.25)

    # 仓位公式
    box(ax1, 0.5, 6.0, 5.2, 0.0, "", "#ffffff", GRAY, fs=10)  # 占位
    ax1.text(3.1, 6.35, "仓位公式（最有价值的贡献）", fontsize=10, color=DARK,
             ha="center", va="center", zorder=4)
    ax1.text(3.1, 5.95, "1 单位 = 账户 1% 风险 ÷ (2×ATR × 每点价值)",
             fontsize=10.5, color="#1e3a6b", ha="center", va="center",
             bbox=dict(boxstyle="round,pad=0.3", fc="#e3f2fd", ec="#1e3a6b", lw=1.2), zorder=5)

    # ---- 右：金字塔加仓示意 ----
    seq = [
        (0, 100, 103, 99, 102.5),
        (1, 102.5, 105, 101.5, 104.5),
        (2, 104.5, 108, 103.5, 107.5),   # 突破入场
        (3, 107.5, 109.5, 106, 106.5),   # 回调
        (4, 106.5, 110.5, 106, 110),     # 加仓点1
        (5, 110, 112, 108.5, 109),       # 回调
        (6, 109, 113.5, 108.5, 113),     # 加仓点2
        (7, 113, 114.5, 111.5, 112),
        (8, 112, 116.5, 111.5, 116),     # 加仓点3
        (9, 116, 118, 114.5, 115),
        (10, 115, 119.5, 114.5, 119),
    ]
    for x, o, h, l, c in seq:
        candle(ax2, x, o, h, l, c, width=0.55)

    # 入场线
    hl_line(ax2, -0.5, 10.8, 107.5, color=TEAL, ls="--", lw=1.4, label="突破 20 日高点入场")
    # 加仓点
    for x, y, t in [(4, 110, "第 2 单"), (6, 113, "第 3 单"), (8, 116, "第 4 单")]:
        mark(ax2, x, y, t, dy=0.5, color=ORANGE, fs=9.5, box=True)
    # 初始止损
    hl_line(ax2, 0.0, 10.8, 103.5, color=DOWN, ls=":", lw=1.4, label="初始止损 2×ATR")
    # 移动止损阶梯
    stops = [(2.0, 103.5), (4.2, 104.5), (6.2, 107.0), (8.2, 110.5), (10.2, 113.5)]
    xs = [s[0] for s in stops]
    ys = [s[1] for s in stops]
    ax2.plot(xs, ys, color=UP, lw=1.8, ls="-", marker="o", ms=4, zorder=5,
             label="止损跟随上移（只进不退）")
    annotate_mark(ax2, 4.2, 104.5, "每次加仓\n独立止损", 1.2, 101.5, color=UP, fs=9, ha="right")

    ax2.legend(loc="lower right", fontsize=8.5, framealpha=0.9)
    style_ax(ax2, xlim=(-0.8, 11.6), ylim=(98, 122))
    ax2.set_title("金字塔加仓：只在盈利时加，止损跟随上移", fontsize=11.5, color=DARK, pad=8)

    fig.suptitle("海龟交易法则：趋势跟踪的鼻祖——规则全客观，仓位由波动率决定",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p4_turtle.png")


# ============ 图 4-10 出场：期望值的另一半 ============
def fig_p4_exit_ev():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：期望值公式分解 ----
    style_ax(ax1, xlim=(0, 6.2), ylim=(0, 6.6))
    ax1.set_title("期望值公式：入场决定下限，出场决定上限", fontsize=11.5, color=DARK, pad=8)
    # 公式
    ax1.text(3.1, 5.9, "期望值 = 胜率 × 平均盈利 − 败率 × 平均亏损",
             fontsize=11, color=DARK, ha="center", va="center",
             bbox=dict(boxstyle="round,pad=0.35", fc="#fff3e0", ec=ORANGE, lw=1.4), zorder=5)
    # 入场管什么
    box(ax1, 0.5, 3.6, 5.2, 1.5, "入场决定「胜率的下限」\n——好信号 = 顺势 + 好位置 + 好形态\n只过滤烂交易，不决定赚多少", "#e3f2fd", "#1e3a6b", fs=10)
    # 出场管什么
    box(ax1, 0.5, 1.5, 5.2, 1.5, "出场决定「平均盈利的上限」\n——同样的入场，不同的出场\n长期期望值能差一倍", "#e8f5e9", UP, fs=10)
    arrow(ax1, 3.1, 5.3, 3.1, 5.1)
    arrow(ax1, 3.1, 3.6, 3.1, 3.0)

    # ---- 右：出场三问 ----
    style_ax(ax2, xlim=(0, 6.2), ylim=(0, 6.6))
    ax2.set_title("出场要回答的三个问题", fontsize=11.5, color=DARK, pad=8)
    box(ax2, 0.5, 5.1, 5.2, 1.2, "① 错了怎么办 → 止损\n（入场时就定死，不是亏了才想）", "#ffebee", DOWN, fs=10)
    box(ax2, 0.5, 3.4, 5.2, 1.2, "② 对了怎么办 → 止盈目标\n（结构位 / 固定 RR / 区间投射）", "#e8f5e9", UP, fs=10)
    box(ax2, 0.5, 1.7, 5.2, 1.2, "③ 对了之后怎么扩大 →\n移动止损与分批（只进不退）", "#fff3e0", ORANGE, fs=10)
    box(ax2, 0.5, 0.3, 5.2, 1.0, "90% 的人花在入场，10% 花在出场——反了", "#eceff1", GRAY, fs=10)
    for yy in (5.1 + 1.2, 3.4 + 1.2, 1.7 + 1.2):
        arrow(ax2, 3.1, yy, 3.1, yy - 1.2)

    fig.suptitle("出场是期望值的另一半：入场决定你上不上车，出场决定你赚多少、留不留得住",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p4_exit_ev.png")


# ============ 图 4-12 一笔交易的完整生命周期 ============
def fig_p4_lifecycle():
    fig, ax = plt.subplots(figsize=(12.2, 6.2))
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 7.0)

    # 主流程（横向，5 步）
    steps = [
        (0.3, 4.2, "入场前\n背景过 位置过 信号过\n算好止损/目标/仓位", "#e3f2fd", "#1e3a6b"),
        (3.0, 4.2, "入场\n信号确认挂单成交\n止损单同时挂好", "#e8f5e9", UP),
        (5.7, 4.2, "到 1R\n平 50%，剩余止损\n移到入场价（保本）", "#fff3e0", ORANGE),
        (8.4, 4.2, "推进中\n每出新 HL\n止损上移（结构法）", "#e8f4f2", TEAL),
        (11.1, 4.2, "结局判定", "#eceff1", GRAY),
    ]
    for x, y, t, fc, ec in steps:
        box(ax, x, y, 2.3, 1.6, t, fc, ec, fs=10)
    arrow(ax, 2.6, 5.0, 3.0, 5.0)
    arrow(ax, 5.3, 5.0, 5.7, 5.0)
    arrow(ax, 8.0, 5.0, 8.4, 5.0)
    arrow(ax, 10.7, 5.0, 11.1, 5.0)

    # 两个结局分支
    box(ax, 0.3, 1.5, 5.4, 1.5, "结局 A：跌破结构 → 剩余止损离场\n（锁定部分利润，把「赚了又还回去」删掉）", "#ffebee", DOWN, fs=10)
    box(ax, 6.0, 1.5, 5.4, 1.5, "结局 B：到达流动性池/目标 → 全部止盈\n（趋势的钱吃满）", "#e8f5e9", UP, fs=10)
    arrow(ax, 11.1, 4.2, 5.7, 3.0, color=DOWN, lw=1.8, rad=-0.25)
    arrow(ax, 11.1, 4.2, 8.7, 3.0, color=UP, lw=1.8, rad=-0.2)

    # 例外
    box(ax, 9.4, 5.9, 3.3, 0.75, "例外：8 根 K 线不动\n→ 时间止损，主动离场", "#fff3e0", ORANGE, fs=9.5)
    arrow(ax, 9.9, 5.9, 9.6, 5.85, color=ORANGE, lw=1.4, rad=-0.1)

    # 底部：决策只发生两次
    box(ax, 0.3, 0.15, 12.1, 0.8, "整个生命周期里「决策」只发生两次：入场前（计划）和到 1R 时（分批）——其余全是机械执行",
        "#e8f4f2", TEAL, fs=10.5)

    style_ax(ax)
    fig.suptitle("一笔交易的完整生命周期：决策只发生两次，其余全是机械执行",
                 fontsize=12.5, color=DARK, y=0.97)
    savefig(fig, "fig_p4_lifecycle.png")


# ============ 图 4-13 完整案例 ============
def fig_p4_case():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.9))

    # ---- 左：价格路径 + 止损阶梯 ----
    seq = [
        (0, 1.1085, 1.1095, 1.1082, 1.1092),   # 观察
        (1, 1.1092, 1.1098, 1.1088, 1.1095),
        (2, 1.1095, 1.1090, 1.1086, 1.1088),   # 回调到 HL 区
        (3, 1.1088, 1.1092, 1.1062, 1.1090),   # 锤子信号 K（长下影到 1.1062）
        (4, 1.1090, 1.1118, 1.1089, 1.1115),   # 入场 1.1090 → 到 1R=1.1115
        (5, 1.1115, 1.1130, 1.1110, 1.1125),   # 新高，HL 1.1120
        (6, 1.1125, 1.1152, 1.1123, 1.1145),   # 推进到 1.1145，HL 1.1135
        (7, 1.1145, 1.1152, 1.1132, 1.1138),   # 回调
        (8, 1.1138, 1.1150, 1.1136, 1.1150),   # 到达目标 1.1150（结局A）
    ]
    for x, o, h, l, c in seq:
        candle(ax1, x, o, h, l, c, width=0.55)

    # 价位线
    hl_line(ax1, -0.5, 9.2, 1.1150, color=UP, ls="-", lw=1.6, label="目标 1.1150（2.4R）")
    hl_line(ax1, -0.5, 9.2, 1.1115, color=ORANGE, ls="--", lw=1.3, label="1R = 1.1115")
    hl_line(ax1, -0.5, 9.2, 1.1090, color=TEAL, ls="-", lw=1.3, label="入场 1.1090")
    hl_line(ax1, -0.5, 9.2, 1.1065, color=DOWN, ls=":", lw=1.3, label="止损 1.1065（25 pips）")

    # 标注
    annotate_mark(ax1, 3, 1.1090, "锤子信号\n回调到 HL 区", 0.6, 1.1075, color=ORANGE, fs=9, ha="right")
    mark(ax1, 4, 1.1115, "到 1R：平 1 手，剩止损→1.1090", dy=0.0009, color=ORANGE, fs=8.5, box=True)
    mark(ax1, 6, 1.1145, "新 HL 1.1135：止损上移", dy=0.0009, color=TEAL, fs=8.5, box=True)
    mark(ax1, 8, 1.1150, "到目标：全平", dy=0.0009, color=UP, fs=9, box=True)

    # 止损阶梯（虚线上升）
    stops = [(3.5, 1.1065), (4.5, 1.1090), (5.5, 1.1120), (6.5, 1.1135)]
    xs = [s[0] for s in stops]
    ys = [s[1] for s in stops]
    ax1.plot(xs, ys, color=DOWN, lw=1.6, ls="--", marker="o", ms=4, zorder=5,
             label="止损阶梯（只进不退）")

    ax1.legend(loc="lower right", fontsize=8, framealpha=0.9)
    style_ax(ax1, xlim=(-0.8, 9.4), ylim=(1.1050, 1.1170))
    ax1.set_title("价格路径：入场 1.1090 → 1R 分批 → 止损阶梯上移", fontsize=11.5, color=DARK, pad=8)

    # ---- 右：结局 A/B 对比 ----
    style_ax(ax2, xlim=(0, 6.2), ylim=(0, 6.6))
    ax2.set_title("两种结局：从第 2 步起就不亏", fontsize=11.5, color=DARK, pad=8)
    box(ax2, 0.5, 4.6, 5.2, 1.5, "结局 A：到目标 1.1150 全平\n前半仓 60 pips + 后半仓 60 pips\n总盈利 ≈ 120 pips", "#e8f5e9", UP, fs=10)
    box(ax2, 0.5, 2.5, 5.2, 1.5, "结局 B：回调跌破 1.1135 止损\n前半仓 60 pips + 后半仓 45 pips\n总盈利 ≈ 105 pips", "#fff3e0", ORANGE, fs=10)
    box(ax2, 0.5, 0.6, 5.2, 1.3, "关键：从第 2 步起最差 = 保本/小赚\n分批 + 保本把「赚了又还回去」\n从可能里删掉", "#e8f4f2", TEAL, fs=10)

    fig.suptitle("完整案例（做多，趋势回调）：入场 1.1090 · 止损 1.1065 · 目标 1.1150 · 2 手",
                 fontsize=12.5, color=DARK, y=0.985)
    savefig(fig, "fig_p4_case.png")


if __name__ == "__main__":
    fig_p4_six_elements()
    fig_p4_turtle()
    fig_p4_exit_ev()
    fig_p4_lifecycle()
    fig_p4_case()
    print("批次46 五张图生成完成")
