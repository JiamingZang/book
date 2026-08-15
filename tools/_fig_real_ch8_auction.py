# -*- coding: utf-8 -*-
"""图 8-5R：拍卖理论的真实循环——趋势 → 停止 → 平衡 → 失衡 → 接受（BTC 5 分钟，2026-07-01）
数据源：Binance BTCUSDT 5m（data/btcusdt_5m.csv）
教学点（8.10 拍卖理论）：市场是拍卖机，价格+时间+成交量定"价值"，在平衡与失衡间循环
- 趋势（10:00-13:40）：价格从 58771 推到 59374（+1.0%）——失衡，单向运动
- 停止（14:00-16:40）：冲高 59374 后大量反向交易，回落至 58500 —— A.趋势停止
- 平衡（16:40-20:45）：价格在 58350-59000 横盘近 4 小时（下沿 3 次测试 58326/58420/58439）
  ——市场有效，"价值"在此；时间累积长、成交量堆积
- 失衡（21:00）：巨量 V=635（常态 ~40 的 16 倍）把价格从下沿推离——主导方进场
- 接受（21:15-21:35）：价格停留 + 回踩 58602 守住（收盘不回下沿）= 参与者接受新价位
- 转换（21:45）：放量 V=383 突破上沿 59000 → 59410 新高——离开区间再次失衡，趋势展开
呼应 8.10"接受=收盘确认+放量（真突破）；拒绝=假突破（插破收回）"；反向例见图 4-2R
"""
import csv
import datetime as dt
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

UP = "#e53935"      # 涨（红）
DOWN = "#26a69a"    # 跌（绿）
GRAY = "#90a4ae"
DARK = "#263238"
ORANGE = "#ef6c00"
TEAL = "#00897b"
BLUE = "#1e3a6b"

def load_csv(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "t": dt.datetime.strptime(r["time"], "%Y-%m-%d %H:%M"),
                "o": float(r["open"]), "h": float(r["high"]),
                "l": float(r["low"]), "c": float(r["close"]),
                "v": float(r["volume"]),
            })
    return rows

def t_minutes(x):
    return x.timestamp() / 60

def slice_seg(rows, start, end):
    return [r for r in rows if start <= r["t"] < end]

rows = load_csv("data/btcusdt_5m.csv")

# 07-01 全天：08:00-22:10，展示趋势→停止→平衡→失衡→接受完整循环
seg = slice_seg(rows, dt.datetime(2026, 7, 1, 8, 0), dt.datetime(2026, 7, 1, 22, 10))
t = [t_minutes(r["t"]) for r in seg]
o = [r["o"] for r in seg]
h = [r["h"] for r in seg]
l = [r["l"] for r in seg]
c = [r["c"] for r in seg]
v = [r["v"] for r in seg]
T0 = t[0]

def tx(x):
    return t_minutes(dt.datetime.strptime(x, "%Y-%m-%d-%H:%M")) - T0

fig, (ax, axv) = plt.subplots(
    2, 1, figsize=(15.8, 7.4), dpi=110, sharex=True,
    gridspec_kw={"height_ratios": [3.0, 1.0], "hspace": 0.05})

# ---------- 上：K 线 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    ax.plot([t[i], t[i]], [l[i], h[i]], color=color, lw=1.0, zorder=3)
    lo, hi = min(o[i], c[i]), max(o[i], c[i])
    ax.add_patch(plt.Rectangle((t[i] - 1.4, lo), 2.8, max(hi - lo, 1),
                               facecolor=color, edgecolor=color, lw=0.4, zorder=4))

spans = [
    ("2026-07-01-08:00", "2026-07-01-09:40", BLUE, 0.05),
    ("2026-07-01-09:40", "2026-07-01-13:40", UP, 0.07),
    ("2026-07-01-13:40", "2026-07-01-16:40", "#ef5350", 0.06),
    ("2026-07-01-16:40", "2026-07-01-20:50", TEAL, 0.10),
    ("2026-07-01-20:50", "2026-07-01-21:12", ORANGE, 0.18),
    ("2026-07-01-21:12", "2026-07-01-21:40", "#26a69a", 0.12),
    ("2026-07-01-21:40", "2026-07-01-22:10", UP, 0.10),
]
for t0s, t1s, color, alpha in spans:
    ax.axvspan(tx(t0s), tx(t1s), color=color, alpha=alpha, zorder=1)

# 平衡区上沿/下沿
ax.axhline(58990.0, color=GRAY, lw=1.2, ls="--", zorder=2, alpha=0.9)
ax.axhline(58350.0, color=GRAY, lw=1.2, ls="--", zorder=2, alpha=0.9)

marks = [
    ("2026-07-01-09:00", 59300, "下跌（8-9 时）\n随后停止", BLUE, -70, 55, 9),
    ("2026-07-01-12:30", 59450, "趋势阶段（失衡）：\n58771 → 59374 (+1.0%)", UP, -90, 20, 10),
    ("2026-07-01-15:30", 59150, "停止（A）：冲高 59374 后\n大量反向交易，回落至 58500", "#ef5350", -100, -20, 9.5),
    ("2026-07-01-18:45", 58420, "平衡（价值区）：58350-58990\n横盘近 4 小时，下沿 3 次测试\n= 市场有效，“价值”在此", TEAL, -40, 85, 10),
    ("2026-07-01-21:05", 58950, "失衡：巨量 V=635\n（常态 ~40 的 16 倍）\n主导方把价格推离下沿", ORANGE, 30, 70, 10),
    ("2026-07-01-21:32", 58620, "接受：回踩 58602 守住\n（收盘不回下沿）\n参与者接受新价位", DOWN, 30, -90, 9.5),
    ("2026-07-01-21:58", 59550, "转换：放量 V=383\n突破上沿 58990 → 59410\n离开区间，趋势展开", UP, -50, -10, 10),
]
for x, y, text, color, xoff, dy, fs in marks:
    ax.annotate(text, xy=(tx(x), y),
                xytext=(tx(x) + xoff, y + dy),
                fontsize=fs, color=color, ha="center", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.1))

ax.set_title("图 8-5R 拍卖理论的真实循环：趋势 → 停止 → 平衡 → 失衡 → 接受（BTCUSDT 5m，2026-07-01 08:00 ~ 22:10）",
             fontsize=11, color=DARK, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.set_yticks([])
ax.set_xticks([])

# ---------- 下：成交量 ----------
for i in range(len(seg)):
    color = UP if c[i] >= o[i] else DOWN
    axv.bar(t[i], v[i], width=2.8, color=color, alpha=0.75, zorder=3)
for x, y, text, color, xoff, dy in [
    ("2026-07-01-21:02", 635, "失衡 V=635", ORANGE, -35, -70),
    ("2026-07-01-21:46", 383, "转换 V=383", UP, 40, -55),
    ("2026-07-01-11:00", 172, "平衡区量能温和\n（30-80）", GRAY, 55, -10),
]:
    axv.annotate(text, xy=(tx(x), y),
                 xytext=(tx(x) + xoff, y + dy),
                 fontsize=9, color=color, ha="center", va="center", zorder=6,
                 arrowprops=dict(arrowstyle="->", color=color, lw=0.9))
axv.set_title("成交量：平衡区量能温和（时间换空间），失衡与转换才放量（兴趣投票）",
              fontsize=10, color=DARK, loc="left")
for s in ["top", "right"]:
    axv.spines[s].set_visible(False)
axv.set_yticks([])

tick_ts = [tx(x) for x in
           ["2026-07-01-08:00", "2026-07-01-10:00", "2026-07-01-12:00",
            "2026-07-01-14:00", "2026-07-01-16:00", "2026-07-01-18:00",
            "2026-07-01-20:00", "2026-07-01-22:00"]]
axv.set_xticks(tick_ts)
axv.set_xticklabels(["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"],
                    fontsize=8, color=GRAY)
axv.tick_params(length=0)

plt.savefig("handbook/images/fig_real_ch8_auction.png", dpi=110, facecolor="white",
            bbox_inches="tight")
print("saved")
