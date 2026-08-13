# -*- coding: utf-8 -*-
"""批次48 修复：第 4 章图号 12-16 重排，使图号与正文顺序严格一致
当前倒挂：4-12(分批止盈)/4-13(保本)/4-14(时间止损) 插在 4.14~4.17 节，
但 4.12/4.13 节的图（出场期望值=4-15、MM 四类=4-16）排在其前 → img 顺序 15,16,12,13,14
重排：15→12, 16→13, 12→14, 13→15, 14→16（环形映射，必须占位符两步法）
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

PATH = "handbook/04_第4章_交易系统.md"
mapping = {15: 12, 16: 13, 12: 14, 13: 15, 14: 16}

with open(PATH, encoding="utf-8") as f:
    s = f.read()

# 第一步：旧号 → 占位符（(?!\d) 防前缀）
for old in sorted(mapping):
    s = re.sub(r"图 4-%d(?!\d)" % old, "图 4-FIX%d" % old, s)

# 第二步：占位符 → 新号
for old, new in mapping.items():
    s = re.sub(r"图 4-FIX%d(?!\d)" % old, "图 4-%d" % new, s)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("批次48 修复：第 4 章图号 12-16 重排完成")
