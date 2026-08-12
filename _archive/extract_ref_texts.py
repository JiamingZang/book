# -*- coding: utf-8 -*-
"""提取重点参考 PDF 全文为 txt，供阅读提炼"""
import pathlib
import pymupdf

base = pathlib.Path(r"c:\Users\18315\Desktop\新建文件夹")
outdir = pathlib.Path(r"c:\Users\18315\Desktop\新建文件夹\_ref_texts")
outdir.mkdir(exist_ok=True)

targets = [
    "阿布10种最佳价格行为交易模式.pdf",
    "高概率微通道交易系统核心：如何入场_平仓_管理订单。10,000Trades_舒_笔记(2)(1).pdf",
    "高概率微通道交易系统基础，值得反复学习。10,000Trades_Ali_舒服学_笔记(1).pdf",
    "威科夫2_0+市场结构、成交量分布与订单流.pdf",
    "突破做单后续.pdf",
    "GRANDMA策略-Rose.pdf",
    "洛氏霍克交易法.pdf",
    "2025雷神导师计划.pdf",
]

for name in targets:
    cands = [f for f in base.iterdir() if name[:8] in f.name]
    if not cands:
        print("NOT FOUND:", name)
        continue
    f = cands[0]
    doc = pymupdf.open(f)
    texts = []
    for i in range(doc.page_count):
        t = doc[i].get_text("text")
        texts.append(f"\n===== 第 {i+1} 页 =====\n" + t)
    out = outdir / (f.stem[:20] + ".txt")
    out.write_text("".join(texts), encoding="utf-8")
    print(f"OK: {f.name} -> {out.name} ({doc.page_count}页)")
    doc.close()
print("done")
