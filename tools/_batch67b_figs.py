# -*- coding: utf-8 -*-
"""
批次 67b：第 9 章 4 张新图（补缺图节）
- fig_p9_platform.png     图 9-2  9.2 平台选择：先定品种再选平台 + 四实操维度 + 警惕低考核费
- fig_p9_funded.png       图 9-5  9.5 拿到 Funded 之后：五条注意事项 + 心态转变
- fig_p9_withdraw.png     图 9-6  9.6 出金与合规（中国大陆视角）
- fig_p9_rules_pitfall.png 图 9-7 9.7 规则细节：五坑（违反=封号）+ 自查清单

运行：python tools/_batch67b_figs.py（须在仓库根目录）
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from draw_handbook_figs import (style_ax, savefig, draw_box, flow_arrow,
                                UP, DOWN, TEAL, DARK, GRAY, ORANGE)


# ================================================================ 图 9-2 平台选择
def fig_platform():
    fig, ax = plt.subplots(figsize=(13.0, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.75, "平台选择：先定品种，再选平台", fontsize=13.5,
            color=DARK, ha="center", weight="bold")

    # 左：决策
    draw_box(ax, 0.6, 4.6, 3.6, 1.7, "", ec=DARK)
    ax.text(2.4, 6.05, "你做什么方法？", fontsize=12, color=DARK,
            ha="center", weight="bold")
    ax.text(2.4, 5.05, "品种机制决定\n工具与策略（第 1.2）", fontsize=9.0,
            color=GRAY, ha="center")
    flow_arrow(ax, 4.2, 6.0, 5.6, 6.0)
    flow_arrow(ax, 4.2, 5.0, 5.6, 5.0)

    # 左下一行两个选择
    draw_box(ax, 5.7, 5.35, 3.5, 1.35, "", ec=TEAL)
    ax.text(7.45, 6.35, "量价方法", fontsize=11, color=DARK, ha="center", weight="bold")
    ax.text(7.45, 5.75, "Wyckoff / 订单流 / Volume Profile\n→ 选期货平台（量真实）", fontsize=8.8, color=DARK, ha="center")
    ax.text(7.45, 6.42, "①", fontsize=11, color=TEAL, ha="center")
    draw_box(ax, 5.7, 3.75, 3.5, 1.35, "", ec=UP)
    ax.text(7.45, 4.75, "价格行为 / SMC", fontsize=11, color=DARK, ha="center", weight="bold")
    ax.text(7.45, 4.15, "纯价格行为对量价依赖低\n→ 选外汇平台（FTMO 等）", fontsize=8.8, color=DARK, ha="center")
    ax.text(7.45, 4.82, "②", fontsize=11, color=UP, ha="center")

    # 平台示例
    draw_box(ax, 9.6, 5.35, 3.3, 1.35, "", ec=GRAY)
    ax.text(11.25, 6.35, "期货：Topstep / Apex", fontsize=9.6, color=DARK, ha="center", weight="bold")
    ax.text(11.25, 5.75, "量价正统战场", fontsize=8.8, color=GRAY, ha="center")
    draw_box(ax, 9.6, 3.75, 3.3, 1.35, "", ec=GRAY)
    ax.text(11.25, 4.75, "外汇：FTMO / FundedNext", fontsize=9.6, color=DARK, ha="center", weight="bold")
    ax.text(11.25, 4.15, "最主流考核盘", fontsize=8.8, color=GRAY, ha="center")

    # 右：四个实操维度
    ax.text(6.7, 3.45, "平台对比的实操维度（不止看考核费）", fontsize=11.5,
            color=DARK, ha="center", weight="bold")
    dims = [
        ("规则透明度", "规则文档是否完整\n是否频繁改规则"),
        ("出金口碑", "搜「平台名 + 出金/封号」\n看真实反馈"),
        ("点差 / 佣金", "第 6.6：点差是隐性成本\n考核盘普遍点差偏大"),
        ("客服响应", "考核中遇技术问题\n客服态度决定体验"),
    ]
    dx = 0.8
    for name, desc in dims:
        draw_box(ax, dx, 1.55, 2.8, 1.7, "", ec=TEAL)
        ax.text(dx + 1.4, 3.0, name, fontsize=10.2, color=DARK, ha="center", weight="bold")
        ax.text(dx + 1.4, 2.0, desc, fontsize=8.3, color=DARK, ha="center")
        dx += 3.05

    draw_box(ax, 0.8, 0.25, 11.9, 0.9,
             "警惕：考核费只是最表面的成本——别被「49 美元挑战 10 万」的广告带着走，过低考核费常靠高通过率假象或隐藏规则收割",
             ec=DOWN, fs=9.5, tc=DARK)

    savefig(fig, "fig_p9_platform.png")


# ================================================================ 图 9-5 Funded 之后
def fig_funded():
    fig, ax = plt.subplots(figsize=(13.0, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.75, "拿到 Funded 不是终点，是新的起点", fontsize=13.5,
            color=DARK, ha="center", weight="bold")

    # 左：通过考核 → 五条注意事项
    draw_box(ax, 0.5, 1.15, 6.9, 5.0, "", ec=UP)
    ax.text(3.95, 5.75, "funded 账户的五条规则", fontsize=12, color=UP,
            ha="center", weight="bold")
    items = [
        ("分成与出金", "通常 80-90% 分成；出金周期 14-30 天；可能有最低盈利要求"),
        ("一致性规则", "不能靠单笔暴利；保持稳定单笔风险"),
        ("回撤规则依旧生效", "日/总回撤线照旧，碰线收回账户——0.5% 纪律继续用"),
        ("别急着放大", "先按考核期节奏跑 1-2 个月，稳定出金一次再考虑加仓/买更大账户"),
    ]
    iy = 5.1
    for name, desc in items:
        draw_box(ax, 0.9, iy - 0.6, 6.1, 0.95, "", ec=TEAL)
        ax.text(1.15, iy, name, fontsize=10.3, color=DARK, ha="left", weight="bold")
        ax.text(1.15, iy - 0.52, desc, fontsize=8.4, color=DARK, ha="left")
        iy -= 1.12

    # 右：心态转变
    draw_box(ax, 7.9, 1.15, 5.1, 5.0, "", ec=ORANGE)
    ax.text(10.45, 5.75, "心态转变：当第二场考核", fontsize=12, color=ORANGE,
            ha="center", weight="bold")
    draw_box(ax, 8.2, 4.3, 4.4, 1.15, "", ec=GRAY)
    ax.text(10.4, 4.95, "考核期目标：过线", fontsize=10.5, color=DARK,
            ha="center", weight="bold")
    ax.text(10.4, 4.42, "纪律完美就够", fontsize=9.0, color=GRAY, ha="center")
    flow_arrow(ax, 10.4, 4.25, 10.4, 3.55, color=ORANGE)
    draw_box(ax, 8.2, 2.6, 4.4, 1.15, "", ec=UP)
    ax.text(10.4, 3.25, "funded 期目标：稳定出金", fontsize=10.5, color=DARK,
            ha="center", weight="bold")
    ax.text(10.4, 2.72, "出金记录 = 真正的信用资产", fontsize=9.0, color=UP, ha="center")
    ax.text(10.45, 1.9, "很多人考核期纪律完美，拿到账户就放飞\n→ 第一个月就碰线收户。把 funded 当「第二场考核」：\n规则一样，奖励从「过线」变成「现金流」",
            fontsize=8.8, color=DOWN, ha="center")

    savefig(fig, "fig_p9_funded.png")


# ================================================================ 图 9-6 出金合规
def fig_withdraw():
    fig, ax = plt.subplots(figsize=(13.0, 6.0))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.0))

    ax.text(6.7, 6.5, "出金与合规（中国大陆视角）", fontsize=13.5,
            color=DARK, ha="center", weight="bold")

    # 流程：账户盈利 → 出金需求 → 三条注意 → 咨询专业人士
    draw_box(ax, 0.6, 4.4, 2.7, 1.5, "账户盈利\n（funded 账户）", ec=UP, fs=10.5)
    flow_arrow(ax, 3.35, 5.15, 4.35, 5.15, color=DARK)
    draw_box(ax, 4.4, 4.4, 2.7, 1.5, "产生出金需求\n（境外汇入）", ec=DARK, fs=10.5)
    flow_arrow(ax, 7.15, 5.15, 8.15, 5.15, color=DARK)
    draw_box(ax, 8.2, 4.4, 4.6, 1.5, "合规三注意", ec=ORANGE, fs=11.5,
              tc=DARK)
    ax.text(10.5, 4.95, "① 个人每年 5 万美元便利化额度\n② 大额境外汇入触发反洗钱问询\n③ 没有干净的官方通道",
            fontsize=8.8, color=DARK, ha="center")

    # 警示
    draw_box(ax, 0.6, 2.3, 12.2, 1.4, "", ec=DOWN)
    ax.text(6.7, 3.25, "务必自行咨询专业人士", fontsize=11.5, color=DOWN,
            ha="center", weight="bold")
    ax.text(6.7, 2.6, "别依赖平台的「出金教程」——资金通道的合规是你自己的责任",
            fontsize=9.5, color=DARK, ha="center")

    draw_box(ax, 0.6, 0.4, 12.2, 1.15,
             "本章只负责把账户做起来（方法 × 仓位 × 执行）；合规问题与交易方法无关，属于个人资金通道的独立议题",
             ec=GRAY, fs=9.5, tc=DARK)

    savefig(fig, "fig_p9_withdraw.png")


# ================================================================ 图 9-7 规则坑
def fig_rules_pitfall():
    fig, ax = plt.subplots(figsize=(13.0, 6.4))
    style_ax(ax, xlim=(0, 13.4), ylim=(0, 7.2))

    ax.text(6.7, 6.7, "规则细节：五个隐藏坑（违反 = 封号）", fontsize=13.5,
            color=DARK, ha="center", weight="bold")

    pits = [
        ("一致性规则", "单笔盈利 ≤ 总盈利\n的 30-50%\n（防一把赌对）"),
        ("周末持仓", "禁止持仓过周末\n防周一跳空\n周五收盘前平仓"),
        ("新闻交易", "禁止重大数据\n前后开仓"),
        ("最低交易天数", "防止快速\n赌达标"),
        ("风格检测", "马丁 / 对冲 /\n高频刷单\n判定违规"),
    ]
    px = 0.55
    for name, desc in pits:
        draw_box(ax, px, 4.35, 2.35, 2.0, "", ec=DOWN)
        ax.text(px + 1.175, 6.15, name, fontsize=9.8, color=DOWN, ha="center", weight="bold")
        ax.text(px + 1.175, 5.0, desc, fontsize=8.0, color=DARK, ha="center")
        px += 2.55

    ax.text(6.7, 4.05, "买考核前，把所有规则读一遍——很多人失败不是技术不行，是没读规则",
            fontsize=10.5, color=DOWN, ha="center", weight="bold")

    # 自查清单
    draw_box(ax, 0.55, 0.9, 12.3, 2.75, "", ec=TEAL)
    ax.text(6.7, 3.3, "规则自查清单（买考核前逐条确认）", fontsize=11.5,
            color=TEAL, ha="center", weight="bold")
    checks = [
        "盈利目标是多少？日/总回撤怎么计算（余额还是权益）？",
        "周末能不能持仓？节假日呢？",
        "数据时段能不能开仓？有没有一致性规则？比例多少？",
        "最低交易天数？最长时间限制？",
        "出金周期和最低出金额？分成比例？",
    ]
    cy = 2.75
    for t in checks:
        ax.add_patch(Rectangle((1.0, cy - 0.11), 0.22, 0.22, facecolor="white",
                               edgecolor=DARK, lw=1.2, zorder=5))
        ax.text(1.45, cy - 0.08, t, fontsize=9.0, color=DARK, ha="left", va="center")
        cy -= 0.42

    ax.text(6.7, 0.28, "「回撤怎么计算」是最常被忽略的细节：余额 vs 权益，浮亏是否占用回撤额度——定义性细节决定持仓管理策略",
            fontsize=8.8, color=GRAY, ha="center")

    savefig(fig, "fig_p9_rules_pitfall.png")


if __name__ == "__main__":
    fig_platform()
    fig_funded()
    fig_withdraw()
    fig_rules_pitfall()
    print("批次 67b 第 9 章 4 张图全部生成")
