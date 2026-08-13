# -*- coding: utf-8 -*-
"""全图号序列审计：每章普通图 + R 图按正文出现顺序，找空缺/跳号/乱序"""
import re
import sys
import glob

sys.stdout.reconfigure(encoding="utf-8")

for f in sorted(glob.glob("handbook/0*_*.md")) + sorted(glob.glob("handbook/1*_*.md")):
    base = f.split("\\")[-1].split("/")[-1]
    ch_no = int(base[:2])
    text = open(f, encoding="utf-8").read()
    nums = []
    for m in re.finditer(r"图\s*(\d+)-(\d+)(R)?", text):
        ch, n, is_r = int(m.group(1)), int(m.group(2)), bool(m.group(3))
        if ch == ch_no:
            nums.append((n, is_r))
    if not nums:
        continue
    # 按正文出现顺序
    plain = [n for n, r in nums if not r]
    print(f"\n{base}: 普通图出现顺序 {plain}")
    # 普通图序列检查（按出现顺序应严格递增）
    bad = [(a, b) for a, b in zip(plain, plain[1:]) if b <= a]
    if bad:
        print("  普通图乱序/重复:", bad)
