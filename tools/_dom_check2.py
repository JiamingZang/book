import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

t = open("_dom3.html", encoding="utf-8").read()
print("figcap class:", t.count('class="figcap"'))
print("fig- anchors total:", len(re.findall(r'id="fig-', t)))
print("anchor ids:", re.findall(r'id="fig-([^"]+)"', t)[:40])
print("anchor ids tail:", re.findall(r'id="fig-([^"]+)"', t)[-5:])
print("html len:", len(t))
