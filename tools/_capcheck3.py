# -*- coding: utf-8 -*-
"""批次45c：检查第 3 章 img 是否缺 figcap"""
import re

p = "handbook/03_第3章_入场信号.md"
lines = open(p, encoding="utf-8").read().splitlines()
missing = []
for i, ln in enumerate(lines):
    m = re.match(r"!\[(图 3-[\dR]+)", ln)
    if m:
        num = m.group(1)
        nxt = ""
        for j in range(i + 1, min(i + 3, len(lines))):
            fm = re.match(r"\*(图 3-[\dR]+)", lines[j].strip())
            if fm:
                nxt = fm.group(1)
                break
        if nxt != num:
            missing.append((i + 1, num, nxt or "无"))
print("缺 figcap:", missing if missing else "无")
