# -*- coding: utf-8 -*-
"""抽样提取阿布价格行为学 PDF 文本，判断内容性质与重叠度"""
import fitz, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

out = []
for fn, pages in [("阿布价格行为学（基础篇）_01-36.pdf", [0, 5, 10, 20, 30, 50, 80, 120, 180, 260, 400, 600, 900, 1400, 2000, 2800]),
                  ("阿布价格行为学（进阶篇）_37-52.pdf", [0, 5, 10, 20, 50, 100, 200, 400, 700, 1100, 1390])]:
    d = fitz.open(fn)
    out.append(f"===== {fn} 共 {d.page_count} 页 =====")
    for i in pages:
        if i >= d.page_count:
            continue
        t = d[i].get_text().replace("\n", " | ")[:150]
        out.append(f"[页{i}] {t}")
    d.close()

open("_abu_sample.txt", "w", encoding="utf-8").write("\n\n".join(out))
print("done")
