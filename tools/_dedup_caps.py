# -*- coding: utf-8 -*-
"""批次45c修复：删除重复 figcap——同一图号连续出现（隔空行）时保留最后一个"""
import re, glob

pat = re.compile(r"\*图 (\d+-\d+R?)([^\]]*)\*\n\n\*图 (\d+-\d+R?)([^\]]*)\*")

for p in sorted(glob.glob("handbook/0*_*.md")):
    s = open(p, encoding="utf-8").read()
    removed = 0
    while True:
        m = pat.search(s)
        if not m or m.group(1) != m.group(3):
            break
        # 保留第二个（原有/最后一个），删第一个
        s = s[: m.start()] + f"*图 {m.group(3)}{m.group(4)}*" + s[m.end():]
        removed += 1
    if removed:
        open(p, "w", encoding="utf-8", newline="\n").write(s)
        print(p, "删重复", removed, "个")
print("完成")
