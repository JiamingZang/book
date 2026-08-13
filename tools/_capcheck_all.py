# -*- coding: utf-8 -*-
"""批次45c：全库检查 img 是否缺 figcap（img 后 2 行内无 *图 X-X* 行）"""
import re, glob

pat_img = re.compile(r"!\[(图 \d+-\d+R?[^\]]*)\]\(images/([^)]+)\)")
pat_cap = re.compile(r"\*(图 \d+-\d+R?[^\]]*)\*")

total_missing = 0
for p in sorted(glob.glob("handbook/0*_*.md")):
    lines = open(p, encoding="utf-8").read().splitlines()
    missing = []
    for i, ln in enumerate(lines):
        m = pat_img.match(ln.strip())
        if not m:
            continue
        num = m.group(1).split()[1]  # "3-6" 部分
        nxt = ""
        for j in range(i + 1, min(i + 3, len(lines))):
            fm = pat_cap.match(lines[j].strip())
            if fm:
                nxt = fm.group(1).split()[1]
                break
        if nxt != num:
            missing.append((i + 1, num, nxt or "无"))
    if missing:
        total_missing += len(missing)
        print(f"== {p} 缺 {len(missing)} ==")
        for L, num, nxt in missing:
            print(f"  L{L} 图{num} 附近figcap:{nxt}")
print("总计缺 figcap:", total_missing)
