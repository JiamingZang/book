# -*- coding: utf-8 -*-
"""确认 7/07 区间日、7/08 全天、7/14 凌晨段形态"""
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])


def show(seg, title, n=None, step=1):
    print(f"\n===== {title} ({len(seg)} bars) =====")
    s = seg.iloc[::step] if n is None else seg.head(n).iloc[::step]
    for _, r in s.iterrows():
        print(
            f'  {r["time"].strftime("%m-%d %H:%M")}  O {r["open"]:.0f}  H {r["high"]:.0f}'
            f'  L {r["low"]:.0f}  C {r["close"]:.0f}  V {r["volume"]:.0f}'
        )


# 7/07 全天（每 30 分钟一根，压缩）
show(df[(df["time"] >= "2026-07-07 00:00") & (df["time"] <= "2026-07-07 23:55")], "7/07 全天", step=6)

# 7/08 凌晨 00:00-08:00（看冲高回落）
show(df[(df["time"] >= "2026-07-08 00:00") & (df["time"] <= "2026-07-08 08:00")], "7/08 凌晨", step=3)

# 7/14 凌晨 00:00-12:00
show(df[(df["time"] >= "2026-07-14 00:00") & (df["time"] <= "2026-07-14 12:00")], "7/14 凌晨-中午", step=3)
