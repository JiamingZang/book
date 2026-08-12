# -*- coding: utf-8 -*-
"""扫描上证指数 20 日实现波动率（年化），找最近的暴涨回落案例"""
import akshare as ak
import pandas as pd
import numpy as np

df = ak.stock_zh_index_daily(symbol="sh000001")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
ret = df["close"].pct_change()
rv = ret.rolling(20).std() * np.sqrt(252) * 100  # 年化 %
df["rv20"] = rv

sel = df.loc["2026-03-01":]
out = []
for i in range(0, len(sel), 5):
    r = sel.iloc[i]
    out.append(f"{r.name.date()}  收盘={r['close']:.0f}  RV20={r['rv20']:.1f}%")
out.append("--- 峰值日 ---")
peak = sel["rv20"].idxmax()
out.append(f"RV20 峰值: {peak.date()} = {sel.loc[peak,'rv20']:.1f}%  (收盘 {sel.loc[peak,'close']:.0f})")
# 局部峰值：前后 5 日均更低
vals = sel["rv20"].values
for i in range(5, len(vals) - 5):
    if vals[i] > 20 and vals[i] == max(vals[i-5:i+6]):
        out.append(f"局部峰: {sel.index[i].date()} RV20={vals[i]:.1f}%")
open("_rv_scan.txt", "w", encoding="utf-8").write("\n".join(out))
print("done")
