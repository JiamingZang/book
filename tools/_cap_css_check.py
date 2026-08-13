# -*- coding: utf-8 -*-
"""检查 HTML figcap CSS 样式与实例"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

html = open("handbook/trading-handbook.html", encoding="utf-8").read()
m = re.search(r"\.figcap\s*\{[^}]*\}", html)
print("figcap CSS:", m.group(0) if m else "未定义")
m2 = re.search(r'<p class="figcap">[^<]*</p>', html)
print("实例:", m2.group(0) if m2 else "无")
m3 = re.findall(r'<p class="figcap">', html)
print("figcap 数量:", len(m3))
