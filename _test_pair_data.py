# -*- coding: utf-8 -*-
"""测试配对交易真实图数据：沪深300 vs 中证500 指数日线（新浪源）"""
import akshare as ak
import pandas as pd

pairs = [("sh000300", "沪深300"), ("sz399905", "中证500"),
         ("sh000001", "上证指数"), ("sz399001", "深证成指"),
         ("sh510300", "300ETF"), ("sh510050", "50ETF"), ("sh510500", "500ETF")]

data = {}
for code, name in pairs:
    try:
        df = ak.stock_zh_index_daily(symbol=code) if code.startswith(("sh0", "sz3")) else ak.stock_zh_a_daily(symbol=code)
        df = df.tail(10)
        data[name] = df
        print(f"OK {name}({code}): 最新收盘 {df.close.iloc[-1]:.3f} @ {df.date.iloc[-1]}")
    except Exception as e:
        print(f"FAIL {name}({code}): {type(e).__name__}: {str(e)[:80]}")
