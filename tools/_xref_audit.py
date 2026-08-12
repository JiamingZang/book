# -*- coding: utf-8 -*-
"""P3-3: 交叉引用完整性审计
1. 标题编号连续性/唯一性检查
2. 所有「第 N.M」引用悬空检查
"""
import re
import glob
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

titles = {}
for fn in glob.glob('handbook/*.md'):
    for line in open(fn, encoding='utf-8').readlines():
        m = re.match(r'^### (\d+)\.(\d+)', line)
        if m:
            titles.setdefault(m.group(1), set()).add(int(m.group(2)))

print('=== 标题编号连续性检查 ===')
for ch in sorted(titles, key=int):
    nums = sorted(titles[ch])
    missing = [x for x in range(1, len(nums) + 1) if x not in nums]
    dup = [x for x in set(nums) if len([n for n in nums if n == x]) > 1]
    print(f'第{ch}章: {len(nums)}节 起始={nums[0]} 结尾={nums[-1]} 缺失={missing if missing else "无"} 重复={dup if dup else "无"}')

print('=== 交叉引用悬空检查 ===')
bad = 0
for fn in glob.glob('handbook/*.md'):
    for i, line in enumerate(open(fn, encoding='utf-8').readlines(), 1):
        for m in re.finditer(r'(?:第 ?)(\d+)\.(\d+)(?!\d)(?!%)(?!％)', line):
            ch, sec = m.group(1), int(m.group(2))
            if ch in titles and sec not in titles[ch]:
                snippet = line.strip()[:70]
                print(f'  悬空: {fn}:{i}: 引用 第{ch}.{sec} 但第{ch}章无此节 | {snippet}')
                bad += 1
print('悬空引用总数:', bad)
