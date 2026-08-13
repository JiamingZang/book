import re
import sys

import markdown

sys.stdout.reconfigure(encoding="utf-8")

t = open("handbook/01_第1章_市场是怎么运作的.md", encoding="utf-8").read()
html = markdown.markdown(t, extensions=["tables", "fenced_code", "sane_lists"])
m = re.search(r"<img[^>]*>", html)
print("first img tag:", repr(m.group(0)))
alts = re.findall(r'<img alt="(图 [^"]*)"', html)
print("img tags:", len(re.findall(r"<img", html)))
print("alt 图注:", len(alts))
print("sample alt:", alts[0][:60])

# 全量统计两种格式
import glob

tot_img = 0
tot_alt = 0
tot_em = 0
for f in sorted(glob.glob("handbook/*.md")):
    t = open(f, encoding="utf-8").read()
    h = markdown.markdown(t, extensions=["tables", "fenced_code", "sane_lists"])
    tot_img += len(re.findall(r"<img", h))
    tot_alt += len(re.findall(r'<img alt="图 [^"]*"', h))
    tot_em += len(re.findall(r"<em>图 \d", h))
print("TOTAL img:", tot_img, "alt-caption:", tot_alt, "em-caption:", tot_em)
