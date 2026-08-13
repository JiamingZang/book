# -*- coding: utf-8 -*-
"""BTC/ETH 5分钟真实教学图（Binance 数据，2026-06-29 ~ 08-13）
- fig_real_eth_2leg.png   2-1R  ETH 两段式移动（7/14-7/16）
- fig_real_btc_day.png    4-2R  BTC 一个交易日状态机（7/21）
- fig_real_btc_range.png  4-4R  BTC 交易区间双底+突破（8/2-8/4）
- fig_real_btc_sweep.png  5-1R  BTC 扫流动性+CHoCH 反转日（7/31）
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
    """画 K 线：seg 需含 time/open/high/low/close"""
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


# ============ 1. ETH 两段式移动（2-1R，第2章 2.8） ============
df = pd.read_csv("data/ethusdt_5m.csv", parse_dates=["time"])
seg = df[(df.time >= "2026-07-14 18:00") & (df.time <= "2026-07-16 20:00")].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 第一腿：7/14 20:55 突破拉升（1798→1861），21:20 1879
t1 = pd.Timestamp("2026-07-14 20:55")
# 中间横盘蓄势：7/14 22:00 ~ 7/15 20:00（低点 1859-1885 抬高）
t2 = pd.Timestamp("2026-07-15 20:30")
# 第二腿：7/15 21:00 拉升（1927→1937），23:35 1936
t3 = pd.Timestamp("2026-07-15 23:30")
# 7/16 高位横盘后 16:20 大跌
t4 = pd.Timestamp("2026-07-16 16:20")

ax.annotate("第一腿：20:55 突破拉升\n1798 → 1879（+4.5%）\n大实体趋势 K 线 + 跟进",
            xy=(t1 + pd.Timedelta(minutes=60), 1875),
            xytext=(t1 + pd.Timedelta(minutes=-160), 1922),
            fontsize=10, color=TEAL, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

ax.annotate("横盘蓄势（约 22 小时）\n低点逐步抬高 1859 → 1885\n不是反转，是第二腿前的整理",
            xy=(t2, 1896),
            xytext=(t2 + pd.Timedelta(minutes=60), 1908),
            fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

ax.annotate("第二腿：21:00 再次拉升\n1885 → 1937（≈ 第一腿长度）\n两段式移动（2LD）完整兑现",
            xy=(t3, 1936),
            xytext=(t3 + pd.Timedelta(minutes=-230), 1944),
            fontsize=10, color=TEAL, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

ax.annotate("两段走完 → 高位横盘\n随后 7/16 16:20 大跌 -2.6%\n第二腿后不追多（2LD 完成）",
            xy=(t4 + pd.Timedelta(minutes=-60), 1882),
            xytext=(t4 + pd.Timedelta(minutes=-300), 1902),
            fontsize=9.5, color=RED, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=RED, lw=1),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 第一腿长度等幅线
y0, y1 = 1798.0, 1879.0
ax.annotate("", xy=(pd.Timestamp("2026-07-14 22:30"), y1), xytext=(pd.Timestamp("2026-07-14 22:30"), y0),
            arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.4))
ax.text(pd.Timestamp("2026-07-14 22:50"), (y0 + y1) / 2, "第一腿长度\n（第二腿量度目标）",
        fontsize=8.5, color=TEAL, va="center", zorder=6)

fmt_ax(ax, "ETH（以太坊）5 分钟：两段式移动（2LD）——第一腿 → 横盘蓄势 → 第二腿等幅（2026-07-14 ~ 07-16）",
       "数据源：Binance ETHUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_eth_2leg.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_eth_2leg.png")

# ============ 2. BTC 突破生命周期（4-9R，第4章 4.29） ============
df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
seg = df[(df.time >= "2026-06-29 08:00") & (df.time <= "2026-06-29 16:00")].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 区间上下沿（08:40-11:00）
ax.axvspan(pd.Timestamp("2026-06-29 08:40"), pd.Timestamp("2026-06-29 11:00"),
           color="#1565c0", alpha=0.06, zorder=1)
ax.axhline(59700, color=BLUE, lw=1.2, ls="--", zorder=4)
ax.axhline(58900, color=BLUE, lw=1.2, ls="--", zorder=4)
ax.text(pd.Timestamp("2026-06-29 08:05"), 59800, "区间上沿 ≈ 59700\n（08:55、10:35 两次测试）", fontsize=9.5,
        color=BLUE, fontweight="bold", zorder=6)
ax.text(pd.Timestamp("2026-06-29 08:05"), 58750, "区间下沿 ≈ 58900\n（10:10 测试）", fontsize=9.5,
        color=BLUE, fontweight="bold", zorder=6)

# 突破 11:05-11:25
ax.annotate("11:05 放量阳线突破前高（V=232）\n11:25 冲高 60233（突破后新高）\n→ 突破发生，切系统一",
            xy=(pd.Timestamp("2026-06-29 11:25"), 60233),
            xytext=(pd.Timestamp("2026-06-29 09:15"), 60450),
            fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

# 回踩守住 11:35
ax.annotate("11:35 回踩 59878 不破上沿\n= 突破测试成功：顺势入场点\n止损放回踩低点下方",
            xy=(pd.Timestamp("2026-06-29 11:35"), 59878),
            xytext=(pd.Timestamp("2026-06-29 12:15"), 59520),
            fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 深回调 13:10
ax.annotate("13:10 深回调 59392\n跌回区间内部 = 测试失败\n持仓者被扫止损，但别反手\n它可能是新一轮突破的起点",
            xy=(pd.Timestamp("2026-06-29 13:10"), 59392),
            xytext=(pd.Timestamp("2026-06-29 13:45"), 58820),
            fontsize=9.5, color=RED, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=RED, lw=1),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 第二腿 14:15
ax.annotate("14:15 反转再上 60346 新高\n= 失败的回调本身成了新突破\n每一步都等收盘确认",
            xy=(pd.Timestamp("2026-06-29 14:15"), 60346),
            xytext=(pd.Timestamp("2026-06-29 13:55"), 60420),
            fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

ax.set_ylim(58650, 60650)
fmt_ax(ax, "BTC（比特币）5 分钟：突破生命周期——区间 → 突破 → 回踩守住 → 深回调失败 → 第二腿（2026-06-29）",
       "数据源：Binance BTCUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_btc_day.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_btc_day.png")

# ============ 3. ETH 交易区间完整生命周期（4-3R，第4章 4.4） ============
df = pd.read_csv("data/ethusdt_5m.csv", parse_dates=["time"])
seg = df[(df.time >= "2026-07-02 00:00") & (df.time <= "2026-07-02 23:55")].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 区间上下沿
ax.axhline(1657, color=BLUE, lw=1.4, ls="--", zorder=4)
ax.axhline(1614, color=BLUE, lw=1.4, ls="--", zorder=4)
ax.text(pd.Timestamp("2026-07-02 00:10"), 1665, "区间上沿 ≈ 1657\n17:35 冲 1652、19:10 冲 1657 两次放量测试回落", fontsize=9.5,
        color=BLUE, fontweight="bold", zorder=6)
ax.text(pd.Timestamp("2026-07-02 00:10"), 1588, "区间下沿 ≈ 1614\n凌晨 00:50-01:05 多次测试后收回", fontsize=9.5,
        color=BLUE, fontweight="bold", zorder=6)

# 上沿两次测试标注
ax.annotate("17:35 放量冲高 1652（V=10881）\n19:10 再冲 1657（V=9734）\n两次都回落 = 边界 fade：上沿做空",
            xy=(pd.Timestamp("2026-07-02 19:10"), 1657),
            xytext=(pd.Timestamp("2026-07-02 16:30"), 1730),
            fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

# 下沿测试标注
ax.annotate("凌晨下沿 1614 多次测试\n扫掉下方止损后收回（3.2 假突破）",
            xy=(pd.Timestamp("2026-07-02 00:50"), 1614),
            xytext=(pd.Timestamp("2026-07-02 02:30"), 1570),
            fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 突破 20:25-21:30
ax.annotate("20:25 放量阳线收 1663.8 站上上沿（第一根收盘站上）\n20:30 冲 1669.7 又插破收回 = 最后洗盘\n21:15-21:30 连续放量大阳站稳（1676.5 → 1706.3，V=10547）\n→ 真突破三条件齐，切趋势思维",
            xy=(pd.Timestamp("2026-07-02 21:30"), 1706),
            xytext=(pd.Timestamp("2026-07-02 14:00"), 1740),
            fontsize=9.5, color=RED, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=RED, lw=1),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# 高潮 22:10
ax.annotate("22:10 高潮 1725（+4%）\n22:20 起回落，23:05 低 1688.7\n高潮后不追",
            xy=(pd.Timestamp("2026-07-02 22:10"), 1725),
            xytext=(pd.Timestamp("2026-07-02 23:10"), 1770),
            fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=DARK, lw=1),
            arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

ax.set_ylim(1555, 1795)
fmt_ax(ax, "ETH（以太坊）5 分钟：交易区间完整生命周期——下沿多测 → 上沿双测 → 突破 → 高潮（2026-07-02）",
       "数据源：Binance ETHUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_eth_range.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_eth_range.png")

# ============ 4. BTC 扫流动性+CHoCH 反转日（5-1R，第5章 5.3/5.4） ============
df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
seg = df[(df.time >= "2026-07-31 08:00") & (df.time <= "2026-07-31 20:00")].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
draw_candles(ax, seg)

# 前高/前低（早盘）
ax.axhline(64822, color=GRAY, lw=1.2, ls=":", zorder=4)
ax.text(pd.Timestamp("2026-07-31 08:00"), 64840, "早盘前高 64822（流动性池）", fontsize=9, color=GRAY, zorder=6)

# Sweep：09:10 冲高 65410
t_s = pd.Timestamp("2026-07-31 09:10")
ax.annotate("09:10 插破前高 65410\n扫掉上方追多止损（BSL）\n随即大阴线收回 → SWEEP 成立\n收盘回池内 = 突破失败",
            xy=(t_s, 65410),
            xytext=(t_s + pd.Timedelta(minutes=85), 65050),
            fontsize=9.5, color=RED, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

# CHoCH：10:00 跌破前低 64690
t_c = pd.Timestamp("2026-07-31 10:00")
ax.axvline(t_c, color=ORANGE, lw=1.2, ls=":", zorder=4)
ax.annotate("10:00 跌破早盘低点 64690\n= CHoCH（多头结构被破坏）\n强位移 K 线确认\n→ 停止做多，转空头思维",
            xy=(t_c, 64467),
            xytext=(t_c + pd.Timedelta(minutes=-70), 64000),
            fontsize=9.5, color=ORANGE, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))

# 下跌结构 LL+LH
ax.annotate("下跌趋势结构：LL + LH\n14:30 反抽 64497（LH）\n→ 顺势做空入场点（反抽不破前高）\n止损放 LH 上方",
            xy=(pd.Timestamp("2026-07-31 14:30"), 64497),
            xytext=(pd.Timestamp("2026-07-31 15:30"), 65000),
            fontsize=9.5, color=TEAL, fontweight="bold", zorder=6,
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.2))

# 日内低点 18:05 63610
ax.annotate("18:05 日内低点 63610\n全天 -2.7%（65410 → 63610）\n尾盘反抽 64012：\n下跌日不抄底，等次日结构",
            xy=(pd.Timestamp("2026-07-31 18:05"), 63610),
            xytext=(pd.Timestamp("2026-07-31 19:30"), 63000),
            fontsize=9.5, color=DARK, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8e1", edgecolor=DARK, lw=1),
            arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))

fmt_ax(ax, "BTC（比特币）5 分钟：扫流动性 → CHoCH → 下跌趋势日（2026-07-31，全天 -2.7%）",
       "数据源：Binance BTCUSDT 5m K 线 · 教学示意，不构成投资建议")
fig.savefig("handbook/images/fig_real_btc_sweep.png", bbox_inches="tight", facecolor="white")
print("saved: fig_real_btc_sweep.png")
