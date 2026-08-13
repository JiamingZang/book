# -*- coding: utf-8 -*-
"""批次45c：第 3 章补 figcap——img 行后插入 *图 3-X alt文本*"""
import re

p = "handbook/03_entry_signals.md"
s = open(p, encoding="utf-8").read()

# 匹配 img 行后跟空行（无 figcap）：![图 3-X ...](...)\n\n
pat = re.compile(r"(!\[(图 3-[\dR]+[^\]]*)\]\([^)]+\))\n\n")
cnt = 0
def rep(m):
    global cnt
    cnt += 1
    return f"{m.group(1)}\n\n*{m.group(2)}*\n\n"

s2 = pat.sub(rep, s)
open(p, "w", encoding="utf-8", newline="\n").write(s2)
print("补 figcap:", cnt, "处")
