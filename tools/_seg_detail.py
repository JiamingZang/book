# -*- coding: utf-8 -*-
"""输出选定段的局部极值明细，供人工确定图表标注点"""
import csv, datetime, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "_seg_detail_out.txt")

def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({"t": datetime.datetime.strptime(r["time"], "%Y-%m-%d %H:%M"),
                         "o": float(r["open"]), "h": float(r["high"]),
                         "l": float(r["low"]), "c": float(r["close"])})
    return rows

SEGS = [
    ("ETH 两段式", "ethusdt_5m.csv", "07-02 15:30", "07-03 00:15"),
    ("BTC 突破-回调-第二腿", "btcusdt_5m.csv", "07-14 19:15", "07-15 02:40"),
    ("BTC sweep下跌日", "btcusdt_5m.csv", "07-02 04:10", "07-02 11:10"),
    ("BTC HL阶梯上升", "btcusdt_5m.csv", "06-29 22:10", "06-30 02:35"),
    ("BTC ATR平静到爆发", "btcusdt_5m.csv", "07-01 15:00", "07-01 23:15"),
    ("BTC 区间突破候选", "btcusdt_5m.csv", "06-29 08:40", "06-29 16:20"),
]

def main():
    lines = []
    for tag, fname, t0s, t1s in SEGS:
        rows = load(os.path.join(DATA, fname))
        t0 = datetime.datetime.strptime("2026-" + t0s, "%Y-%m-%d %H:%M")
        t1 = datetime.datetime.strptime("2026-" + t1s, "%Y-%m-%d %H:%M")
        seg = [r for r in rows if t0 <= r["t"] <= t1]
        lines.append("==== %s %s [%d根] ====" % (fname[:6], tag, len(seg)))
        # 区间统计
        hi = max(r["h"] for r in seg); lo = min(r["l"] for r in seg)
        lines.append("区间 [%.1f ~ %.1f] 宽 %.1f" % (lo, hi, hi - lo))
        # 每10根采样
        for i in range(0, len(seg), 10):
            r = seg[i]
            lines.append("  %s  O%.1f H%.1f L%.1f C%.1f" % (r["t"].strftime("%m-%d %H:%M"),
                                                           r["o"], r["h"], r["l"], r["c"]))
        # 局部极值（±6根窗口）
        exts = []
        for i in range(len(seg)):
            w = seg[max(0, i - 6): i + 7]
            if seg[i]["h"] == max(x["h"] for x in w) and seg[i]["h"] > seg[i]["o"]:
                exts.append("H@%s %.1f" % (seg[i]["t"].strftime("%m-%d %H:%M"), seg[i]["h"]))
            elif seg[i]["l"] == min(x["l"] for x in w) and seg[i]["l"] < seg[i]["o"]:
                exts.append("L@%s %.1f" % (seg[i]["t"].strftime("%m-%d %H:%M"), seg[i]["l"]))
        lines.append("极值: " + " | ".join(exts))
        lines.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("written", OUT)

if __name__ == "__main__":
    main()
