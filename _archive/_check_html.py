# -*- coding: utf-8 -*-
import re, os, sys
sys.stdout.reconfigure(encoding="utf-8")
h = open("handbook/trading-handbook.html", encoding="utf-8").read()
print("h1 count:", len(re.findall(r"<h1>", h)))
print("h2 count:", len(re.findall(r"<h2>", h)))
imgs = re.findall(r'<img[^>]+src="([^"]+)"', h)
print("img refs:", len(imgs))
missing = [p for p in set(imgs) if not os.path.exists("handbook/" + p)]
print("missing imgs:", missing)
print("tables:", len(re.findall(r"<table>", h)))
print("real figs ok:", "fig_real_trend" in h and "fig_real_range" in h and "fig_real_climax" in h)
