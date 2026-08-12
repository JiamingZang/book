# -*- coding: utf-8 -*-
"""2026-01 深坑案例完整轨迹：z 从 -2.84 到 -4.04 再到回归"""
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

rows = df.loc["2025-12-20":"2026-03-31"].reset_index()
out = []
for i in range(0, len(rows), 3):
    r = rows.iloc[i]
    out.append(f"{r['date'].date()}  300={r['hs300']:.0f}  500={r['zz500']:.0f}  z={r['z']:.2f}")
out.append("--- 关键日 ---")
for d in ["2025-12-31", "2026-01-05", "2026-01-08", "2026-01-12", "2026-01-16", "2026-01-23", "2026-02-06", "2026-03-02", "2026-03-31"]:
    r = df.loc[d]
    out.append(f"{d}  300={r['hs300']:.0f}  500={r['zz500']:.0f}  z={r['z']:.2f}")
# 01-05 建仓的盈亏轨迹（多300空500，等名义）
out.append("--- 01-05 建仓（多300空500）盈亏 ---")
p0 = (df.loc["2026-01-05", "hs300"], df.loc["2026-01-05", "zz500"])
for d in ["2026-01-12", "2026-02-06", "2026-03-31", "2026-06-30", "2026-08-12"]:
    r = df.loc[d]
    pl = (r["hs300"]/p0[0]-1) - (r["zz500"]/p0[1]-1)
    out.append(f"{d}: 300 {(r['hs300']/p0[0]-1)*100:+.1f}% | 500 {(r['zz500']/p0[1]-1)*100:+.1f}% | 净 {pl*100:+.1f}%")
open("_pair_jan.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
