# -*- coding: utf-8 -*-
"""批次47 图号顺延：第4章插入 5 张新图（4.10/4.11/4.12/4.13/4.14）
普通图 4-10~4-20 → 4-15~4-25（出场期望值 10→15, MM 11→16, 生命周期 12→17, 案例 13→18,
二次突破 14→19, 区间限价 15→20, 通道分类 16→21, 通道演变 17→22, always-in 18→23, 20GB 19→24, ORB 20→25）
R 图 4-1R~4-9R 不动；章节号（如"4.10 节"）不受影响（只匹配"图 4-X"模式）
占位符两步法：旧号→PH 占位→新号，全程 (?!\d) 负向前瞻防止 PH1 误伤 PH10~PH20
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

PATH = "handbook/04_trading_system.md"

mapping = {10: 15, 11: 16, 12: 17, 13: 18, 14: 19,
           15: 20, 16: 21, 17: 22, 18: 23, 19: 24, 20: 25}

with open(PATH, encoding="utf-8") as f:
    s = f.read()

# 第一步：旧号 → 占位符（(?!\d) 防止 4-1 匹配 4-10~4-20 前缀；图号后不跟数字才替换）
for old in sorted(mapping, reverse=True):
    s = re.sub(r"图 4-%d(?!\d)" % old, "图 4-PH%d" % old, s)

# 第二步：占位符 → 新号（(?!\d) 防止 PH1 误伤 PH10~PH20）
for old, new in mapping.items():
    s = re.sub(r"图 4-PH%d(?!\d)" % old, "图 4-%d" % new, s)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("批次47 图号顺延完成（4-10~4-20 → 4-15~4-25）")
