# -*- coding: utf-8 -*-
"""图编号审计 v2：只统计图片行（^![图 X-Y），合成图应连续无重复；
真实图（X-YR）单独列出检查（允许任意编号）。"""
import re
import glob

ok = True
for f in sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/10_*.md")):
    t = open(f, encoding="utf-8").read()
    imgs = re.findall(r"^!\[图 (\d+-\d+R?)", t, re.M)
    if not imgs:
        continue
    ch = int(imgs[0].split("-")[0])
    syn = []   # 合成图序列
    real = []  # R 图列表
    for s in imgs:
        if s.endswith("R"):
            real.append(s)
        else:
            syn.append(int(s.split("-")[1]))
    # 合成图连续检查
    dup = [n for n in set(syn) if syn.count(n) > 1]
    miss = [n for n in range(1, max(syn) + 1) if n not in syn]
    if dup or miss:
        ok = False
        print("%s !!! 合成图 重复:%s 缺失:%s" % (f[9:11], dup, miss))
    if real:
        print("%s 真实图: %s" % (f[9:11], ", ".join(real)))
print("OK" if ok else "FAIL")
