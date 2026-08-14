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

# 新图注文本定位（alt 版 figcap；图号随批次 45b/46/47 顺延过，此处为当前号）
for t in ["图 1-3R 真实数据：BTC 与 ETH 的相关性不是常数", "图 2-3R 真实数据：尖峰 → 第二波衰竭", "图 10-4R 真实数据：IV 与 RV 的真实关系", "图 9-1R 真实数据：同一批真实交易记录",
          "图 9-2R 真实数据：考核的隐形杀手不是爆仓，是平庸", "图 9-3R 真实数据：考核通过率 Monte Carlo",
          "图 8-3R 真实数据：40 组 EMA 参数全部亏损",
          "图 6-1R 真实数据：同样的 82 笔交易", "图 6-2R 真实数据：ATR 波动率通道",
          "图 8-2R 真实数据：样本量幻觉"]:
    pages = [i + 1 for i in range(doc.page_count) if t in doc[i].get_text()]
    print(f"{t}: 页 {pages}")
