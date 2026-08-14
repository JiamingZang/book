# -*- coding: utf-8 -*-
"""图 4-6R 真实数据：外包K线一成一败（BTC 5 分钟，2026-06-30 / 07-30）
- 数据：Binance BTCUSDT 5m K 线（data/btcusdt_5m.csv）
- 左（成功例 07-30 01:30）：前低支撑区横盘 → 多头外包K（H/L 完全包住前棒、实体≈2 倍、
  低点正好回踩 01:00-01:25 整理区低点 = 位置赋予形态意义）→ 后续 02:00 冲 64649（+1.2%）顺失败方向
- 右（失败例 06-30 21:30）：大阴外包K（做空信号）→ 21:40-22:00 快速反抽突破前高 58762
  → 空头被套（trapped）→ 22:00 冲 59277 = 被套方止损回补是反向燃料（4.24 "失败信号的二次交易"）
- 教学：4.24 外包K 实战五条的真实数据验证——先失败再吞没、顺失败方向、位置赋予意义、
  突破幅度比较法（左例低点下方有买家）、失败信号反杀（右例）
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

def draw_panel(ax, i0, i1, ob_idx, title, marks, spans):
    """画一段 5m K 线，标注外包K与事件"""
    seg = df.iloc[i0:i1].reset_index(drop=True)
    t = seg["time"].values
    o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
    for i in range(len(seg)):
        color = UP if c[i] >= o[i] else DOWN
        ax.plot([t[i], t[i]], [l[i], h[i]], color=color, lw=1.1, zorder=3)
        lo, hi = min(o[i], c[i]), max(o[i], c[i])
        ax.add_patch(plt.Rectangle((t[i] - pd.Timedelta(minutes=1.6), lo),
                                   pd.Timedelta(minutes=3.2), max(hi - lo, 1),
                                   facecolor=color, edgecolor=color, lw=0.5, zorder=4))
    # 外包K高亮（整根放大）
    ob = seg.iloc[ob_idx]
    ax.add_patch(plt.Rectangle((ob["time"] - pd.Timedelta(minutes=2.2), ob["low"]),
                               pd.Timedelta(minutes=4.4), ob["high"] - ob["low"],
                               fill=False, ec=ORANGE, lw=2.0, zorder=5))
    # 背景色带
    for t0, t1, color, alpha in spans:
        ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)
    # 标注
    for x, y, text, color, dy in marks:
        ax.annotate(text, xy=(pd.Timestamp(x), y), xytext=(pd.Timestamp(x), y + dy),
                    fontsize=9, color=color, ha="center", zorder=6,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.0))
    ax.set_title(title, fontsize=11, color=DARK, loc="left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.6), dpi=110)
fig.patch.set_facecolor("white")
for ax in axes:
    ax.set_facecolor("white")

# ===== 左：成功例 07-30 00:55 ~ 02:15 =====
draw_panel(axes[0], 8838, 8860, 7, "① 多头外包K成功：先失败再吞没 → 顺失败方向（BTC 5m，2026-07-30 00:55 ~ 02:15）",
           [("2026-07-30 01:30", 63980, "外包K（多头）\nH/L 完全包住前棒\n实体≈2 倍，低点回踩\n前低支撑区", ORANGE, 150),
            ("2026-07-30 02:05", 64720, "后续 +1.2%\n顺势延续", UP, -40),
            ("2026-07-30 01:10", 63650, "前低支撑区\n01:00-01:25 横盘", TEAL, -90)],
           [("2026-07-30 00:55", "2026-07-30 01:28", TEAL, 0.08),
            ("2026-07-30 01:32", "2026-07-30 02:15", UP, 0.06)])

# ===== 右：失败例 06-30 20:50 ~ 22:15 =====
draw_panel(axes[1], 440, 460, 8, "② 空头外包K失败反杀：被套方止损回补 = 反向燃料（BTC 5m，2026-06-30 20:50 ~ 22:15）",
           [("2026-06-30 21:30", 58700, "外包K（空头）\n大阴实体吞没前棒\n做空信号", DOWN, 60),
            ("2026-06-30 21:52", 58880, "快速反抽突破前高\n= 信号失败", ORANGE, 80),
            ("2026-06-30 22:00", 59360, "22:00 冲 59277\n空头被套 → 止损回补\n推动价格继续上行", UP, -60)],
           [("2026-06-30 21:30", "2026-06-30 21:38", DOWN, 0.08),
            ("2026-06-30 21:40", "2026-06-30 22:15", UP, 0.07)])

fig.suptitle("外包K线（Outside Bar）真实案例：先失败再吞没，交易方向 = 第一根 K 线的失败方向——左例位置赋予形态（前低支撑区），右例失败后的二次交易反杀被套者（4.24）", fontsize=12, color=DARK, y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("handbook/images/fig_real_ch4_outsidebar.png", dpi=110, facecolor="white", bbox_inches="tight")
print("已生成 handbook/images/fig_real_ch4_outsidebar.png")
