# -*- coding: utf-8 -*-
"""扫描配对价差：找 z-score 偏离>2 后回归均值的清晰案例"""
import akshare as ak
import pandas as pd
import numpy as np

def get(code):
    df = ak.stock_zh_index_daily(symbol=code)
    df = df.rename(columns={"date": "date", "close": "close"})
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["close"]

def scan(a_name, b_name, label, win=60, n_days=400):
    a, b = get(a_name), get(b_name)
    df = pd.concat([a, b], axis=1, keys=["a", "b"]).dropna().tail(n_days)
    lr = np.log(df["a"] / df["b"])
    m = lr.rolling(win).mean()
    s = lr.rolling(win).std()
    z = (lr - m) / s
    df["z"] = z
    # 找 z>2 的片段
    over = (df["z"] > 2).astype(int)
    segs = []
    start = None
    for i, v in over.items():
        if v == 1 and start is None:
            start = i
        elif v == 0 and start is not None:
            segs.append((start, i))
            start = None
    if start is not None:
        segs.append((start, df.index[-1]))
    print(f"===== {label} ({a_name} vs {b_name}) 最近{n_days}日, win={win} =====")
    print(f"相关性: {df['a'].corr(df['b']):.3f}")
    for st, en in segs[-5:]:
        zmax = df.loc[st:en, "z"].max()
        zmax_date = df.loc[st:en, "z"].idxmax()
        # 之后 20 日 z 是否回归到 1 以下
        after = df.loc[en:, "z"]
        if len(after) > 3:
            z_now = after.iloc[min(3, len(after)-1)]
        else:
            z_now = float("nan")
        print(f"  z>2 段: {st.date()} ~ {en.date()} | z峰值 {zmax:.1f} @ {zmax_date.date()} | 3日后z: {z_now:.1f}")
    return df

for pair in [("sh000300", "sz399905", "沪深300 vs 中证500"),
             ("sh000001", "sz399001", "上证指数 vs 深证成指")]:
    df = scan(*pair)
    # 存 csv 供画图
    df.to_csv(f"_pair_{pair[2].replace(' ', '_')}.csv")
