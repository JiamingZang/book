# -*- coding: utf-8 -*-
"""批次44 PDF 验证：总页数 + fig_real_ma 嵌入 + 图注文本"""
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

doc = pymupdf.open("handbook/trading-handbook.pdf")
print("总页数:", doc.page_count)

# 找 fig_real_ma 所在页（按尺寸 1491x699 附近）
for i in range(doc.page_count):
    for x in doc.get_page_images(i, full=True):
        if x[2] > 1400 and abs(x[3] - 700) < 40:
            print(f"  可能 fig_real_ma: 页{i+1} {x[7]} {x[2]}x{x[3]}")

for t in ["图 4-5R 真实数据：均线趋势跟踪", "图 4-8R 真实数据：突破生命周期"]:
    pages = [i + 1 for i in range(doc.page_count) if t in doc[i].get_text()]
    print(f"{t}: 页 {pages}")
