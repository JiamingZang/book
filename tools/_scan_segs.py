# -*- coding: utf-8 -*-
"""精确定位候选形态段：输出关键时间点的 OHLC，确认形态细节"""
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
df["day"] = df["time"].dt.date


def show(seg, title, n=None):
    print(f"\n===== {title} ({len(seg)} bars) =====")
    s = seg if n is None else seg.head(n)
    for _, r in s.iterrows():
        print(
            f'  {r["time"].strftime("%m-%d %H:%M")}  O {r["open"]:.0f}  H {r["high"]:.0f}'
            f'  L {r["low"]:.0f}  C {r["close"]:.0f}  V {r["volume"]:.1f}'
        )


# 1. 7/14 探底拉回（spring 候选）：找日内低点前后
d1 = df[df["day"] == pd.Timestamp("2026-07-14").date()]
low_i = d1["low"].idxmin()
print("7/14 日内低点 bar:", df.loc[low_i, "time"], df.loc[low_i, "low"])
show(df[(df["time"] >= "2026-07-14 12:00") & (df["time"] <= "2026-07-14 16:00")], "7/14 低点前后", n=48)

# 2. 7/08 冲高回落（诱多候选）：找日内高点前后
d2 = df[df["day"] == pd.Timestamp("2026-07-08").date()]
hi_i = d2["high"].idxmax()
print("\n7/08 日内高点 bar:", df.loc[hi_i, "time"], df.loc[hi_i, "high"])
show(df[(df["time"] >= "2026-07-08 08:00") & (df["time"] <= "2026-07-08 12:00")], "7/08 高点前后", n=48)

# 3. 7/01 单边上涨（趋势日候选）：看开盘到收盘结构
show(df[(df["time"] >= "2026-07-01 08:00") & (df["time"] <= "2026-07-01 14:00")], "7/01 上涨段", n=72)
