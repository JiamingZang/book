# -*- coding: utf-8 -*-
"""扫描无图的长节：找出篇幅大但没有配图的章节，作为补图候选"""
import re
import os

OUT = []
def out(s=""):
    OUT.append(str(s))
    print(s)

handbook = "handbook"
files = sorted(f for f in os.listdir(handbook) if f.endswith(".md") and not f.startswith("README"))

for fn in files:
    path = os.path.join(handbook, fn)
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    # 按标题切分
    sections = []  # (标题, 行号, 文本)
    cur_title, cur_start = None, 0
    buf = []
    for i, line in enumerate(lines):
        m = re.match(r"^#{2,4} (.+)$", line)
        if m:
            if cur_title:
                sections.append((cur_title, cur_start, "".join(buf)))
            cur_title, cur_start = m.group(1), i + 1
            buf = []
        else:
            buf.append(line)
    if cur_title:
        sections.append((cur_title, cur_start, "".join(buf)))

    for title, ln, text in sections:
        # 去掉图片行和表格行后的字数
        text_noimg = re.sub(r"!\[.*?\]\(.*?\)", "", text)
        text_noimg = re.sub(r"^\s*\|.*\|\s*$", "", text_noimg, flags=re.M)
        n = len(text_noimg)
        has_img = "![" in text
        # 只报 1200+ 字且无图的节
        if n >= 1200 and not has_img:
            out(f"{fn} L{ln} [{n}字] 无图: {title}")

with open("_nogap_scan_out.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT))
print("saved: _nogap_scan_out.txt")
