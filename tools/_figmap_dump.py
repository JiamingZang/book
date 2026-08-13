# -*- coding: utf-8 -*-
"""按行号 dump 指定章节全部图引用（普通 + R），用于确定重编号方案"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

for fname in ["handbook/02_price_action.md", "handbook/04_trading_system.md"]:
    print(f"\n===== {fname} =====")
    lines = open(fname, encoding="utf-8").read().splitlines()
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(r"图\s*(\d+)-(\d+)(R)?", ln):
            ch, n, is_r = m.group(1), m.group(2), bool(m.group(3))
            if ch == fname[9:11].lstrip("0"):
                tag = "R" if is_r else " "
                print(f"  L{i:5d}  图{ch}-{n}{tag}  {ln.strip()[:80]}")
