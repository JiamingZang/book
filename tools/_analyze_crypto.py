# -*- coding: utf-8 -*-
"""分析 Binance BTC/ETH 5m 数据，定位典型教学段（输出 UTF-8 文件避免 PowerShell 乱码）"""
import pandas as pd

OUT = []
def out(s=""):
    OUT.append(str(s))
    print(s)

for sym, name in [("btcusdt", "BTCUSDT"), ("ethusdt", "ETHUSDT")]:
    df = pd.read_csv(f"data/{sym}_5m.csv", parse_dates=["time"])
    df["day"] = df["time"].dt.date
    out(f"===== {name} =====")
    out(f"总范围: {df.time.iloc[0]} -> {df.time.iloc[-1]}  共{len(df)}根")

    daily = df.groupby("day").agg(o=("open", "first"), h=("high", "max"),
                                  l=("low", "min"), c=("close", "last"),
                                  v=("volume", "sum"))
    daily["chg%"] = (daily["c"] / daily["o"] - 1) * 100
    out("\n-- 日线汇总（最后20天）--")
    for d, r in daily.tail(20).iterrows():
        out(f"{d}  O={r.o:.0f} H={r.h:.0f} L={r.l:.0f} C={r.c:.0f} 日变幅={r['chg%']:+.2f}%")

    # 候选段详细 5m 极值
    segments = {
        "上升趋势": ("2026-07-20 00:00", "2026-07-21 20:00"),
        "横盘区间": ("2026-08-03 00:00", "2026-08-07 20:00"),
        "大跌段":   ("2026-07-31 08:00", "2026-07-31 20:00"),
    }
    for tag, (t0, t1) in segments.items():
        seg = df[(df.time >= t0) & (df.time <= t1)]
        out(f"\n-- {tag} {t0[:10]}~{t1[:10]} 共{len(seg)}根 --")
        out(f"区间: {seg.high.max():.0f} / {seg.low.min():.0f}  首={seg.open.iloc[0]:.0f} 末={seg.close.iloc[-1]:.0f}")
        # 找关键转折：3根内高低点变化 > 0.8%
        thr = seg.close.mean() * 0.008
        for i in range(2, len(seg) - 2):
            hh = seg.high.iloc[i] >= seg.high.iloc[i-1:i+3].max()
            ll = seg.low.iloc[i] <= seg.low.iloc[i-1:i+3].min()
            if hh or ll:
                chg = (seg.close.iloc[i] / seg.close.iloc[i-1] - 1) * 100
                if abs(chg) > 0.25 or hh or ll:
                    d = seg.time.iloc[i]
                    if hh and ll:
                        tag2 = "十字/外包"
                    elif hh:
                        tag2 = "波段高"
                    else:
                        tag2 = "波段低"
                    out(f"  {d}  {tag2}  H={seg.high.iloc[i]:.0f} L={seg.low.iloc[i]:.0f} C={seg.close.iloc[i]:.0f} 单根{chg:+.2f}%")
    out("\n")

with open("_crypto_analyze_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("saved: _crypto_analyze_out.txt")
