# -*- coding: utf-8 -*-
"""Binance 加密 5m K线数据拉取（批次34：真实图数据源）
用法: python tools/_fetch_binance.py
输出: data/btcusdt_5m.csv, data/ethusdt_5m.csv（时间,open,high,low,close,volume）
"""
import json, time, urllib.request, os, datetime

BASE = "https://api.binance.com/api/v3/klines"
SYMBOLS = ["BTCUSDT", "ETHUSDT"]
DAYS = 45  # 拉取天数

def fetch_klines(symbol, interval="5m", start_ms=None, end_ms=None):
    """分页拉取，每次 1000 根"""
    rows = []
    while True:
        url = "%s?symbol=%s&interval=%s&limit=1000" % (BASE, symbol, interval)
        if start_ms:
            url += "&startTime=%d" % start_ms
        if end_ms:
            url += "&endTime=%d" % end_ms
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        d = json.load(urllib.request.urlopen(req, timeout=20))
        if not d:
            break
        rows.extend(d)
        last = d[-1][0]
        if len(d) < 1000:
            break
        start_ms = last + 1  # 下一段从最后一根之后开始
        time.sleep(0.2)
    return rows

def main():
    os.makedirs("data", exist_ok=True)
    end_ms = int(time.time() * 1000)
    start_ms = end_ms - DAYS * 86400 * 1000
    for sym in SYMBOLS:
        rows = fetch_klines(sym, start_ms=start_ms)
        # 按时间升序去重
        seen = {}
        for k in rows:
            seen[k[0]] = k
        rows = [seen[t] for t in sorted(seen)]
        path = "data/%s_5m.csv" % sym.lower()
        with open(path, "w", encoding="utf-8") as f:
            f.write("time,open,high,low,close,volume\n")
            for k in rows:
                t = datetime.datetime.fromtimestamp(k[0] / 1000).strftime("%Y-%m-%d %H:%M")
                f.write("%s,%s,%s,%s,%s,%s\n" % (t, k[1], k[2], k[3], k[4], k[5]))
        print("%s: %d 根 -> %s" % (sym, len(rows), path))

if __name__ == "__main__":
    main()
