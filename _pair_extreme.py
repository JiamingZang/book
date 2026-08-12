# -*- coding: utf-8 -*-
"""扫描更长时间窗口：找 z 偏离后继续走到极端的案例（止损教学）"""
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
z = (lr - lr.rolling(win).mean()) / lr.rolling(win).std()
df["z"] = z

out = []
# 极值时段
for lo, hi in [(-99, -3.5), (3.5, 99), (-99, -2.8), (2.8, 99)]:
    segs = (df["z"] > lo) & (df["z"] < hi) if lo < 0 and hi < 0 else ((df["z"] > lo) & (df["z"] < hi)) if lo > 0 else None
sel = df[(df["z"] < -2.8) | (df["z"] > 2.8)]
out.append("=== z 超出 ±2.8 的日期 ===")
for d, r in sel.iterrows():
    out.append(f"{d.date()}  z={r['z']:.2f}  300={r['hs300']:.0f}  500={r['zz500']:.0f}")
open("_pair_extreme.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
