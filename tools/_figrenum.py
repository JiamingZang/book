# -*- coding: utf-8 -*-
"""批次31：全章节图号按正文顺序重编号（占位符两步法，R图不参与）"""
import re, glob

# 每章映射：{旧号: 新号}（仅合成图；R 图保持）
JOBS = [
    ("05_smc.md", {12: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}, "5"),
    ("06_position_and_risk.md", {5: 3, 6: 4, 7: 5, 3: 6, 4: 7}, "6"),
    ("07_execution_and_mindset.md", {5: 4, 4: 5}, "7"),
    ("08_tools_and_validation.md", {7: 2, 2: 3, 6: 4, 3: 5, 4: 6, 5: 7}, "8"),
    ("09_prop_firm.md", {4: 3, 3: 4}, "9"),
    ("10_options.md", {5: 3, 3: 4, 4: 5}, "10"),
]

for fn, mapping, ch in JOBS:
    path = "handbook/" + fn
    t = open(path, encoding="utf-8").read()
    # 第一步：旧号 → 占位符（负向前瞻防止误伤 R 图与多位数）
    for old in sorted(mapping, reverse=True):
        t = re.sub(r"图 %s-%d(?!R)(?!\d)" % (ch, old), "图 %s-PH%d" % (ch, old), t)
    # 第二步：占位符 → 新号
    for old, new in mapping.items():
        t = t.replace("图 %s-PH%d" % (ch, old), "图 %s-%d" % (ch, new))
    open(path, "w", encoding="utf-8", newline="\n").write(t)
    print("已重编号:", fn, mapping)
print("完成")
