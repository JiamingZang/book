# -*- coding: utf-8 -*-
"""扫描各章无图节，输出配图覆盖矩阵（只读分析用）"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

for f in sorted(os.listdir("handbook")):
    if not f.endswith(".md") or f in ("README.md",):
        continue
    path = os.path.join("handbook", f)
    text = open(path, encoding="utf-8").read()
    secs = re.findall(r"^### ([0-9.]+)\s", text, re.M)
    imgs = set(re.findall(r"!\[[^\]]*\]\(images/([^)]+)\)", text))
    noimg = []
    for s in secs:
        m = re.search(r"^### " + re.escape(s) + r"\s.*?(?=^### |\Z)", text, re.M | re.S)
        if m and "![" not in m.group(0):
            noimg.append(s)
    print(f"{f}: {len(secs)}节 {len(imgs)}图 | 无图节: {', '.join(noimg)}")
