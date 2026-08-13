# -*- coding: utf-8 -*-
"""验证 7/01 趋势日 vs 7/07 区间日的 EMA20/50 行为"""
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
df["day"] = df["time"].dt.date


def report(d, title):
    seg = df[df["day"] == pd.Timestamp(d).date()].copy()
    seg["above"] = seg["close"] > seg["ema20"]
    print(f"\n===== {title} ({d}) =====")
    print(f"  全天 {len(seg)} 根 K 线, 收 {seg['close'].iloc[0]:.0f} -> {seg['close'].iloc[-1]:.0f}")
    # 均线上方占比（分时段）
    for label, s in [("00-08", seg[seg["time"].dt.hour < 8]),
                     ("08-16", seg[(seg["time"].dt.hour >= 8) & (seg["time"].dt.hour < 16)]),
                     ("16-24", seg[seg["time"].dt.hour >= 16])]:
        if len(s):
            print(f"  {label}: 收盘>EMA20 占比 {s['above'].mean()*100:.0f}%")
    # 穿越次数（EMA20 上下切换）
    cross = (seg["above"].diff().fillna(0) != 0).sum()
    print(f"  EMA20 上下穿越次数: {cross}")
    # 回踩 EMA20 的 HL（局部低点接近 EMA20）
    seg["ema_dist"] = (seg["low"] - seg["ema20"]).abs()
    print(f"  低点距 EMA20 中位距离: {seg['ema_dist'].median():.0f} 点")


report("2026-07-01", "趋势日（spring + HH/HL）")
report("2026-07-07", "区间日（震荡）")
report("2026-07-14", "spring 反转上涨日")
