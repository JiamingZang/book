# -*- coding: utf-8 -*-
"""图 8-3R 真实数据：40 组 EMA 参数全部亏损——换参数救不了负期望策略
数据：Binance BTCUSDT 5m K 线重采样 1H（2026-07-02 ~ 08-10，与图 8-1R 同数据段）
策略族：EMA 快线/慢线交叉双向趋势跟踪（金叉做多/死叉做空），2×ATR 固定止损
网格：快线 {5,10,15,20,25,30,40,50} × 慢线 {50,75,100,150,200} = 40 组（39 组有效）
上=参数热力图（fast×slow，色=总 R，深红→白，全部 <0）
下左=40 组总 R 排序条形（全红）+ 最差/最不差标注
下右=样本量 vs 总 R 散点（样本越足越诚实：41 笔 5/50 亏 -12.6R，9 笔 50/200 只显示 -5.9R）
核心实证：① 40/40 全亏、平均每笔 R 全为负 → 参数不是问题，策略-行情不匹配才是
② 最不差 vs 最差 = 亏多亏少，不是赚亏；③ 每组 9~41 笔 << 8.7 的 100+ 门槛 → 挑参数=在噪音里找规律
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False

# ---------- 数据与回测 ----------
df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
h1 = df.resample("1h", on="time").agg(open=("open", "first"), high=("high", "max"), low=("low", "min"),
                                      close=("close", "last"), volume=("volume", "sum")).dropna().reset_index()
h1["atr"] = (h1["high"] - h1["low"]).rolling(14).mean()

def bt(fast, slow):
    e = h1["close"].ewm(span=fast, adjust=False).mean()
    s = h1["close"].ewm(span=slow, adjust=False).mean()
    long = e > s
    cross = long.diff().fillna(False)
    Rs = []
    for i in range(len(h1)):
        if cross.iloc[i] and not np.isnan(h1["atr"].iloc[i]) and h1["atr"].iloc[i] > 0:
            entry = h1["close"].iloc[i]
            risk = 2 * h1["atr"].iloc[i]
            stop = entry - risk if long.iloc[i] else entry + risk
            exit_p = None
            for j in range(i + 1, len(h1)):
                if long.iloc[i]:
                    if h1["low"].iloc[j] <= stop:
                        exit_p = stop; break
                    if not long.iloc[j]:
                        exit_p = h1["close"].iloc[j]; break
                else:
                    if h1["high"].iloc[j] >= stop:
                        exit_p = stop; break
                    if long.iloc[j]:
                        exit_p = h1["close"].iloc[j]; break
            if exit_p is None:
                exit_p = h1["close"].iloc[-1]
            Rs.append((exit_p - entry) / risk if long.iloc[i] else (entry - exit_p) / risk)
    return len(Rs), sum(Rs)

fasts = [5, 10, 15, 20, 25, 30, 40, 50]
slows = [50, 75, 100, 150, 200]
grid = np.zeros((len(fasts), len(slows)))
ns = np.zeros((len(fasts), len(slows)), dtype=int)
rows = []
for i, f in enumerate(fasts):
    for j, s in enumerate(slows):
        n, tot = bt(f, s)
        grid[i, j] = tot
        ns[i, j] = n
        if n > 0:
            rows.append((f, s, n, tot, tot / n))
D = pd.DataFrame(rows, columns=["fast", "slow", "n", "tot", "per"])
D = D.sort_values("tot")

best = D.iloc[-1]   # 最不差（总 R 最大）
worst = D.iloc[0]   # 最差
v2050 = grid[fasts.index(20), slows.index(50)]

# ---------- 颜色 ----------
RED_D, RED, ORANGE, LIGHT, WHITE = "#b71c1c", "#e53935", "#ff8a65", "#ffccbc", "#ffffff"
GRAY, TXT = "#9e9e9e", "#333333"
TEAL = "#00897b"
cmap = LinearSegmentedColormap.from_list("loss", [RED_D, RED, ORANGE, LIGHT, WHITE], N=256)

# ---------- 画布 ----------
fig = plt.figure(figsize=(14.28, 9.4), dpi=100)
fig.patch.set_facecolor("white")

# ===== 上：热力图 =====
ax1 = fig.add_axes([0.09, 0.53, 0.80, 0.39])
vmin, vmax = -13, 0
im = ax1.imshow(grid, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
ax1.set_xticks(range(len(slows)))
ax1.set_xticklabels(slows, fontsize=10)
ax1.set_yticks(range(len(fasts)))
ax1.set_yticklabels(fasts, fontsize=10)
ax1.set_xlabel("EMA 慢线参数", fontsize=12)
ax1.set_ylabel("EMA 快线参数", fontsize=12)
ax1.set_title("EMA 参数网格 × 总 R：40 组全部亏损（红）——图 8-1R 的 20/50 只是亏损高原上普通的一点",
              fontsize=13, fontweight="bold", color=TXT, pad=10)
for i in range(len(fasts)):
    for j in range(len(slows)):
        v = grid[i, j]
        col = "white" if v < -9 else TXT
        ax1.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=9.5, color=col, fontweight="bold")
# 20/50 格加框
ax1.add_patch(plt.Rectangle((slows.index(50) - 0.5, fasts.index(20) - 0.5), 1, 1,
                            fill=False, edgecolor="black", lw=2.2))
ax1.annotate("20/50（图 8-1R 同款）：-6.6R 也亏",
             xy=(slows.index(50), fasts.index(20)), xytext=(2.6, 7.1),
             fontsize=10.5, color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))
cb = fig.colorbar(im, ax=ax1, fraction=0.032, pad=0.02)
cb.set_label("总 R（全部为负）", fontsize=10)
cb.ax.tick_params(labelsize=9)

# ===== 下左：排序条形 =====
ax2 = fig.add_axes([0.09, 0.10, 0.46, 0.34])
x = np.arange(len(D))
ax2.barh(x, D["tot"].values, color=RED, alpha=0.85, height=0.75)
ax2.axvline(0, color=GRAY, lw=1.2, ls="--")
ax2.text(0.3, len(D) - 0.6, "零线（盈利区）", fontsize=9, color=GRAY, ha="left")
ax2.invert_yaxis()
ax2.set_yticks([])
ax2.set_xlim(-15, 3)
ax2.set_xlabel("总 R（按参数组合从最差到最不差排序）", fontsize=11)
ax2.set_title(f"39 组有效参数全部亏损：最差 {worst['tot']:.1f}R（{worst['fast']}/{worst['slow']}）· 最不差 {best['tot']:.1f}R（{best['fast']}/{best['slow']}）",
              fontsize=12, fontweight="bold", color=TXT, pad=8)
ax2.annotate(f"最差\n{worst['fast']}/{worst['slow']} = {worst['tot']:.1f}R\n（{worst['n']} 笔）",
             xy=(worst["tot"], 0), xytext=(-13.5, 3.5),
             fontsize=9.5, color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
ax2.annotate(f"最不差\n{best['fast']}/{best['slow']} = {best['tot']:.1f}R\n（{best['n']} 笔）",
             xy=(best["tot"], len(D) - 1), xytext=(-10.0, len(D) - 4.5),
             fontsize=9.5, color=RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
ax2.grid(axis="x", lw=0.4, alpha=0.25)
ax2.set_axisbelow(True)
ax2.spines[["top", "right"]].set_visible(False)

# ===== 下右：样本量 vs 总 R =====
ax3 = fig.add_axes([0.62, 0.10, 0.32, 0.34])
ax3.scatter(D["n"], D["tot"], s=42, color=TEAL, alpha=0.85, edgecolor="white", lw=0.6, zorder=3)
ax3.axhline(0, color=GRAY, lw=1, ls="--")
# 标注两个端点
b = D[D["n"] == D["n"].max()].iloc[0]
sm = D[D["n"] == D["n"].min()].iloc[0]
ax3.annotate(f"样本最足 {b['fast']}/{b['slow']}：\n{b['n']} 笔 → {b['tot']:.1f}R\n（亏得最诚实）",
             xy=(b["n"], b["tot"]), xytext=(16, -11.2),
             fontsize=9, color="#00695c", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1))
ax3.annotate(f"样本最少 {sm['fast']}/{sm['slow']}：\n{sm['n']} 笔 → 只显示 {sm['tot']:.1f}R\n（还没亏够笔数）",
             xy=(sm["n"], sm["tot"]), xytext=(2.5, -3.2),
             fontsize=9, color="#00695c", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.1))
ax3.set_xlabel("样本量（笔数）", fontsize=11)
ax3.set_ylabel("总 R", fontsize=11)
ax3.set_title(f"样本越足越诚实：平均每笔 R 全为负（{D['per'].min():.2f} ~ {D['per'].max():.2f}）\n9~41 笔 << 8.7 验证门槛 100+ 笔",
              fontsize=11.5, fontweight="bold", color=TXT, pad=8)
ax3.grid(True, lw=0.4, alpha=0.25)
ax3.spines[["top", "right"]].set_visible(False)

fig.text(0.995, 0.015, "数据源：Binance BTCUSDT 5m K 线重采样 1H · 2026-07-02 ~ 08-10 · 教学示意（参数未优化），不构成投资建议",
         ha="right", fontsize=8.5, color=GRAY)

out = "handbook/images/fig_real_ch8_params.png"
fig.savefig(out, dpi=100, facecolor="white")
print("saved", out)
print(f"关键数字: 有效组 {len(D)} · 全负 {int((D['tot'] < 0).all())} · 最差 {worst['tot']:.1f}R({worst['fast']}/{worst['slow']},{worst['n']}笔) · "
      f"最不差 {best['tot']:.1f}R({best['fast']}/{best['slow']},{best['n']}笔) · 20/50 {v2050:.1f}R · "
      f"每笔R {D['per'].min():.2f}~{D['per'].max():.2f} · 笔数 {D['n'].min()}~{D['n'].max()}")

# ---------- 像素验证 ----------
from PIL import Image
im = np.array(Image.open(out).convert("RGB"))
h, w, _ = im.shape
total = h * w
for name, rgb in [("深红", RED_D), ("红", RED), ("橙", ORANGE), ("青", TEAL)]:
    r, g, b = int(rgb[1:3], 16), int(rgb[3:5], 16), int(rgb[5:7], 16)
    mask = (abs(im[:, :, 0].astype(int) - r) < 40) & (abs(im[:, :, 1].astype(int) - g) < 40) & (abs(im[:, :, 2].astype(int) - b) < 40)
    print(f"{name}: {mask.sum() / total * 100:.2f}%")
print("size:", im.shape[1], "x", im.shape[0])
