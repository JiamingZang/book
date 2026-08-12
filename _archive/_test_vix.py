# -*- coding: utf-8 -*-
"""测试 VIX 数据源可用性"""
import akshare as ak
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

tests = [
    ("ak.option_cboe_volatility_index", lambda: ak.option_cboe_volatility_index()),
    ("ak.stock_us_daily(VIX)", lambda: ak.stock_us_daily(symbol="VIX")),
    ("ak.index_vix", lambda: ak.index_vix()),
]
for name, fn in tests:
    try:
        df = fn()
        print(f"OK {name}: 列={list(df.columns)[:8]} 行数={len(df)}")
        print(df.tail(2).to_string())
    except Exception as e:
        print(f"FAIL {name}: {type(e).__name__}: {str(e)[:100]}")
