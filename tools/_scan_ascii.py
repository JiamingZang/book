# -*- coding: utf-8 -*-
"""扫描各章代码块内 ASCII 图残留（批次30 审计用）"""
import re, glob

PAT = re.compile(r"[╱╲│─┌┐└┘├┤●▒○▲▼←→↑↓]")
for f in sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/1*.md")):
    s = open(f, encoding="utf-8").read()
    inblock = False
    art = []
    for i, ln in enumerate(s.split("\n"), 1):
        if ln.strip().startswith("```"):
            inblock = not inblock
            continue
        if inblock and PAT.search(ln):
            art.append(i)
    if art:
        print(f, "代码块内图形行:", len(art), art[:12])
print("扫描完成")
