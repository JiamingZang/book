# -*- coding: utf-8 -*-
"""批次46：第 4 章图号顺延（占位符两步法，R 图不动）
旧普通图 → 新普通图：1→2,2→3,...,7→8, 8→11, 9→14,...,15→20
新图插入用最终号（4-1/4-9/4-10/4-12/4-13），不与顺延后的号冲突
注意：第二步必须用正则 (?!\d) 边界，否则 '图 4-PH1' 会误伤 '图 4-PH10' 前缀
"""
import re

p = "handbook/04_trading_system.md"
s = open(p, encoding="utf-8").read()

# 映射：旧号 → 新号（普通图；R 图保持原样）
mapping = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8,
           8: 11, 9: 14, 10: 15, 11: 16, 12: 17, 13: 18, 14: 19, 15: 20}

# 第一步：旧号 → 占位符（负向前瞻防 R 图与多位数）
pat = re.compile(r"图 4-(\d+)(?!R|\d)")
hits = pat.findall(s)
print("顺延命中", len(hits), "处")
for old in sorted(mapping, reverse=True):
    s = re.sub(r"图 4-%d(?!R|\d)" % old, "图 4-PH%d" % old, s)

# 第二步：占位符 → 新号（(?!\d) 防止 PH1 误伤 PH10~PH15）
for old, new in mapping.items():
    s = re.sub(r"图 4-PH%d(?!\d)" % old, "图 4-%d" % new, s)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("已写入")
# 验证
s2 = open(p, encoding="utf-8").read()
print("剩余占位符:", s2.count("PH"))
