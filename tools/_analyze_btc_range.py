# -*- coding: utf-8 -*-
"""快速分析 BTC 8/1-8/4 区间段"""
import pandas as pd

OUT = []
def out(s=""):
    OUT.append(str(s))
    print(s)

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
seg = df[(df.time >= "2026-08-01 00:00") & (df.time <= "2026-08-04 23:55")]
out(f"BTC 8/1-8/4 共{len(seg)}根 区间 {seg.high.max():.0f}/{seg.low.min():.0f} 首={seg.open.iloc[0]:.0f} 末={seg.close.iloc[-1]:.0f}")

daily = seg.groupby(seg["time"].dt.date).agg(o=("open", "first"), h=("high", "max"),
                                             l=("low", "min"), c=("close", "last"))
for d, r in daily.iterrows():
    out(f"{d}  O={r.o:.0f} H={r.h:.0f} L={r.l:.0f} C={r.c:.0f}")

# 关键转折（3根窗口）
for i in range(2, len(seg) - 2):
    hh = seg.high.iloc[i] >= seg.high.iloc[i-1:i+3].max()
    ll = seg.low.iloc[i] <= seg.low.iloc[i-1:i+3].min()
    if hh or ll:
        chg = (seg.close.iloc[i] / seg.close.iloc[i-1] - 1) * 100
        if abs(chg) > 0.12 or (hh and ll):
            d = seg.time.iloc[i]
            tag2 = "十字/外包" if (hh and ll) else ("波段高" if hh else "波段低")
            out(f"  {d}  {tag2}  H={seg.high.iloc[i]:.0f} L={seg.low.iloc[i]:.0f} C={seg.close.iloc[i]:.0f} 单根{chg:+.2f}%")

with open("_btc_range_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("saved: _btc_range_out.txt")
