# -*- coding: utf-8 -*-
"""图 3-4R 真实数据：双顶失败 vs 双底成功（BTC 5 分钟，2026-07-29 / 07-17）
- 数据：Binance BTCUSDT 5m K 线（data/btcusdt_5m.csv）
- 左（双顶失败 07-29）：第一顶 64745(17:55) → 回调 64140(21:20, -0.9%) → 21:30-22:00 快速冲顶
  第二顶 64719(22:00, 差 26 点未破=LH, 长上影) → 追高者被套 → 持续阴跌至 63410(次日 04:00, -2.0%)
- 右（双底成功 07-17）：第一底 62710(14:10) → 反弹 63362(19:40, +1.0%) → 第二底 62538(21:40,
  创新低=扫多止损, 21:35-21:45 三次测试不破) → 21:55 大阳反转(实体 334 点) → 持续上涨至
  64388(次日 02:30, +3.0%)——被扫损方止损回补是燃料
- 教学：3.9 双顶/双底的真实数据验证——失败形态（LH 双顶 / sweep 双底）反而是高概率反向信号
  （3.2 假突破、4.24 失败信号二次交易）
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

UP, DOWN, GRAY, DARK, TEAL, ORANGE = "#e53935", "#26a69a", "#90a4ae", "#263238", "#00897b", "#ef6c00"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"]).sort_values("time").reset_index(drop=True)

def draw_panel(ax, i0, i1, title, marks, spans):
    """画一段 5m K 线，标注关键点与背景色带"""
    seg = df.iloc[i0:i1].reset_index(drop=True)
    t = seg["time"].values
    o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
    for i in range(len(seg)):
        color = UP if c[i] >= o[i] else DOWN
        ax.plot([t[i], t[i]], [l[i], h[i]], color=color, lw=1.0, zorder=3)
        lo, hi = min(o[i], c[i]), max(o[i], c[i])
        ax.add_patch(plt.Rectangle((t[i] - pd.Timedelta(minutes=1.4), lo),
                                   pd.Timedelta(minutes=2.8), max(hi - lo, 1),
                                   facecolor=color, edgecolor=color, lw=0.4, zorder=4))
    # 背景色带
    for t0, t1, color, alpha in spans:
        ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)
    # 标注：(x, y, text, color, xoff_min, yoff, fontsize)
    for x, y, text, color, xoff, dy, fs in marks:
        ax.annotate(text, xy=(pd.Timestamp(x), y),
                    xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                    fontsize=fs, color=color, ha="center", va="center", zorder=6,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.1))
    ax.set_title(title, fontsize=11, color=DARK, loc="left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.6), dpi=110)
fig.patch.set_facecolor("white")
for ax in axes:
    ax.set_facecolor("white")

# ===== 左：双顶失败 07-29 14:00 ~ 07-30 04:00 =====
draw_panel(axes[0], 8752, 8881, "① 双顶失败：第二顶更低 = 追高者被套（BTC 5m，2026-07-29 14:00 ~ 07-30 04:00）",
           [("2026-07-29 17:55", 64745, "第一顶 64745", ORANGE, 0, 80, 9),
            ("2026-07-29 21:20", 64140, "回调 64140\n-0.9%", DOWN, 0, -140, 9),
            ("2026-07-29 22:00", 64719, "第二顶 64719\n差 26 点未破 = LH\n长上影 = 追高被套", ORANGE, 0, 110, 9),
            ("2026-07-30 04:00", 63410, "持续阴跌\n至 63410 -2.0%", DOWN, 0, -170, 9)],
           [("2026-07-29 14:00", "2026-07-29 17:55", UP, 0.05),
            ("2026-07-29 18:00", "2026-07-29 21:25", GRAY, 0.09),
            ("2026-07-29 22:10", "2026-07-30 04:00", DOWN, 0.07)])

# ===== 右：双底成功 07-17 13:00 ~ 07-18 04:00 =====
draw_panel(axes[1], 5244, 5407, "② 双底成功：第二底创新低扫多 → 被套方回补=燃料（BTC 5m，2026-07-17 13:00 ~ 07-18 04:00）",
           [("2026-07-17 14:10", 62710, "第一底 62710", DOWN, 0, -150, 9),
            ("2026-07-17 19:40", 63362, "反弹 63362\n+1.0%", UP, 0, 70, 9),
            ("2026-07-17 21:40", 62538, "第二底 62538\n创新低=扫多止损\n三次测试不破", ORANGE, 20, -145, 9),
            ("2026-07-17 21:55", 63154, "21:55 大阳反转\n被扫止损回补=燃料", UP, 0, 95, 9),
            ("2026-07-18 02:30", 64388, "持续上涨\n至 64388 +3.0%", UP, 0, 75, 9)],
           [("2026-07-17 13:00", "2026-07-17 14:10", DOWN, 0.06),
            ("2026-07-17 14:20", "2026-07-17 21:25", GRAY, 0.08),
            ("2026-07-17 21:35", "2026-07-18 04:00", UP, 0.06)])

fig.suptitle("双顶失败 vs 双底成功：极值测试的两种结局——第二顶更低 = 多头力竭；第二底创新低 = 扫损后反转（3.9 双顶/双底的真实数据验证）", fontsize=12, color=DARK, y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("handbook/images/fig_real_ch3_doubletop.png", dpi=110, facecolor="white", bbox_inches="tight")
print("已生成 handbook/images/fig_real_ch3_doubletop.png")
