# -*- coding: utf-8 -*-
"""正向缩写审计：正文（00-10 章）中出现的大写缩写，是否都有术语表条目。
用途：找出"正文在用、词典没有"的缩写，决定补入术语表。"""
import re
import glob

gl = open("handbook/11_附录_术语表与学习资源.md", encoding="utf-8").read()

body = ""
for f in sorted(glob.glob("handbook/0*.md") + glob.glob("handbook/10_*.md")):
    body += open(f, encoding="utf-8").read()

# 正文中的大写缩写 token（2-6 个字母，可带数字如 H1/H2、20GB）
tokens = re.findall(r"\b[A-Z]{2,6}\d*\b", body)
from collections import Counter
cnt = Counter(tokens)

# 术语表已覆盖的词（提取每个表格行第一个单元格的所有大写 token）
covered = set()
for line in gl.splitlines():
    m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
    if m:
        cell = m.group(1)
        for t in re.findall(r"[A-Z]{2,6}\d*", cell):
            covered.add(t)

# 常见噪声：货币/日期/普通词
noise = {"ES", "SPX", "SPY", "QQQ", "NQ", "YM", "CL", "GC", "USD", "EUR", "GBP",
         "JPY", "CHF", "CAD", "AUD", "NZD", "DXY", "VIX", "FOMC", "CPI", "NFP",
         "ETF", "ETF", "A股", "PM", "AM", "OK", "PDF", "MD", "HTML", "URL", "AI",
         "CEO", "PPT", "QQ", "PC", "L", "S", "M", "W", "R", "RR", "R-multiple",
         "ATR", "K", "V", "X", "Y", "C", "O", "H", "L", "T"}
# 只报告出现 >= 2 次且未被覆盖的
missing = []
for tok, n in cnt.most_common():
    if n >= 2 and tok not in covered and tok not in noise and len(tok) >= 2:
        missing.append((tok, n))

print("正文大写缩写种类:", len(cnt))
print("未被术语表覆盖（出现>=2次）:")
for tok, n in missing:
    print("  %-8s %d 次" % (tok, n))
