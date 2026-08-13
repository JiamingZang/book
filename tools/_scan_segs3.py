# -*- coding: utf-8 -*-
"""确认 7/08、7/14 全天关键点位"""
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
df["day"] = df["time"].dt.date

d = df[df["day"] == pd.Timestamp("2026-07-08").date()]
print("7/08 low:", d.loc[d["low"].idxmin(), "time"], d["low"].min().round(0))
print("7/08 收盘:", d["close"].iloc[-1].round(0))

d2 = df[df["day"] == pd.Timestamp("2026-07-14").date()]
print("7/14 high:", d2.loc[d2["high"].idxmax(), "time"], d2["high"].max().round(0))
print("7/14 收盘:", d2["close"].iloc[-1].round(0))
seg = d2[d2["time"] >= "2026-07-14 17:00"]
for _, r in seg.iloc[::6].iterrows():
    print(
        f'  {r["time"].strftime("%H:%M")}  O {r["open"]:.0f} H {r["high"]:.0f}'
        f'  L {r["low"]:.0f} C {r["close"]:.0f} V {r["volume"]:.0f}'
    )

# 7/14 12:00-17:00（白天横盘后启动点）
seg2 = d2[(d2["time"] >= "2026-07-14 12:00") & (d2["time"] <= "2026-07-14 17:00")]
print("--- 7/14 12:00-17:00 ---")
for _, r in seg2.iloc[::3].iterrows():
    print(
        f'  {r["time"].strftime("%H:%M")}  O {r["open"]:.0f} H {r["high"]:.0f}'
        f'  L {r["low"]:.0f} C {r["close"]:.0f} V {r["volume"]:.0f}'
    )
