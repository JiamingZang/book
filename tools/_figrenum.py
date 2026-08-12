# -*- coding: utf-8 -*-
"""批次31：全章节图号按正文顺序重编号（占位符两步法，R图不参与）"""
import re, glob

# 每章映射：{旧号: 新号}（仅合成图；R 图保持）
JOBS = [
    ("05_第5章_聪明钱概念SMC.md", {12: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}, "5"),
    ("06_第6章_仓位与风险.md", {5: 3, 6: 4, 7: 5, 3: 6, 4: 7}, "6"),
    ("07_第7章_执行与心态.md", {5: 4, 4: 5}, "7"),
    ("08_第8章_工具与验证.md", {7: 2, 2: 3, 6: 4, 3: 5, 4: 6, 5: 7}, "8"),
    ("09_第9章_Prop考核实战.md", {4: 3, 3: 4}, "9"),
    ("10_第10章_期权.md", {5: 3, 3: 4, 4: 5}, "10"),
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
