# -*- coding: utf-8 -*-
"""图 9-3R 真实数据：考核通过率 Monte Carlo——同一批 82 笔真实交易 × 7 档单笔风险 × 重排 20000 次
- 数据：EMA20/50 回测 82 笔真实逐笔记录（BTC 1H，2026-07-02 ~ 08-10，data/_bt_ema_trades.csv）
- 规则：+8% 达标（峰值碰线即过，图 9-2R 同口径）、-10% 总回撤出局（峰值回撤打穿即出局）
- 上：MC 重排 20000 次 × 7 档风险的堆叠概率条形（灰=平庸 红=出局 绿=达标）
     低风险 0.25%/0.5% 平庸 100%（考核费无限续费）；1.0% 出局 15.3% 开始出现；
     1.5%+ 出局 86.6%~99%（重仓送分）；达标率最高仅 13.4%（3.0% 档）
- 下左：真实顺序确定性模拟 7 档终值——0.25%~1.0% 平庸、1.5%/2.0% 出局、3.0% 碰巧达标
     展示"单次样本会骗人"（呼应 8.2 样本量幻觉 / 7.3 近因偏差）
- 下右：达标率/出局率随风险曲线——风险越高出局率冲顶，达标率永远起不来
- 教学结论：负期望系统买考核，低风险=平庸、中风险=出局开始出现、高风险=出局为主；
     达标率最高仅 13.4%——先回测验证（8.2/8.7）再买考核
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GREEN, RED, GRAY, DARK = "#26a69a", "#ef5350", "#90a4ae", "#263238"
BLUE, AMBER = "#1565c0", "#ffb300"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

rng = np.random.default_rng(20260814)
tr = pd.read_csv("data/_bt_ema_trades.csv")
R = tr["R"].values  # 82 笔真实 R
assert len(R) == 82

RISKS = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
TARGET, DD_LIM = 0.08, -0.10  # +8% 达标 / -10% 总回撤出局
N_MC = 20000


def run_sim(seq, risk):
    """逐笔模拟：返回 (结局, 最终净值, 出局笔数, 达标笔数)
    结局: 'pass' 达标 / 'blow' 出局 / 'medi' 平庸
    顺序: 每笔更新净值 → 先看峰值是否碰 +8%（达标）→ 再看回撤是否打穿 -10%（出局）
    """
    risk = risk / 100.0
    eq = 1.0
    peak = 1.0
    for i, r in enumerate(seq):
        eq *= (1.0 + r * risk)
        if eq > peak:
            peak = eq
        if peak >= 1.0 + TARGET:
            return "pass", eq, i + 1, i + 1
        if eq / peak - 1.0 <= DD_LIM:
            return "blow", eq, i + 1, i + 1
    return "medi", eq, len(seq), len(seq)


def mc(risk, n=N_MC):
    n_pass = n_blow = 0
    for _ in range(n):
        out = run_sim(rng.permutation(R), risk)
        if out[0] == "pass":
            n_pass += 1
        elif out[0] == "blow":
            n_blow += 1
    n_medi = n - n_pass - n_blow
    return n_pass / n * 100, n_blow / n * 100, n_medi / n * 100


# ===== 数据 =====
mc_p, mc_b, mc_m = [], [], []
real_ends, real_kinds, real_at = [], [], []
for risk in RISKS:
    p, b, m = mc(risk)
    mc_p.append(p); mc_b.append(b); mc_m.append(m)
    kind, eq, at, _ = run_sim(R, risk)
    real_kinds.append(kind)
    real_ends.append(eq)
    real_at.append(at)

# 打印校验（正文数字必须与之一致）
print("=== MC 20000 次（风险%: 达标% 出局% 平庸%）===")
for risk, p, b, m in zip(RISKS, mc_p, mc_b, mc_m):
    print(f"  {risk:>4}%: 达标 {p:.1f}%  出局 {b:.1f}%  平庸 {m:.1f}%")
print("=== 真实顺序确定性（风险%: 结局 终值 出局/达标笔数）===")
for risk, k, e, a in zip(RISKS, real_kinds, real_ends, real_at):
    tag = {"pass": "达标", "blow": "出局", "medi": "平庸"}[k]
    print(f"  {risk:>4}%: {tag}  终值 {(e - 1) * 100:+.1f}%  第{a}笔")
print(f"总R {R.sum():.2f}  胜率 {(R > 0).mean() * 100:.1f}%  82笔")

# ===== 绘图 =====
fig = plt.figure(figsize=(13, 8.6), dpi=110)
fig.patch.set_facecolor("white")
gs = fig.add_gridspec(2, 2, height_ratios=[1.18, 1], width_ratios=[1.35, 1],
                      hspace=0.42, wspace=0.18,
                      left=0.065, right=0.985, top=0.92, bottom=0.075)

# ---- 上：MC 堆叠概率条（占两列宽）----
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(RISKS))
w = 0.62
ax1.bar(x, mc_m, w, color=GRAY, label="平庸（不达标不出局）", zorder=3)
ax1.bar(x, mc_b, w, bottom=mc_m, color=RED, label="出局（打穿 -10% 总回撤）", zorder=3)
ax1.bar(x, mc_p, w, bottom=[a + b for a, b in zip(mc_m, mc_b)], color=GREEN,
        label="达标（碰到 +8% 目标）", zorder=3)

# 每档标注关键数字
for i, (risk, p, b, m) in enumerate(zip(RISKS, mc_p, mc_b, mc_m)):
    if m > 0:
        ax1.text(i, m / 2, f"平庸\n{m:.1f}%", ha="center", va="center",
                 fontsize=8.5, color="white", fontweight="bold", zorder=6)
    if b > 0:
        ax1.text(i, m + b / 2, f"出局\n{b:.1f}%", ha="center", va="center",
                 fontsize=8.5, color="white", fontweight="bold", zorder=6)
    if p > 0:
        ax1.text(i, m + b + p / 2, f"达标\n{p:.1f}%", ha="center", va="center",
                 fontsize=8.5, color="white", fontweight="bold", zorder=6)

# 顶部注释箭头（针对三档关键档）
ax1.annotate("低风险：平庸 100%\n0% 达标、0% 出局\n→ 考核费无限续费", xy=(0, 100),
             xytext=(-0.15, 118), fontsize=9.5, color=GRAY, fontweight="bold",
             ha="center", zorder=6,
             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1))
ax1.annotate("中风险：出局开始出现\n（1.0% 出局 {:.1f}%）".format(mc_b[3]),
             xy=(3, mc_b[3] + mc_m[3]),
             xytext=(3.1, 118), fontsize=9.5, color=RED, fontweight="bold",
             ha="center", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
ax1.annotate("高风险：出局为主\n（1.5%+ 出局 {:.1f}%~{:.1f}%）\n达标率最高仅 {:.1f}%".format(
                 mc_b[4], max(mc_b), max(mc_p)),
             xy=(6, mc_b[6] + mc_m[6]),
             xytext=(5.9, 130), fontsize=9.5, color=RED, fontweight="bold",
             ha="center", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))

ax1.set_xticks(x)
ax1.set_xticklabels([f"{r:.2g}%" if r < 1 else f"{r:g}%" for r in RISKS], fontsize=10)
ax1.set_xlabel("单笔风险（82 笔真实 R 随机重排 × 20000 次模拟）", fontsize=10)
ax1.set_ylabel("模拟占比（%）", fontsize=10)
ax1.set_ylim(0, 142)
ax1.set_title("同一批 82 笔真实交易（总 R −7.83，期望为负）× 7 档风险：考核结局的概率分布",
              fontsize=13, color=DARK, pad=10)
ax1.legend(loc="upper left", fontsize=9, frameon=False, ncol=3)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
for s in ["top", "right"]:
    ax1.spines[s].set_visible(False)
ax1.axhline(0, color=GRAY, lw=1)

# ---- 下左：真实顺序确定性结局 ----
ax2 = fig.add_subplot(gs[1, 0])
bar_colors = [{"pass": GREEN, "blow": RED, "medi": GRAY}[k] for k in real_kinds]
vals = [(e - 1) * 100 for e in real_ends]
bars = ax2.bar(x, vals, w, color=bar_colors, alpha=0.9, zorder=3)
# 出局档画成 -10% 线以下的打叉（表示中途撞线作废）
for i, (k, e) in enumerate(zip(real_kinds, real_ends)):
    tag = {"pass": "达标", "blow": "出局", "medi": "平庸"}[k]
    if k == "blow":
        ax2.text(i, -11.5, f"{tag}\n(第{real_at[i]}笔撞线)", ha="center", va="top",
                 fontsize=8.5, color=RED, fontweight="bold", zorder=6)
        ax2.plot([i - 0.25, i + 0.25], [-11, -11], color=RED, lw=2, zorder=6)
    else:
        ax2.text(i, vals[i] + (0.6 if k == "pass" else -0.9), f"{tag}\n{vals[i]:+.1f}%",
                 ha="center", va="bottom" if k == "pass" else "top",
                 fontsize=8.5, color=DARK if k == "medi" else GREEN,
                 fontweight="bold", zorder=6)
ax2.axhline(0, color=GRAY, lw=1)
ax2.axhline(8, color=GREEN, lw=1.2, ls="--")
ax2.axhline(-10, color=RED, lw=1.2, ls="--")
ax2.text(6.35, 8.4, "+8% 目标", fontsize=8, color=GREEN, ha="right", fontweight="bold")
ax2.text(6.35, -10.8, "-10% 出局线", fontsize=8, color=RED, ha="right", fontweight="bold")
ax2.annotate("3.0% 真实那次碰巧达标\n——但 MC 说它出局率 86.6%、\n达标率仅 13.4%（见上图）",
             xy=(6, vals[6]), xytext=(3.6, 14),
             fontsize=9, color=AMBER, fontweight="bold", zorder=6,
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=AMBER, lw=1.2),
             arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.2))
ax2.set_xticks(x)
ax2.set_xticklabels([f"{r:.2g}%" if r < 1 else f"{r:g}%" for r in RISKS], fontsize=10)
ax2.set_ylabel("真实顺序终值（净值 − 1，%）", fontsize=9.5)
ax2.set_ylim(-14.5, 17)
ax2.set_title("真实顺序只有一次：0.25%~1.0% 平庸、\n1.5%/2.0% 出局、3.0% 碰巧达标",
              fontsize=11.5, color=DARK, pad=8)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
for s in ["top", "right"]:
    ax2.spines[s].set_visible(False)

# ---- 下右：达标率/出局率随风险曲线 ----
ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(x, mc_p, color=GREEN, lw=2.4, marker="o", ms=5, zorder=4, label="达标率")
ax3.plot(x, mc_b, color=RED, lw=2.4, marker="s", ms=5, zorder=4, label="出局率")
ax3.fill_between(x, 0, mc_b, color=RED, alpha=0.10, zorder=2)
ax3.axhline(50, color=GRAY, lw=1, ls=":")
ax3.text(0.05, 52, "50% 生死线", fontsize=8.5, color=GRAY, fontweight="bold")
ax3.annotate("出局率冲顶：\n1.5% 起 95%+", xy=(4, mc_b[4]), xytext=(4.6, 30),
             fontsize=9, color=RED, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
ax3.annotate("达标率永远起不来：\n全档最高 13.4%", xy=(6, mc_p[6]), xytext=(2.0, 22),
             fontsize=9, color=GREEN, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
ax3.set_xticks(x)
ax3.set_xticklabels([f"{r:.2g}%" if r < 1 else f"{r:g}%" for r in RISKS], fontsize=9)
ax3.set_xlabel("单笔风险", fontsize=10)
ax3.set_ylabel("MC 概率（%）", fontsize=9.5)
ax3.set_ylim(0, 108)
ax3.set_title("达标率 vs 出局率：\n风险调高只加快出局，救不了达标",
              fontsize=11.5, color=DARK, pad=8)
ax3.legend(loc="center left", fontsize=9, frameon=False)
ax3.grid(axis="y", color="#eceff1", lw=0.7)
for s in ["top", "right"]:
    ax3.spines[s].set_visible(False)

fig.text(0.985, 0.012, "数据源：Binance BTCUSDT 5m K 线重采样 1H 真实回测逐笔记录（82 笔）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.savefig("handbook/images/fig_real_ch9_passrate.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch9_passrate.png")
