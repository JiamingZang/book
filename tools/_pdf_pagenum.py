"""
为 PDF 每页底部居中插入页码（深藏青小号，参考 ElegantBook 页脚页码）。
- 封面页（第 1 页）不插页码
- 全量保存：合并之前 incremental 写入的书签，文件体积更小
- 颜色 #1e3a6b = (0.1176, 0.2275, 0.4196)，字号 9

运行：python _pdf_pagenum.py handbook/trading-handbook.pdf
"""
import os
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")

PDF = sys.argv[1] if len(sys.argv) > 1 else "handbook/trading-handbook.pdf"
NAVY = (0.1176, 0.2275, 0.4196)  # #1e3a6b
FONT = "helv"
SIZE = 9
Y_OFF = 22  # 距底边距离

doc = pymupdf.open(PDF)
n_pages = len(doc)
for i, page in enumerate(doc):
    if i == 0:
        continue  # 封面页不插页码
    n = i + 1
    w = page.rect.width
    text_w = pymupdf.get_text_length(str(n), fontname=FONT, fontsize=SIZE)
    page.insert_text(
        (w / 2 - text_w / 2, page.rect.height - Y_OFF),
        str(n),
        fontsize=SIZE,
        color=NAVY,
        fontname=FONT,
    )

tmp = PDF + ".tmp.pdf"
doc.save(tmp)
doc.close()
os.replace(tmp, PDF)
print(f"ok: 页码已插入 {n_pages - 1} 页（封面除外），全量保存 {PDF}")
