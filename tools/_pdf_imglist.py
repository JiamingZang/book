# -*- coding: utf-8 -*-
"""列出 PDF 中所有嵌入图片名（含新图）"""
import sys
from collections import Counter

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

doc = pymupdf.open("handbook/trading-handbook.pdf")
names = []
for i in range(doc.page_count):
    for x in doc.get_page_images(i, full=True):
        names.append(x[7])
c = Counter(names)
print("唯一图片:", len(c))
for n in sorted(c):
    if "real" in n or "pinbar" in n or "p3" in n:
        print("  NEW:", n, "x", c[n])
print("--- 非 real 前 10 个 ---")
for n in sorted(c):
    if "real" not in n:
        print("  ", n, "x", c[n])
