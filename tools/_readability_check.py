# -*- coding: utf-8 -*-
"""内容可读性体检：找超长段落/超长行/密集文字块（批次32）"""
import glob, re

OUT = []

def out(s):
    OUT.append(s)
    print(s)

def block_len(lines, i):
    """从 i 起连续非空且非块元素的行数"""
    n = 0
    for j in range(i, len(lines)):
        s = lines[j].strip()
        if not s or s.startswith(("#", "|", "-", "*", ">", "```", "!")) or re.match(r"^\d+\.", s):
            break
        n += 1
    return n

for f in sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/1*.md")):
    lines = open(f, encoding="utf-8").read().split("\n")
    issues = []
    for i, ln in enumerate(lines):
        if len(ln) > 150:
            issues.append("长行 L%d: %d字 %s..." % (i + 1, len(ln), ln[:45]))
        b = block_len(lines, i)
        if b >= 6:
            issues.append("墙文字 L%d: 连续%d行正文" % (i + 1, b))
    if issues:
        out("=====" + f.split("\\")[-1])
        for x in issues[:8]:
            out("  " + x)
open("_readability_out.txt", "w", encoding="utf-8").write("\n".join(OUT))
print("体检完成 -> _readability_out.txt")
