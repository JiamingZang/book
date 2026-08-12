# -*- coding: utf-8 -*-
"""检查所有章节图号是否按正文出现顺序连续（批次31 审计）"""
import re, glob

for f in sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/1*.md")):
    t = open(f, encoding="utf-8").read()
    nums = re.findall(r"!\[(图 (\d+)-(\d+)(R)?)", t)
    if not nums:
        continue
    ch = nums[0][1]
    seq = [(int(n[2]), n[3]) for n in nums]
    # 合成图（非 R）按出现顺序应为 1..N 递增；R 图保持不参与
    synth = [n for n, r in seq if not r]
    real = [n for n, r in seq if r]
    ok = synth == list(range(1, len(synth) + 1))
    flag = "OK" if ok else "!! 乱序"
    print("%s 合成图: %s %s  真实图: %s" % (f.split("\\")[-1], synth, flag, real))
print("检查完成")
