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
for t in ["图 1-3R 真实数据：下跌趋势中的尖峰陷阱", "图 1-4R 真实数据：BTC 与 ETH 的相关性不是常数", "图 2-3R 真实数据：尖峰 → 第二波衰竭", "图 2-4R 真实数据：恐慌抛售高潮 → 插针收回", "图 10-4R 真实数据：IV 与 RV 的真实关系", "图 10-5R 真实数据：波动率的分布不是正态",
          "图 9-2R 真实数据：考核的隐形杀手不是爆仓，是平庸", "图 9-3R 真实数据：考核通过率 Monte Carlo", "图 9-4R 真实数据：考核中最危险的一天",
          "图 8-3R 真实数据：40 组 EMA 参数全部亏损",
          "图 6-1R 真实数据：回本不对称", "图 6-2R 真实数据：同样的 82 笔交易", "图 6-3R 真实数据：ATR 波动率通道", "图 6-4R 真实数据：止损后价格回来了",
          "图 7-1R 真实数据：规则系统的持仓时长", "图 7-2R 真实数据：连亏不是故障，是分布", "图 7-3R 真实数据：报复交易的数学", "图 7-4R 真实数据：一页真实交易日志的统计视图"]:
    pages = [i + 1 for i in range(doc.page_count) if t in doc[i].get_text()]
    print(f"{t}: 页 {pages}")
