# -*- coding: utf-8 -*-
"""fig_real_ma.png 像素验证：红绿K线 + 蓝EMA + 橙EMA + 白底"""
import sys
from collections import Counter

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

pix = pymupdf.Pixmap("handbook/images/fig_real_ma.png")
c = Counter()
for y in range(0, pix.height, 3):
    for x in range(0, pix.width, 3):
        r, g, b = pix.pixel(x, y)[:3]
        if r > 200 and g < 110 and b < 110:
            c["red_k"] += 1
        elif r < 120 and g > 130 and b < 175:
            c["green_k"] += 1
        elif b > 150 and r < 90 and g > 90:
            c["blue_line"] += 1
        elif r > 200 and 90 < g < 150 and b < 60:
            c["orange_line"] += 1
        elif r > 245 and g > 245 and b > 245:
            c["white"] += 1
print(f"{pix.width}x{pix.height} 红K:{c['red_k']} 绿K:{c['green_k']} 蓝EMA:{c['blue_line']} 橙EMA:{c['orange_line']} 白:{c['white']}")
