# -*- coding: utf-8 -*-
"""验证 PDF：总页数 + 新图嵌入（5 张真实图 + fig_p3_pinbar）"""
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

doc = pymupdf.open("handbook/trading-handbook.pdf")
print("总页数:", doc.page_count)

targets = ["fig_real_trend2", "fig_real_fakeout", "fig_real_pinbar",
           "fig_real_spring", "fig_real_volprof", "fig_p3_pinbar"]
found = {t: [] for t in targets}
for i in range(doc.page_count):
    imgs = doc.get_page_images(i, full=True)
    for x in imgs:
        name = x[7]
        for t in targets:
            if t in name:
                found[t].append(i + 1)
for t in targets:
    pages = found[t]
    print(f"{t:22s} 嵌入页: {pages if pages else '未找到'}")
