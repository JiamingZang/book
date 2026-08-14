# -*- coding: utf-8 -*-
"""图 7-4R：报复交易的数学——同一批 82 笔交易，连亏后加倍 vs 固定风险
数据源：data/_bt_ema_trades.csv（EMA20/50 回测 82 笔真实逐笔 R，BTC 1H，2026-07-02 ~ 08-10）
规则：固定风险 = 每笔 0.5%；报复 = 每连亏 1 笔风险 ×mult（上限 20%），赢后归 0.5%
真实序列结果：
- 固定 0.5%：期末 0.9612（-3.9%）、最大回撤 -5.6%（不合格系统在纪律下也活着）
- ×1.5：期末 0.9268（-7.3%）、最大回撤 -9.0%（贴考核线）
- ×2：期末 0.8806（-11.9%）、最大回撤 -16.4%（爆考核 -10% 线）
- ×3：期末 0.5959（-40.4%）、最大回撤 -41.5%（账户腰斩）
最长连亏 6 笔（第 77-82 笔，08-09 起）：×2 策略该段风险 0.5%→1%→2%→4%→8%→16%
教学点（7.4 连亏应对 + 7.6 军规第 2 条）：
- 连亏是概率必然（P≥6=80.5%，图 7-2R），问题不是连亏本身，是连亏后的反应
- 报复交易把"连亏"（方差）变成"出局"（结果）；纪律者熬过 6 连亏只回撤 -5.6%
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#1565c0"     # 纪律（固定）
ORANGE = "#ef6c00"   # ×1.5
RED = "#e53935"      # ×2（爆考核）
DARKRED = "#8e1a1a"  # ×3（腰斩）
GRAY = "#90a4ae"
DARK = "#263238"
TEAL = "#00897b"

t = pd.read_csv("data/_bt_ema_trades.csv")
R = t["R"].values
N = len(R)

def sim(mult):
    risk = 0.005
    eq = 1.0
    curve = [1.0]
    risks = [risk]
    for r in R:
        eq *= 1 + risk * r
        curve.append(eq)
        if r < 0:
            risk = min(risk * mult, 0.20)
        else:
            risk = 0.005
        risks.append(risk)
    return np.array(curve), np.array(risks)

curves = {m: sim(m)[0] for m in [1.0, 1.5, 2.0, 3.0]}
risks2 = sim(2.0)[1]

fig, (ax, axr) = plt.subplots(
    2, 1, figsize=(15.8, 6.6), dpi=110, sharex=True,
    gridspec_kw={"height_ratios": [2.6, 1.0], "hspace": 0.08})

x = np.arange(N + 1)

# ---------- 上：资金曲线 ----------
styles = [
    (1.0, BLUE, "固定 0.5% 风险（纪律）", 2.6, 0),
    (1.5, ORANGE, "连亏 ×1.5", 1.7, 0),
    (2.0, RED, "连亏 ×2", 1.8, 0),
    (3.0, DARKRED, "连亏 ×3", 1.6, 0),
]
for m, color, label, lw, _ in styles:
    ax.plot(x, curves[m], color=color, lw=lw, zorder=4 if m != 1.0 else 6,
            label=label)

# 主要连亏段垂直虚线
streaks = [(5, 9), (24, 28), (46, 50), (76, 81)]
for a, b in streaks:
    ax.axvspan(a, b + 1, color=GRAY, alpha=0.12, zorder=1)
ax.axvspan(76, 82, color=RED, alpha=0.10, zorder=1)
ax.text(41, 0.955, "主要连亏段（7-2R 已证：这是 40% 胜率的正常分布）",
        fontsize=9, color=GRAY, ha="center", va="top", zorder=5)

# 最长 6 连亏段标注
ax.annotate("最长 6 连亏（第 77-82 笔）\nP(≥6)=80.5% 的正常分布\n×2 在此段风险 0.5%→16%",
            xy=(81, 0.90), xytext=(64, 0.82),
            fontsize=9.5, color=DARKRED, ha="center", va="center", zorder=7,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=RED, lw=1),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))

# 期末标注
for m, color, label, lw, _ in styles:
    y = curves[m][-1]
    dy = 0.018 if m == 1.0 else (0.016 if m == 1.5 else 0.012)
    ax.annotate(f"{label}\n期末 {y-1:+.1%}",
                xy=(N, y), xytext=(N + 1.5, y - dy),
                fontsize=9, color=color, ha="left", va="center", zorder=7,
                fontweight="bold" if m in (1.0, 2.0) else "normal")

ax.axhline(1.0, color=GRAY, lw=0.9, ls=":", zorder=2)
ax.text(N + 1.5, 1.003, "本金线", fontsize=8, color=GRAY, va="bottom")

ax.set_title("图 7-4R 报复交易的数学——同一批 82 笔交易，连亏后加倍 vs 固定风险（数据：EMA20/50 回测 82 笔真实逐笔，BTC 1H，2026-07-02 ~ 08-10）",
             fontsize=11, color=DARK, loc="left")
ax.set_ylabel("账户净值（初始 = 1.0）", fontsize=10)
ax.set_ylim(0.55, 1.045)
ax.set_xlim(-2, 94)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#eceff1", lw=0.7)
ax.legend(loc="lower left", fontsize=9, frameon=False)
ax.set_xticks([])

# 考核 -10% 回撤提示
ax.text(88, 0.615, "×3 期末 −40.4%\n（账户腰斩）", fontsize=9, color=DARKRED,
        ha="center", va="bottom", zorder=7,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor=DARKRED, lw=1))

# ---------- 下：×2 策略风险锯齿 ----------
axr.step(x, risks2 * 100, where="post", color=RED, lw=1.4, zorder=3)
axr.axhline(0.5, color=BLUE, lw=1.4, ls="--", zorder=2)
axr.text(1, 0.62, "基准 0.5%（纪律线）", fontsize=8.5, color=BLUE, ha="left", va="bottom")
axr.annotate("连亏 6 笔 → 风险翻倍 5 次：\n0.5% → 16%", xy=(80.5, 16), xytext=(60, 13.5),
             fontsize=9, color=RED, ha="center", va="center", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
axr.set_title("×2 策略的单笔风险：每连亏 1 笔翻倍，赢 1 笔归位——第 77-82 笔连亏时风险已失控到 16%（= 32 倍基准）",
              fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axr.spines[s].set_visible(False)
axr.set_ylabel("单笔风险（%）", fontsize=10)
axr.set_yticks([0.5, 4, 8, 12, 16, 20])
axr.set_ylim(0, 21)

# 底部时间刻度（按笔序号 → 日期，每 10 笔）
tick_idx = list(range(0, N + 1, 10))
axr.set_xticks(tick_idx)
axr.set_xticklabels([f"#{i}" for i in tick_idx], fontsize=8, color=GRAY)
axr.tick_params(length=0)
axr.set_xlim(-2, 94)

fig.text(0.995, 0.008, "模拟：同一 R 序列 × 4 种资金管理规则；每笔风险 = 单笔亏损 ±0.5%×R · 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)

plt.savefig("handbook/images/fig_real_ch7_revenge.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved handbook/images/fig_real_ch7_revenge.png")
