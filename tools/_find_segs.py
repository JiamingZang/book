# -*- coding: utf-8 -*-
"""
在 BTC/ETH 5m 数据中挖掘"短而完整"的教学剧情段（60~140 根 K 线内）：
1. 区间突破  2. 两段式 push-pull  3. sweep+CHoCH 反转下跌  4. 趋势 HL 阶梯回调
输出候选段到 _seg_scan_out.txt，供人工挑选。
"""
import csv, datetime, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "_seg_scan_out.txt")

def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({"t": datetime.datetime.strptime(r["time"], "%Y-%m-%d %H:%M"),
                         "o": float(r["open"]), "h": float(r["high"]),
                         "l": float(r["low"]), "c": float(r["close"])})
    return rows

def atr_of(rows, i, n=14):
    s = 0
    pc = rows[i - 1]["c"]
    for j in range(max(0, i - n + 1), i + 1):
        r = rows[j]
        s += max(r["h"] - r["l"], abs(r["h"] - pc), abs(r["l"] - pc))
        pc = r["c"]
    return s / min(n, i + 1)

def fmt(rows, i):
    return rows[i]["t"].strftime("%m-%d %H:%M")

def find_range_break(rows, name):
    """区间（>=30根，振幅<2.2xATR均值）→ 收盘突破 → 35根内回踩守住 → 新高"""
    out = []
    n = len(rows)
    for s in range(0, n - 130):
        seg = rows[s:s + 130]
        # 区间段：前 30 根内窄
        pre = seg[:30]
        hi = max(x["h"] for x in pre); lo = min(x["l"] for x in pre)
        atrs = [atr_of(rows, s + j) for j in range(30)]
        if hi - lo > 2.2 * sum(atrs) / len(atrs):
            continue
        if hi - lo < 0.08 * hi:  # 太窄可能是死水
            continue
        # 突破：30 根之后 20 根内收盘 > hi
        b = None
        for j in range(30, 55):
            if seg[j]["c"] > hi:
                b = s + j
                break
        if b is None:
            continue
        # 回踩守住：突破后 35 根内收盘不回区间内部（回踩用收盘价判定）
        aft = rows[b:b + 36]
        dip = min(x["c"] for x in aft)
        if dip < hi - 0.5 * (hi - lo):
            continue
        # 新高：突破后 35 根内最高 > hi + 0.05*(hi-lo)
        hi2 = max(x["h"] for x in aft)
        if hi2 <= hi + 0.1 * (hi - lo):
            continue
        end = b + 35
        out.append((name, rows[s]["t"], rows[end]["t"], end - s + 1,
                    "区间突破: 区间[%.1f,%.1f] 突破@%s 回踩低%.1f 新高%.1f" % (
                        hi, lo, fmt(rows, b), dip, hi2)))
    return out

def find_two_leg(rows, name):
    """第一腿(15-30根,>1.0%) → 回调(5-20根,回撤<60%) → 第二腿(15-30根,>0.8%) → 20根内高潮回落"""
    out = []
    n = len(rows)
    for s in range(0, n - 130):
        seg = rows[s:s + 130]
        # 第一腿高点：s+15..s+45 内最高
        p1 = s + 15 + max(range(30), key=lambda k: seg[15 + k]["h"])
        if p1 - s < 15: continue
        rise1 = seg[p1 - s]["h"] - seg[0]["o"]
        if rise1 / seg[0]["o"] < 0.008: continue
        # 回调低点：p1+5..p1+25 内最低
        p2 = p1 + 5 + min(range(20), key=lambda k: seg[p1 + 5 + k - s]["l"])
        dd = seg[p1 - s]["h"] - seg[p2 - s]["l"]
        if dd <= 0 or (seg[p1 - s]["h"] - seg[p2 - s]["l"]) / rise1 > 0.75: continue
        # 第二腿高点：p2+10..p2+35 内最高
        p3 = p2 + 10 + max(range(25), key=lambda k: seg[p2 + 10 + k - s]["h"])
        rise2 = seg[p3 - s]["h"] - seg[p2 - s]["l"]
        if rise2 / seg[p2 - s]["l"] < 0.005: continue
        # 高潮回落：p3+5..p3+25 内收盘低于 p3 高点 0.4%
        aft = seg[p3 - s + 5: p3 - s + 26]
        if not aft or max(x["c"] for x in aft) > seg[p3 - s]["h"] * 0.998:
            continue
        end = p3 + 25
        out.append((name, rows[s]["t"], rows[end]["t"], end - s + 1,
                    "两段式: 腿1@%s +%.1f%% 回调@%s -%.1f%% 腿2@%s +%.1f%% 回落" % (
                        fmt(rows, p1), 100 * rise1 / seg[0]["o"], fmt(rows, p2),
                        100 * dd / seg[p1 - s]["h"], fmt(rows, p3),
                        100 * rise2 / seg[p2 - s]["l"])))
    return out

def find_sweep(rows, name):
    """40根窗口新高 → 15根内收盘 < 前60根最低 → 下跌30根累计-0.8%"""
    out = []
    n = len(rows)
    for s in range(60, n - 100):
        pre = rows[s - 30:s]
        h1 = max(x["h"] for x in pre); h1i = s - 30 + pre.index(next(x for x in pre if x["h"] == h1))
        lo_prev = min(x["l"] for x in rows[s - 60:s])
        # 冲高后立即跌破前低（s..s+20）
        for j in range(s, min(s + 20, n - 60)):
            if rows[j]["c"] < lo_prev:
                # 之后下跌段
                aft = rows[j:j + 35]
                if max(x["h"] for x in aft) - min(x["l"] for x in aft) < 0.005 * lo_prev:
                    break
                low = min(x["l"] for x in aft)
                drop = (h1 - low) / h1
                if drop > 0.008:
                    end = j + 35
                    out.append((name, rows[s - 30]["t"], rows[end]["t"], end - (s - 30) + 1,
                                "sweep: 冲高@%s %.1f 破前低@%s %.1f 跌至@%s -%.1f%%" % (
                                    fmt(rows, h1i), h1, fmt(rows, j), lo_prev,
                                    fmt(rows, aft.index(min(aft, key=lambda x: x["l"])) + j), 100 * drop)))
                break
    return out

def find_hl_trend(rows, name):
    """上升趋势 2-3 次 HL 回调：每段 60-110 根，回调 3-8 根回撤<40%，总涨幅>1.5%"""
    out = []
    n = len(rows)
    for s in range(0, n - 130):
        seg = rows[s:s + 130]
        # 找 3 个依次抬高的低点（HL）
        lows = []
        i = 5
        while i < 120 and len(lows) < 3:
            w = seg[i:i + 12]
            li = i + w.index(min(w, key=lambda x: x["l"]))
            if li > i:
                lows.append(s + li)
                i = li + 4
            else:
                i += 1
        if len(lows) < 3:
            continue
        if not (lows[1] > lows[0] and lows[2] > lows[1]):
            continue
        # 每个 HL 之后都创新高
        ok = True
        for k in range(3):
            nxt = rows[lows[k]:lows[k] + 25]
            if max(x["h"] for x in nxt) <= rows[lows[k]]["l"]:
                ok = False; break
        if not ok:
            continue
        total = (rows[lows[2] + 15]["c"] - seg[0]["o"]) / seg[0]["o"]
        if total < 0.012:
            continue
        end = lows[2] + 20
        out.append((name, rows[s]["t"], rows[end]["t"], end - s + 1,
                    "HL趋势: HL@%s %.1f HL@%s %.1f HL@%s %.1f 总+%.1f%%" % (
                        fmt(rows, lows[0]), rows[lows[0]]["l"],
                        fmt(rows, lows[1]), rows[lows[1]]["l"],
                        fmt(rows, lows[2]), rows[lows[2]]["l"], 100 * total)))
    return out

def find_vol_shift(rows, name):
    """波动率切换段：100 根内 ATR 前半均值 / 后半均值 > 1.7（平静→爆发 或 爆发→平静）"""
    out = []
    n = len(rows)
    for s in range(0, n - 100):
        at = [atr_of(rows, s + j) for j in range(100)]
        a1 = sum(at[:50]) / 50
        a2 = sum(at[50:]) / 50
        ratio = max(a1, a2) / max(min(a1, a2), 1e-9)
        if ratio < 1.7:
            continue
        if a2 > a1:
            desc = "平静→爆发 (ATR %.0f→%.0f)" % (a1, a2)
        else:
            desc = "爆发→平静 (ATR %.0f→%.0f)" % (a1, a2)
        out.append((name, rows[s]["t"], rows[s + 99]["t"], 100, desc))
    return out


def dedup(segs, gap_h=6):
    """同品种段去重：起始时间间隔小于 gap_h 的保留第一条"""
    segs = sorted(segs, key=lambda x: x[1])
    out = []
    for s in segs:
        if out and (s[1] - out[-1][1]).total_seconds() < gap_h * 3600:
            continue
        out.append(s)
    return out

def main():
    btc = load(os.path.join(DATA, "btcusdt_5m.csv"))
    eth = load(os.path.join(DATA, "ethusdt_5m.csv"))
    lines = []
    for name, rows in (("BTC", btc), ("ETH", eth)):
        for tag, fn in (("区间突破", find_range_break), ("两段式", find_two_leg),
                        ("sweep", find_sweep), ("HL趋势", find_hl_trend),
                        ("波动切换", find_vol_shift)):
            cands = dedup(fn(rows, name))
            lines.append("==== %s %s 候选 %d 段 ====" % (name, tag, len(cands)))
            for c in cands[:12]:
                lines.append("  %s ~ %s [%d根] %s" % (c[1].strftime("%m-%d %H:%M"),
                                                      c[2].strftime("%m-%d %H:%M"), c[3], c[4]))
            lines.append("")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("written", OUT, len(lines), "lines")

if __name__ == "__main__":
    main()
