# -*- coding: utf-8 -*-
"""盘点工作区参考资料：提取各 PDF 前几页文本，快速了解内容主题"""
import pathlib
import fitz  # pymupdf

base = pathlib.Path(r"c:\Users\18315\Desktop\新建文件夹")
# 排除 handbook/ 与我们的脚本
files = [f for f in base.rglob("*") if f.is_file() and f.suffix.lower() == ".pdf"
         and "handbook" not in f.parts]
files.sort(key=lambda f: f.stat().st_size)

for f in files:
    size_mb = f.stat().st_size / 1e6
    try:
        doc = fitz.open(f)
        npages = doc.page_count
        # 取前 4 页文本，拼出目录线索
        head = ""
        for i in range(min(4, npages)):
            head += doc[i].get_text("text")[:600]
        head = " ".join(head.split())
        print(f"\n{'='*100}")
        print(f"【{f.name}】 {size_mb:.1f}MB {npages}页")
        print(f"  {head[:500]}")
        doc.close()
    except Exception as e:
        print(f"\n【{f.name}】 ERROR: {e}")
