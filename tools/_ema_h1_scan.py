# -*- coding: utf-8 -*-
"""1H 聚合的 EMA20/50 行为验证：45 天全景"""
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
h1 = df.resample("1h", on="time").agg(
    open=("open", "first"), high=("high", "max"), low=("low", "min"),
    close=("close", "last"), volume=("volume", "sum")).dropna()
h1 = h1.reset_index()
h1["ema20"] = h1["close"].ewm(span=20, adjust=False).mean()
h1["ema50"] = h1["close"].ewm(span=50, adjust=False).mean()
h1["above"] = h1["close"] > h1["ema20"]
cross = (h1["above"].diff().fillna(0) != 0).sum()
print(f"1H K线 {len(h1)} 根 ({h1['time'].iloc[0]} ~ {h1['time'].iloc[-1]})")
print(f"EMA20 穿越次数: {cross}（45 天，日均 {cross/45:.1f} 次）")
print(f"收盘>EMA20 占比: {h1['above'].mean()*100:.0f}%")
# 分月段看
for label, s in [("6/29-7/13", h1[h1["time"] < "2026-07-14"]),
                 ("7/14-7/31", h1[(h1["time"] >= "2026-07-14") & (h1["time"] < "2026-08-01")]),
                 ("8/01-8/13", h1[h1["time"] >= "2026-08-01"])]:
    if len(s):
        print(f"  {label}: 收盘>EMA20 {s['above'].mean()*100:.0f}%  穿越 {(s['above'].diff().fillna(0)!=0).sum()} 次")
# 找最长单边段
runs, cur, cur_start = [], [], None
prev = None
for _, r in h1.iterrows():
    if prev is None or r["above"] != prev:
        if cur:
            runs.append((cur_start, len(cur), prev))
        cur, cur_start = [], r["time"]
    cur.append(r["time"])
    prev = r["above"]
runs.append((cur_start, len(cur), prev))
runs.sort(key=lambda x: -x[1])
print("最长连续单边段（上方/下方）:")
for t0, n, above in runs[:4]:
    t1 = t0 + pd.Timedelta(hours=n)
    print(f"  {'上方' if above else '下方'} {n} 根 1H ≈ {n} 小时: {t0.strftime('%m-%d %H')} -> {t1.strftime('%m-%d %H')}")
