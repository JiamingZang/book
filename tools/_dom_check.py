import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

t = open("_dom3.html", encoding="utf-8").read()
print("fig anchors:", len(re.findall(r'id="fig-\d', t)))
print("fig links:", len(re.findall(r'href="#fig-\d', t)))
print("ansbtn:", t.count('class="ansbtn"'))
print("startbtn:", t.count("startbtn"))
i = t.find('href="#fig-')
print("sample:", t[i - 40 : i + 30].replace("\n", " "))
