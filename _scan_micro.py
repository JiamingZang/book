# -*- coding: utf-8 -*-
"""扫描 510300 5 分钟线，找教科书级微通道段"""
import akshare as ak
import pandas as pd

df = ak.stock_zh_a_minute(symbol='sh510300', period='5', adjust='')
df['day'] = pd.to_datetime(df['day'])
for c in ['open', 'high', 'low', 'close']:
    df[c] = df[c].astype(float)

lows = df['low'].values
days = df['day'].values
closes = df['close'].values
opens = df['open'].values

runs = []
start = 0
for i in range(1, len(lows)):
    if lows[i] < lows[i-1] - 1e-9:
        if i - start >= 8:
            runs.append((start, i-1))
        start = i
if len(lows) - start >= 8:
    runs.append((start, len(lows)-1))

print('低点非递减段(>=8根):', len(runs))
for s, e in runs:
    seg = df.iloc[s:e+1]
    up_ratio = (seg['close'] >= seg['open']).mean()
    rise = seg['close'].iloc[-1] / seg['close'].iloc[0] - 1
    # 通道倾角：低点回归斜率
    xs = list(range(e-s+1))
    import numpy as np
    k = np.polyfit(xs, seg['low'].values, 1)[0]
    print(f'{str(days[s])[:16]} ~ {str(days[e])[:16]}  n={e-s+1:2d} 阳线比={up_ratio:.0%} 涨幅={rise:+.1%} 低点斜率={k:.5f}')
