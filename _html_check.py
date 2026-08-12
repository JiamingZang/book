# -*- coding: utf-8 -*-
"""HTML 锚点完整性校验：标题 id 与 TOC 链接一一对应"""
import re

t = open("handbook/trading-handbook.html", encoding="utf-8").read()
ids = set(re.findall(r"<h[123] id=\"(sec-\d+)\"", t))
hrefs = set(re.findall(r"href=\"#(sec-\d+)\"", t))
print("标题id数:", len(ids), "TOC链接数:", len(hrefs))
print("链接悬空:", sorted(hrefs - ids)[:8] if hrefs - ids else "无")
print("标题无链接:", sorted(ids - hrefs)[:8] if ids - hrefs else "无")
print("组件存在:", all(x in t for x in ["id=\"progress\"", "id=\"backtop\"", "id=\"toc\"", "addEventListener"]))
