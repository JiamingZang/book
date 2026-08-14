# -*- coding: utf-8 -*-
"""图 5-2R（新）：sweep 失败——同一个池子 62700，上午 spring 成功、下午扫完继续跌
（BTC 5 分钟，2026-07-06，较池子 62700 -2.2%、较日内高 63999 -4.2%）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）
教学点：5.3 扫流动性"收盘站稳池外 = 真突破，别反向"——
  凌晨 04:25/04:30 两次测试 62700 不破（肥池子 SSL）→ 05:05 插破 62609 收回 →
  06:20-06:30 放量突破（V 363/399）→ 07:15 日高 63999（spring 成功版）
  → 午后阴跌回测 → 17:35 插破 62700 到 62631、收盘 62665 站池外（20 分钟不收回）
  → 18:00-19:30 收回池内但反抽 63000 无力（逃命点）→ 19:55 放量再破（V 373/601/503）
  → 21:30 恐慌 V 1115（全天最大量）→ 21:35 低 61307（较 62700 -2.2%、较日高 -4.2%）
  ——sweep 不是自动反转机：成败由"收盘裁决 + 收回后的行为"决定（呼应 5.3 识别清单）
"""
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

UP = "#e53935"      # 涨（红）
DOWN = "#26a69a"    # 跌（绿）
GRAY = "#90a4ae"
DARK = "#263238"
ORANGE = "#ef6c00"
TEAL = "#00897b"
BLUE = "#1e3a6b"
RED = "#ef5350"

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
i0 = df["time"].searchsorted(pd.Timestamp("2026-07-06 00:00"))
i1 = df["time"].searchsorted(pd.Timestamp("2026-07-06 23:55"))
seg = df.iloc[i0:i1].reset_index(drop=True)
t = seg["time"].values
o, h, l, c = seg["open"].values, seg["high"].values, seg["low"].values, seg["close"].values
v = seg["volume"].values

POOL = 62700.0
sweep_low = 62631.0      # 17:35 插破低
panic_low = float(seg["low"].min())   # 61306.84 @ 21:35
day_high = float(seg["high"].max())   # 63999 @ 07:15
drop_pool = (panic_low / POOL - 1) * 100
drop_high = (panic_low / day_high - 1) * 100
vmed = float(seg["volume"].median())
print(f"日高 {day_high:.0f} | 日低 {panic_low:.0f} | 较池子 {drop_pool:.1f}% | 较日高 {drop_high:.1f}% | V中位 {vmed:.0f}")

fig, (ax, axv) = plt.subplots(
    2, 1, figsize=(15.8, 7.0), dpi=110, sharex=True,
    gridspec_kw={"height_ratios": [3.0, 1.0], "hspace": 0.05})
fig.patch.set_facecolor("white")

# ---------- 上：K 线 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    ax.plot([t[i], t[i]], [l[i], h[i]], color=color, lw=1.0, zorder=3)
    lo, hi = min(o[i], c[i]), max(o[i], c[i])
    ax.add_patch(plt.Rectangle((t[i] - pd.Timedelta(minutes=1.4), lo),
                               pd.Timedelta(minutes=2.8), max(hi - lo, 1),
                               facecolor=color, edgecolor=color, lw=0.4, zorder=4))

spans = [
    ("2026-07-06 00:00", "2026-07-06 05:05", BLUE, 0.05),
    ("2026-07-06 05:05", "2026-07-06 07:30", ORANGE, 0.12),
    ("2026-07-06 07:30", "2026-07-06 17:35", BLUE, 0.05),
    ("2026-07-06 17:35", "2026-07-06 21:35", RED, 0.08),
    ("2026-07-06 21:35", "2026-07-06 23:55", GRAY, 0.06),
]
for t0, t1, color, alpha in spans:
    ax.axvspan(pd.Timestamp(t0), pd.Timestamp(t1), color=color, alpha=alpha, zorder=1)

# 池子线 62700
ax.axhline(POOL, color=GRAY, lw=1.4, ls="--", zorder=2, alpha=0.95)
ax.text(pd.Timestamp("2026-07-06 00:15"), POOL + 30, "池子 SSL：62700（凌晨两次测试不破）",
        fontsize=10, color=DARK, zorder=6)
ax.text(pd.Timestamp("2026-07-06 22:30"), POOL + 30, "收盘站稳池外 = 真破位",
        fontsize=10, color=RED, fontweight="bold", zorder=6)

marks = [
    ("2026-07-06 04:25", 62860, "① 凌晨 04:25/04:30\n两次测试 62700 不破\n= 被验证的肥池子", BLUE, 20, 80, 10),
    ("2026-07-06 06:15", 64060, "② 05:05 插破 62609\n10 分钟收回 → 06:20-06:30\n放量突破（V 363/399）\n07:15 日高 63999 = spring 成功", ORANGE, -30, -40, 9.5),
    ("2026-07-06 13:10", 63100, "③ 午后阴跌回测\n13:00 破 63000\n→ 17:00 回到池子边缘", BLUE, -80, -60, 9.5),
    ("2026-07-06 17:35", 62580, "④ 17:35 插破 62700\n到 62631，收盘 62665 站池外\n20 分钟 4 根收盘不收回\n= 破位裁决（不是 spring）", RED, -40, -100, 10),
    ("2026-07-06 18:45", 62900, "⑤ 18:00-19:30 收回池内\n但反抽 63000 无力\n= 逃命点 / 新空头入场", ORANGE, 90, -10, 9.5),
    ("2026-07-06 20:00", 62200, "⑥ 19:55 放量再破 62700\nV 373→601→503\n低 61799", RED, 20, -60, 9.5),
    ("2026-07-06 21:35", 61400, f"⑦ 21:35 恐慌低 {panic_low:.0f}\n全天最低（V 1115 = 31 倍常态）\n较池子 {drop_pool:.1f}% / 较日高 {drop_high:.1f}%", RED, -50, -110, 10),
]
for x, y, text, color, xoff, dy, fs in marks:
    ax.annotate(text, xy=(pd.Timestamp(x), y),
                xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                fontsize=fs, color=color, ha="center", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1))

ax.set_title(f"图 5-2R 真实数据：sweep 失败——同一个池子 62700，上午 spring 成功、下午扫完继续跌（BTCUSDT 5m，2026-07-06，较池子 {drop_pool:.1f}% / 较日高 {drop_high:.1f}%）",
             fontsize=11, color=DARK, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.set_yticks([])
ax.set_xticks([])

# ---------- 下：成交量 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    axv.bar(t[i], v[i], width=pd.Timedelta(minutes=2.8), color=color, alpha=0.75, zorder=3)
for x, y, text, color, xoff, dy in [
    ("2026-07-06 06:25", 399, "放量突破 V 363/399\n（常态 10 倍）", ORANGE, 40, 60),
    ("2026-07-06 20:02", 601, "放量破位 V 373→601→503", RED, -10, -70),
    ("2026-07-06 21:30", 1115, "恐慌 V 1115\n= 31 倍常态（全天最大量）", RED, -60, 40),
]:
    axv.annotate(text, xy=(pd.Timestamp(x), y),
                 xytext=(pd.Timestamp(x) + pd.Timedelta(minutes=xoff), y + dy),
                 fontsize=9, color=color, ha="center", va="center", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=color, lw=0.9))
axv.set_title("成交量（成功段放量突破；失败段收回时量小，放量再破 + 恐慌下杀才是确认）",
              fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axv.spines[s].set_visible(False)
axv.set_yticks([])

tick_ts = pd.date_range("2026-07-06 00:00", "2026-07-06 23:00", freq="3h")
axv.set_xticks(tick_ts)
axv.set_xticklabels([x.strftime("%H:%M") for x in tick_ts], fontsize=8, color=GRAY)
axv.tick_params(length=0)

plt.savefig("handbook/images/fig_real_ch5_sweepfail.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved: handbook/images/fig_real_ch5_sweepfail.png")
