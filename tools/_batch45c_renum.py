# -*- coding: utf-8 -*-
"""批次45c：第 3 章图号顺延 3-1~3-14 → 3-2~3-15（R 图 3-1R~3-3R 不动）
新图 3-1 判定框架插入 3.1 节，其后全部普通图 +1。
仅匹配"图 3-N"（N 后非 R 非数字），正文日期如"3-13 起 7 天"无"图"前缀不受影响。
"""
import re

p = "handbook/03_entry_signals.md"
s = open(p, encoding="utf-8").read()

pat = re.compile(r"图 3-(\d+)(?!R|\d)")
hits = pat.findall(s)
print("顺延命中", len(hits), "处:", hits)

s2 = pat.sub(lambda m: f"图 3-{int(m.group(1)) + 1}", s)
open(p, "w", encoding="utf-8", newline="\n").write(s2)
print("已写入")
