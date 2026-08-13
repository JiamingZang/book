# -*- coding: utf-8 -*-
"""批次35：4张新合成图
A. fig_p4_breakout_flow.png  图4-4 突破生命周期流程（4.5）
B. fig_p4_trailing_stop.png  图4-8 移动止损机制（4.15）
C. fig_p6_atr.png            图6-3 ATR止损与波动率（6.5）
D. fig_p7_flow.png           图7-4 交易三时刻流程（7.3）
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

RED, GREEN, GRAY = "#ef5350", "#26a69a", "#90a4ae"
BLUE, ORANGE, DARK, TEAL, PURPLE = "#1565c0", "#ef6c00", "#263238", "#00897b", "#6a1b9a"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

# ============ A. 突破生命周期流程 ============
fig, ax = plt.subplots(figsize=(13, 7.2), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def box(x, y, w, h, text, fc="#e3f2fd", ec=BLUE, fs=10.5, bold=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6",
                                facecolor=fc, edgecolor=ec, lw=1.6, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=DARK, fontweight="bold" if bold else "normal", zorder=4)


def arrow(x1, y1, x2, y2, color=GRAY, text=None, tx=0, ty=0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=18, color=color, lw=1.8, zorder=2))
    if text:
        ax.text((x1 + x2) / 2 + tx, (y1 + y2) / 2 + ty, text, ha="center", va="center",
                fontsize=9, color=color, fontweight="bold", zorder=5,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="none"))

box(34, 88, 32, 8, "区间压缩（波动收缩）\n价格贴近区间边界", fc="#fff8e1", ec=ORANGE)
arrow(50, 88, 50, 82)
box(34, 70, 32, 9, "突破发生\n大实体收盘在区间外 + 放量", fc="#e8f5e9", ec=GREEN)
arrow(50, 70, 50, 64)
box(34, 52, 32, 9, "无回调：突破仍在进行\n价格同向走，缺口在扩大", fc="#e3f2fd", ec=BLUE)
arrow(50, 52, 50, 46)
box(30, 34, 40, 9, "出现回调：突破结束（或失败）\n市场开始测试突破点", fc="#fce4ec", ec=RED)

# 分叉
arrow(38, 34, 22, 26, color=GREEN, text="测试守住", tx=8, ty=3)
box(3, 16, 28, 8, "测试成功：缺口升级\n= 测量缺口（MG）\n预期同向第二波", fc="#e8f5e9", ec=GREEN, fs=9.5)
arrow(62, 34, 78, 26, color=RED, text="测试失败", tx=-6, ty=3)
box(69, 16, 28, 8, "测试失败：缺口闭合\n= 衰竭缺口（EG）\n反转信号", fc="#fce4ec", ec=RED, fs=9.5)

# 循环：失败回调可成新突破
arrow(83, 16, 83, 10, color=PURPLE)
box(60, 1, 40, 7, "失败的回调本身可成新突破：\n关闭缺口的那根 K 线收盘站对方向，\n同方向至少再期待一根 K 线", fc="#f3e5f5", ec=PURPLE, fs=9)
arrow(60, 4.5, 34, 4.5, color=PURPLE)
box(8, 1, 22, 7, "回到区间压缩状态\n循环重新开始", fc="#fff8e1", ec=ORANGE, fs=9.5)

ax.set_title("突破的完整生命周期：突破 → 制造缺口 → 测试 → 缺口升级或降级（你等的不是突破那一下，是测试的结果）",
             fontsize=12.5, color=DARK, pad=12)
fig.tight_layout()
fig.savefig("handbook/images/fig_p4_breakout_flow.png", bbox_inches="tight", facecolor="white")
print("saved: fig_p4_breakout_flow.png")

# ============ B. 移动止损机制 ============
rng = np.random.default_rng(7)
n = 60
x = np.arange(n)
# 上升趋势价格路径：HH+HL
trend = 0.10 * np.cumsum(rng.normal(0.08, 0.3, n))
wave = 0.35 * np.sin(np.arange(n) / 4.2)
close = 50 + trend + wave + rng.normal(0, 0.06, n)
high = close + np.abs(rng.normal(0, 0.22, n))
low = close - np.abs(rng.normal(0, 0.22, n))

fig, ax = plt.subplots(figsize=(13, 6.2), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# K 线简化
for i in range(n):
    c = RED if close[i] >= close[i - 1] else GREEN
    ax.plot([x[i], x[i]], [low[i], high[i]], color=c, lw=0.7)
    ax.plot([x[i], x[i]], [min(close[i], close[i-1]) if i else close[i], close[i]], color=c, lw=2.2)

# HL 标注（找局部低点）
hl_idx = []
for i in range(3, n - 3):
    if low[i] <= min(low[i-3:i]) and low[i] <= min(low[i+1:i+4]):
        hl_idx.append(i)
for i in hl_idx:
    ax.plot(x[i], low[i], marker="v", color=TEAL, ms=7, zorder=5)
ax.annotate("每个新 HL（更高低点）\n收盘确认后移动止损", xy=(x[hl_idx[2]], low[hl_idx[2]]),
            xytext=(x[hl_idx[2]] - 6, low[hl_idx[2]] + 1.2), fontsize=9.5, color=TEAL,
            fontweight="bold", arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 结构移动止损阶梯
levels = [close[0] - 1.0]
for i in hl_idx:
    lv = low[i] - 0.12
    if lv > levels[-1]:
        levels.append(lv)
xs = [0] + [x[hl_idx[k]] for k in range(min(len(levels) - 1, len(hl_idx)))]
for k in range(1, len(levels)):
    ax.hlines(levels[k], xs[k], xs[k] + 8 if k < len(levels) - 1 else n - 1,
              color=BLUE, lw=2.0, zorder=4)
    if k < len(levels) - 1:
        ax.vlines(xs[k] + 8, levels[k], levels[k + 1], color=BLUE, lw=2.0, zorder=4)
ax.text(n - 14, levels[-1] + 0.25, "结构移动法：止损=最新 HL 下方\n只进不退", fontsize=10,
        color=BLUE, fontweight="bold")

# ATR 移动法（近似平行通道）
atr = np.convolve(np.abs(high - low), np.ones(5) / 5, mode="same")
up_line = close + 1.6 * atr
dn_line = close - 1.6 * atr
ax.plot(x, dn_line, color=ORANGE, lw=1.5, ls="--", zorder=3)
ax.fill_between(x, up_line, dn_line, color=ORANGE, alpha=0.06, zorder=1)
ax.text(n - 16, dn_line[-1] - 0.8, "ATR 移动法：止损=k×ATR 通道\n（不盯结构，但正常回调可能扫掉）", fontsize=10,
        color=ORANGE, fontweight="bold")

# 入场标注
ax.plot(0, close[0], marker="o", color=DARK, ms=8, zorder=5)
ax.annotate("入场", xy=(0, close[0]), xytext=(2, close[0] + 1.1), fontsize=10,
            color=DARK, fontweight="bold", arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

ax.set_title("移动止损的两种机制：结构移动法（HL 阶梯，只进不退） vs ATR 移动法（平行通道跟随）",
             fontsize=13, color=DARK, pad=12)
ax.set_xlabel("K 线序号（示意）", fontsize=10)
ax.set_ylabel("价格", fontsize=10)
ax.grid(axis="y", color="#eceff1", lw=0.7)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("handbook/images/fig_p4_trailing_stop.png", bbox_inches="tight", facecolor="white")
print("saved: fig_p4_trailing_stop.png")

# ============ C. ATR 通道 ============
rng = np.random.default_rng(11)
n = 90
x = np.arange(n)
vol = 0.18 + 0.5 * (1 + np.tanh((x - 55) / 9))  # 波动率先收缩后扩张
center = 100 + 6 * np.sin(x / 16) + 0.05 * x
noise = rng.normal(0, 1, n) * vol
close2 = center + noise
atr2 = np.convolve(np.abs(np.diff(close2, prepend=close2[0])), np.ones(5) / 5, mode="same")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 6.8), dpi=110, sharex=True,
                               gridspec_kw={"height_ratios": [3, 1]})
fig.patch.set_facecolor("white")
for axx in (ax1, ax2):
    axx.set_facecolor("white")

# 上：价格 + ATR 通道
ax1.plot(x, close2, color=DARK, lw=1.4, zorder=3)
ax1.fill_between(x, close2 + 1.5 * atr2, close2 - 1.5 * atr2, color=BLUE, alpha=0.12, zorder=1)
ax1.plot(x, close2 + 1.5 * atr2, color=BLUE, lw=1.2, ls="--")
ax1.plot(x, close2 - 1.5 * atr2, color=BLUE, lw=1.2, ls="--")
ax1.annotate("低波动期：通道窄\n固定 50 点止损 = \"大\"止损\n（正常波动都装不下）", xy=(20, close2[20] + 1.5 * atr2[20]),
             xytext=(6, 112), fontsize=9.5, color=ORANGE, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
ax1.annotate("高波动期：通道宽\n固定 50 点止损 = \"小\"止损\n（连噪音都盖不住，必被扫）", xy=(72, close2[72] + 1.5 * atr2[72]),
             xytext=(52, 88), fontsize=9.5, color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax1.axhline(100, color=GRAY, lw=1, ls=":")
ax1.text(2, 100.6, "固定止损 50 点（不随波动率调整）", fontsize=9, color=GRAY)
ax1.set_title("ATR 止损：同样的固定点数，不同波动率下含义完全不同——止损距离应 = k × ATR(14)",
              fontsize=12.5, color=DARK, pad=10)
ax1.set_ylabel("价格", fontsize=10)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
for s in ["top", "right"]:
    ax1.spines[s].set_visible(False)

# 下：ATR 柱
ax2.bar(x, atr2, color="#90caf9", width=0.8, zorder=3)
ax2.set_ylabel("ATR(14)", fontsize=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
for s in ["top", "right"]:
    ax2.spines[s].set_visible(False)
ax2.text(30, atr2.max() * 0.65, "波动收缩（ATR 走低）", fontsize=9.5, color=ORANGE, fontweight="bold")
ax2.text(62, atr2.max() * 0.65, "波动扩张（ATR 走高）", fontsize=9.5, color=RED, fontweight="bold")

fig.tight_layout()
fig.savefig("handbook/images/fig_p6_atr.png", bbox_inches="tight", facecolor="white")
print("saved: fig_p6_atr.png")

# ============ D. 交易三时刻流程 ============
fig, ax = plt.subplots(figsize=(13, 5.6), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def card(x, w, title, items, fc, ec, ty=58):
    ax.add_patch(FancyBboxPatch((x, ty), w, 34, boxstyle="round,pad=0.7",
                                facecolor=fc, edgecolor=ec, lw=2, zorder=3))
    ax.text(x + w / 2, ty + 29, title, ha="center", va="center", fontsize=13,
            color=DARK, fontweight="bold", zorder=4)
    for k, it in enumerate(items):
        ax.text(x + 4, ty + 23 - k * 5.4, it, fontsize=9.5, color=DARK, zorder=4, va="top")


card(3, 28, "盘前 · 冷静时刻\n（做计划）",
     ["① 查经济日历，标数据炸弹", "② 画结构：HTF 方向/关键位/流动性池", "③ 写计划：品种/setup/风险预算", "④ 确认状态：状态差→降预算或不做"],
     "#e8f5e9", GREEN)
card(36, 28, "盘中 · 执行时刻\n（只执行）",
     ["① checklist 逐条打勾再入场", "② 不看浮盈亏，只看是否符合计划", "③ 连亏 2 笔→强制休息", "④ 不临场改止损/仓位/目标"],
     "#e3f2fd", BLUE)
card(69, 28, "盘后 · 复盘时刻\n（做记录）",
     ["① 记录每笔交易（含心理状态）", "② 统计今天执行率", "③ 只深挖一笔最典型的对/错单"],
     "#fff8e1", ORANGE)

# 箭头
ax.add_patch(FancyArrowPatch((33, 75), (35, 75), arrowstyle="-|>", mutation_scale=20, color=GRAY, lw=2, zorder=2))
ax.add_patch(FancyArrowPatch((66, 75), (68, 75), arrowstyle="-|>", mutation_scale=20, color=GRAY, lw=2, zorder=2))

# 底部说明
ax.text(50, 38, "决策（计划、复盘）都在冷静时刻做，盘中只剩执行——情绪最易失控的时段被规则框死",
        ha="center", fontsize=11.5, color=DARK, fontweight="bold")
ax.add_patch(FancyBboxPatch((10, 12), 80, 18, boxstyle="round,pad=0.7",
                            facecolor="#fce4ec", edgecolor=RED, lw=1.5, zorder=3))
ax.text(50, 21, "边界要物理化：计划写在纸上/文档里（不是脑子里）；盘中不打开新闻和社交软件；复盘用固定模板\n"
                "脑子的计划，情绪一上来就删了——边界越硬，情绪越没有操作空间",
        ha="center", va="center", fontsize=9.5, color=DARK, zorder=4)

ax.set_title("交易流程三时刻：仪式化压缩情绪的操作空间", fontsize=13.5, color=DARK, pad=12)
fig.tight_layout()
fig.savefig("handbook/images/fig_p7_flow.png", bbox_inches="tight", facecolor="white")
print("saved: fig_p7_flow.png")
