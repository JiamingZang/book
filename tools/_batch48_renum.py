# -*- coding: utf-8 -*-
"""批次48 图号顺延（双文件）
第 4 章：4.20 节插入图 4-19 → 普通图 19~25 → 20~26
第 6 章：6.3 节插入图 6-2、6.10 节插入图 6-7、6.11 节插入图 6-8
        → 普通图 2~7 → 3~10（2→3,3→4,4→5,5→6,6→9,7→10）
R 图不动（第4章 4-1R~4-9R、第6章 6-1R）；章节号（如"4.19 节"）不受影响
占位符两步法 + (?!\d) 负向前瞻防止 PH1/PH2 前缀误伤
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

JOBS = [
    ("handbook/04_trading_system.md",
     {19: 20, 20: 21, 21: 22, 22: 23, 23: 24, 24: 25, 25: 26}),
    ("handbook/06_position_and_risk.md",
     {2: 3, 3: 4, 4: 5, 5: 6, 6: 9, 7: 10}),
]

for path, mapping in JOBS:
    with open(path, encoding="utf-8") as f:
        s = f.read()
    # 第一步：旧号 → 占位符（从大到小 + (?!\d) 防前缀）
    for old in sorted(mapping, reverse=True):
        s = re.sub(r"图 %d-%d(?!\d)" % (int(path[9:11]), old),
                   "图 %d-PH%d" % (int(path[9:11]), old), s)
    # 第二步：占位符 → 新号
    for old, new in mapping.items():
        s = re.sub(r"图 %d-PH%d(?!\d)" % (int(path[9:11]), old),
                   "图 %d-%d" % (int(path[9:11]), new), s)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"批次48 顺延完成: {path} ({min(mapping)}->{min(mapping.values())} ... {max(mapping)}->{max(mapping.values())})")
