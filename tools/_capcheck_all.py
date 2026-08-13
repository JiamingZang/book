# -*- coding: utf-8 -*-
"""全库检查 img/excalidraw 是否缺 figcap（图片行后 2 行内无 *图 X-X* 行）
v51：兼容 Excalidraw 引用 `![[fig_x.excalidraw]]`（图号从后续图注行获取）
"""
import re, glob

pat_img = re.compile(r"!\[(图 \d+-\d+R?[^\]]*)\]\(images/([^)]+)\)")
pat_ex = re.compile(r"!\[\[(fig_[a-z0-9_]+)\.excalidraw\]\]")
pat_cap = re.compile(r"\*(图 \d+-\d+R?[^\]]*)\*")

total_missing = 0
for p in sorted(glob.glob("handbook/0*_*.md")):
    lines = open(p, encoding="utf-8").read().splitlines()
    missing = []
    for i, ln in enumerate(lines):
        strip = ln.strip()
        m = pat_img.match(strip)
        is_ex = bool(pat_ex.match(strip))
        if not m and not is_ex:
            continue
        # 图号：普通图从本行 alt；excalidraw 从后续图注行
        num = m.group(1).split()[1] if m else None
        nxt = ""
        for j in range(i + 1, min(i + 3, len(lines))):
            fm = pat_cap.match(lines[j].strip())
            if fm:
                nxt = fm.group(1).split()[1]
                break
        if is_ex:
            # excalidraw 行本身无图号，要求 2 行内有图注即可
            if not nxt:
                missing.append((i + 1, "excalidraw", "无"))
        elif nxt != num:
            missing.append((i + 1, num, nxt or "无"))
    if missing:
        total_missing += len(missing)
        print(f"== {p} 缺 {len(missing)} ==")
        for L, num, nxt in missing:
            print(f"  L{L} 图{num} 附近figcap:{nxt}")
print("总计缺 figcap:", total_missing)
