# -*- coding: utf-8 -*-
"""像素验证 5 张新真实图：红绿 K 线 + 标注色齐全"""
import sys
from collections import Counter

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

files = ["fig_real_trend2", "fig_real_fakeout", "fig_real_pinbar", "fig_real_spring", "fig_real_volprof"]

def sample(path, step=4):
    pix = pymupdf.Pixmap(path)
    c = Counter()
    for y in range(0, pix.height, step):
        for x in range(0, pix.width, step):
            r, g, b = pix.pixel(x, y)[:3]
            if r > 200 and g < 110 and b < 110:
                c["red_k"] += 1
            elif r < 120 and g > 130 and b < 175:
                c["green_k"] += 1
            elif r < 90 and g > 120 and b > 150:
                c["teal_ann"] += 1
            elif 220 < r < 255 and 130 < g < 180 and b < 120:
                c["orange_ann"] += 1
            elif r > 225 and g > 225 and b > 225:
                c["white"] += 1
    return pix.width, pix.height, c

for f in files:
    w, h, c = sample(f"handbook/images/{f}.png")
    print(f"{f:22s} {w}x{h} 红K:{c['red_k']:5d} 绿K:{c['green_k']:5d} teal:{c['teal_ann']:5d} 橙:{c['orange_ann']:5d} 白:{c['white']:6d}")
