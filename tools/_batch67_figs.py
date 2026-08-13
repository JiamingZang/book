# -*- coding: utf-8 -*-
"""
批次 67：第 8 章 5 张新图（补缺图节）
- fig_p8_workspace.png    图 8-3  8.1 图表与分析：四屏 MTF 布局 + 关键位提醒 + MT5 订单面板
- fig_p8_journal_fields.png 图 8-4 8.3 交易日志与复盘：日志字段两阶段（前 9 列计划 / 后 5 列结果）
- fig_p8_sim_standard.png 图 8-5  8.4 模拟盘：验证三关 + 两陷阱
- fig_p8_calendar.png    图 8-6  8.5 信息与日历：数据前后 15 分钟窗口
- fig_p8_antipitfall.png 图 8-7  8.6 防坑清单：四坑 + 防御

运行：python tools/_batch67_figs.py（须在仓库根目录）
复用 draw_handbook_figs.py 的 house style（draw_box/flow_arrow/candle/style_ax/savefig 等）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from draw_handbook_figs import (candle, hl_line, mark, annotate_mark, arrows,
                                style_ax, savefig, draw_box, flow_arrow,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)

rng = np.random.default_rng(42)


def gen_candles(n=12, start=97.0, touch=100.5, vol=0.55, seed=1):
    """生成一串围绕 touch 的 K 线：先涨到关键位、回踩、再突破——用于迷你屏"""
    r = np.random.default_rng(seed)
    out = []
    y = start
    xs = np.linspace(0.4, 11.6, n)
    for i, x in enumerate(xs):
        o = y
        if i < n // 3:
            c = y + (touch - y) * 0.55 + r.normal(0, vol * 0.5)
        elif i < 2 * n // 3:
            c = y - vol * 0.6 + r.normal(0, vol * 0.35)
        else:
            c = y + vol * 0.9 + r.normal(0, vol * 0.4)
        h = max(o, c) + abs(r.normal(0, vol * 0.5))
        l = min(o, c) - abs(r.normal(0, vol * 0.5))
        out.append((x, o, h, l, c))
        y = c
    return out


# ================================================================ 图 8-3 图表工作区
def fig_workspace():
    fig = plt.figure(figsize=(13.2, 7.0))
    # --- 左侧：四屏 MTF（子坐标轴，真实迷你 K 线图） ---
    panels = [
        ("日线 D1", 0.035, 0.56, 0.30, 0.35),
        ("4H",       0.355, 0.56, 0.30, 0.35),
        ("1H",       0.035, 0.10, 0.30, 0.35),
        ("15m",      0.355, 0.10, 0.30, 0.35),
    ]
    for title, px, py, pw, ph in panels:
        ax = fig.add_axes([px, py, pw, ph])
        style_ax(ax, xlim=(-0.5, 12.5), ylim=(95.0, 105.5))
        k = gen_candles(seed=5)
        for x, o, h, l, c in k:
            candle(ax, x, o, h, l, c, width=0.62)
        # 关键位：四屏共用同一条 100.0 虚线
        hl_line(ax, -0.5, 12.5, 100.0, color=DOWN, ls="--", lw=1.3)
        # 触及关键位那根 K 线标出提醒
        touch_x = k[len(k) // 3][0]
        ax.plot([touch_x], [100.3], marker="^", color=ORANGE, ms=9, zorder=6)
        ax.text(touch_x + 0.7, 101.3, "触及关键位\n→ 手机提醒", fontsize=8.5,
                color=ORANGE, va="center", zorder=6)
        ax.set_title(title, fontsize=11, color=DARK, pad=4)
        ax.text(0.4, 96.2, "关键位 100.0", fontsize=8.5, color=DOWN, va="center")

    # --- 右侧：MT5 订单面板（主轴） ---
    axm = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    style_ax(axm, xlim=(0, 13.4), ylim=(0, 7.2))
    px0, py0, pw, ph = 8.85, 1.35, 4.1, 4.9
    axm.add_patch(Rectangle((px0, py0), pw, ph, facecolor="white",
                            edgecolor=DARK, lw=1.6, zorder=3))
    axm.text(px0 + pw / 2, py0 + ph - 0.32, "MT5 订单面板", fontsize=12.5,
             color=DARK, ha="center", zorder=5, weight="bold")
    axm.text(px0 + pw / 2, py0 + ph - 0.72, "prop 考核盘主流操作端：挂单 / 止损 / 出金",
             fontsize=8.8, color=GRAY, ha="center", zorder=5)
    rows = [
        ("品种", "EURUSD", DARK),
        ("方向", "Buy（做多）", UP),
        ("入场", "1.0850（限价单，永不滑点）", DARK),
        ("止损", "1.0820（同时挂好，机器执行）", DOWN),
        ("目标", "1.0910（OCO，RR≈2）", UP),
        ("仓位", "0.5 手 = 风险 0.5%（6.2 公式）", ORANGE),
    ]
    ry = py0 + ph - 1.15
    for name, val, col in rows:
        axm.text(px0 + 0.25, ry, name, fontsize=10.5, color=GRAY,
                 va="center", zorder=5)
        axm.text(px0 + 1.35, ry, val, fontsize=10.5, color=col,
                 va="center", zorder=5)
        axm.plot([px0 + 0.12, px0 + pw - 0.12], [ry - 0.42, ry - 0.42],
                 color="#eceff1", lw=1.0, zorder=4)
        ry -= 0.62
    axm.text(px0 + pw / 2, py0 - 0.28, "入场前挂好止损——机器执行，不给情绪留机会（第 1.3）",
             fontsize=9.2, color=DOWN, ha="center", zorder=5)

    # --- 底部：工具配置清单（8.1 的半小时清单） ---
    steps = [
        ("① 多图表布局", "日线+4H+1H+15m\n四屏对齐（MTF）"),
        ("② 关键位模板", "水平线 + 区域高亮\n存成常用模板"),
        ("③ 手机提醒", "TradingView App\n价格到达即推送"),
        ("④ 合约规格", "点值 / 保证金\n抄进笔记（第 6 章）"),
    ]
    sx = 0.3
    for name, desc in steps:
        draw_box(axm, sx, 0.35, 2.55, 1.05, f"{name}\n{desc}", ec=TEAL, fs=9.5)
        if sx < 7.6:
            flow_arrow(axm, sx + 2.62, 0.875, sx + 3.12, 0.875, color=GRAY)
        sx += 3.15
    axm.text(8.85, 0.85, "四屏看的是同一段行情：\n大周期定方向，小周期找入场",
             fontsize=9.5, color=DARK, va="center")

    savefig(fig, "fig_p8_workspace.png")


# ================================================================ 图 8-4 日志字段两阶段
def fig_journal_fields():
    fig, ax = plt.subplots(figsize=(13.0, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    # 时间轴：入场前 → 平仓后
    flow_arrow(ax, 1.1, 6.35, 12.3, 6.35, color=DARK)
    ax.text(1.1, 6.62, "入场前（填计划）", fontsize=11.5, color=UP, ha="left", weight="bold")
    ax.text(12.3, 6.62, "平仓后（填结果与反思）", fontsize=11.5, color=ORANGE,
            ha="right", weight="bold")
    ax.text(6.7, 6.45, "同一行，分两次填", fontsize=9.5, color=GRAY,
            ha="center", va="center", style="italic")

    # 左面板：前 9 列（计划）
    draw_box(ax, 0.4, 1.0, 6.5, 5.0, "", ec=UP)
    ax.text(3.65, 5.62, "前 9 列 = 计划（入场前填）", fontsize=12, color=UP,
            ha="center", weight="bold")
    plan = ["日期/时间", "品种", "方向", "背景（趋势/区间）", "信号（触发）",
            "入场价", "止损价（距离/R）", "目标价（RR）", "仓位（手数+风险%）"]
    for i, t in enumerate(plan):
        r, c = divmod(i, 3)
        bx, by = 0.75 + c * 2.0, 4.45 - r * 1.15
        draw_box(ax, bx, by, 1.85, 0.78, t, ec=TEAL, fs=9.0)
    ax.text(3.65, 1.32, "把入场前的判断固定下来——这是防事后偏差的起点",
            fontsize=9.0, color=GRAY, ha="center")

    # 右面板：后 5 列（结果）
    draw_box(ax, 7.15, 1.0, 5.9, 5.0, "", ec=ORANGE)
    ax.text(10.1, 5.62, "后 5 列 = 结果与反思（平仓后填）", fontsize=12,
            color=ORANGE, ha="center", weight="bold")
    result = [("结果(R)", "盈亏，以 R 计（第 6 章）"),
              ("是否按计划", "是/否——执行率核心（第 7 章）"),
              ("心理状态", "平静 / 急切 / FOMO（第 7.5）"),
              ("截图链接", "入场前的图"),
              ("复盘备注", "哪里对、哪里错")]
    for i, (t, d) in enumerate(result):
        by = 4.5 - i * 0.9
        draw_box(ax, 7.5, by, 5.2, 0.72, f"{t}：{d}", ec=ORANGE, fs=9.0)

    # 中间竖虚线 + 警示
    ax.plot([6.95, 6.95], [0.9, 6.1], color=DOWN, ls=":", lw=1.4)
    ax.text(6.95, 6.0, "先填计划\n后填结果", fontsize=9.5, color=DOWN,
            ha="center", va="bottom", weight="bold")

    # 底部：统计用法
    draw_box(ax, 0.4, 0.12, 12.65, 0.75,
             "统计用法（每周 10 分钟）：筛选 是否按计划=否 的行 → 执行率；执行率 < 80% 问题不在系统在执行；再按 信号 分组算胜率/平均 R → 最差的 setup 优化或砍掉",
             ec=DARK, fs=9.5, tc=DARK)

    savefig(fig, "fig_p8_journal_fields.png")


# ================================================================ 图 8-5 模拟盘验证标准
def fig_sim_standard():
    fig, ax = plt.subplots(figsize=(13.0, 6.2))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.75, "模拟盘验证三关（全过 → 才买下一次考核）",
            fontsize=13, color=DARK, ha="center", weight="bold")

    gates = [
        ("关卡 1", "样本量 100+ 笔", "覆盖趋势与震荡\n两种行情", UP),
        ("关卡 2", "期望值为正", "按第 6 章公式\n扣成本后仍为正", UP),
        ("关卡 3", "执行率 > 80%", "计划内单 ÷ 总单\n（8.3 日志统计）", UP),
    ]
    gx = 0.7
    for num, title, desc, col in gates:
        draw_box(ax, gx, 4.3, 3.5, 1.95, "", ec=col)
        ax.text(gx + 1.75, 5.95, num, fontsize=10.5, color=col, ha="center", weight="bold")
        ax.text(gx + 1.75, 5.5, title, fontsize=12, color=DARK, ha="center", weight="bold")
        ax.text(gx + 1.75, 4.72, desc, fontsize=9.5, color=DARK, ha="center")
        ax.text(gx + 3.1, 6.1, "√", fontsize=16, color=UP, ha="center", weight="bold")
        if gx < 9.0:
            flow_arrow(ax, gx + 3.62, 5.28, gx + 4.18, 5.28, color=GRAY)
        gx += 4.25
    draw_box(ax, 12.35, 5.0, 0.7, 0.6, "√", ec=UP, fs=14)

    # 两个陷阱
    ax.text(6.7, 3.95, "模拟盘的两个陷阱", fontsize=12, color=DOWN,
            ha="center", weight="bold")
    traps = [
        ("陷阱 ① 没有真实资金压力 → 心理状态失真",
         "所以模拟期最重要的统计不是盈亏，是执行率——执行习惯可迁移，盈亏感受不可迁移"),
        ("陷阱 ② 想证明自己 → 模拟盘重仓",
         "规则不变：0.5% 风险照旧执行，否则你训练的是错误习惯"),
    ]
    tx = 0.7
    for title, desc in traps:
        draw_box(ax, tx, 1.55, 5.9, 2.15, "", ec=DOWN)
        ax.text(tx + 0.25, 3.35, title, fontsize=10.5, color=DOWN, ha="left", weight="bold")
        ax.text(tx + 0.25, 2.35, desc, fontsize=9.3, color=DARK, ha="left")
        tx += 6.2

    draw_box(ax, 0.7, 0.25, 12.0, 0.85,
             "prop 考核盘本身就是模拟盘——训练期就用它当战场，不另外找模拟盘（TradingView Paper 免费版也可）",
             ec=DARK, fs=9.5, tc=DARK)

    savefig(fig, "fig_p8_sim_standard.png")


# ================================================================ 图 8-6 日历规避
def fig_calendar():
    fig, ax = plt.subplots(figsize=(13.0, 6.0))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.0))

    ax.text(6.7, 6.55, "日历的用法不是预测数据，是规避数据", fontsize=13,
            color=DARK, ha="center", weight="bold")

    # 顶部：一周日历
    days = ["周一", "周二", "周三", "周四", "周五"]
    events = ["", "", "20:30 CPI\n（高影响）", "", "21:30 非农\n（高影响）"]
    dx = 0.8
    for i, (d, ev) in enumerate(zip(days, events)):
        draw_box(ax, dx, 4.55, 2.15, 1.7, "", ec=DARK if ev else GRAY)
        ax.text(dx + 1.075, 6.05, d, fontsize=11, color=DARK, ha="center", weight="bold")
        if ev:
            ax.text(dx + 1.075, 5.0, "" + ev, fontsize=8.8, color=DOWN,
                    ha="center", va="center", weight="bold")
        dx += 2.4

    ax.text(12.55, 5.4, "每周日把下周的\n高影响事件标进计划", fontsize=9.0,
            color=GRAY, ha="right", va="center")

    # 底部：事件窗口放大（时间轴）
    ax.text(6.7, 4.15, "以 20:30 数据公布为例——前后 15 分钟是禁区",
            fontsize=11, color=DARK, ha="center", weight="bold")
    # 时间轴
    ax.plot([1.0, 12.6], [2.15, 2.15], color=DARK, lw=1.6)
    for t, lab in [(2.5, "20:15"), (6.7, "20:30 数据公布"), (10.9, "20:45")]:
        ax.plot([t, t], [2.0, 2.3], color=DARK, lw=1.4)
        ax.text(t, 1.62, lab, fontsize=10, color=DARK, ha="center")
    # 禁区（红）
    ax.add_patch(Rectangle((2.5, 1.9), 4.2, 0.55, facecolor=DOWN, alpha=0.18,
                           edgecolor=DOWN, lw=1.2, zorder=3))
    ax.add_patch(Rectangle((6.7, 1.9), 4.2, 0.55, facecolor=DOWN, alpha=0.18,
                           edgecolor=DOWN, lw=1.2, zorder=3))
    ax.text(4.6, 2.85, "数据前 15 分钟：不开新仓", fontsize=9.5, color=DOWN,
            ha="center", weight="bold")
    ax.text(8.8, 2.85, "数据后 15 分钟：不开新仓", fontsize=9.5, color=DOWN,
            ha="center", weight="bold")
    ax.text(6.7, 2.95, "▲ 公布瞬间波动最大", fontsize=8.8, color=ORANGE,
            ha="center", weight="bold")
    # 可开仓区（绿）
    ax.add_patch(Rectangle((1.0, 1.9), 1.5, 0.55, facecolor=UP, alpha=0.15,
                           edgecolor=UP, lw=1.2, zorder=3))
    ax.add_patch(Rectangle((11.5, 1.9), 1.1, 0.55, facecolor=UP, alpha=0.15,
                           edgecolor=UP, lw=1.2, zorder=3))
    ax.text(1.75, 1.48, "正常", fontsize=8.5, color=UP, ha="center")
    ax.text(12.05, 1.48, "正常", fontsize=8.5, color=UP, ha="center")

    draw_box(ax, 1.0, 0.2, 11.6, 0.8,
             "军规第 5 条（第 7.6）：数据前后 15 分钟不开新仓；已有持仓提前收紧止损——VIX 飙升时进一步降仓",
             ec=DOWN, fs=9.5, tc=DARK)

    savefig(fig, "fig_p8_calendar.png")


# ================================================================ 图 8-7 防坑清单
def fig_antipitfall():
    fig, ax = plt.subplots(figsize=(13.0, 6.2))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.7, "防坑清单：四个坑 + 对应防御", fontsize=13, color=DARK,
            ha="center", weight="bold")

    cards = [
        ("坑 ① 免费信号群 / 跟单 / 自动交易软件",
         "工具只用来分析，不把账户 API 交给第三方——跟单收的是你的接盘，软件收的是你的数据"),
        ("坑 ② 数据源单一",
         "一个数据异常时换源交叉验证：Yahoo / Alpha Vantage / investing.com 互查"),
        ("坑 ③ 全信回测结果",
         "警惕前视偏差与漏扣滑点——回测期望值至少打八折再当真实预期（8.2）"),
        ("坑 ④ 幸存者偏差",
         "晒单的都是活下来的，爆仓的不会发帖——用完整交易日志说话（8.3）"),
    ]
    pos = [(0.6, 4.3), (6.9, 4.3), (0.6, 1.2), (6.9, 1.2)]
    for (title, defense), (cx, cy) in zip(cards, pos):
        draw_box(ax, cx, cy, 5.9, 2.6, "", ec=DOWN)
        ax.text(cx + 0.25, cy + 2.2, title, fontsize=10.8, color=DOWN,
                ha="left", weight="bold")
        ax.text(cx + 0.25, cy + 1.15, "防御：", fontsize=9.8, color=UP,
                ha="left", va="center", weight="bold")
        ax.text(cx + 1.0, cy + 1.15, defense, fontsize=9.3, color=DARK,
                ha="left", va="center")

    draw_box(ax, 0.6, 0.12, 12.2, 0.8,
             "防坑的底层逻辑：交易行业的“免费午餐”全都是收费的——你的工具链只需要清单里的正经工具，任何“额外赠送”都要警惕",
             ec=DARK, fs=9.8, tc=DARK)

    savefig(fig, "fig_p8_antipitfall.png")


if __name__ == "__main__":
    fig_workspace()
    fig_journal_fields()
    fig_sim_standard()
    fig_calendar()
    fig_antipitfall()
    print("批次 67 第 8 章 5 张图全部生成")
