# -*- coding: utf-8 -*-
"""BTC 5分钟真实教学图 第二弹（Binance 数据，2026-06-29 ~ 08-13）
- fig_real_trend2.png  2-2R  7/01 spring 巨量下影 + HH/HL 趋势结构（第2章 2.3）
- fig_real_fakeout.png 3-1R  7/08 凌晨冲高 → 放量下跌日（第3章 3.2 假突破）
- fig_real_pinbar.png  3-2R  7/01 09:10 巨量锤子线特写（第3章 3.3 Pin Bar）
- fig_real_spring.png  5-2R  7/14 凌晨扫 SSL → 横盘蓄势 → 巨量突破上涨日（第5章 5.3）
- fig_real_volprof.png 5-3R  8/11-8/13 Volume Profile 真实分布（第5章 5.12）
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

RED, GREEN, GRAY = "#ef5350", "#26a69a", "#90a4ae"
BLUE, ORANGE, DARK, TEAL = "#1565c0", "#ef6c00", "#263238", "#00897b"
plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False


def draw_candles(ax, seg, body_w=2.2):
    for _, r in seg.iterrows():
        o, h, l, c = r["open"], r["high"], r["low"], r["close"]
        t = r["time"]
        up = c >= o
        color = RED if up else GREEN
        ax.plot([t, t], [l, h], color=color, lw=0.8, zorder=2)
        ax.add_patch(plt.Rectangle((t - pd.Timedelta(minutes=body_w), min(o, c)),
                                   pd.Timedelta(minutes=body_w * 2), abs(c - o) + 1e-9,
                                   facecolor=color, edgecolor=color, lw=0.5, zorder=3))


def fmt_ax(ax, title, src):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d %H:%M"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8.5)
    ax.set_ylabel("价格 (USDT)", fontsize=10)
    ax.set_title(title, fontsize=13, color=DARK, pad=12)
    ax.text(0.995, -0.14, src, transform=ax.transAxes, ha="right", fontsize=8, color=GRAY)
    ax.grid(axis="y", color="#eceff1", lw=0.7)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    fig.tight_layout()


df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])

# ============ 1. 7/01 spring + HH/HL 趋势（2-2R） ============
seg = df[(df.time >= "2026-07-01 08:00") & (df.time <= "2026-07-01 14:00")].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 09:10 巨量下影 spring
t0 = pd.Timestamp("2026-07-01 09:10")
ax.annotate("09:10 巨量锤子线（V=1551，全天最大）\n下影探到 57800 后收回——扫掉 58000 下方空头止损\n= spring / 扫流动性（5.3）",
            xy=(t0 + pd.Timedelta(minutes=45), 58170),
            xytext=(pd.Timestamp("2026-07-01 08:35"), 59600),
            fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3e0", edgecolor=ORANGE, lw=1),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

# 09:35 突破
ax.annotate("09:35 放量大阳线（V=255）\n收盘站上 58500 → 趋势启动\n突破 = 顺势入场点",
            xy=(pd.Timestamp("2026-07-01 09:35"), 58933),
            xytext=(pd.Timestamp("2026-07-01 10:20"), 59800),
            fontsize=9.5, color=RED, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# HH/HL 连线
hh = [(pd.Timestamp("2026-07-01 09:35"), 58933), (pd.Timestamp("2026-07-01 10:20"), 59032),
      (pd.Timestamp("2026-07-01 11:50"), 59315), (pd.Timestamp("2026-07-01 12:45"), 59457)]
hl = [(pd.Timestamp("2026-07-01 09:20"), 58225), (pd.Timestamp("2026-07-01 10:00"), 58775),
      (pd.Timestamp("2026-07-01 11:15"), 58906), (pd.Timestamp("2026-07-01 13:25"), 59154)]
ax.plot([t for t, _ in hh], [y for _, y in hh], color=TEAL, lw=1.4, ls="-", zorder=5)
ax.plot([t for t, _ in hl], [y for _, y in hl], color=BLUE, lw=1.4, ls="--", zorder=5)
ax.text(pd.Timestamp("2026-07-01 10:05"), 59500, "更高高点 HH", fontsize=9, color=TEAL, fontweight="bold", zorder=6)
ax.text(pd.Timestamp("2026-07-01 10:05"), 58080, "更高低点 HL（趋势 = HH + HL）", fontsize=9, color=BLUE, fontweight="bold", zorder=6)

# 浅回调
ax.annotate("13:05-13:35 浅回调 59126-59292\n低点高于前 HL = 顺势回调\nH2 入场点（3.11），止损回调低点下方",
            xy=(pd.Timestamp("2026-07-01 13:20"), 59174),
            xytext=(pd.Timestamp("2026-07-01 12:30"), 58600),
            fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

ax.set_ylim(57400, 60100)
fmt_ax(ax, "BTC（比特币）5 分钟：巨量 spring 启动 → HH/HL 趋势结构 → 浅回调（2026-07-01 08:00-14:00，+1.0%）",
       "数据源：Binance BTCUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_trend2.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_trend2.png")

# ============ 2. 7/08 冲高回落下跌日（3-1R） ============
seg = df[(df.time >= "2026-07-08 00:00") & (df.time <= "2026-07-08 23:55")].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 01:45 冲高
t1 = pd.Timestamp("2026-07-08 01:45")
ax.axhline(64232, color=GRAY, lw=1.1, ls=":", zorder=4)
ax.annotate("01:45 冲高 64232：\n扫掉 64000 上方追多止损（BSL）\n2 小时内跌回 63600 下方 → 假突破 / 诱多",
            xy=(t1 + pd.Timedelta(minutes=60), 64170),
            xytext=(pd.Timestamp("2026-07-08 03:10"), 64500),
            fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3e0", edgecolor=ORANGE, lw=1),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

# 09:35 巨量阴线
ax.annotate("09:35 放量阴线（V=264）\n跌破早盘平台 63300\n= 突破失败后的第一次确认",
            xy=(pd.Timestamp("2026-07-08 09:35"), 63012),
            xytext=(pd.Timestamp("2026-07-08 08:00"), 64400),
            fontsize=9.5, color=RED, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 16:05 反抽 62941 失败
ax.annotate("16:05 反抽 62941 失败\n16:30-17:30 放量破位（V=282/668）\n反弹至前低下方 = 破位确认（3.2 测试）",
            xy=(pd.Timestamp("2026-07-08 17:30"), 62180),
            xytext=(pd.Timestamp("2026-07-08 14:00"), 63200),
            fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

# 尾盘低点
ax.annotate("23:25 尾盘低点 61545\n较前收 63930 跌 -3.7%\n下跌日：反弹到前低附近做空\n不抄底，等次日结构",
            xy=(pd.Timestamp("2026-07-08 23:25"), 61545),
            xytext=(pd.Timestamp("2026-07-08 21:30"), 60900),
            fontsize=9.5, color=BLUE, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f5e9", edgecolor=BLUE, lw=1),
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))

ax.set_ylim(60600, 64800)
fmt_ax(ax, "BTC（比特币）5 分钟：凌晨冲高诱多 → 放量下跌 → 破位加速（2026-07-08 全天，较前收 -3.7%）",
       "数据源：Binance BTCUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_fakeout.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_fakeout.png")

# ============ 3. 7/01 巨量锤子线特写（3-2R） ============
seg = df[(df.time >= "2026-07-01 08:55") & (df.time <= "2026-07-01 10:00")].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 09:10 锤子线标注（价格）
t0 = pd.Timestamp("2026-07-01 09:10")
ax.annotate("09:10 巨量锤子线\n开 58294 → 低 57800 → 收 58170\n下影约 370 点 ≈ 3 倍实体（124）\nV = 1551：全天最大量",
            xy=(t0, 57800),
            xytext=(pd.Timestamp("2026-07-01 08:52"), 58800),
            fontsize=10, color=ORANGE, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3e0", edgecolor=ORANGE, lw=1.2),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.4))

# 成交量柱（底部）
axv = ax.twinx()
vols = seg["volume"]
axv.bar(seg["time"], vols, width=pd.Timedelta(minutes=3.5), color=GRAY, alpha=0.55, zorder=1)
axv.set_ylim(0, vols.max() * 2.6)
axv.set_yticks([])
axv.spines["top"].set_visible(False)
axv.spines["right"].set_visible(False)

# 量注释
axv.annotate("V = 1551\n（全天最大量）",
             xy=(t0, 1551), xytext=(pd.Timestamp("2026-07-01 09:06"), 2500),
             fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
             arrowprops=dict(arrowstyle="->", color=DARK, lw=1.1))

# 后续确认
ax.annotate("09:35-09:40 大阳线放量突破 58500\n（V=255/173）→ 锤子线确认\n入场：突破 58298 或回调不破低点",
            xy=(pd.Timestamp("2026-07-01 09:37"), 58933),
            xytext=(pd.Timestamp("2026-07-01 09:50"), 59600),
            fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 支撑线
ax.axhline(57800, color=ORANGE, lw=1.2, ls="--", zorder=4)
ax.text(pd.Timestamp("2026-07-01 08:56"), 57860, "低点 57800（止损参考位）", fontsize=8.5, color=ORANGE, zorder=6)

ax.set_ylim(57500, 60000)
fmt_ax(ax, "BTC（比特币）5 分钟：巨量锤子线（Pin Bar）——下影 494 点 ≈ 4 倍实体，V=1551 全天最大（2026-07-01）",
       "数据源：Binance BTCUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_pinbar.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_pinbar.png")

# ============ 4. 7/14 spring 反转上涨日（5-2R） ============
seg = df[(df.time >= "2026-07-14 00:00") & (df.time <= "2026-07-14 23:55")].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 02:20 spring
t0 = pd.Timestamp("2026-07-14 02:20")
ax.axhline(61825, color=ORANGE, lw=1.2, ls="--", zorder=4)
ax.annotate("02:20 探底 61825\n跌破前低 61900（凌晨低点逐级下移）\n扫掉 61900 下方空头止损（SSL）后收回\n= spring / 诱空",
            xy=(t0, 61825),
            xytext=(t0 + pd.Timedelta(minutes=60), 61300),
            fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3e0", edgecolor=ORANGE, lw=1),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

# 白天横盘蓄势
ax.axvspan(pd.Timestamp("2026-07-14 12:00"), pd.Timestamp("2026-07-14 17:00"),
           color=BLUE, alpha=0.06, zorder=1)
ax.text(pd.Timestamp("2026-07-14 11:50"), 63000, "白天横盘蓄势（12:00-17:00）\n62500 一线三次下探不破（15:45/16:00/16:10）\n16:30 后低点抬高到 62632\n= 底部结构在形成，等突破",
        fontsize=9, color=BLUE, fontweight="bold", zorder=6, ha="left")

# 20:30 突破
t1 = pd.Timestamp("2026-07-14 20:30")
ax.annotate("20:30 巨量突破（V=1254）\n收盘站上 62900 平台 → 追多信号\n突破后回踩（21:00-22:00）不破 63500\n= 二次确认",
            xy=(t1 + pd.Timedelta(minutes=30), 63589),
            xytext=(pd.Timestamp("2026-07-14 18:30"), 64000),
            fontsize=9.5, color=RED, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 尾盘加速
ax.annotate("23:00-23:30 加速冲高\n64966 全天高点（V=256/708）\n尾盘高潮：追多的最后入场点\n次日不再追",
            xy=(pd.Timestamp("2026-07-14 23:30"), 64966),
            xytext=(pd.Timestamp("2026-07-14 23:00"), 65400),
            fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

ax.set_ylim(61000, 65600)
fmt_ax(ax, "BTC（比特币）5 分钟：spring 反转上涨日——凌晨扫 SSL → 横盘蓄势 → 巨量突破 → 尾盘加速（2026-07-14，+3.4%）",
       "数据源：Binance BTCUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_spring.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_spring.png")

# ============ 5. 8/11-8/13 Volume Profile（5-3R） ============
seg = df[df.time >= "2026-08-11 00:00"].reset_index(drop=True)

fig, (ax, axp) = plt.subplots(1, 2, figsize=(13, 6.5), dpi=110,
                              gridspec_kw={"width_ratios": [3.2, 1], "wspace": 0.04})
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 计算 Volume Profile：按价格分桶累加成交量
lo, hi = seg["low"].min(), seg["high"].max()
n_bins = 42
edges = np.linspace(lo, hi, n_bins + 1)
volprof = np.zeros(n_bins)
for _, r in seg.iterrows():
    for i in range(n_bins):
        ol = max(r["low"], edges[i])
        oh = min(r["high"], edges[i + 1])
        if oh > ol:
            frac = (oh - ol) / (r["high"] - r["low"]) if r["high"] > r["low"] else 1.0
            volprof[i] += r["volume"] * frac
centers = (edges[:-1] + edges[1:]) / 2

axp.barh(centers, volprof, height=(hi - lo) / n_bins * 0.9,
         color=BLUE, alpha=0.65, zorder=2)
axp.set_ylim(lo, hi)
axp.set_yticks([])
axp.set_xticks([])
for s in ["top", "right", "bottom"]:
    axp.spines[s].set_visible(False)
axp.spines["left"].set_visible(False)

# POC / HVN / LVN 标注
poc_i = int(np.argmax(volprof))
poc = centers[poc_i]
ax.axhline(poc, color=RED, lw=1.3, ls="--", zorder=4)
ax.text(seg["time"].iloc[3], poc + 25, "POC %.0f（整段最大量节点）" % poc,
        fontsize=9, color=RED, fontweight="bold", zorder=6)
axp.axhline(poc, color=RED, lw=1.3, ls="--", zorder=3)

# 找 HVN/LVN：量大于 1.4 倍中位数为 HVN，小于 0.5 倍为 LVN
med = np.median(volprof)
hvn_idx = [i for i in range(n_bins) if volprof[i] > med * 1.4]
lvn_idx = [i for i in range(n_bins) if volprof[i] < med * 0.5 and lo + 60 < centers[i] < hi - 60]
if hvn_idx:
    ax.axhspan(centers[hvn_idx[0]] - 30, centers[hvn_idx[-1]] + 30, color=BLUE, alpha=0.10, zorder=1)
    ax.text(seg["time"].iloc[2], centers[hvn_idx[-1]] + 85,
            "HVN 堆积区 %.0f-%.0f" % (centers[hvn_idx[0]], centers[hvn_idx[-1]]),
            fontsize=8.5, color=BLUE, zorder=6)
# LVN 按连续段分别画（上方快速区 + 下方低量区）
if lvn_idx:
    groups = []
    cur = [lvn_idx[0]]
    for i in lvn_idx[1:]:
        if i == cur[-1] + 1:
            cur.append(i)
        else:
            groups.append(cur)
            cur = [i]
    groups.append(cur)
    for g in groups:
        c0, c1 = centers[g[0]], centers[g[-1]]
        ax.axhspan(c0 - 30, c1 + 30, color=GREEN, alpha=0.10, zorder=1)
        ax.text(seg["time"].iloc[2], c0 - 65, "LVN 快速通过区 %.0f-%.0f" % (c0, c1),
                fontsize=8.5, color=GREEN, zorder=6)

# 突破段标注
ax.annotate("8/12 18:00 放量（V=151）突破 64100（POC 一线）\n→ 两小时穿过 LVN 冲 64500（逼近前高 64515）\n冲高失败 → 快速回落\n8/13 跌至 63310-63661，在 63400 重新堆积企稳\n（单日 POC 63415）",
            xy=(pd.Timestamp("2026-08-12 18:00"), 64218),
            xytext=(pd.Timestamp("2026-08-12 07:00"), 64800),
            fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

fmt_ax(ax, "BTC（比特币）5 分钟 + Volume Profile：量按价格横向分布——HVN 堆积、LVN 快速区、POC 磁力（2026-08-11 ~ 08-13）",
       "数据源：Binance BTCUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_volprof.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_volprof.png")
