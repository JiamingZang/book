# -*- coding: utf-8 -*-
"""扫描各章小节：无图小节清单（### 级）"""
import re
import sys
import glob

sys.stdout.reconfigure(encoding="utf-8")

for f in sorted(glob.glob("handbook/0*_*.md")) + sorted(glob.glob("handbook/1*_*.md")):
    lines = open(f, encoding="utf-8").read().splitlines()
    sections = []  # (level, title, has_img)
    cur_level, cur_title, has_img = None, None, False
    for ln in lines:
        m = re.match(r"^(#{2,3})\s+(.*)", ln)
        if m:
            if cur_title is not None:
                sections.append((cur_level, cur_title, has_img))
            cur_level, cur_title, has_img = len(m.group(1)), m.group(2).strip(), False
        elif "](images/" in ln or "![[fig_" in ln:
            has_img = True
    if cur_title is not None:
        sections.append((cur_level, cur_title, has_img))
    missing = [f"{lvl}-{t}" for lvl, t, h in sections if lvl == 3 and not h]
    if missing:
        print(f"\n{f.split(chr(92))[-1]}: {len(sections)} 个小节, {len(missing)} 个无图")
        for t in missing:
            print("   ", t[:60])
