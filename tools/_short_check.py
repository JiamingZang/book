# -*- coding: utf-8 -*-
"""短而不清扫描：找解释过短的孤立定义条目（批次32）"""
import glob, re

OUT = []
def out(s):
    OUT.append(s)
    print(s)

for f in sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/1*.md")):
    lines = open(f, encoding="utf-8").read().split("\n")
    for i, ln in enumerate(lines):
        s = ln.strip()
        # 定义条目：**名词**：解释，且整行 < 150 字
        if s.startswith("**") and "**：" in s and len(s) < 150:
            body = s.split("**：", 1)[1]
            # 解释太短（<45字）且没有例证/数字
            if len(body) < 45 and not re.search(r"[0-9０-９]|例如|比如|例：", body):
                out("%s L%d: %d字 %s" % (f.split("\\")[-1], i + 1, len(s), s[:80]))
open("_short_out.txt", "w", encoding="utf-8").write("\n".join(OUT))
print("短条目扫描完成 -> _short_out.txt")
