# -*- coding: utf-8 -*-
"""
语义引用审计：抽取全书所有"呼应/详见/见/参考 X.Y"类引用，与目标节标题比对。
用法：python _xref_semantic.py > _semantic_report.txt
"""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
OUT = open("_semantic_report.txt", "w", encoding="utf-8")
def p(*a):
    print(*a, file=OUT)
    print(*a)

HANDBOOK = "handbook"
FILES = sorted(f for f in os.listdir(HANDBOOK) if f.endswith(".md") and f[0].isdigit())

# 1) 建立 节号 -> 标题 映射
titles = {}   # (ch, sec) -> title
for fn in FILES:
    path = os.path.join(HANDBOOK, fn)
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        m = re.match(r"^#{2,3}\s+(\d+)\.(\d+)[\s　]+(.+)$", line.strip())
        if m:
            ch, sec, title = int(m.group(1)), int(m.group(2)), m.group(3).strip()
            titles[(ch, sec)] = (fn, i, title)

# 2) 提取引用并输出
pat = re.compile(
    r"(呼应|详见|见|参考|参照|对应|同|呼应自|回顾|先看|后看)"
    r"[\s　]*(第)?(\d{1,2})[\.．](\d{1,2})"
)
# 也匹配括号内裸引用如 （4.3）、(10.6 用途一)、8.3 的 R 数据
pat2 = re.compile(r"[（(](\d{1,2})[\.．](\d{1,2})")
pat3 = re.compile(r"(?<![\d.])(\d{1,2})[\.．](\d{1,2})\s*(节|章|的|：|:)")

p("=" * 78)
p("A. 带引导词的引用（呼应/详见/见/参考...）")
p("=" * 78)
rows = []
for fn in FILES:
    path = os.path.join(HANDBOOK, fn)
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        if line.strip().startswith("!"):
            continue
        for m in pat.finditer(line):
            ch, sec = int(m.group(3)), int(m.group(4))
            target = titles.get((ch, sec))
            tag = "OK " if target else "MISS"
            ttl = target[2][:28] if target else "（无此节号！）"
            rows.append((tag, f"{fn}:{i}", m.group(0), f"{ch}.{sec}", ttl))
for r in rows:
    p(f"[{r[0]}] {r[1]:<28} 「{r[2]}」-> {r[3]:<6} {r[4]}")

p()
p("=" * 78)
p("B. 括号裸引用（（4.3）/ (10.6) / (4.3/4.27)）")
p("=" * 78)
rows2 = []
for fn in FILES:
    path = os.path.join(HANDBOOK, fn)
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        for m in pat2.finditer(line):
            ch, sec = int(m.group(1)), int(m.group(2))
            target = titles.get((ch, sec))
            tag = "OK " if target else "MISS"
            ttl = target[2][:28] if target else "（无此节号！）"
            rows2.append((tag, f"{fn}:{i}", m.group(0), f"{ch}.{sec}", ttl))
for r in rows2:
    p(f"[{r[0]}] {r[1]:<28} 「{r[2]}」-> {r[3]:<6} {r[4]}")

p()
p("=" * 78)
p("C. 混合引用（4.3/4.27、5.12、8.3 的 R 数据）")
p("=" * 78)
seen = set()
rows3 = []
for fn in FILES:
    path = os.path.join(HANDBOOK, fn)
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        for m in pat3.finditer(line):
            ch, sec = int(m.group(1)), int(m.group(2))
            target = titles.get((ch, sec))
            tag = "OK " if target else "MISS"
            ttl = target[2][:28] if target else "（无此节号！）"
            key = (ch, sec, tag)
            rows3.append((tag, f"{fn}:{i}", m.group(0)[:24], f"{ch}.{sec}", ttl))
for r in rows3:
    p(f"[{r[0]}] {r[1]:<28} 「{r[2]}」-> {r[3]:<6} {r[4]}")

miss = [r for r in rows + rows2 + rows3 if r[0] == "MISS"]
p()
p("=" * 78)
p(f"MISS 汇总（悬空引用）: {len(miss)} 条")
p("=" * 78)
for r in miss:
    p(f"{r[1]:<28} 「{r[2]}」-> {r[3]} {r[4]}")
OUT.close()
