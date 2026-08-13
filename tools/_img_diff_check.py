# -*- coding: utf-8 -*-
"""md 引用图片数 vs HTML img 数差异排查"""
import re
import sys
import glob
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

md = ""
for f in sorted(glob.glob("handbook/*.md")):
    md += open(f, encoding="utf-8").read()
md_refs = re.findall(r"\]\((images/[^)]+)\)", md)
print("md 引用图片:", len(md_refs), " 唯一:", len(set(md_refs)))
md_dup = {k: v for k, v in Counter(md_refs).items() if v > 1}
print("md 重复引用:", md_dup)

html = open("handbook/trading-handbook.html", encoding="utf-8").read()
print("html <img 总数:", len(re.findall(r"<img", html)))
imgs = re.findall(r'<img[^>]*src="([^"]+)"', html)
print("html img src 数:", len(imgs), " 唯一:", len(set(imgs)))
dups = {k: v for k, v in Counter(imgs).items() if v > 1}
print("html 重复 img:", dups)
