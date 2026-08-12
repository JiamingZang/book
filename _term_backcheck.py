# -*- coding: utf-8 -*-
"""术语表反向审计：术语表条目是否在正文（00-10 章）出现。
用途：找出"词典有、正文从未使用"的条目，决定删除或标注参考性质。"""
import re
import glob

GL = "handbook/11_附录_术语表与学习资源.md"
gl = open(GL, encoding="utf-8").read()

body = ""
for f in sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/10_*.md")):
    body += open(f, encoding="utf-8").read()

terms = []
for line in gl.splitlines():
    m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
    if m:
        cell = m.group(1).strip()
        if cell and cell != "术语" and not cell.startswith("---") and "（" not in cell[:4]:
            terms.append(cell)

missing = []
for t in terms:
    # 主名取第一个分隔符前的词
    t0 = re.split(r"[/（( ]", t)[0].strip()
    if len(t0) < 2:
        continue
    if t0 not in body:
        missing.append((t, t0))

print("术语条目数:", len(terms))
print("正文未出现的条目:")
for t, t0 in missing:
    print("  ", t)
