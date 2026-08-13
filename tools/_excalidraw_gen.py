# -*- coding: utf-8 -*-
"""批次 51：流程图类图片 Excalidraw 化
把 12 张"方框+箭头"流程图从纯 matplotlib 改为 Excalidraw 双输出：
  - .excalidraw（Obsidian 可编辑、手绘风渲染）
  - .png（matplotlib 渲染，HTML/PDF 流水线继续使用）

转换清单（图号不变，文件名不变，仅新增 .excalidraw 同名字文件）：
  fig_p2_checklist       图 2-13 逐棒检查单
  fig_p3_framework       图 3-1  判定框架
  fig_p4_breakout_flow   图 4-5  突破生命周期
  fig_p4_state_machine   图 4-6  状态机
  fig_p4_state_tree      图 4-7  状态判定树
  fig_p5_smc_flow        图 5-6  SMC 交易流程
  fig_p7_three_stages    图 7-1  心理三阶段
  fig_p7_flow            图 7-4  三时刻流程
  fig_p8_verify_loop     图 8-1  验证闭环
  fig_p8_review_flow     图 8-2  复盘流水线
  fig_p9_prop_flow       图 9-1  考核三段式
  fig_p10_strategy_tree  图 10-6 期权策略决策树

运行：python -X utf8 tools/_excalidraw_gen.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _excalidraw_lib import ExcaliDoc, UP, DOWN, GRAY, DARK, ORANGE, TEAL, NAVY

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "handbook", "images")
BLUE = "#1565c0"
PURPLE = "#6a1b9a"
GREEN = UP

# ---------------------------------------------------------------- 图 2-13 逐棒检查单
def fig_p2_checklist():
    doc = ExcaliDoc("fig_p2_checklist", xlim=(0, 10), ylim=(0, 10.8), figsize=(13.5, 5.8),
                    title="逐棒检查单（Al Brooks）：先上下文再形态、先信号质量再计划、先二次入场再反转、先跟随再确认、先惯性再逆势、看不懂就等下一根")
    # 左面板：五步流程
    steps = ["① 分类：趋势棒/十字星/内包/外包？",
             "② 角色：结构/信号/入场/确认棒？",
             "③ 上下文：趋势/通道/区间/突破后/反转？",
             "④ 跟随：后 1-2 根同向推进？",
             "⑤ 更新计划：顺势/等二次/等测试/放弃/不做"]
    ys = [8.35, 6.65, 4.95, 3.25, 1.55]
    for i, (t, y) in enumerate(zip(steps, ys)):
        doc.box(0.3, y, 4.0, 1.25, t, ec=DARK, fs=10)
        if i < 4:
            doc.arrow(2.3, y + 1.25, 2.3, ys[i + 1] + 1.25, color=TEAL)
    doc.text(2.3, 10.2, "每根 K 线收盘后（10 秒内跑完）", fs=10.5, color=TEAL)
    doc.text(2.3, 0.2, "① 五步固定流程", fs=11, color=DARK)
    # 右面板：六条口诀
    tips = [("① 先上下文，再形态", 5.4, 7.9), ("② 先信号质量，再入场计划", 5.4, 5.7),
            ("③ 先二次入场，再评估反转", 5.4, 3.5), ("④ 先跟随，再确认可交易", 5.4, 1.3),
            ("⑤ 先惯性，再逆势", 9.0, 7.9), ("⑥ 看不懂，就等下一根", 9.0, 5.7)]
    for t, x, y in tips:
        doc.box(x, y, 3.6, 1.7, t, ec=TEAL, fs=10.5)
    doc.text(7.2, 0.35, "没有跟随的信号，不能当成高概率机会", fs=9.5, color=DARK)
    doc.text(7.2, 10.2, "② 六条口诀（每次看图默念）", fs=11, color=DARK)
    doc.export(OUT)


# ---------------------------------------------------------------- 图 3-1 判定框架
def fig_p3_framework():
    doc = ExcaliDoc("fig_p3_framework", xlim=(0, 12), ylim=(0, 6.6), figsize=(12.2, 6.2),
                    title="判定框架：背景 × 位置 × 形态——三道闸按顺序过，任何一道不过就放弃")
    doc.box(4.6, 5.9, 2.8, 0.62, "看到一根信号 K（如锤子线）", ec=TEAL, fs=11, fc="#e8f4f2")
    doc.arrow(6.0, 5.9, 6.0, 5.65, color=DARK)
    gates = [
        (0.4, "闸 1：背景（大方向）\nHTF 方向一致吗？\n趋势还是区间？", "只做顺势信号", "#fff3e0", ORANGE),
        (4.2, "闸 2：位置（关键位）\n在支撑/阻力/结构点上吗？\n半空中的信号是噪音", "信号必须放在位置里读", "#e8f4f2", TEAL),
        (8.0, "闸 3：形态（信号 K）\n收盘/影线/实体合格吗？\n最后一道确认", "第 3.10 质量标准", "#fff3e0", ORANGE),
    ]
    for x, title, sub, fc, ec in gates:
        doc.box(x, 3.9, 3.4, 1.7, title, ec=ec, fs=10, fc=fc)
        doc.text(x + 1.7, 3.55, sub, fs=8.5, color=GRAY)
        doc.arrow(x + 1.7, 3.9, x + 1.7, 3.65, color=DARK)
    doc.arrow(2.1, 4.75, 4.2, 4.75, color=DARK)
    doc.arrow(5.9, 4.75, 8.0, 4.75, color=DARK)
    for x in (2.1, 5.9, 9.7):
        doc.line(x, 3.9, x, 2.9, color=DOWN, dashed=True, lw=1.6)
        doc.text(x, 3.05, "否", fs=9.5, color=DOWN)
        doc.line(x, 2.9, x + 1.4, 2.9, color=DOWN, dashed=True, lw=1.6)
        doc.box(x + 1.4, 2.55, 1.55, 0.7, "放弃", ec=DOWN, fs=10, fc="#ffebee")
    doc.arrow(9.7, 3.65, 9.7, 2.3, color=DARK)
    doc.box(7.7, 1.5, 4.0, 1.0, "三道闸全过 → 入场\n（按第 6 章仓位公式算好手数再执行）",
            ec=UP, fs=10, fc="#e8f5e9", tc="#1b5e20")
    doc.box(0.4, 1.5, 4.6, 1.0, "信号质量 = 背景 × 位置 × 形态\n三者相乘，缺一个就是零",
            ec=NAVY, fs=10, fc="#e3f2fd")
    doc.text(6.0, 0.6, "三道闸把「感觉」替换成「清单」——这是对抗情绪的唯一工程化方法（第 7 章）", fs=10, color=DARK)
    doc.export(OUT)


# ---------------------------------------------------------------- 图 4-5 突破生命周期
def fig_p4_breakout_flow():
    doc = ExcaliDoc("fig_p4_breakout_flow", xlim=(0, 10.5), ylim=(0, 10), figsize=(13.0, 7.2),
                    title="突破的完整生命周期：突破 → 制造缺口 → 测试 → 缺口升级或降级（你等的不是突破那一下，是测试的结果）")
    doc.box(3.4, 8.8, 3.2, 0.9, "区间压缩（波动收缩）\n价格贴近区间边界", ec=ORANGE, fs=10, fc="#fff8e1")
    doc.arrow(5.0, 8.8, 5.0, 8.2, color=GRAY)
    doc.box(3.4, 7.0, 3.2, 1.0, "突破发生\n大实体收盘在区间外 + 放量", ec=GREEN, fs=10, fc="#e8f5e9")
    doc.arrow(5.0, 7.0, 5.0, 6.4, color=GRAY)
    doc.box(3.4, 5.2, 3.2, 1.0, "无回调：突破仍在进行\n价格同向走，缺口在扩大", ec=BLUE, fs=10, fc="#e3f2fd")
    doc.arrow(5.0, 5.2, 5.0, 4.6, color=GRAY)
    doc.box(3.0, 3.4, 4.0, 1.0, "出现回调：突破结束（或失败）\n市场开始测试突破点", ec=DOWN, fs=10, fc="#fce4ec")
    doc.arrow(3.8, 3.4, 2.2, 2.6, color=GREEN, rad=0.0)
    doc.text(2.2, 3.05, "测试守住", fs=9, color=GREEN)
    doc.box(0.3, 1.5, 2.8, 1.0, "测试成功：缺口升级\n= 测量缺口（MG）\n预期同向第二波", ec=GREEN, fs=9, fc="#e8f5e9")
    doc.arrow(6.2, 3.4, 7.8, 2.6, color=DOWN, rad=0.0)
    doc.text(7.4, 3.05, "测试失败", fs=9, color=DOWN)
    doc.box(7.2, 1.5, 2.8, 1.0, "测试失败：缺口闭合\n= 衰竭缺口（EG）\n反转信号", ec=DOWN, fs=9, fc="#fce4ec")
    doc.arrow(8.6, 1.5, 8.6, 1.1, color=PURPLE)
    doc.box(5.6, 0.1, 4.4, 0.8, "失败的回调本身可成新突破：关闭缺口的那根 K 线收盘站对方向，\n同方向至少再期待一根 K 线",
            ec=PURPLE, fs=8.5, fc="#f3e5f5")
    doc.arrow(5.6, 0.5, 3.4, 0.5, color=PURPLE)
    doc.box(0.6, 0.1, 2.3, 0.8, "回到区间压缩状态\n循环重新开始", ec=ORANGE, fs=9.5, fc="#fff8e1")
    doc.export(OUT)


# ---------------------------------------------------------------- 图 4-6 状态机
def fig_p4_state_machine():
    doc = ExcaliDoc("fig_p4_state_machine", xlim=(0, 13.2), ylim=(0, 6.6), figsize=(12.5, 6.2),
                    title="状态机（4.5）：结构判定 → 三系统切换——先判结构，再选系统，不跨状态混用")
    doc.box(0.3, 3.0, 2.1, 1.1, "结构判定\nHH+HL / LH+LL / 区间", ec=DARK, fs=10.5)
    doc.box(4.0, 5.2, 2.2, 1.0, "上升趋势", ec=UP, fs=10.5)
    doc.box(4.0, 3.0, 2.2, 1.0, "下降趋势", ec=DOWN, fs=10.5)
    doc.box(4.0, 0.5, 2.2, 1.0, "区间", ec=ORANGE, fs=10.5)
    doc.box(7.8, 1.7, 2.0, 0.9, "边界未破", ec=ORANGE, fs=10.5)
    doc.box(7.8, 0.3, 2.0, 0.9, "边界被破", ec=ORANGE, fs=10.5)
    doc.box(10.5, 5.2, 2.5, 1.0, "系统一\n顺势回调做多", ec=UP, fs=10.5)
    doc.box(10.5, 3.0, 2.5, 1.0, "系统一（镜像）\n下降趋势做空", ec=DOWN, fs=10.5)
    doc.box(10.5, 1.7, 2.5, 0.9, "系统二\n区间边界反向", ec=ORANGE, fs=10.5)
    doc.box(10.5, 0.3, 2.5, 0.9, "系统三\n突破跟随", ec=ORANGE, fs=10.5)
    doc.arrow(2.4, 4.05, 4.0, 5.7, rad=0.18, color=DARK)
    doc.arrow(2.4, 3.55, 4.0, 3.5, color=DARK)
    doc.arrow(2.4, 3.0, 4.0, 1.0, rad=-0.18, color=DARK)
    doc.arrow(6.2, 5.7, 10.5, 5.7, color=DARK)
    doc.arrow(6.2, 3.5, 10.5, 3.5, color=DARK)
    doc.arrow(6.2, 1.3, 7.8, 1.3, rad=-0.25, color=DARK)
    doc.arrow(6.2, 0.7, 7.8, 0.4, rad=0.25, color=DARK)
    doc.arrow(9.8, 2.15, 10.5, 2.15, color=DARK)
    doc.arrow(9.8, 0.75, 10.5, 0.75, color=DARK)
    doc.arrow(12.2, 1.2, 12.2, 4.6, color=GRAY, dashed=True, rad=0.3)
    doc.text(11.4, 2.9, "回到系统一", fs=9.5, color=GRAY, ha="right")
    doc.export(OUT)


# ---------------------------------------------------------------- 图 4-7 状态判定树
def fig_p4_state_tree():
    doc = ExcaliDoc("fig_p4_state_tree", xlim=(0, 18.6), ylim=(0, 9.5), figsize=(15.5, 8.2),
                    title="状态判定树：通道与区间的唯一入口——每一步都有硬条件，斜率/视觉宽度只作辅助")
    doc.box(5.2, 7.6, 4.6, 1.4, "是否存在有序波段序列？\n（≥2 组 HH+HL / LL+LH）", ec=DARK, fs=11)
    doc.box(1.0, 5.0, 4.8, 1.4, "序列 ≥3 组且可画\n平行趋势线？", ec=TEAL, fs=11)
    doc.box(9.2, 5.0, 4.8, 1.4, "清晰上下边界？\n（各 ≥2 次测试）", ec=TEAL, fs=11)
    doc.box(0.4, 2.4, 4.6, 1.7, "按最近回撤分类：\n<30% 窄 / 30-50% 常规\n50-78.6% 宽通道（4.21）", ec=UP, fs=10)
    doc.box(5.6, 2.4, 4.6, 1.7, "trending_tr\n趋势型区间（仅 2 组）\n同框架、置信度更低", ec=GRAY, fs=10)
    doc.box(9.2, 2.4, 4.6, 1.7, "trading_range\n普通交易区间\n（区间策略，4.3）", ec=DOWN, fs=10)
    doc.box(14.4, 2.4, 3.9, 1.7, "extreme_tr\n极端区间\n期望值为负，不做", ec=GRAY, fs=10)
    doc.arrow(6.0, 7.6, 3.2, 6.4, color=DARK, rad=-0.15)
    doc.arrow(9.0, 7.6, 11.4, 6.4, color=DARK, rad=0.15)
    doc.arrow(3.4, 5.0, 3.4, 4.1, color=TEAL)
    doc.arrow(5.8, 5.0, 7.8, 4.1, color=TEAL, rad=-0.2)
    doc.arrow(11.5, 5.0, 11.5, 4.1, color=TEAL)
    doc.arrow(13.8, 5.0, 15.6, 4.1, color=TEAL, rad=0.25)
    doc.text(4.3, 7.25, "是", fs=10, color=DARK)
    doc.text(10.6, 7.25, "否", fs=10, color=DARK)
    doc.text(3.9, 4.62, "是", fs=10, color=TEAL)
    doc.text(6.9, 4.62, "否", fs=10, color=TEAL)
    doc.text(11.9, 4.62, "是", fs=10, color=TEAL)
    doc.text(14.9, 4.62, "否", fs=10, color=TEAL)
    doc.text(7.6, 0.35, "最新波段出现 LL（涨）/ HH（跌）→ 立即重估是否转区间；状态转换期降级处理（弱信号不做，目标保守）",
             fs=10, color=DARK)
    doc.export(OUT)


# ---------------------------------------------------------------- 图 5-6 SMC 交易流程
def fig_p5_smc_flow():
    doc = ExcaliDoc("fig_p5_smc_flow", xlim=(0, 14), ylim=(0, 6.6), figsize=(14.5, 6.4),
                    title="完整 SMC 交易流程（5.7）：多级别背景 → 五步执行 → 本质是第 4 章趋势回调系统的翻译版")
    doc.box(0.4, 5.15, 13.2, 1.25, "背景（多级别过滤）：日线上升趋势 → 4H CHoCH 警告 → 1H 等做多回调", ec=GRAY, fs=11)
    doc.arrow(1.7, 5.12, 1.7, 4.95, color=GRAY)
    steps = [
        (0.6, "① 画结构\nswing 高低点\nBSL / SSL 池\n看涨 OB、FVG\n→ 2.4 / 5.2-5.6", TEAL),
        (3.2, "② 等 sweep\n插破前低 SSL\n快速收回 / 长影\n→ 3.2 / 5.3", ORANGE),
        (5.8, "③ 找入场区\nFVG / OB 区域\n15m 锤子 / 内包\n→ 4.3 / 5.5-5.6", TEAL),
        (8.4, "④ 执行\nOB 入场 + 确认\n止损 sweep 低点下\n→ 4.2 / 5.5", ORANGE),
        (11.0, "⑤ 管理\n1R 移保本\n跑向 BSL / 2R\n→ 4.4 / 4.13", TEAL),
    ]
    for i, (x, txt, col) in enumerate(steps):
        doc.box(x, 2.7, 2.2, 2.2, txt, ec=col, fs=9.5)
        if i < 4:
            doc.arrow(x + 2.2, 3.8, x + 2.6, 3.8, color=GRAY)
    doc.box(0.4, 0.35, 13.2, 1.95,
            "关键认知：这套流程 = 第 4 章趋势回调系统的 SMC 翻译版——语言不同，数学一样。\n"
            "画结构=趋势判断（2.4）｜等 sweep=假突破确认（3.2）｜FVG/OB=回调入场区（4.3）\n"
            "止损 SSL 外=结构止损（4.2）｜目标 BSL=前高目标（4.13）",
            ec=TEAL, fs=10)
    doc.export(OUT)


# ---------------------------------------------------------------- 图 7-1 心理三阶段
def fig_p7_three_stages():
    doc = ExcaliDoc("fig_p7_three_stages", xlim=(0, 13.8), ylim=(0, 6.8), figsize=(13.5, 6.2),
                    title="心理成熟的三个阶段：从看单笔结果，到看一致执行")
    cols = [
        (0.4, DARK, "阶段 1：结果导向（新手）", "关注：这笔赚没赚\n赚了=天才，亏了=系统骗人\n情绪随单笔盈亏起伏"),
        (4.9, ORANGE, "阶段 2：规则导向（进阶）", "关注：有没有按规则做\n开始执行规则\n但情绪仍随盈亏起伏"),
        (9.4, UP, "阶段 3：概率导向（成熟）", "关注：是否一致执行了\n正期望值系统\n看 100 笔的分布，不是这一笔"),
    ]
    for x, c, title, body in cols:
        doc.box(x, 3.6, 4.0, 1.6, title, ec=c, fs=12, tc=c)
        doc.box(x, 0.9, 4.0, 2.0, body, ec=GRAY, fs=10.5)
    doc.arrow(4.55, 4.4, 4.85, 4.4, color=DARK)
    doc.arrow(9.05, 4.4, 9.35, 4.4, color=DARK)
    doc.text(6.9, 0.25, "评价标准从「赚没赚」换成「有没有一致执行」，心态问题就解决了一大半", fs=11, color=DARK)
    doc.text(6.9, 6.45, "好交易 = 按计划执行的亏损单；坏交易 = 侥幸赚钱的违规单", fs=11, color=DARK)
    doc.export(OUT)


# ---------------------------------------------------------------- 图 7-4 三时刻流程
def fig_p7_flow():
    doc = ExcaliDoc("fig_p7_flow", xlim=(0, 10), ylim=(0, 10), figsize=(13.0, 5.6),
                    title="交易流程三时刻：仪式化压缩情绪的操作空间")
    doc.box(0.3, 5.8, 2.8, 3.4, "盘前 · 冷静时刻\n（做计划）\n① 查经济日历，标数据炸弹\n② 画结构：HTF 方向/关键位/流动性池\n③ 写计划：品种/setup/风险预算\n④ 确认状态：状态差→降预算或不做",
            ec=GREEN, fs=9, fc="#e8f5e9")
    doc.box(3.6, 5.8, 2.8, 3.4, "盘中 · 执行时刻\n（只执行）\n① checklist 逐条打勾再入场\n② 不看浮盈亏，只看是否符合计划\n③ 连亏 2 笔→强制休息\n④ 不临场改止损/仓位/目标",
            ec=BLUE, fs=9, fc="#e3f2fd")
    doc.box(6.9, 5.8, 2.8, 3.4, "盘后 · 复盘时刻\n（做记录）\n① 记录每笔交易（含心理状态）\n② 统计今天执行率\n③ 只深挖一笔最典型的对/错单",
            ec=ORANGE, fs=9, fc="#fff8e1")
    doc.arrow(3.1, 7.5, 3.6, 7.5, color=GRAY)
    doc.arrow(6.4, 7.5, 6.9, 7.5, color=GRAY)
    doc.text(5.0, 3.8, "决策（计划、复盘）都在冷静时刻做，盘中只剩执行——情绪最易失控的时段被规则框死", fs=11, color=DARK)
    doc.box(1.0, 1.1, 8.0, 1.8,
            "边界要物理化：计划写在纸上/文档里（不是脑子里）；盘中不打开新闻和社交软件；复盘用固定模板\n"
            "脑子的计划，情绪一上来就删了——边界越硬，情绪越没有操作空间",
            ec=DOWN, fs=9.5, fc="#fce4ec")
    doc.export(OUT)


# ---------------------------------------------------------------- 图 8-1 验证闭环
def fig_p8_verify_loop():
    doc = ExcaliDoc("fig_p8_verify_loop", xlim=(0, 13.4), ylim=(0, 7.4), figsize=(12.0, 6.4),
                    title="验证闭环（8.7）：回测→模拟盘→小资金实盘→复盘，不达标回到回测——没有达到门槛前，永远在练，不上真钱")
    doc.box(1.6, 5.6, 3.0, 1.3, "① 回测 100+ 笔\n期望值 > 0？\nSQN > 2？", ec=TEAL, fs=10.5)
    doc.box(8.8, 5.6, 3.0, 1.3, "② 模拟盘 100 笔\n执行率 > 90%？", ec=TEAL, fs=10.5)
    doc.box(8.8, 1.6, 3.0, 1.3, "③ 最小资金实盘\n验证情绪与执行", ec=ORANGE, fs=10.5)
    doc.box(1.6, 1.6, 3.0, 1.3, "④ 复盘 + 日志\n重算真实期望值", ec=ORANGE, fs=10.5)
    doc.arrow(4.6, 6.25, 8.8, 6.25, color=GRAY)
    doc.arrow(10.3, 5.6, 10.3, 2.9, color=GRAY)
    doc.arrow(8.8, 2.25, 4.6, 2.25, color=GRAY)
    doc.arrow(1.6, 2.9, 1.6, 5.6, rad=0.35, color=GRAY)
    doc.text(5.6, 4.1, "任一环节不达标 → 回到 ①\n“没有达到门槛前，永远在练，不上真钱”", fs=10, color=DARK)
    doc.export(OUT)


# ---------------------------------------------------------------- 图 8-2 复盘流水线
def fig_p8_review_flow():
    doc = ExcaliDoc("fig_p8_review_flow", xlim=(0, 14), ylim=(0, 6.4), figsize=(14.5, 6.2),
                    title="复盘体系（8.8）：日→周→月三层节奏，结论反馈回系统——复盘是持续验证的引擎")
    doc.box(0.5, 5.15, 13.0, 0.9, "复盘的核心不是「自责」，是「收集数据」——每笔交易无论对错，都是下一个决策的依据",
            ec=GRAY, fs=11)
    boxes = [
        (0.5, "日复盘（15 分钟）\n记录每笔（含心理状态）\n算当天执行率\n深入复盘 1 笔典型单", TEAL),
        (5.1, "周复盘（1 小时）\n胜率 / 盈亏比 / 期望 / 执行率\n对比上周：执行率↓？计划外？\n权益曲线是否接近警戒线\n这周盈亏是系统还是运气？", ORANGE),
        (9.7, "月复盘（半天）\n100+ 笔重算期望值\n砍掉持续亏损的 setup\n审视心理模式（7.5 高危画像）\n决定：继续 / 优化 / 暂停", GRAY),
    ]
    for i, (x, txt, col) in enumerate(boxes):
        doc.box(x, 2.3, 3.9, 2.45, txt, ec=col, fs=10)
        if i < 2:
            doc.arrow(x + 3.9, 3.52, x + 4.6, 3.52, color=GRAY)
    doc.box(0.5, 0.35, 13.0, 1.05, "决策反馈：继续 / 优化 / 暂停——把结论带回下一个日复盘（修正规则或坚持规则）",
            ec=TEAL, fs=10.5)
    doc.arrow(11.65, 2.3, 11.65, 1.4, color=DARK)
    doc.arrow(2.45, 1.4, 2.45, 2.3, color=DARK)
    doc.export(OUT)


# ---------------------------------------------------------------- 图 9-1 考核三段式
def fig_p9_prop_flow():
    doc = ExcaliDoc("fig_p9_prop_flow", xlim=(0, 13.6), ylim=(0, 6.6), figsize=(12.5, 5.8),
                    title="考核三段式（9.1）：Phase 1 → Phase 2 → Funded，各带盈利目标与回撤约束")
    doc.box(0.9, 3.0, 3.4, 2.2, "Phase 1 挑战\n盈利目标 8-10%\n日回撤 ≤5%\n总回撤 ≤8-10%", ec=DOWN, fs=10.5)
    doc.box(5.4, 3.0, 3.4, 2.2, "Phase 2 验证\n盈利目标 ≈5%\n规则相同\n验证不是运气", ec=ORANGE, fs=10.5)
    doc.box(9.9, 3.0, 3.4, 2.2, "Funded 实盘\n分成 80-90%\n回撤线仍在\n出金 14-30 天", ec=UP, fs=10.5)
    doc.arrow(4.3, 4.1, 5.4, 4.1, color=GRAY)
    doc.arrow(8.8, 4.1, 9.9, 4.1, color=GRAY)
    doc.text(4.85, 5.6, "主要淘汰关：目标最高、最容易重仓冲刺撞线", fs=9.5, color=DOWN)
    doc.text(11.6, 1.2, "不是终点：=「第二场考核」\n纪律不变，奖励从过线变现金流", fs=9.5, color=UP)
    doc.box(2.9, 6.0, 7.8, 0.6, "三段式考核：先定品种再选平台，读全规则（周末/新闻/一致性）", ec=DARK, fs=10.5)
    doc.export(OUT)


# ---------------------------------------------------------------- 图 10-6 期权策略决策树
def fig_p10_strategy_tree():
    doc = ExcaliDoc("fig_p10_strategy_tree", xlim=(0, 14), ylim=(0, 6.4), figsize=(14.5, 6.2),
                    title="期权策略决策树（10.6）：按「你想干什么」四分支选工具——名字可以忘，目的不能忘")
    doc.box(5.0, 5.05, 4.0, 0.95, "你想干什么？\n先有目的，再选工具（10.6）", ec=DARK, fs=11)
    branches = [
        (0.5, "怕仓位出事\n→ 保护性 Put\n买保险，锁最大回吐\n前提：趋势仓位想继续拿", TEAL),
        (4.0, "持仓想收租\n→ 备兑 Call\n卖虚值收权利金\n前提：震荡市、不指望大涨", ORANGE),
        (7.5, "有方向、锁风险\n→ 垂直价差\n买一卖一，净成本入场\n前提：盈利封顶可接受", DOWN),
        (11.0, "赌大波动不赌方向\n→ 跨式\nCall + Put 一起买\n前提：IV 没透支（10.5）", UP),
    ]
    for i, (x, txt, col) in enumerate(branches):
        doc.box(x, 2.55, 3.0, 2.1, txt, ec=col, fs=10)
        doc.arrow(7.0, 5.02, x + 1.5, 4.68, rad=-0.18 if i % 2 == 0 else 0.18, color=DARK)
    doc.box(0.5, 0.35, 13.0, 1.15,
            "四种用途 = 图 10-4 的四种到期损益形状：保险(保护性 Put) / 收租(备兑 Call) / 封顶方向(价差) / 波动(跨式)\n"
            "先定用途 → 再选形状 → 最后检查前提（IV 是否高位、是否接受封顶）",
            ec=GRAY, fs=10)
    doc.export(OUT)


def main():
    print("生成 Excalidraw 流程图（12 张）…")
    fig_p2_checklist()
    fig_p3_framework()
    fig_p4_breakout_flow()
    fig_p4_state_machine()
    fig_p4_state_tree()
    fig_p5_smc_flow()
    fig_p7_three_stages()
    fig_p7_flow()
    fig_p8_verify_loop()
    fig_p8_review_flow()
    fig_p9_prop_flow()
    fig_p10_strategy_tree()
    print("完成")


if __name__ == "__main__":
    main()
