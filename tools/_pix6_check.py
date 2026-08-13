# -*- coding: utf-8 -*-
"""fig_p3_pinbar.png 像素验证：红绿 K 线、橙色支撑/阻力线、白色底"""
import sys
from collections import Counter

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

pix = pymupdf.Pixmap("handbook/images/fig_p3_pinbar.png")
c = Counter()
for y in range(0, pix.height, 3):
    for x in range(0, pix.width, 3):
        r, g, b = pix.pixel(x, y)[:3]
        if r > 200 and g < 110 and b < 110:
            c["red_k"] += 1
        elif r < 120 and g > 130 and b < 175:
            c["green_k"] += 1
        elif 230 < r < 260 and 130 < g < 190 and b < 90:
            c["orange_line"] += 1
        elif r > 245 and g > 245 and b > 245:
            c["white"] += 1
print(f"{pix.width}x{pix.height} 红K:{c['red_k']} 绿K:{c['green_k']} 橙线:{c['orange_line']} 白:{c['white']}")
