# -*- coding: utf-8 -*-
"""扫描 BTC/ETH 5m 数据，定位典型教学形态段（趋势日/区间日/假突破/扫流动性等）"""
import sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

df = pd.read_csv("data/btcusdt_5m.csv", parse_dates=["time"])
df["day"] = df["time"].dt.date
df["rng"] = (df["high"] - df["low"]) / df["close"] * 100

# 每日统计：涨跌幅、振幅、是否单边
daily = df.groupby("day").agg(
    o=("open", "first"),
    c=("close", "last"),
    hi=("high", "max"),
    lo=("low", "min"),
    rng_pct=("rng", "sum"),
).reset_index()
daily["chg"] = (daily["c"] - daily["o"]) / daily["o"] * 100
daily["hi_lo"] = (daily["hi"] - daily["lo"]) / daily["o"] * 100

print("=== 单边趋势日（|chg| > 1.8%） ===")
trend = daily[daily["chg"].abs() > 1.8].sort_values("chg", key=abs, ascending=False)
for _, r in trend.head(12).iterrows():
    print(f'{r["day"]}  涨跌 {r["chg"]:+.2f}%  振幅 {r["hi_lo"]:.2f}%  {r["o"]:.0f}→{r["c"]:.0f}')

print("\n=== 大振幅区间日（|chg| < 0.8%, 振幅 > 2.2%） ===")
rng = daily[(daily["chg"].abs() < 0.8) & (daily["hi_lo"] > 2.2)].sort_values("hi_lo", ascending=False)
for _, r in rng.head(8).iterrows():
    print(f'{r["day"]}  涨跌 {r["chg"]:+.2f}%  振幅 {r["hi_lo"]:.2f}%  {r["o"]:.0f}→{r["c"]:.0f}')

print("\n=== 先冲高后回落（诱多/扫流动性候选）===")
for _, r in daily.iterrows():
    # 日内先冲高：收盘离高点远（上影长），且涨过 1.2% 后回落
    if r["hi_lo"] > 2.0 and (r["hi"] - r["c"]) / r["o"] * 100 > 0.8 and r["chg"] < 0.3:
        print(f'{r["day"]}  冲高 {r["hi"]:.0f} 收 {r["c"]:.0f} 回落 {(r["hi"]-r["c"])/r["o"]*100:.2f}%  全天 {r["chg"]:+.2f}%')

print("\n=== 先探底后拉升（诱空/扫流动性候选）===")
for _, r in daily.iterrows():
    if r["hi_lo"] > 2.0 and (r["c"] - r["lo"]) / r["o"] * 100 > 0.8 and r["chg"] > -0.3:
        print(f'{r["day"]}  探底 {r["lo"]:.0f} 收 {r["c"]:.0f} 拉回 {(r["c"]-r["lo"])/r["o"]*100:.2f}%  全天 {r["chg"]:+.2f}%')
