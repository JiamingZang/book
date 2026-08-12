# -*- coding: utf-8 -*-
"""渲染图片型 PDF 页面为 PNG，供读图解析"""
import pymupdf, os

JOBS = [
    ('leishen', r'c:\Users\18315\Desktop\新建文件夹\2025雷神导师计划.pdf', 37),
    ('top10', r'c:\Users\18315\Desktop\新建文件夹\阿布10种最佳价格行为交易模式.pdf', 11),
    ('abbrev', r'c:\Users\18315\Desktop\新建文件夹\阿布缩写翻译及解释.pdf', 20),
    ('ross', r'c:\Users\18315\Desktop\新建文件夹\洛氏霍克交易法.pdf', 40),
    ('wyckoff2', r'c:\Users\18315\Desktop\新建文件夹\威科夫2_0+市场结构、成交量分布与订单流.pdf', 40),
    ('breakout_next', r'c:\Users\18315\Desktop\新建文件夹\突破做单后续.pdf', 50),
]
OUT = r'c:\Users\18315\Desktop\新建文件夹\_pdf_pages'
os.makedirs(OUT, exist_ok=True)

for name, path, n in JOBS:
    doc = pymupdf.open(path)
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    for i in range(min(n, len(doc))):
        pg = doc[i]
        pix = pg.get_pixmap(dpi=120)
        pix.save(os.path.join(d, f'{i+1:03d}.png'))
    print(f'{name}: {min(n, len(doc))} pages rendered')
    doc.close()
