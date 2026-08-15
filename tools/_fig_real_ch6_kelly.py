# -*- coding: utf-8 -*-
"""图 6-5R 真实数据：凯利公式在真实回测上——"满凯利"与"凯利说别交易"
（EMA20/50 趋势跟踪回测，BTC 1H，2026-07-02 ~ 08-10，82 笔，总 R -7.83，验证不合格——同图 8-1R 数据）
- 上：同一批真实 R 序列 × 3 种下注信念的资金曲线：
    乐观满凯利 10%（新手按 40% 胜率/2 盈亏比套公式）→ 第 20 笔就打穿 -10% 考核线
    半凯利 5% → 第 27 笔打穿；1/4 凯利 2.5% → 期末勉强活着
    纪律 0.5% 固定风险 → 全程没碰线，期末 -3.9%（负期望系统只有轻仓能活）
  真实 f* 用样本估计 = -24%（负期望系统，凯利的数学答案是"空仓别交易"）
- 下：滚动 f* 估计——用前 k 笔估计胜率/盈亏比再套凯利：
    前 20 笔 f*≈+3%（看起来能下注），前 40 笔转负，全部 82 笔 → -24%
  ——凯利三个陷阱里"输入不准"的真实形态：回测样本越少，f* 越可能是幻觉
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 字体 fallback：Windows 用雅黑，Linux 用文泉驿
_zh = None
for cand in ["Microsoft YaHei", "WenQuanYi Zen Hei"]:
    if any(f.name == cand for f in font_manager.fontManager.ttflist):
        _zh = cand
        break
plt.rcParams["font.family"] = _zh or "sans-serif"
plt.rcParams["axes.unicode_minus"] = False

BLUE, ORANGE = "#1565c0", "#ef6c00"
RED, TEAL, GRAY, DARK = "#ef5350", "#00897b", "#90a4ae", "#263238"

# ---- 读取真实回测交易 ----
trades = []
with open("data/_bt_ema_trades.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        trades.append(float(row["R"]))
R = np.array(trades)
N = len(R)
idx = np.arange(1, N + 1)

# 真实样本统计（与图 8-1R 一致）
p = (R > 0).mean()
wins, losses = R[R > 0], R[R <= 0]
b = wins.mean() / abs(losses.mean()) if len(losses) else 0.0
fstar = (b * p - (1 - p)) / b if b > 0 else -1.0  # 真实 f*（负期望→负值）

# ---- 三条"信念"资金曲线 ----
# 乐观新手：以为 p=0.4, b=2 → f*=10%（正文示例），上满/半/1/4 凯利
kelly_opt = 0.10
curves = {}
for name, frac in [("满凯利 10%", 1.0), ("半凯利 5%", 0.5), ("1/4 凯利 2.5%", 0.25)]:
    f = kelly_opt * frac
    curves[name] = np.cumprod(1 + f * R)
curves["纪律 0.5% 固定风险"] = np.cumprod(1 + 0.005 * R)

# 各曲线打穿 -10% 线的真实笔数（供标注）
cross_n = {}
for name, f in [("满凯利 10%", 0.10), ("半凯利 5%", 0.05), ("1/4 凯利 2.5%", 0.025)]:
    eq = np.cumprod(1 + f * R)
    cross_n[name] = int(np.argmax(eq < 0.9) + 1) if (eq < 0.9).any() else None

# ---- 滚动 f* 估计 ----
roll_k = []
roll_f = []
for k in range(5, N + 1):
    sub = R[:k]
    pp = (sub > 0).mean()
    ww, ll = sub[sub > 0], sub[sub <= 0]
    if len(ww) and len(ll):
        bb = ww.mean() / abs(ll.mean())
        ff = (bb * pp - (1 - pp)) / bb if bb > 0 else -1.0
    else:
        ff = np.nan
    roll_k.append(k)
    roll_f.append(ff)
roll_k = np.array(roll_k)
roll_f = np.array(roll_f)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14.2, 8.6), dpi=110,
                               gridspec_kw={"height_ratios": [1.2, 1]})
fig.patch.set_facecolor("white")
for ax in (ax1, ax2):
    ax.set_facecolor("white")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# ===== 上：资金曲线 =====
for name, eq in curves.items():
    c = RED if name == "满凯利 10%" else (ORANGE if name == "半凯利 5%" else (TEAL if name == "1/4 凯利 2.5%" else BLUE))
    cn = cross_n.get(name)
    label = name + (f"（第 {cn} 笔打穿 -10% 线）" if cn else "")
    ax1.plot(idx, eq, drawstyle="steps-post", color=c, lw=1.8, label=label)

ax1.axhline(1.0, color=GRAY, lw=1, ls=":")
ax1.axhline(0.9, color=GRAY, lw=1.2, ls="--")
ax1.text(0.5, 0.898, "典型 prop 考核总回撤线 -10%",
         fontsize=9, color=GRAY, va="top", zorder=6)

# 打穿点标注
for name, col in [("满凯利 10%", RED), ("半凯利 5%", ORANGE), ("1/4 凯利 2.5%", TEAL)]:
    cn = cross_n.get(name)
    if not cn:
        continue
    eq = curves[name]
    ax1.annotate(f"{name}\n第 {cn} 笔净值 {eq[cn - 1]:.2f}——打穿出局",
                 xy=(cn, eq[cn - 1]), xytext=(cn + 6, 0.52),
                 fontsize=9.5, color=col, fontweight="bold", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=col, lw=1.2))
# 纪律曲线终点标注
ax1.annotate("纪律 0.5%：全程没碰线\n期末 -3.9%——负期望系统只有轻仓能活",
             xy=(N, curves["纪律 0.5% 固定风险"][-1]), xytext=(30, 1.06),
             fontsize=9.5, color=BLUE, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))

ax1.set_ylabel("账户净值（起点 = 1.0）", fontsize=10)
ax1.set_title("同样的 82 笔真实交易：凯利公式的三种用法，三种命运（乐观满凯利最先出局；真实 f* = -23% 表示凯利的答案是“别交易”）",
              fontsize=12.5, color=DARK, pad=12)
ax1.legend(loc="lower left", fontsize=9.5, frameon=False)
ax1.grid(axis="y", color="#eceff1", lw=0.7)
ax1.set_xticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 82])
ax1.set_xlim(0.5, N + 1)

# ===== 下：滚动 f* 估计 =====
ax2.plot(roll_k, roll_f, color=DARK, lw=1.8, zorder=5)
ax2.axhline(0, color=GRAY, lw=1, ls=":")
ax2.axhline(fstar, color=RED, lw=1.4, ls="--")
ax2.text(2, fstar + 0.02, f"全部 82 笔：f* = {fstar * 100:.0f}%（负期望 → 空仓）",
         fontsize=9.5, color=RED, fontweight="bold", zorder=6)

# 前 20 笔"幻觉正 f*"标注
k20 = roll_f[np.searchsorted(roll_k, 20) - 1]
ax2.annotate(f"前 20 笔：f* ≈ +{k20 * 100:.0f}%\n（回测 20 笔时以为能下注）",
             xy=(20, k20), xytext=(28, 0.30),
             fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))
ax2.annotate("样本越多越接近真相：凯利的“输入不准”\n不是误差小问题，是样本量问题（呼应 8-2R）",
             xy=(70, roll_f[np.searchsorted(roll_k, 70) - 1]), xytext=(46, 0.55),
             fontsize=9.5, color=DARK, zorder=6,
             arrowprops=dict(arrowstyle="->", color=DARK, lw=1.1))

ax2.set_xlabel("已观察的交易笔数 k", fontsize=10)
ax2.set_ylabel("用前 k 笔估计的 f*", fontsize=10)
ax2.set_title("滚动 f* 估计：输入不准的根源是样本量（真实 82 笔，EMA20/50，BTC 1H）",
              fontsize=11.5, color=DARK, pad=10)
ax2.grid(axis="y", color="#eceff1", lw=0.7)
ax2.set_xticks([5, 20, 40, 60, 82])
ax2.set_xlim(2, N + 1)
ax2.set_ylim(min(np.nanmin(roll_f), fstar) - 0.08, 0.45)

fig.text(0.995, 0.012, "数据源：Binance BTCUSDT 5m K 线重采样 1H 回测（82 笔）· 教学示意，不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig("handbook/images/fig_real_ch6_kelly.png", bbox_inches="tight", facecolor="white")
print("saved: handbook/images/fig_real_ch6_kelly.png")
print(f"p={p:.3f} b={b:.3f} fstar={fstar*100:.1f}%")
