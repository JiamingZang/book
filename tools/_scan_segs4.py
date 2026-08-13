# -*- coding: utf-8 -*-
"""确认 7/08 尾盘、7/14 白天、8/11-8/13 VP 段"""
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
df["day"] = df["time"].dt.date


def show(seg, title, step=6):
    print(f"\n===== {title} =====")
    for _, r in seg.iloc[::step].iterrows():
        print(
            f'  {r["time"].strftime("%m-%d %H:%M")}  O {r["open"]:.0f} H {r["high"]:.0f}'
            f'  L {r["low"]:.0f} C {r["close"]:.0f} V {r["volume"]:.0f}'
        )


d = df[df["day"] == pd.Timestamp("2026-07-08").date()]
show(d[(d["time"] >= "2026-07-08 12:00")], "7/08 12:00-23:55")

d2 = df[df["day"] == pd.Timestamp("2026-07-14").date()]
show(d2[(d2["time"] >= "2026-07-14 03:00") & (d2["time"] <= "2026-07-14 12:00")], "7/14 03:00-12:00")

v = df[df["time"] >= "2026-08-11 00:00"]
print("\n8/11-8/13 范围:", v["low"].min().round(0), "-", v["high"].max().round(0))
show(v, "8/11-8/13 概要", step=36)
