# -*- coding: utf-8 -*-
"""批次45 像素验证：三张新图尺寸 + 关键颜色像素统计"""
import sys
import fitz  # pymupdf

sys.stdout.reconfigure(encoding="utf-8")

TARGETS = {
    "fig_p2_trendline.png": {"teal": 0, "orange": 0, "down": 0},
    "fig_p2_gaps.png": {"teal": 0, "orange": 0, "down": 0, "blue": 0},
    "fig_p4_fib.png": {"teal": 0, "orange": 0, "down": 0},
}
C = {
    "teal": (38, 166, 154), "orange": (255, 152, 0),
    "down": (239, 83, 80), "blue": (66, 165, 245),
}

for name, want in TARGETS.items():
    path = f"handbook/images/{name}"
    doc = fitz.open(path)
    pix = doc[0].get_pixmap()
    doc.close()
    w, h = pix.width, pix.height
    cnt = {k: 0 for k in want}
    step = 3  # 采样步长
    for yy in range(0, h, step):
        for xx in range(0, w, step):
            r, g, b = pix.pixel(xx, yy)[:3]
            for k, (cr, cg, cb) in C.items():
                if abs(r - cr) < 30 and abs(g - cg) < 30 and abs(b - cb) < 30:
                    cnt[k] += 1
    ok = all(cnt[k] > 20 for k in want)
    print(f"{name}: {w}x{h} 颜色像素 {cnt} -> {'OK' if ok else 'MISSING'}")
