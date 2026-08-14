# -*- coding: utf-8 -*-
"""图 2-4R 真实数据：8 状态周期频谱拼图（BTC 5m，2026-06-29 ~ 07-02）
- 数据：Binance BTCUSDT 5m K 线（data/btcusdt_5m.csv）
- 2×4 网格：从强到弱 8 种市场状态各取真实片段——尖峰/微型通道/紧凑通道/常规通道/
  宽通道/趋势型区间/交易区间/极端区间
- 主判据 = 最近回撤百分比（<30% 窄 / 30-50% 常规 / 50-78.6% 宽）+ 波段结构与方向偏好
- 教学：2.12 周期频谱的真实数据验证——状态是连续频谱不是离散标签，每格下方标注交易含义
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

UP, DOWN, GRAY, DARK, TEAL, ORANGE = "#e53935", "#26a69a", "#90a4ae", "#263238", "#00897b", "#ef6c00"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"]).sort_values("time").reset_index(drop=True)

# 每个状态：窗口 (start, end)、标题、教学要点
states = [
    ("2026-06-29 19:55", "2026-06-29 20:15", "① 尖峰（Spike）", "回撤≈0%：连续 3 根大阳创新高\n只做回撤 SPS，禁追 SCS"),
    ("2026-06-30 00:25", "2026-06-30 01:15", "② 微型通道（Micro Ch）", "2-10 根几乎无回撤\n等突破失败顺势入场"),
    ("2026-07-02 09:00", "2026-07-02 11:05", "③ 紧凑通道（Tight Ch）", "回撤 <30%：只做顺势\n第一个逆势突破通常失败"),
    ("2026-07-01 21:00", "2026-07-01 23:00", "④ 常规通道（Normal Ch）", "回撤 30-50%：只做顺势\n回调到均线/趋势线是入场点"),
    ("2026-06-29 08:40", "2026-06-29 10:45", "⑤ 宽通道/台阶（Broad Ch）", "回撤 50-78.6%：锯齿形\n突破后必回测，等测试顺势"),
    ("2026-06-29 11:20", "2026-06-29 13:25", "⑥ 趋势型区间（Trending TR）", "方向偏好但序列 <3 组\n顺势优先，禁逆势边界"),
    ("2026-06-29 16:40", "2026-06-29 18:45", "⑦ 交易区间（Trading Range）", "上下边界清晰：边界高抛低吸\n中部不交易，等边界"),
    ("2026-07-01 04:00", "2026-07-01 06:05", "⑧ 极端区间（Extreme TR）", "极窄横盘：期望值为负\n不交易是最佳选择"),
]

fig, axes = plt.subplots(2, 4, figsize=(16.5, 7.2), dpi=110)
fig.patch.set_facecolor("white")

for idx, (t0, t1, title, tip) in enumerate(states):
    ax = axes[idx // 4][idx % 4]
    ax.set_facecolor("white")
    seg = df[(df["time"] >= t0) & (df["time"] <= t1)].reset_index(drop=True)
    t = seg["time"].values
    o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
    for i in range(len(seg)):
        color = UP if c[i] >= o[i] else DOWN
        ax.plot([t[i], t[i]], [l[i], h[i]], color=color, lw=1.0, zorder=3)
        lo, hi = min(o[i], c[i]), max(o[i], c[i])
        ax.add_patch(plt.Rectangle((t[i] - pd.Timedelta(minutes=1.7), lo),
                                   pd.Timedelta(minutes=3.4), max(hi - lo, 1),
                                   facecolor=color, edgecolor=color, lw=0.4, zorder=4))
    # 统计打印（供核对）
    ret = (c[-1] - c[0]) / c[0] * 100
    rng = (h.max() - l.min()) / c[0] * 100
    up_dir = c[-1] > c[0]
    peak = h.max() if up_dir else h.min()
    trough = l.min() if up_dir else l.max()
    move = abs(c[-1] - c[0])
    dd = (abs(peak - trough) - move) / move * 100 if move > 1e-9 else 0
    print(f"{title}: 根数 {len(seg)} 涨幅 {ret:.2f}% 区间 {rng:.2f}% 回撤/推进 {dd:.0f}%")
    ax.set_title(title, fontsize=10.5, color=DARK, loc="left")
    ax.text(0.03, 0.04, tip, transform=ax.transAxes, fontsize=8, color=GRAY, va="bottom", ha="left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

fig.suptitle("8 状态周期频谱（Al Brooks）的真实数据拼图（BTC 5m，2026-06-29 ~ 07-02）：从强到弱 8 种市场状态，主判据 = 最近回撤百分比 + 波段结构——同一品种 4 天里走完 8 种状态，频谱是连续的、状态会转换", fontsize=12.5, color=DARK, y=0.99)
plt.subplots_adjust(left=0.03, right=0.995, top=0.90, bottom=0.05, wspace=0.28, hspace=0.42)
plt.savefig("handbook/images/fig_real_ch2_spectrum.png", dpi=110, facecolor="white", bbox_inches="tight")
print("已生成 handbook/images/fig_real_ch2_spectrum.png")
