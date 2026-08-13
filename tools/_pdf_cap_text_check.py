# -*- coding: utf-8 -*-
"""验证 PDF 中图注文本可见：检索若干 R 图图注 + 新图图注"""
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

doc = pymupdf.open("handbook/trading-handbook.pdf")
targets = [
    "图 2-1R 真实数据", "图 3-1R 真实数据", "图 3-2R 真实数据",
    "图 5-1R 真实数据", "图 5-3R 真实数据", "图 4-7R 真实数据",
    "图 3-2 Pin Bar", "图 10-3R 真实数据",
]
for t in targets:
    pages = []
    for i in range(doc.page_count):
        text = doc[i].get_text()
        if t in text:
            pages.append(i + 1)
    print(f"{t:24s} 出现页: {pages if pages else '未找到'}")
