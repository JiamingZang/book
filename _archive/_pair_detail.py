# -*- coding: utf-8 -*-
"""详细检查 2026-06-15 以来 沪深300/中证500 价差与 z-score，确定图叙事"""
import akshare as ak
import pandas as pd
import numpy as np

def get(code):
    df = ak.stock_zh_index_daily(symbol=code)
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["close"]

a, b = get("sh000300"), get("sz399905")
df = pd.concat([a, b], axis=1, keys=["hs300", "zz500"]).dropna()
lr = np.log(df["hs300"] / df["zz500"])
win = 60
m = lr.rolling(win).mean()
s = lr.rolling(win).std()
z = (lr - m) / s
df["z"] = z
df = df.loc["2026-06-01":]

# 每 3 行打印一次
rows = df.reset_index()
out = []
for i in range(0, len(rows), 3):
    r = rows.iloc[i]
    out.append(f"{r['date'].date()}  300={r['hs300']:.0f}  500={r['zz500']:.0f}  z={r['z']:.2f}")
out.append("--- 关键日 ---")
for d in ["2026-07-16", "2026-07-20", "2026-07-24", "2026-07-27", "2026-07-28", "2026-07-30", "2026-08-04", "2026-08-12"]:
    r = df.loc[d]
    out.append(f"{d}  300={r['hs300']:.0f}  500={r['zz500']:.0f}  z={r['z']:.2f}")
open("_pair_detail.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
