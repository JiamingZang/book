# -*- coding: utf-8 -*-
"""批次45 PDF 验证：总页数 + 图 xref 数 + 新图注文本定位"""
import sys
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

doc = pymupdf.open("handbook/trading-handbook.pdf")
print("总页数:", doc.page_count)

# 全库图片 xref 统计
seen = set()
for i in range(doc.page_count):
    for x in doc.get_page_images(i, full=True):
        seen.add(x[0])
print("图片 xref 数:", len(seen))

# 新图注文本定位（alt 版 figcap）
for t in ["图 2-7 趋势线与通道", "图 2-8 缺口四类", "图 4-7 斐波那契回撤",
          "图 4-5R 真实数据：移动止损", "图 6-1R 真实数据：ATR 波动率通道",
          "图 2-13 尖峰识别", "图 4-9R 真实数据：突破生命周期"]:
    pages = [i + 1 for i in range(doc.page_count) if t in doc[i].get_text()]
    print(f"{t}: 页 {pages}")
