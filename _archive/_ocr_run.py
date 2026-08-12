# -*- coding: utf-8 -*-
"""批量 OCR 渲染后的 PDF 页面"""
import os, glob
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR()
OUT = r'c:\Users\18315\Desktop\新建文件夹\_ocr_out'
os.makedirs(OUT, exist_ok=True)

dirs = ['leishen', 'top10', 'abbrev', 'ross', 'wyckoff2', 'breakout_next']
for d in dirs:
    src = os.path.join(r'c:\Users\18315\Desktop\新建文件夹\_pdf_pages', d)
    res = []
    for f in sorted(glob.glob(os.path.join(src, '*.png'))):
        result, _ = ocr(f)
        txt = ''
        if result:
            txt = '\n'.join(line[1] for line in result)
        res.append(f'===== {os.path.basename(f)} =====')
        res.append(txt)
    with open(os.path.join(OUT, d + '.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(res))
    print(f'{d} done: {len(res)} lines')
