# -*- coding: utf-8 -*-
"""
批次 75a：第 9 章 1 张新图（补缺图节 9.9）
- fig_p9_learning_budget.png   图 9-9  9.9 账户规模的现实：学费预算三档 + 与 prop 的三个推论 + 季节性日历

运行：python tools/_batch75a_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from draw_handbook_figs import (style_ax, savefig, draw_box,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


def fig_learning_budget():
    fig, ax = plt.subplots(figsize=(13.4, 7.6))
    style_ax(ax, xlim=(0, 13.8), ylim=(0, 8.0))

    ax.text(6.9, 7.6, "账户规模的现实：先算清学费账，再谈赚多少（Al Brooks 的提醒）",
            fontsize=12, color=DARK, ha="center", weight="bold")

    # ============ 左：三档现实 ============
    draw_box(ax, 0.3, 0.9, 6.4, 6.2, "", ec=DARK)
    ax.text(3.5, 6.8, "① 你的资金够交学费吗（三档现实）", fontsize=11, color=DARK, ha="center", weight="bold")

    # 档位 1：ES 新手
    draw_box(ax, 0.6, 5.1, 5.8, 1.3, "", ec=TEAL)
    ax.text(3.5, 6.05, "ES 新手：账户至少 10,000-25,000 美元",
            fontsize=10, color=DARK, ha="center", weight="bold")
    ax.text(3.5, 5.42, "学习期可能亏 1-2 年——“赚几天 → 一把亏回去”的循环；\n账户太小，学费没交完就被清算",
            fontsize=8.6, color=DARK, ha="center")

    # 档位 2：$500 广告
    draw_box(ax, 0.6, 3.6, 5.8, 1.3, "", ec=DOWN)
    ax.text(3.5, 4.55, "\"500 美元账户做 Emini\" 的广告 = 数学诈骗",
            fontsize=10, color=DARK, ha="center", weight="bold")
    ax.text(3.5, 3.92, "ES 每点 50 美元，最小止损 5-10 点就是 250-500 美元；\n亏两笔就没了——练的不是执行力，是恐惧",
            fontsize=8.6, color=DARK, ha="center")

    # 档位 3：大账户也只做 1 手
    draw_box(ax, 0.6, 2.1, 5.8, 1.3, "", ec=ORANGE)
    ax.text(3.5, 3.05, "就算有 100,000 美元，持续盈利前也只做 1 手 ES",
            fontsize=10, color=DARK, ha="center", weight="bold")
    ax.text(3.5, 2.42, "资金规模 ≠ 交易规模——第 6 章的\"实际风险\"才是唯一该听的标准",
            fontsize=8.6, color=DARK, ha="center")

    # 档位 4：小资金走低价路线
    draw_box(ax, 0.6, 0.35, 5.8, 1.5, "", ec=UP)
    ax.text(3.5, 1.45, "只能承受 5,000 美元亏损？换品种，别硬上",
            fontsize=10, color=DARK, ha="center", weight="bold")
    ax.text(3.5, 0.82, "低价高流动性股票/ETF（20 美元以下、波动 20 美分级）\n+ SPY 周期权（平值/略虚值 1 美元以下，管理得当亏约 0.20 美元 = 20 美元）",
            fontsize=8.2, color=DARK, ha="center")
    ax.text(3.5, 0.48, "→ 真实市场、真实金钱、真实情绪，但每次试错成本接近零",
            fontsize=8.6, color=UP, ha="center", weight="bold")

    # ============ 右：三推论 + 季节性日历 ============
    # 三推论
    draw_box(ax, 7.0, 4.2, 6.5, 2.9, "", ec=DARK)
    ax.text(10.25, 6.75, "② 与 prop 考核的三个推论", fontsize=11, color=DARK, ha="center", weight="bold")

    draw_box(ax, 7.2, 5.55, 6.1, 1.0, "", ec=TEAL)
    ax.text(7.35, 6.2, "1", fontsize=9, color="white", ha="center", va="center", weight="bold",
            bbox=dict(boxstyle="circle", fc=TEAL, ec="none"))
    ax.text(7.75, 6.2, "考核费是最便宜的学习工具，但不是唯一成本：", fontsize=9.4, color=DARK, va="center")
    ax.text(7.75, 5.8, "一两次考核费 50-500 美元，比亏 10,000 美元学费便宜得多——\n前提是拿考核的纪律练，而不是当赌场", fontsize=8.4, color=DARK, va="center")

    draw_box(ax, 7.2, 4.55, 6.1, 0.9, "", ec=TEAL)
    ax.text(7.35, 5.0, "2", fontsize=9, color="white", ha="center", va="center", weight="bold",
            bbox=dict(boxstyle="circle", fc=TEAL, ec="none"))
    ax.text(7.75, 5.0, "考过后仍需要真钱账户：", fontsize=9.4, color=DARK, va="center")
    ax.text(7.75, 4.62, "funded 是平台的，随时可能碰线收户；你自己的钱才决定生涯能否继续", fontsize=8.4, color=DARK, va="center")

    draw_box(ax, 7.2, 3.55, 6.1, 0.9, "", ec=TEAL)
    ax.text(7.35, 4.0, "3", fontsize=9, color="white", ha="center", va="center", weight="bold",
            bbox=dict(boxstyle="circle", fc=TEAL, ec="none"))
    ax.text(7.75, 4.0, "前 100 笔的目标不是赚钱，是执行率：", fontsize=9.4, color=DARK, va="center")
    ax.text(7.75, 3.62, "考核盘给了真实资金级别的环境练这件事，这是它最大的价值", fontsize=8.4, color=DARK, va="center")

    # 季节性日历
    draw_box(ax, 7.0, 0.9, 6.5, 2.5, "", ec=GRAY)
    ax.text(10.25, 3.1, "③ 季节性日历（只排期，不作信号）", fontsize=11, color=DARK, ha="center", weight="bold")

    rows = [
        ("全年 67% 正收益年份", "收盘高于开盘的年份占 67% → 别在典型熊市年死磕", TEAL),
        ("1 月晴雨表", "1 月涨 → 全年上涨概率 82% → 1 月适合启动考核", ORANGE),
        ("五月卖出走开", "涨幅集中在 10 月-次年 4 月 → 夏季练执行，不冲考核", GRAY),
        ("9 月最弱", "只比其他月份平均差 1% → 别当不可逾越的坎", DOWN),
    ]
    y = 2.7
    for name, desc, c in rows:
        draw_box(ax, 7.2, y, 6.1, 0.52, "", ec=c)
        ax.text(7.35, y + 0.26, name, fontsize=8.8, color=c, va="center", weight="bold")
        ax.text(8.55, y + 0.26, desc, fontsize=8.2, color=DARK, va="center")
        y -= 0.62

    ax.text(10.25, 0.55, "Brooks 的态度：影响\"何时启动考核\"的预期管理，不影响\"这笔单要不要进\"——别把季节当信号，把它当日历",
            fontsize=8.6, color=DARK, ha="center", style="italic")

    savefig(fig, "fig_p9_learning_budget.png")


if __name__ == "__main__":
    fig_learning_budget()
    print("batch75a done")
