# -*- coding: utf-8 -*-
"""批次45c：全库补 figcap——img 行后无 *图 X-X* 图注的，插入 alt 文本版图注
仅处理 img 行后紧跟空行的情况（img\n\n）"""
import re, glob

pat = re.compile(r"(!\[(图 \d+-\d+R?[^\]]*)\]\(images/[^)]+\))\n\n")

for p in sorted(glob.glob("handbook/0*_*.md")):
    s = open(p, encoding="utf-8").read()
    cnt = 0
    def rep(m):
        global cnt
        cnt += 1
        return f"{m.group(1)}\n\n*{m.group(2)}*\n\n"
    s2 = pat.sub(rep, s)
    if cnt:
        open(p, "w", encoding="utf-8", newline="\n").write(s2)
        print(p, "补", cnt, "处")
print("完成")
