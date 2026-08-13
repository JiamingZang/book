# -*- coding: utf-8 -*-
"""按尺寸找新图：fig_real_* 5张 ≈1430x715，fig_p3_pinbar ≈1708x808"""
import sys
from collections import Counter

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

doc = pymupdf.open("handbook/trading-handbook.pdf")
sizes = Counter()
big = []
for i in range(doc.page_count):
    for x in doc.get_page_images(i, full=True):
        w, h = x[2], x[3]
        sizes[(w, h)] += 1
        if w >= 1300 or (w >= 1600 and h >= 700):
            big.append((i + 1, x[7], w, h))
print("大图（w>=1300 或 1600x700+）:")
for p, n, w, h in sorted(big):
    print(f"  页{p:3d} {n:8s} {w}x{h}")
